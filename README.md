
# Twitch Streamer Test Automation Framework

This repository contains a Selenium-based test automation framework in Python, built to automate Twitch platform tests on a mobile emulator.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Generating Reports with Allure](#generating-reports-with-allure)
- [Directory Structure](#directory-structure)

## Prerequisites
- Python 3.8 or higher
- Google Chrome
- ChromeDriver (automatically managed by WebDriver Manager)
- Allure command-line tool for generating reports ([installation guide](https://docs.qameta.io/allure/#_get_started))

## Installation

1. **Clone the repository**:
    ```bash
    git clone git@github.com:vtly-volkov/WAP_testing.git
    cd WAP_testing
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Allure** (required for report generation):
    - **On macOS**:
        ```bash
        brew install allure
        ```
    - **On Windows**:
        Download the Allure binary from [here](https://github.com/allure-framework/allure2/releases) and add it to your system PATH.

## Configuration

### Chrome Mobile Emulator Setup

This framework uses a mobile emulator by setting Chrome's device emulation in `conftest.py`. The default device is set to "Pixel 3". Modify `chrome_mobile_emulator()` in `conftest.py` to specify other devices as needed.

### Environment Variables (Optional)

Set environment variables to configure paths if needed. This is generally not required as the framework auto-generates temporary files where necessary.

## Writing Tests

Tests are written using `pytest` and follow a simple structure. 

### Example Test Case

Below is an example of a test case to search for a StarCraft II streamer on Twitch:

```python
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

@allure.feature("Twitch Streaming Test")
@allure.story("Search and open a streamer for StarCraft II")
def test_twitch_starcraft_search(chrome_mobile_emulator):
    driver = chrome_mobile_emulator
    driver.get("https://www.twitch.tv")
    
    with allure.step("Click the search icon"):
        search_icon = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Search']")
        search_icon.click()
    
    with allure.step("Input 'StarCraft II' in search"):
        search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
        search_input.send_keys("StarCraft II")
        search_input.send_keys(Keys.ENTER)
        time.sleep(3)  # Wait for results to load
    
    with allure.step("Select a random streamer"):
        streamer_list = driver.find_elements(By.CSS_SELECTOR, "div[role='list'] div.ieOTqj a.tw-link")
        assert streamer_list, "No streamers found."
        random.choice(streamer_list).click()
    
    with allure.step("Take a screenshot of the streamer's page"):
        # Save a screenshot for Allure
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            screenshot_path = tmp_file.name
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Streamer Page", attachment_type=allure.attachment_type.PNG)
```

## Running Tests

1. **Run All Tests**:
    ```bash
    pytest
    ```

2. **Run Specific Test**:
    ```bash
    pytest tests/test_twitch_streamer.py::test_twitch_starcraft_search
    ```

## Generating Reports with Allure

To generate and view an Allure report:

1. **Run Tests**: Ensure tests generate results in the `allure-results` directory.

2. **Generate and Open Report**:
    ```bash
    allure serve allure-results
    ```

Alternatively, to generate a static report in `allure-report` directory:
   ```bash
   allure generate allure-results -o allure-report --clean
   allure open allure-report
   ```

## Directory Structure

The project is organized as follows:

```plaintext
.
├── tests/
│   ├── test_twitch_streamer.py     # Example test file
│   └── conftest.py                 # Pytest fixtures for setup/teardown
├── requirements.txt                # Dependencies
└── README.md                       # Project documentation
```

## Notes
- **Temporary Files**: Screenshots are saved in cross-platform compatible temporary directories using Python's `tempfile` module.
- **Error Handling**: The framework includes handling for modals/pop-ups that may appear before streams load.

## Additional Resources
- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Allure Documentation](https://docs.qameta.io/allure/)
