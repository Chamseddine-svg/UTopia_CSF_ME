from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_locators import LoginLocators  # Fixed import

class LoginPage:

    URL = "https://www.saucedemo.com/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self._type(LoginLocators.USERNAME, username)
        self._type(LoginLocators.PASSWORD, password)
        self.driver.find_element(*LoginLocators.LOGIN_BTN).click()

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(LoginLocators.ERROR_MSG)
        ).text

    def close_error(self):
        self.driver.find_element(*LoginLocators.ERROR_CLOSE_BTN).click()

    def is_error_closed(self):
        return len(self.driver.find_elements(*LoginLocators.ERROR_MSG)) == 0

    def _type(self, locator, value):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)