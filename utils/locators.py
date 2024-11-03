from selenium.webdriver.common.by import By


class Locators:
    search_icon = (By.CSS_SELECTOR, "a[aria-label='Search']")
    search_input = (By.CSS_SELECTOR, "input[placeholder='Search...']")
    channels_tab = (By.XPATH, "//div[contains(text(), 'Channels')]")
    streamer_list = (By.CSS_SELECTOR, "div[role='list'] div.ieOTqj a.tw-link")
    random_streamer = (By.CSS_SELECTOR, "div[role='list'] div.ieOTqj a.tw-link")
    start_watching = (By.XPATH, "//div[contains(text(), 'Start Watching')]")
    proceed = (By.XPATH, "//div[contains(text(), 'Proceed')]")
    main_content = (By.CSS_SELECTOR, "main[aria-label='Main Content']")