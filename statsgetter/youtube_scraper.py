from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os

class YTscraper:
    def __init__(self, channel_title):
        self.channel_title = channel_title

    def get_channel_id_or_username_from_title(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(' -- incognito')
        # the 2 lines below are for running on docker
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # can minimize time consumption. Reference: https://github.com/dinuduke/Selenium-chrome-firefox-tips
        prefs = {
        "profile.managed_default_content_settings.images":2,
        "profile.default_content_setting_values.notifications":2,
        "profile.managed_default_content_settings.stylesheets":2,
        "profile.managed_default_content_settings.cookies":2,
        "profile.managed_default_content_settings.javascript":1,
        "profile.managed_default_content_settings.plugins":1,
        "profile.managed_default_content_settings.popups":2,
        "profile.managed_default_content_settings.geolocation":2,
        "profile.managed_default_content_settings.media_stream":2,
        }
        chrome_options.add_experimental_option("prefs",prefs)

        try:
            # the 2 lines are used in heroku
            chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        except:
            driver = webdriver.Chrome(chrome_options=chrome_options)


        # get to the search result in youtube
        url = "https://www.youtube.com/results?search_query=" + self.channel_title
        driver.get(url)

        driver.implicitly_wait(3)

        # get either channel_id or channel_username from channel_url
        try:
            channel_url = driver.find_element_by_css_selector('#contents > ytd-channel-renderer').find_element_by_xpath(".//div/div/a").get_attribute("href")
            if "youtube.com/channel/" in channel_url:
                channel_id = channel_url.split("youtube.com/channel/", 1)[1]
                driver.quit()
                return [True, channel_id]
            else:
                channel_username = channel_url.split("youtube.com/user/", 1)[1]
                driver.quit()
                return [False, channel_username]
        except NoSuchElementException:
            return
