# **MyAnimeList Scraper** <p align="center">
    <img alt="ViewCount" src="https://views.whatilearened.today/views/github/MShawon/github-clone-count-badge.svg">
    <a href='https://github.com/MShawon/github-clone-count-badge'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url=https://gist.githubusercontent.com/MShawon/cf89f3274d06170b8a4973039aa6220a/raw/clone.json&logo=github'></a>
</p>
***************************************************************************************************************************
### **Introduction**

This is a Python script for scraping anime data from the website MyAnimeList. It uses Selenium webdriver to navigate the website and extract anime information such as the titles, characters, streaming services, and more. The scraped data is then stored in JSON files.

***************************************************************************************************************************

### **Setup**

To use this script, you will need to have the following installed:

- Python 3
- Selenium
- Mozilla Firefox browser

***************************************************************************************************************************

### **Installation**

1. Clone the repository to your local machine.
2. Install the required dependencies with `pip install webdriver-manager` and `pip install selenium` .
3. Run the script with `python scrape_myanimelist.py`.

***************************************************************************************************************************

### **Usage**

1. Clone this repository to your local machine.
2. Open the terminal and navigate to the repository.
3. Run the command `python3 scrape_myanimelist.py` to start the script.

***************************************************************************************************************************

### **How it Works**

The script loops through each letter of the alphabet and scrapes all the anime data for that letter. It then saves the data in a JSON file named after the corresponding letter. For example, anime titles starting with the letter "A" will be saved in a file called "A.json".

The script navigates to each page of anime titles for each letter using Selenium webdriver. It also uses the expected_conditions module to handle waiting for elements to load before scraping data.

The script extracts various data points for each anime such as the English and Japanese titles, characters, streaming services, and more. If data is not available, it is marked as "N/A" in the JSON file.

***************************************************************************************************************************

### **Conclusion**

This Python script provides a way to easily scrape anime data from the website MyAnimeList. The data can be used for analysis, recommendations, or any other purpose. Feel free to modify the script to suit your needs.

***************************************************************************************************************************

Note: Do not abuse the site with excessive requests or use this code for unethical purposes. This code is intended for educational purposes only.
