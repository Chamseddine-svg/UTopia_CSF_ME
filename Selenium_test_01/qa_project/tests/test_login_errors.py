import pytest
from pages.login_page import LoginPage
from utils.json_reader import load_test_data
from selenium.common.exceptions import TimeoutException

test_data = load_test_data("data/login_errors.json")

@pytest.mark.parametrize("data", test_data, ids=lambda d: d["case"])
def test_login_error_messages(driver, data):
    login = LoginPage(driver)
    login.load()
    login.login(data["username"], data["password"])

    try:
        # Try to get the error message
        error_message = login.get_error_message()
        # Assert it matches the expected error
        assert error_message == data["expected_error"], (
            f"Test {data['case']} failed: expected error '{data['expected_error']}', got '{error_message}'"
        )
        # Close error and verify
        login.close_error()
        assert login.is_error_closed()
    except TimeoutException:
        # No error appeared → user logged in instead
        pytest.fail(f"Test {data['case']} failed: user logged in instead of showing error")

