from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

class YTscraper:
    def __init__(self, channel_title):
        self.channel_title = channel_title

    def get_channel_id_from_title(self):
        chrome_options = webdriver.ChromeOptions()
        '''will use in heroku below'''
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument(' -- incognito')
        driver = webdriver.Chrome(chrome_options=chrome_options) #executable_path=os.environ.get("CHROMEDRIVER_PATH"),

        # Now you can start using Selenium
        driver.get('https://www.youtube.com/')

        driver.implicitly_wait(3)

        search_box = driver.find_element_by_xpath('//input[@id="search"]')

        # type channel title in the search box
        search_box.send_keys(self.channel_title)

        # click search button
        search_btn = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
        search_btn.click()

        driver.implicitly_wait(3)

        # get either channel_id or channel_username from channel_url
        channel_url = driver.find_element_by_css_selector('#contents > ytd-channel-renderer').find_element_by_xpath(".//div/div/a").get_attribute("href")
        if "youtube.com/channel/" in channel_url:
            channel_id = channel_url.split("youtube.com/channel/", 1)[1]
            return [True, channel_id]
        else:
            channel_username = channel_url.split("youtube.com/user/", 1)[1]
            return [False, channel_username]
