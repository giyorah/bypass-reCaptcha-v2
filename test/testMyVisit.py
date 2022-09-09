import sys
from selenium import webdriver
import random
import logging

sys.path.append('../src/')
from BotDetection import *

def config_logger(level: int = logging.INFO) -> None:
    fmt = '[%(levelname)s] %(message)s'
    logging.basicConfig(level=level, format=fmt)

USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44",
                    ]

# START OF PROGRAM - Create a Firefox driver
user_agent = random.choice(USER_AGENT_LIST)
options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", user_agent)
options.add_argument("--width=942")
options.add_argument("--height=1122")
# options.headless = True <-- this lets the applet run in silent (hidden) mode
driver = webdriver.Firefox(options=options)
driver.set_window_position(0, 0)

# Open the MyVisit webpage
config_logger()
url = 'http://myvisit.com/#!/home/provider/56'
logging.info(f"Opening the URL: {url}")
logging.info(f"Chosen user agent: {user_agent}")
driver.get(url)
sleep_gauss(7)
bypass_bot_detection(driver)
