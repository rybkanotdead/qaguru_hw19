import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
from config import config
from selene_ac import utils
from appium import webdriver


@pytest.fixture(scope='function')
def android_management():
    options_dict = {
        "app": config.app if config.app.startswith('bs://')
        else utils.resource.path(config.app),
        "appWaitActivity": "org.wikipedia.*",
    }

    if config.udid:
        options_dict["udid"] = config.udid
    if config.deviceName:
        options_dict["deviceName"] = config.deviceName
    if config.platformVersion:
        options_dict["platformVersion"] = config.platformVersion

    options = UiAutomator2Options().load_capabilities(options_dict)

    if config.context == 'bstack':
        options.set_capability('bstack:options', {
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack first_test',
            'userName': config.bstack_userName,
            'accessKey': config.bstack_accessKey,
        })

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            config.remote_url,
            options=options
        )

    browser.config.timeout = config.timeout
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield
    utils.attach.attach_screenshot(browser)
    utils.attach.attach_xml(browser)

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    if config.context == 'bstack':
        utils.attach.attach_bstack_video(session_id)