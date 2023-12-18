#!/usr/bin/env python3

"""This script launches a browser (or mpv if possible) to the Twitch page of
the streamer passed as argument to the program if they're currently livestreaming,
else it will notify the user and won't launch the browser."""

import sys
import webbrowser

from shutil import which
from subprocess import Popen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

# Check if the user passed an argument to the program
if len(sys.argv) != 2:
    print("Usage: twitch.py <streamer>")
    sys.exit(0)

# Get the streamer name from the command line
streamer: str = sys.argv[1]

# Compose the URL to the streamer's Twitch page
url: str = "https://www.twitch.tv/" + streamer

# Do not open the browser
options: webdriver.ChromeOptions = webdriver.ChromeOptions()
options.add_argument("headless")

# Create a new Chrome session
driver: webdriver.Chrome = webdriver.Chrome(options=options)
# Get the page
driver.get(url)

print(f"Checking if {streamer} is online...")

# Initialize the element variable (the <p> element that contains the error message if the user is offline)
element: WebElement | None = None

# Raises error if the element is not found
try:
    # Locates the <p> element that contains the error message if the user is either offline or banned
    element = driver.find_element(
        By.XPATH,
        "//*[@id='root']/div/div[1]/div/main/div[1]/div[3]/div/div/div/div/div[2]/p",
    )
# Streamer is online
except NoSuchElementException:
    print(f"{streamer} is online! - Redirecting to Twitch page...")

    # EAFP
    try:
        # This will only work if the user is using Linux
        # If `mpv` and `yt-dlp` are installed, use it to open the stream
        # substitute with `vlc` or `mplayer` commands if you prefer respectively
        if which("mpv") and which("yt-dlp"):
            Popen(
                [
                    "mpv",
                    "--fullscreen",
                    "--no-terminal",
                    "--ytdl-format=best",
                    url,
                ]
            )
    except FileNotFoundError:
        # Open a tab in the browser to the streamer's Twitch page
        webbrowser.open(url)

    # Close the browser
    driver.quit()
    # Exit the program
    sys.exit(0)

print(f"{streamer} is offline! Exiting.")
