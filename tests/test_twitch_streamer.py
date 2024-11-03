import random
import tempfile

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

from settings import get_settings
from utils.base_page import BasePage
from utils.locators import Locators

settings = get_settings()


@allure.feature("Twitch Streaming Test")
@allure.story("Search and open a streamer for StarCraft II")
def test_twitch_starcraft_search(chrome_mobile_emulator):
    driver = chrome_mobile_emulator
    driver.get(settings.TWITCH_URL)
    page = BasePage(driver)

    with allure.step("Click the search icon"):
        page.find_element(Locators.search_icon).click()

    with allure.step("Input 'StarCraft II' in search"):
        page.find_element(Locators.search_input).send_keys("StarCraft II")
        page.find_element(Locators.search_input).send_keys(Keys.ENTER)
        page.wait_for_page_load(Locators.main_content)
        page.find_element(Locators.channels_tab).click()


    with allure.step("Scroll down twice"):
        actions = ActionChains(driver)
        for _ in range(2):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)

    with allure.step("Select a random StarCraft II streamer"):
        streamer_list = page.find_elements(Locators.streamer_list)
        assert streamer_list, "No streamers found in the list."

        random_streamer = random.choice(streamer_list)
        random_streamer.click()

    with allure.step("Handle modal and take screenshot"):
        try:
            page.find_element(Locators.start_watching).click()
            page.find_element(Locators.proceed).click()
        except:
            pass

        page.wait_for_page_load(Locators.main_content)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            screenshot_path = tmp_file.name
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Streamer Page", attachment_type=allure.attachment_type.PNG)
