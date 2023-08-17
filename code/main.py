# By: Adeshvir Dhillon
# Date: July 9, 2023

"""
Manga Update Web Scraper

This program allows users to track updates for their favorite manga titles by scraping the Manga4Life.com website. It uses Selenium for web scraping, BeautifulSoup for parsing web page contents, and various other libraries for handling date/time, file operations, and parsing.

The program provides the following features:
- Add manga titles to a manga title list
- Delete manga titles from the manga title list
- View the manga title list
- Run the program to check for updates on the Manga4Life website and display the updates

The program uses a Manga class to represent a manga, which stores information about the manga, such as its title, URL, and chapter list. It also provides methods for managing manga data and interacting with a web browser.

The Chapter class represents a chapter of a manga, storing information such as the chapter's title, date, and URL. It includes methods for parsing the date string, comparing chapter dates, and retrieving chapter details.

The program utilizes CSV files to store chapter data for each manga, allowing for persistence across program runs.

To use the program, specify the Chrome driver path and the folder where you want to store the manga files. The program will load the manga title list from a file if it exists, create Manga instances for each title, and present a menu to the user for interacting with the program.

Enjoy tracking your manga chapter updates with Manga Chapter Updates Tracker!
"""

# Imports
# -> Selenium
from selenium import webdriver # Browser
from selenium.webdriver.chrome.options import Options # for headless, detach, etc.
from selenium.webdriver.chrome.service import Service # for driver_path

# -> Webscraping
import requests # for checking if manga exists
from bs4 import BeautifulSoup # for scraping webpage's contents

# -> Date/Time
from datetime import datetime as DATETIME, date as DATE, timedelta as TIMEDELTA # for parsing chapter's date
import time # for pauses to allow browser to load

# -> Files
import os # for changing file directory
import csv # for using comma separated value files

# -> Parsing
import re # for parsing chapter's date from the HTML text

# Classes
class Manga():
    """
    Represents a manga.

    This class stores information about a manga, such as its title, URL, and chapter list.
    It provides methods to add chapters, manage manga data, and interact with a web browser.

    Attributes:
        title (str): The title of the manga.
        url (str): The URL of the manga.
        chapter_list (list): A list of Chapter instances representing the manga's chapters.
        data (list): A list of dictionaries containing chapter data.
        is_new_manga (bool): Indicates if the manga is new.
        has_new_chapters (bool): Indicates if the manga has new chapters.

        chrome_options (Options): Holds options of the browser
        service (Service): Holds service of the browser
        browser (webdriver.Chrome): Selenium browser that opens the manga's Manga4Life page

    Methods:
        set_is_new_manga: Set the manga as new.
        set_has_new_chapters: Set that the manga has new chapters.
        add_chapter: Add a chapter to the manga.
        reset: Reset the manga's attributes.
        contains_chapter: Check if a chapter is in the manga's chapter list.
        get_title: Get the title of the manga.
        get_url: Get the URL of the manga.
        get_is_new_manga: Check if the manga is new.
        get_has_new_chapters: Check if the manga has new chapters.
        get_chapter: Get a specific chapter by index.
        get_chapter_list: Get the list of chapters.
        get_chapter_list_length: Get the length of the chapter list.
        get_data: Get the manga data.
        get_browser: Open the browser and navigate to the manga's URL.
    """

    def __init__(self, title: str, url: str, driver_path: str, is_new_manga: bool = False):
        """Initialize a Manga instance.

        Args:
            title (str): _description_
            url (str): _description_
            driver_path (str): _description_
            is_new_manga (bool, optional): _description_. Defaults to False.
        """
        self.title = title
        self.url = url
        self.chapter_list = []
        self.data = []
        self.is_new_manga = is_new_manga
        self.has_new_chapters = False

        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.service = Service(driver_path)
        self.browser = None

    # Setters/Adders

    def set_is_new_manga(self) -> bool:
        """Set the manga as new."""
        self.is_new_manga = True

    def set_has_new_chapters(self) -> bool:
        """Set that the manga has new chapters."""
        self.has_new_chapters = True

    def add_chapter(self, chapter: 'Chapter', index: int = -1):
        """Add a chapter to the manga.

        Args:
            chapter (Chapter): The Chapter instance to add.
            index (int, optional): The index at which to insert the chapter. Defaults to -1 (append at the end).
        """
        if(self.contains_chapter(chapter) != True):
            if(0 <= index <= len(self.chapter_list)): # Valid index
                self.chapter_list.insert(index, chapter)
                self.data.insert(index, {'Chapter Title': chapter.get_title(), 'Chapter Date': chapter.get_date_string(), 'Chapter URL': chapter.get_url()})
            else: # Invalid index; append at end
                self.chapter_list.append(chapter)
                self.data.append({'Chapter Title': chapter.get_title(), 'Chapter Date': chapter.get_date_string(), 'Chapter URL': chapter.get_url()})
    
    def reset(self):
        """Reset the manga's attributes."""
        if(self.is_new_manga == True and len(self.chapter_list) != 0): # New manga has been initialized
            self.is_new_manga = False
        self.chapter_list = []
        self.data = []
        self.has_new_chapters = False

    # Getters

    def contains_chapter(self, chapter: 'Chapter') -> bool:
        """Check if a chapter is in the manga's chapter list.

        Args:
            chapter (Chapter): The Chapter instance to check.

        Returns:
            bool: True if the chapter is in the manga's chapter list, False otherwise.
        """
        return(chapter in self.chapter_list)
    
    def get_title(self) -> str:
        """Get the title of the manga.

        Returns:
            str: The title of the manga.
        """
        return self.title
    
    def get_url(self) -> str:
        """Get the URL of the manga.

        Returns:
            str: The URL of the manga.
        """
        return self.url
    
    def get_is_new_manga(self) -> bool:
        """Check if the manga is new.

        Returns:
            bool: True if the manga is new, False otherwise.
        """
        return self.is_new_manga
    
    def get_has_new_chapters(self) -> bool:
        """Check if the manga has new chapters.

        Returns:
            bool: True if the manga has new chapters, False otherwise.
        """
        return self.get_has_new_chapters
    
    def get_chapter(self, index: int) -> 'Chapter' | None:
        """Get a specific chapter by index.

        Args:
            index (int): The index of the chapter to retrieve.

        Returns:
            Chapter or None: The Chapter instance if the index is valid, None otherwise.
        """
        if(0 <= index <= len(self.chapter_list)):
            return self.chapter_list[index]
        else:
            return None
    
    def get_chapter_list(self) -> list:
        """Get the list of chapters.

        Returns:
            list: A list of Chapter instances representing the manga's chapters.
        """
        return self.chapter_list
    
    def get_chapter_list_length(self) -> int:
        """Get the length of the chapter list.

        Returns:
            int: The number of chapters in the manga's chapter list.
        """
        return len(self.chapter_list)
    
    def get_data(self) -> list:
        """Get the manga data.

        Returns:
            list: A list of dictionaries containing chapter data.
        """
        return self.data
    
    def get_browser(self):
        """Open the browser and navigate to the manga's URL."""
        self.browser = webdriver.Chrome(service = self.service, options = self.chrome_options)
        self.browser.get(self.url)
    
class Chapter():
    """
    Represents a chapter of a manga.

    This class stores information about a chapter, such as its title, date, and URL.
    It provides methods to parse the date string, compare chapter dates, and retrieve chapter details.

    Attributes:
        title (str): The title of the chapter.
        date (datetime.date): The date of the chapter.
        date_string (str): The original date string of the chapter.
        url (str): The URL of the chapter.

    Methods:
        parse_date: Parse the date string and store the date attributes.
        compare_chapter_dates: Compare the dates of two chapters.
        get_title: Get the title of the chapter.
        get_date: Get the date of the chapter.
        get_date_string: Get the original date string of the chapter.
        get_url: Get the URL of the chapter.
    """

    def __init__(self, title: str, date: str, url: str):
        """Initialize a Chapter instance.

        Args:
            title (str): The title of the chapter.
            date (str): The date of the chapter.
            url (str): The URL of the chapter.
        """
        self.title = title
        self.parse_date(date)
        self.url = url

    def parse_date(self, date: str):
        """Parse the date string and store the date attributes.

        The date string can be in the formats "MM/DD/YYYY", "XX hours ago", or "Yesterday at XX:XX AM/PM".

        Args:
            date (str): The date string to parse.
        """
        if(date[3].isnumeric()): # Date Format: MM/DD/YYYY
            self.date = DATETIME(int(date[6:]), int(date[:2]), int(date[3:5])).date() # Splicing the original string into a datetime object, then storing the object's date
            self.date_string = date # Preserve the original string (for printing to files)
        elif(len(date) < 20): # Date Format: "XX hours ago"
            self.date = DATE.today() # Ignore hours and set the chapter's date to today
            self.date_string = DATE.today().strftime("%m/%d/%Y") # Format today's date into the MM/DD/YYYY format
        else: # Date Format: "Yesterday at XX:XX AM/PM"
            self.date = (DATE.today()) - (TIMEDELTA(1)) # Get yesterday's date (timedelta(day))
            self.date_string = ((DATE.today()) - (TIMEDELTA(1))).strftime("%m/%d/%Y") # Format yesterday's date into the MM/DD/YYYY format

    def compare_chapter_dates(self, other_chapter: 'Chapter') -> bool:
        """Compare the dates of two chapters.

        Args:
            other_chapter (Chapter): The other chapter to compare with.

        Returns:
            bool: True if the current chapter's date is earlier than the other chapter's date
                  or if they were both uploaded on the same date,
                  False otherwise.
        """
        if(self.get_date() == other_chapter.get_date()): # Uploaded same day
            return(self.get_title() != other_chapter.get_title())
        else:
            return(self.get_date() < other_chapter.get_date())
        
    # Getters

    def get_title(self) -> str:
        """Get the title of the chapter.

        Returns:
            str: The title of the chapter.
        """
        return self.title
    
    def get_date(self) -> 'DATETIME.date':
        """Get the date of the chapter.

        Returns:
            datetime.date: The date of the chapter.
        """
        return self.date
    
    def get_date_string(self) -> str:
        """Get the original date string of the chapter.

        Returns:
            str: The original date string of the chapter.
        """
        return self.date_string
    
    def get_url(self) -> str:
        """Get the URL of the chapter.

        Returns:
            str: The URL of the chapter.
        """
        return self.url
    
# Functions
def parse_url(manga_title: str) -> str:
    """Parse the manga title and return the corresponding URL.

    Args:
        manga_title (str): The title of the manga.

    Returns:
        str: The URL of the manga.
    """
    return "https://manga4life.com/manga/{}".format(manga_title)

def get_user_choice() -> int:
    """Get the user's choice from the menu.

    Returns:
        int: The user's choice as an integer.
    """
    user_input = ""

    while True:
        print()
        print("[1]: Run the program")
        print("[2]: Add a manga to the manga title list")
        print("[3]: Delete a manga from the manga title list")
        print("[4]: View the manga list")
        print("[5]: Quit the program")
        print()
        user_input = input("Enter your choice (the corresponding number within the [square braces]): ")
        
        match user_input:
            case "1":
                return 1
            case "2":
                return 2
            case "3":
                return 3
            case "4":
                return 4
            case "5":
                return 5
            case _:
                print("Invalid input, please try again") # Last statement, so it automatically continues

def add_manga(manga_title_list: list) -> str:
    """Add a manga to the manga title list.

    Args:
        manga_title_list (list): The list of manga titles.

    Returns:
        str: The manga title to be added, or 'C' to cancel.
    """
    user_input = ""
    server_response = None # Holds the requests object of the URL of the inputted manga; used to get the server status code
    server_soup = None # Holds the page contents of the URL of the inputted manga

    print()
    print("Please input the URL title of the manga you wish to add (Ex: for the URL [https://manga4life.com/manga/Jujutsu-Kaisen], you would only input [Jujutsu-Kaisen])")

    while True:
        print()
        user_input = input("Enter the title of the manga (or 'C' to cancel): ")

        if(user_input.upper() == "C"):
            return "C"
        elif(user_input in manga_title_list): # Case sensitive
            print("This manga is already in the manga list, please try again")
            continue
        else:
            server_response = requests.get(parse_url(user_input)) # Get the URL
            if(server_response.status_code == 200): # URL is functioning
                server_soup = BeautifulSoup(server_response.content, "html.parser") # Get the content of the URL
                if(server_soup.find(class_="list-group top-10 bottom-5") == None): # This class, which holds the new chapters, does not exist in Manga4Life's MangaNotFound page
                    print("Manga4Life does not contain this manga, please try again")
                    continue
                else: # Valid manga
                    return user_input
            else: # URL is not functioning
                print("This manga does not lead to a working Manga4Life URL, please try again")
                continue

def update_manga_title_file(manga_title_list: list):
    """Update the manga title list file.

    Args:
        manga_title_list (list): The list of manga titles.
    """
    with open("MangaTitleList.txt", 'w', encoding="utf-8") as file:
        for manga_title in manga_title_list:
            file.write(manga_title + "\n")

def delete_manga(manga_title_list: list) -> int | str:
    """Delete a manga from the manga title list.

    Args:
        manga_title_list (list): The list of manga titles.

    Returns:
        int: The index of the manga to be deleted, or 'C' to cancel.
    """
    user_input = ""
    manga_index = 0

    while True:
        print()
        for i in range(0, len(manga_title_list)): # List the manga in the passed list and their 1-indexed indices
            print("(" + str((i+1)) + "): " + manga_title_list[i])
        print()

        user_input = input("Enter the corresponding number (in the [square braces]) of the manga to delete (or 'C' to cancel): ")

        if(user_input.upper() == "C"):
            return "C"
        elif(user_input.isnumeric()):
            manga_index = int(user_input) - 1 # 1-indexed - 1 = 0-indexed
            if(0 <= manga_index <= len(manga_title_list) - 1): # If valid index
                return manga_index
            else:
                print("That number is either too small or too large, please try again")
                continue
        else:
            print("Invalid input, please try again")
            continue

def delete_csvfile(manga_title: str):
    """Delete the CSV file associated with a manga.

    Args:
        manga_title (str): The title of the manga.
    """
    if(os.path.exists(manga_title + ".csv")): # If the csv file exists
        os.remove(manga_title + ".csv")

def list_manga(manga_title_list: list):
    """Print the list of manga titles.

    Args:
        manga_title_list (list): The list of manga titles.
    """
    print()
    print("Manga List: ")
    if(len(manga_title_list) == 0):
        print("None")
        return
    for i in range(0, len(manga_title_list)):
        print("(" + str((i+1)) + "): " + manga_title_list[i]) # 1-indexed

# Main
if __name__ == "__main__":
    # Driver Path [change to your chrome driver path]
    driver_path = r""

    # Manga File Directory [change to the folder where you'd like to store the manga files]
    manga_path = r""
    os.chdir(manga_path)

    # Variables
    manga_title_list = []
    manga_list = []
    user_choice = ""

    # Load manga titles from file, if it exists
    if(os.path.exists("MangaTitleList.txt")):
        with open("MangaTitleList.txt", 'r', encoding="utf-8") as file:
            manga_title_list += [line.strip() for line in file.readlines()]

    # Create Manga instances for each manga title
    for manga_title in manga_title_list:
        manga_list.append(Manga(manga_title, parse_url(manga_title), driver_path))

    print("~Beginning of Program~")
    print()

    while True:
        user_choice = get_user_choice() # Get user choice from menu

        match user_choice:
            case 1: # Run the program
                # Set up browser options and service
                chrome_options = Options()
                chrome_options.add_argument("--headless") # Stops browser from popping up
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Stops USB error messages from appearing on the shell script
                service = Service(driver_path)
                print_text = ""

                # Iterate over manga list
                for manga in manga_list:
                    manga.reset()  
                    print()
                    print("Checking " + manga.get_title() + ", URL: " + manga.get_url())

                    # Load chapter data from CSV file if it exists
                    if(os.path.exists(manga.get_title() + ".csv")):
                        with open(manga.get_title() + ".csv", 'r', newline='', encoding="utf-8") as csvfile:
                            csv_reader = csv.DictReader(csvfile)
                            for row in csv_reader:
                                manga.add_chapter(Chapter(row['Chapter Title'], row['Chapter Date'], row['Chapter URL']))
                    else: # If the manga doesn't have a csv file, it must be new (regardless of when it was added to the manga title list)
                        manga.set_is_new_manga()

                    # Set up and navigate browser
                    browser = webdriver.Chrome(service = service, options = chrome_options)
                    browser.get(manga.get_url())
                    time.sleep(2) # Necessary to properly load page
                    page_source = browser.page_source
                    browser.quit()

                    # Parse page contents and extract chapter information
                    page_soup = BeautifulSoup(page_source, "html.parser")
                    chapters = page_soup.find(class_="list-group top-10 bottom-5 ng-scope")
                    chapter_list = chapters.find_all(class_="list-group-item ChapterLink ng-scope")

                    # Update manga with new chapters
                    insert_index = 0
                    if(manga.get_chapter_list_length() != 0):
                        latest_chapter = manga.get_chapter(0)
                    else:
                        latest_chapter = None

                    for chapter in chapter_list:
                        # Extract chapter details
                        chapter_title_info = chapter.find(style="font-weight:600")
                        chapter_date_info = chapter.find(class_="d-block d-md-none ng-binding")

                        chapter_url = "manga4life.com" + chapter.get('href')
                        chapter_title_raw = re.sub(r'\W+', '', chapter_title_info.getText())
                        chapter_title = chapter_title_raw[:7] + " " + chapter_title_raw[7:]
                        chapter_date = chapter_date_info.getText()

                        curr_chapter = Chapter(chapter_title, chapter_date, chapter_url)

                        if(manga.contains_chapter(curr_chapter)): # Chapter is not recent, thus all further chapters are not recent either
                            break

                        if(latest_chapter != None):
                            if(not latest_chapter.compare_chapter_dates(curr_chapter)): # If not a new chapter
                                break

                        manga.add_chapter(curr_chapter, insert_index) # .addChapter(chapter, index) not .addChapter(index, chapter) <- like .insert()
                        insert_index += 1

                    if(insert_index > 0): # The insert_index having moved implies that new chapters have been added
                        manga.set_has_new_chapters()
                        manga.get_browser()

                    # Write chapter data to CSV file
                    with open(manga.get_title() + ".csv", 'w', newline='', encoding="utf-8") as csvfile:
                        csv_writer = csv.DictWriter(csvfile, fieldnames=['Chapter Title', 'Chapter Date', 'Chapter URL'])
                        csv_writer.writeheader()
                        csv_writer.writerows(manga.get_data())
                
                print()
                print("Updates: ")

                # Print updates
                for manga in manga_list:
                    if(manga.get_is_new_manga() == True):
                        print_text += manga.get_title() + " has been initialized." + "\n"
                    elif(manga.get_has_new_chapters() == True):
                        print_text += manga.get_title() + " has new chapters." + "\n"
                
                if(len(print_text) == 0): # If there were no updates or initializations
                    print("None")
                else:
                    print(print_text)

            case 2: # Add a manga to the manga title list
                manga_to_add = add_manga(manga_title_list)

                if(manga_to_add == "C"): # User inputted to cancel
                    continue

                manga_title_list.append(manga_to_add)
                manga_list.append(Manga(manga_to_add, parse_url(manga_to_add), driver_path, True)) # is_new_manga is passed as True
                print("Manga [" + manga_to_add + "] has been added to the manga title list")
                update_manga_title_file(manga_title_list)

            case 3: # Delete a manga from the manga title listS
                if(len(manga_title_list) == 0):
                    print("There are no manga to delete in the manga title list, please select another choice")
                    continue

                manga_index_to_delete = delete_manga(manga_title_list)

                if(manga_index_to_delete == "C"): # User inputted to cancel
                    continue

                manga_list.pop(manga_index_to_delete) # Index of a manga in the manga_title_list is the same as the manga_list
                delete_csvfile(manga_title_list[manga_index_to_delete])
                print("Manga [" + manga_title_list.pop(manga_index_to_delete) + "] has been deleted from the manga title list") # .pop both deletes and returns
                update_manga_title_file(manga_title_list)

            case 4: # View the manga list
                list_manga(manga_title_list)

            case 5: # Quit the program
                break

    print()
    print("~End of Program~")
