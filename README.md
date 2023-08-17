# Table of Contents
- [Manga Update Web Scraper](#manga-update-web-scraper)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)
- [Disclaimer](#disclaimer)

------------------------------

# Manga Update Web Scraper

![GitHub](https://img.shields.io/github/license/adedhi/manga4life-updates-tracker)

Manga Update Web Scraper is a Python program that allows users to track updates for their favourite manga titles by scraping the Manga4Life.com website. It provides an easy way to stay updated on new manga chapters and read them on the click of a button.

## Features
- Run the program to check for updates on the Manga4Life website and display the updates
- Automatically scrape and retrieve chapter details, including title, date, and URL
- Store chapter data for each manga using CSV files for persistence
- Add manga titles to a manga title list
- Delete manga titles from the manga title list
- View the manga title list

## Requirements
- Python 3.6
- Selenium
- Chrome WebDriver (Make sure to provide the driver path in the program)
- BeautifulSoup
- Requests
- Python CSV module
- Python OS module
- Python time module
- Python re module

## Installation
1. Download the code (main.py).
2. Install the required dependencies (Selenium, BeautifulSoup, Requests).
3. Download and place the ChromeWebDriver executable in the project directory. Make sure to provide the path to the driver in the program (driver_path, line 480)
4. Specify the file location to store the manga updates files. Make sure to provide the location to the program (manga_path, line 483)

## Usage
1. Run the python file (main.py)
2. Add manga titles to the manga title list by specifying the URL title of the manga on Manga4Life.
3. Run the program to check for updates. It will scrape the Manga4Life website and display any new chapters for the tracked manga titles.
4. Delete manga titles from the manga title list if desired.
5. View the manga title list to see the currently tracked manga titles.

------------------------------

# Contributing
Contributions to this project are welcome. Please feel free to contribute.

# License
This project is licensed under the MIT License - learn more about it [here](LICENSE).

# Acknowledgements
- The program depends on the Manga4Life website for retrieving manga information.

# Contact
If you have any questions, suggestions, or feedback, feel free to reach out to me at dadeshvir@gmail.com

# Disclaimer
This program is intended for educational and technical demonstration purposes only. It was developed to showcase programming skills and does not endorse or promote any form of illegal or unethical activity, including accessing unofficial scans or translations of manga.

The Manga4Life website, from which this program retrieves information, may host unofficial scans/translations of manga titles. It is important to note that unauthorized distribution and consumption of copyrighted material may infringe upon the rights of the original authors, artists, and publishers. As a responsible user, it is advised to support the official releases and purchase licensed copies of manga to ensure the creators receive due credit and compensation for their work.

The developer of this program holds no responsibility for any misuse or inappropriate use of the program. The actions and decisions of the users are solely their own responsibility. It is recommended to comply with all relevant copyright laws and terms of service when accessing and using online content.

Please respect the rights of the original authors and artists, and support the official releases to contribute to the manga industry.
