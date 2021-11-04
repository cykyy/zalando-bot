import json
import pickle
import random
import time
import datetime

import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.zbot import ZBot
from src.helper import get_link_details, get_time_difference_in_minute, write_logs

# 1635458594
zbot = ZBot()


def start_script():
    write_logs(f':OK: :beta.py: func: start_script; msg: script fired!;')
    last_fired_time = datetime.datetime.now()  # - datetime.timedelta(minutes=20)
    while True:
        time.sleep(0.3)
        # zbot.add_cookies()
        print('before login()')
        zbot.login()
        print("zbot.logged_in: ", zbot.logged_in)

        # driver = zbot.get_driver()
        # driver.refresh()
        with open('data_test.json') as f:
            data = json.load(f)
        # logics

        for link_key in data.get("products"):  # iterating through all products link
            # print("loop link_url:", link_key)
            link_details = get_link_details(link_key_lst=link_key)
            if not link_details.get('is_added'):
                print("link_url:", link_key)
                print('New product found to add to cart. Adding...')
                time.sleep(0.3)
                # zbot.do_add_to_cart(link_details=link_details)
                zbot.add_to_cart(link_details=link_details, update_data_json=True)
                time.sleep(0.3)
            else:
                # link already added on cart
                pass

            # dummy starts
            time_now = datetime.datetime.now()
            difference = get_time_difference_in_minute(time_now, last_fired_time)
            print('last dummy fired:', difference, 'minutes ago')
            if float(difference) >= 0.50:
                # fire the dummy cart function and update last fired time
                print('Firing Dummy Shot')
                zbot.cart_timer_handler(data.get('dummy_products'))
                print('end of dummy shot')
                last_fired_time = datetime.datetime.now()

        print('**program end**')
        print()
        time.sleep(0.2)  # define the intervals ( eg 2 mins or 5mins or any for script to re run )
        # break
    # time.sleep(50000)
