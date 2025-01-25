import nodriver as uc
import asyncio


async def scraper():
    # Start the driver
    driver = await uc.start()
    print("Driver started successfully!")

    # Navigate to the page
    page = await driver.get('https://www.vietnamairlines.com/vn/en/home')
    print("Navigated to the website.")

    # Wait for the page to load fully
    await page.sleep(5)  # Adjust as necessary
    print("Page loaded.")

    cookie_accept_button = await page.query_selector('#cookie-agree')
    await cookie_accept_button.click()
    await page.sleep(3)

    # Select and interact with the "flight from" input field
    flight_from = await page.query_selector('#city-from-roundtrip')
    await flight_from.click()
    await flight_from.set_value("Ho Chi Minh City (SGN), Vietnam")
    await page.sleep(3)

    # Select and interact with the "flight to" input field
    flight_to = await page.query_selector('#to-bookYourTripTo-OCEANIA > ul > li:nth-child(2) > a > div')
    if flight_to:
        await flight_to.click()
        print("Set 'Flight To' successfully.")
    else:
        print("Failed to find 'Flight To' input field.")

    # Wait briefly to see the result
    await page.sleep(5)

    # Select and click the "oneway" radio button
    oneway = await page.query_selector('#oneway')
    if oneway:
        await oneway.click()
        print("Clicked on the 'One-way' option successfully.")
    else:
        print("Failed to find the 'One-way' radio button.")

    # Wait briefly to observe changes
    await page.sleep(5)

    flight_date = await page.query_selector('#roundtrip-date-depart')
    await flight_date.click()

    table = await page.query_selector('#byt-datespicker > div > div.ui-datepicker-group.ui-datepicker-group-first > table')
    date = await table.query_selector('tbody > tr:nth-child(5) > td:nth-child(5)')
    await date.click()
    if date:
        print("Found date 31")

    # Close the page and driver

    find_flight_button = await page.query_selector('#btnSubmitBookYourTrip')
    await find_flight_button.click()
    await page.sleep(10)

    await page.close()
    print("Page closed. Script finished successfully.")


if __name__ == '__main__':
    asyncio.run(scraper())
