import logging
from typing import Optional, List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
)

from settings import get_settings


settings = get_settings()
logging.basicConfig(level=logging.INFO)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = settings.WAIT_TIMEOUT
        self.wait = WebDriverWait(
            self.driver,
            self.timeout,
            ignored_exceptions=[StaleElementReferenceException],
        )

    def find_element(self, locator) -> WebElement:
        element = None
        try:
            element = self.wait.until(ec.presence_of_element_located(locator))
        except TimeoutException:
            logging.INFO(
                f"BasePage:find_element:Timed out waiting for page to load for {locator}"
            )
        except StaleElementReferenceException:
            logging.INFO(
                f"BasePage:find_element:Element {locator} is not attached to the page document"
            )
        assert (
            element is not None
        ), f"WebElement with locator {locator} is not presented at the page"
        return element

    def find_elements(self, locator: str) -> Optional[List[WebElement]]:
        try:
            return self.wait.until(ec.presence_of_all_elements_located(locator))
        except TimeoutException:
            logging.INFO(f"Elements not found: {locator}")
        except StaleElementReferenceException:
            logging.INFO(
                f"BasePage:find_element:Element {locator} is not attached to the page document"
            )

    def wait_for_page_load(self, locator):
        try:
            self.wait.until(ec.presence_of_element_located(locator))
        except TimeoutException as e:
            logging.ERROR(
                "BasePage:wait_for_page_load:Timed out waiting for page to load"
            )
            raise e

    def is_element_present(self, locator, timeout: int = settings.WAIT_TIMEOUT) -> bool:
        try:
            wait = WebDriverWait(self.driver,
                                 timeout=timeout,
                                 ignored_exceptions=[StaleElementReferenceException])
            wait.until(ec.presence_of_element_located(locator)).is_displayed()
            return True
        except TimeoutException:
            return False