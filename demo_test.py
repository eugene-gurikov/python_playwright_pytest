from datetime import datetime
from random import randint

import pytest
from playwright.sync_api import sync_playwright, expect

now = datetime.utcnow()
ts = datetime.timestamp(now)


@pytest.fixture(scope="session", autouse=True)
def context():
    with sync_playwright() as playwright:
        # create browser and context
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        # close browser and context after run
        context.close()
        context.browser.close()


@pytest.fixture
def homepage_url(request, context):
    # home_url_preset - allows us to proceed to the tests directly using pre-set url
    home_url_preset = request.config.getoption('--home_url_preset')
    if home_url_preset is not None:
        return home_url_preset

    # declare options
    country = request.config.getoption('--country')
    city = request.config.getoption('--city')
    start_url = request.config.getini("base_url")

    page = context.new_page()
    page.goto(start_url)

    # choose country and city, proceed to home page
    if country is not None:
        page.get_by_alt_text(country).click()
        if city is not None:
            page.get_by_alt_text(city).click()
    else:
        # if no expected country and city specified
        # choose any random country, city (if needed) and continue...

        countries = page.query_selector_all("css=[data-testid='TestId__CountryListItemAnchor']")
        get_random_from(countries).click()
        page.wait_for_load_state("domcontentloaded")

        if page.url == start_url:
            cities = page.query_selector_all("css=[data-testid='TestId__CityListItem']")
            get_random_from(cities).click()
            page.wait_for_load_state("domcontentloaded")

    # verify that Home page was opened
    categories_frame = page.query_selector("//h2[contains(., 'Explore Categories')]")
    if page.url == start_url and categories_frame is None:
        raise AssertionError("A proper 'country' or 'city' name wasn't specified correctly! Home page didn't opened!")
    homepage_url = page.url
    page.close()
    return homepage_url


def get_random_from(array):
    return array[randint(0, len(array) - 1)]


def test_run(context, homepage_url) -> None:
    home_page = context.new_page()
    home_page.goto(homepage_url)

    # select random category from the list
    categories = home_page.query_selector_all("css=a.explore-category-item")
    get_random_from(categories).click()

    # wait for Products list to be loaded
    home_page.get_by_test_id("TestId__CategoryHeadline")
    home_page.get_by_test_id("TestId__ProductCardAnchor").last.wait_for()

    # get and select random product from the list
    products = home_page.query_selector_all("css=[data-testid='TestId__ProductCardAnchor']")
    product = get_random_from(products)
    product_title = product.query_selector("span").text_content()

    with context.expect_page() as new_page_info:
        product.click()

    # proceed with newly opened product page
    product_page = new_page_info.value
    product_page.wait_for_load_state("domcontentloaded")
    product_page_title = product_page.locator("css=main [data-testid='TestId__Container'] h1[itemprop='name']")
    product_page_title.wait_for()

    # expect Opened product page title to be equal to selected one
    expect(product_page_title).to_have_text(
        product_title), "Expected product page title to equal the selected one."

    # Verify product basket option shown
    product_basket_options_locator = "css=[data-testid='TestId__ProductBasket'] " \
                                     "> div:not([data-testid='TestId__ProductBasketSelectedItem'])"
    product_basket_options = product_page.locator(product_basket_options_locator)
    basket_count = product_basket_options.count()

    # Select all product basket options and continue
    if basket_count is not 0:
        for i in range(0, basket_count):
            option = product_basket_options.nth(i)
            option.locator("label").click()
            option.wait_for()

            # select first available option
            first_item = option.locator("css=[data-testid='TestId__ProductBasketCatItem'] button:not([disabled])").first
            if first_item.count() is 0:
                continue

            first_item.wait_for()
            first_item.click()

            option.locator("label").click()
            product_page.screenshot(path="screenshots/" + str(ts) + "_item_" + str(i) + ".png")
            product_page.wait_for_timeout(1000)
    else:
        product_page.screenshot(path="screenshots/" + str(ts) + ".png")

    # click on the 'Add to cart', continue
    product_page.get_by_role("button", name="Add to cart").click()
    product_page.get_by_test_id("TestId__ModalContainer").get_by_role("button", name="Continue").click()

    # expect Card message to be visible
    expect(product_page.get_by_role("heading", name="card message")).to_be_visible()
