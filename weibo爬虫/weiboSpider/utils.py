from io import StringIO, BytesIO
import os
import re
from time import sleep
import random
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions, Options
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
import datetime
import pandas as pd
import platform
from selenium.webdriver.common.keys import Keys
# import pathlib

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib


def init_driver(headless=True, proxy=None, show_images=False, option=None, firefox=False, env=None):
    options = ChromeOptions()
    # 不显示浏览器界面
    options.add_argument("--headless")
    # 不使用沙盒模式
    # browser_options.add_argument("--no-sandbox")
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                             '/103.0.0.0 Safari/537.36'}
    if headless is True:
        print("Scraping on headless mode.")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        print("using proxy : ", proxy)
    if show_images == False and firefox == False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    if option is not None:
        options.add_argument(option)

    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(100)
    print("浏览器已成功创建。")

    return driver

