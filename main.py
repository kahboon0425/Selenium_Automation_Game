import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_driver_path = Service("C:Users/User/chromedriver")
driver = webdriver.Chrome(service=chrome_driver_path,  chrome_options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID,"cookie")

# Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR,"#rightPanel #store div")
item_ids = [item.get_attribute("id") for item in items]
# print(item_ids)


# Get current time + 5 seconds
timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5 minutes
while True:
    cookie.click()

    # Every 5 seconds
    if time.time() > timeout:
        price_element = driver.find_elements(By.CSS_SELECTOR, "#rightPanel #store div b")

        item_prices = []

        for prices in price_element:
            if prices.text != "":
                # print(prices.text.split("-"))
                price = int(prices.text.split("-")[1].strip().replace(",", ""))
                # print(price)
                item_prices.append(price)
        #
        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # print(item_prices)

        # Get current cookie count
        money_element = driver.find_element(By.ID,"money")
        current_money = int(money_element.text)
        # print(current_money)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, cookie_id in cookie_upgrades.items():
            if current_money > cost:
                affordable_upgrades[cost] = cookie_id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break









