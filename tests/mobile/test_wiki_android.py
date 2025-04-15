from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be
import allure


def test_search(mobile_management):

    with step("Type search"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
        ).should(be.visible).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).should(
            be.visible
        ).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).should(
            be.visible
        ).type("Appium")

    with step("Verify content found"):
        results = browser.all(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        )
        results.should(have.size_greater_than(0))
        results.first.should(have.text("Appium"))


def test_open_article(mobile_management):

    with step("Type search"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
        ).should(be.visible).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).should(
            be.visible
        ).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).should(
            be.visible
        ).type("Appium")

    with step("Open article"):
        results = browser.all(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        )
        if results:
            results.first.click()
        else:
            allure.attach(
                "No results found",
                name="Search Result Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise Exception('No results found for the search term "Appium"')

        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/closeButton")).click()
        browser.element(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Appium"]')
        ).should(
            be.visible
        )  # Убедиться, что элемент появился
