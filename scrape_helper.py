import nodriver as uc
import helper
import pandas as pd
from datetime import datetime, timedelta


async def load_driver_and_page():
    # Start the driver
    driver = await uc.start()

    # Navigate to the page
    page = await driver.get('https://www.vietnamairlines.com/vn/en/home')
    await page.sleep(2)

    # Accept all cookies
    cookie_accept_button = await page.query_selector('#cookie-agree')
    await cookie_accept_button.click()
    return page

async def fill_in_data(page, date: datetime):
    # Select and interact with the "flight from" input field
    flight_from = await page.query_selector('#city-from-roundtrip')
    await flight_from.click()
    await flight_from.set_value("Ho Chi Minh City (SGN), Vietnam")

    # Select and interact with the "flight to" input field
    flight_to = await page.query_selector('#to-bookYourTripTo-OCEANIA > ul > li:nth-child(2) > a > div')
    await flight_to.click()

    # Select and click the "oneway" radio button
    oneway = await page.query_selector('#oneway')
    await oneway.click()

    # Select date
    flight_date = await page.query_selector('#roundtrip-date-depart')
    await flight_date.click()

    table = await page.query_selector('#byt-datespicker > div > div.ui-datepicker-group.ui-datepicker-group-first > table')
    date = await table.query_selector(helper.date_css_selector(date))
    await date.click()

    find_flight_button = await page.query_selector('#btnSubmitBookYourTrip')
    await find_flight_button.click()
    await page.sleep(8)
    return page

async def scrape_data_30_days(page) -> pd.DataFrame:
    # Initialize an empty DataFrame with the desired structure
    data = pd.DataFrame(columns=['departure', 'destination', 'price', 'brand', 'flight_date', 'scrape_date'])
    i = 0

    while i < 30:
        # Select the cheapest fare for the current day
        selector_path = f'#cdk-accordion-child-1 > div > refx-carousel > div > ul > li:nth-child({i + 8}) > div > button > span.mdc-button__label > div.cell-content-top > div > refx-price-cont > refx-price > span > span'
        cheapest_fare_selector = await page.query_selector(selector_path)

        if cheapest_fare_selector:
            # Create a record and append it to the DataFrame
            record = {
                'departure': 'SGN',
                'destination': 'SYD',
                'price': helper.price_format(cheapest_fare_selector.text),
                'brand': 'VN',
                'scrape_date': datetime.now().strftime("%Y-%m-%d"),
                'flight_date': (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
            }
            data = pd.concat([data, pd.DataFrame([record])], ignore_index=True)  # Update the DataFrame
            i += 1  # Move to the next day only if a fare is found
        else:
            # Handle the "load more" scenario
            load_more_btn = await page.query_selector(
                '#cdk-accordion-child-1 > div > refx-carousel > div > ul > li.more-dates-btn-container.ng-star-inserted > button'
            )
            if load_more_btn:
                await load_more_btn.click()
                await page.sleep(1)

    await page.close()
    return data
