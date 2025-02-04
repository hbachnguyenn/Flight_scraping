import nodriver as uc
import asyncio
from datetime import datetime
import helper



def get_input_from_user(data: dict):
    print("Ho Chi Minh City - Sydney oneway flight")
    print("Please fill in the date of the flight!")
    print()

    while True:
        date = input("Please fill in the date: ")
        month = input("Please fill in the month: ")
        year = input("Please fill in the year: ")
        full_date = helper.date_format(date, month, year)
        if not helper.date_validation(full_date):
            print("Filled date is inappropriate, try again!")
            print()
            continue

        data['date'] = full_date
        break

async def scraper(data: dict):
    # Start the driver
    driver = await uc.start()

    # Navigate to the page
    page = await driver.get('https://www.vietnamairlines.com/vn/en/home')
    await page.sleep(2)

    # Accept all cookies
    cookie_accept_button = await page.query_selector('#cookie-agree')
    await cookie_accept_button.click()

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
    date = await table.query_selector(helper.date_css_selector(data['date']))
    await date.click()

    find_flight_button = await page.query_selector('#btnSubmitBookYourTrip')
    await find_flight_button.click()

    await page.sleep(8)
    for i in range(15):
        finding_date_cheapest_fare = await page.query_selector(f'#cdk-accordion-child-1 > div > refx-carousel > div > ul > li:nth-child({i+2}) > div > button > span.mdc-button__label > div.cell-content-top > div > refx-price-cont > refx-price > span > span')
        finding_date_cheapest_fare = finding_date_cheapest_fare.text
        print(helper.price_format(finding_date_cheapest_fare))

    await page.close()



if __name__ == '__main__':
    flight_info = {}
    get_input_from_user(flight_info)
    asyncio.get_event_loop().run_until_complete(scraper(flight_info))
