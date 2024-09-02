import random
import time
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException, NoSuchWindowException, TimeoutException
from selenium.webdriver.common.by import By
from selenium_recaptcha_solver import RecaptchaException, RecaptchaSolver


class WebScrapper:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()

    def google(self, query: str) -> BeautifulSoup:
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        self.driver.get(url)
        time.sleep(random.randint(5, 40) / 100)

        while True:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            if "подозрительный трафик" not in soup.text:
                break

            self.__solve_captcha(url)

        return soup

    def close(self) -> None:
        self.driver.quit()

    def __solve_captcha(self, url: str) -> None:
        wait_time = 0.1
        solver = RecaptchaSolver(driver=self.driver)

        while True:
            try:
                recaptcha = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                solver.click_recaptcha_v2(iframe=recaptcha)
                return
            except (RecaptchaException, TimeoutException, ElementClickInterceptedException, NoSuchElementException, NoSuchWindowException) as error:
                if "able to locate element" in f"{error}":
                    return

                if "has detected automated queries" in f"{error}":
                    self.driver.quit()
                    self.driver = webdriver.Firefox()
                    self.driver.get(url)
                    return

            time.sleep(wait_time)
            self.driver.get(url)
            wait_time = min(wait_time * 1.5, 5)
