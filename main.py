import requests
import time, os, csv
import json, re, random
from DrissionPage import ChromiumOptions
from DrissionPage import Chromium, ChromiumPage
from requests import session
from lxml.html import fromstring
from fake_useragent import UserAgent
ua = UserAgent()


def browser_setup():
    driver = ChromiumPage()
    time.sleep(2)

    option = ChromiumOptions()
    option.headless()
    return driver


