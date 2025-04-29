from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be
import allure


def perform_search(search_query):
    """Функция для выполнения поиска по запросу"""
    with step("Type search"):
        browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")
        ).should(be.visible).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).should(
            be.visible
        ).click()
        search_box = browser.element(
            (AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")
        )
        search_box.should(be.visible).type(search_query)


def test_search(android_management):
    search_query = "Appium"

    # Выполнение поиска
    perform_search(search_query)

    with step(f"Verify content found for '{search_query}'"):
        results = browser.all(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        )

        assert len(results) > 0, f"No results found for search term '{search_query}'"
        results.first.should(have.text(search_query))


def test_open_article(android_management):
    search_query = "Appium"

    # Выполнение поиска
    perform_search(search_query)

    with step(f"Open article for '{search_query}'"):
        results = browser.all(
            (AppiumBy.ID, "org.wikipedia.alpha:id/page_list_item_title")
        )

        if results:
            results.first.click()
        else:
            allure.attach(
                f"No results found for '{search_query}'",
                name="Search Result Error",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise Exception(f'No results found for search term "{search_query}"')

        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/closeButton")).click()
        browser.element(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Appium"]')
        ).should(
            be.visible
        )  # Проверяем, что элемент появился
