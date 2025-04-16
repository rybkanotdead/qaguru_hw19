import os
import pytest
import allure
import allure_commons
from selene import browser, support
from appium import webdriver
from config import config
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def init_app_session(options):
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options
        )
    browser.config.timeout = float(os.getenv('timeout', '10.0'))
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )


def tear_down_session():
    utils.attach.attach_screenshot(browser)
    utils.attach.attach_xml(browser)

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils.attach.attach_bstack_video(session_id)


def android_options():
    return UiAutomator2Options().load_capabilities({
        'platformVersion': '9.0',
        'deviceName': 'Google Pixel 3',
        'app': config.app,
        "appWaitActivity": "org.wikipedia.*",
        'bstack:options': {
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack Android test',
            'userName': config.bstack_userName,
            'accessKey': config.bstack_accessKey,
        }
    })


def ios_options():
    return XCUITestOptions().load_capabilities({
        'deviceName': 'iPhone 11',
        'platformName': 'ios',
        'platformVersion': '13',
        'app': config.app_ios,
        'bstack:options': {
            'userName': config.bstack_userName,
            'accessKey': config.bstack_accessKey,
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack iOS test',
        }
    })


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Mobile platform to run tests on: android or ios"
    )


@pytest.fixture(scope='function')
def mobile_management(request):
    platform = request.config.getoption("--platform")

    if platform == "android":
        options = android_options()
    elif platform == "ios":
        options = ios_options()
    else:
        raise pytest.UsageError(f"--platform must be 'android' or 'ios', got '{platform}'")

    init_app_session(options)
    yield
    tear_down_session()
