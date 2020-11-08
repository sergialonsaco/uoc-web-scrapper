import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ScrapeQuotes: 
    def __init__(self):
        self.url = "http://quotes.toscrape.com/"
        self.driver = self._init_driver()
        self.data = pd.DataFrame()
        self.top_tags = []

    def _init_driver(self):
        # selenium driver to interact with the website
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        time.sleep(1)
        print(f"--- driver initialized in {self.driver.current_url}")

    def _get_soup_content(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")

    def _get_top_tags(self):
        """
        Get the top ten tags ranking
        """
        soup = self._get_soup_content(self.url)
        top_tags = soup.find("h2", text="Top Ten tags").parent
        self.top_tags = [tag.text.strip() for tag in top_tags.find_all("span")]

    def _navigate_next_page(self):
        """
        Navigates to the next page using the "next" button on it.
        Returns false if its the last page of the website.
        """
        try:
            next_button = self.driver.find_element_by_class_name("next")
        except Exception:
            print("not found")
            return False
        else:
            print("button found")
            a = next_button.find_elements_by_css_selector("*")
            a.click()
            self.url = self.driver.current_url
            return True

    def _is_top_tag(self, tags):
        """
        Evaluates if the given tags are on the top ten tags ranking.
        """
        for tag in tags:
            if tag in self.top_tags:
                return True
        return False

    def _get_quotes(self):
        """
        Scrape all quotes from the current page and store it on self.data
        """
        soup = self._get_soup_content(self.url)
        for quote in soup.find_all("div", "quote"):
            text = quote.find("span", itemprop="text").text
            author = quote.find("small", "author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            author_about = (
                "http://quotes.toscrape.com" + quote.find("a", text="(about)")['href']
            )
            row = pd.Series([author, text, tags, author_about, self._is_top_tag(tags)])
            self.data = self.data.append(row, ignore_index=True)

    def scrape(self):
        """
        Scrape all quotes from the website by navigating through all the pages.
        Store all the data obtained into a Pandas dataframe and returns it.
        """
        print(f"Starting scrapping {self.url}")
        self._get_top_tags()
        self._get_quotes()
        while self._navigate_next_page():
            self._get_quotes()
            print(f"scrapping...{self.url}")

    def to_csv(self, filename):
        """
        Generates a CSV with all the data scrapped.
        """
        if self.data is None:
            raise Exception("No data found")
        self.data.columns = ["author", "quote", "tags", "author_about", "top_ten_tags"]
        self.data.to_csv(filename, index=False)
