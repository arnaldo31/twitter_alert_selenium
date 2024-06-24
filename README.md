# Twitter Alerts (Scraper and Repost)

## Overview

This project aims to automate the process of scraping tweets containing a specific keyword, downloading associated media, and reposting the most liked tweets. The script performs these actions every 20 minutes, ensuring that you stay updated with the latest and most popular tweets. 

## Process of Script

1. **Scrape Tweets**: Fetch tweets containing the exact phrase specified by the given keyword every 20 minutes.
2. **Download Media**: Download all media from the fetched tweets and save them into the `media` folder.
3. **Message of Telegram groups
5. **Log Scraped Tweets**: Save the scraped tweets into `twitter_alert.txt`.
6. **Repeat**: Wait for 20 minutes and repeat the process.

## Technologies Used
- Python
- JSON
- playwright
- 
## Installation

### 1. Install Python

- Ensure you have [Python](https://www.python.org/downloads/) installed.
- During installation, check the `Add to PATH` checkbox.

### 2. Install Required Packages
Open your command prompt (cmd) and run the following commands to install the necessary packages:

     ```
     pip install requests
     pip install python-dotenv
     pip install pytz
     pip install pytest-playwright
     playwright install
     
     ```


### 3. Download the Repository
   - Download this repository's code from [GitHub](https://github.com/arnaldo31/twitter_alert_selenium/archive/refs/heads/main.zip).

### 4. Unzip the File
   - Unzip the downloaded file. If you do not have an unzip application, you can download one [here](https://www.7-zip.org/a/7z2406-x64.exe).

## How to Use

1. Open the folder where this project is saved on your local machine.
2. Log in your twitter account on your main google chrome browser.
2. Open `.env` file if you want to change keyword.
    
5. Add this bot to your group `@artzz_bot`
6. Add Telegram group ID to `telegram_groups_ids.txt` - (e.g., `-4213490693` from "https://web.telegram.org/a/#-4213490693") ensuring the bot is already a member of the group before doing so. 
6. Run the `main.py` script to start the scraping.
7. Scrape results will be saved as `twitter_alerts.txt` located inside the save folder.

## Files and Directory Structure

 - `main.py` - The main script to start the scraping.
 - `save/` - Folder where scraped tweets are saved.
 - `media/` - Folder where downloaded media files are saved.
 - `.env` - containing keyword and telegram bot api key.

