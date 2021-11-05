import datetime
import json
import pickle
import random
import time
import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from helper import get_link_details, update_cart_info_to_data_json, write_logs, get_config, do_send_mail


def check_element_existence(driver, _By, key):
    """If the supplied element found, returns True else returns False"""
    try:
        if _By == 'ID':
            driver.find_element(By.ID, key)
            return True
        elif _By == 'XPATH':
            driver.find_element(By.ID, key)
            return True
    except NoSuchElementException:
        print(":OK: Element not found, No login required. Already Logged in.")
        return False
    return False


class ZBot:
    def __init__(self):
        self.options = uc.ChromeOptions()
        sx = random.randint(1000, 1500)
        sn = random.randint(3000, 4500)
        wsize = "--window-size=" + str(sx - 10) + ',' + str(sn - 10)
        self.options.add_argument(str(wsize))
        self.options.add_argument(
            '--no-first-run --no-service-autorun --password-store=basic --disable-features=UserAgentClientHint')
        # options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36')
        user_data_dir = get_config(args='setting').get('user_data_dir')
        self.options.add_argument(user_data_dir)
        self.driver = uc.Chrome(options=self.options)
        self.driver.get("https://www.zalando-prive.it/")
        self.driver.implicitly_wait(get_config(args='setting').get('initial_implicitly_wait'))  # ok?
        self.logged_in = False

    def add_extra_options(self, option):
        """Sets supplied option to the browser"""
        self.options.add_argument(option)

    def set_chrome_default_profile(self):
        """Sets default chrome profile"""
        user_data_dir = get_config(args='setting').get('user_data_dir')
        self.options.add_argument(user_data_dir)

    def add_cookies(self):
        cookies = pickle.load(open("cookiesUndetected.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
            # print(cookie)
        self.driver.refresh()

    def get_driver(self):
        return self.driver

    def do_login(self):
        """logins to the site"""
        try:
            self.driver.find_element(By.ID, 'topbar-cta-btn').click()
            self.driver.implicitly_wait(3)

            login_mail = self.driver.find_element(By.XPATH, '//*[@id="form-email"]')
            # login_mail.clear()
            auth = get_config(args='auth')
            print('auth:', auth)
            login_mail.send_keys(auth.get('email'))
            login_pass = self.driver.find_element(By.XPATH, '//*[@id="form-password"]')
            login_pass.send_keys(auth.get('password'))
            login_submit = self.driver.find_element(By.XPATH,
                                                    '//*[@id="react-root-form"]/div/div/div[2]/div/div[2]/div/div/div/form/button')
            login_submit.click()
            print('Login succeed!')
            return True
        except Exception as e:
            print(e)
            write_logs(
                f':Error: :zbot.py: func: do_login; msg: Error occurred during login to the site!;')
            return False

    def login(self):
        if check_element_existence(driver=self.driver, _By='ID', key='topbar-cta-btn'):
            if self.do_login():
                self.logged_in = True
        else:
            self.logged_in = True  # though needs more testing on it. Loosely set

    def do_add_to_cart(self, link_details, response_rate=0.10):
        try:
            self.driver.get(link_details.get('link'))
            time.sleep(response_rate)
            # driver.find_element(By.XPATH, '//*[@id="article-information"]/div[5]/div[2]/div[2]/div[3]/button').click()
            if link_details.get('sizeXPATH'):
                self.driver.find_element(By.XPATH, link_details.get('sizeXPATH')).click()  # clicking the size button
            time.sleep(response_rate/3)
            dax = self.driver.find_element(By.XPATH, '//*[@id="addToCartButton"]/button') # clicking the add to cart button
            print(dax.text)
            if dax.text != 'PRENOTATO TEMPORANEAMENTE':
                dax.click()
            else:
                # not on stock
                print('Product is out of stock')
                return False
            return True
        except Exception as ace:
            print("Error: do_add_to_cart: ", ace)
            write_logs(
                f':Error: :zbot.py: func: do_add_to_cart; msg: Error occurred during adding product to cart!;')
            return False

    def add_to_cart(self, link_details, update_data_json=True, dummy=False, response_rate=0.20):
        resp = self.do_add_to_cart(link_details=link_details, response_rate=response_rate)
        if update_data_json and resp:
            if dummy:
                write_logs(f':OK: :zbot.py: func: add_to_cart; msg: dummy shot product({link_details.get("link")}) added to cart; args:[dummyShot=True]')
            else:
                _msg = f'new product({link_details.get("link")}) added to cart.'
                if get_config(args='mail').get('enable'):
                    try:
                        do_send_mail(to_mail=get_config(args='mail').get('to_mail_address'), sub='New product added to cart', msg=_msg + ' Timestamp:' + str(datetime.datetime.now()))
                    except Exception as emx:
                        print(f'Error sending mail.  exception: {emx}')
                        write_logs(f':Error: :zbot.py: func: add_to_cart; msg: Error occurred during sending mail;')
                write_logs(f':OK: :zbot.py: func: add_to_cart; msg: {_msg} ;')
            # now update to data json that we added on the cart.
            update_cart_info_to_data_json(link_details=link_details)

    def do_remove_from_cart(self, link_details):
        # self.driver.get(link_details.get('link'))
        self.driver.find_element(By.XPATH, '//*[@id="header-cart"]').click()
        time.sleep(2)
        # shop_elems = self.driver.find_elements_by_xpath("//div[@class='styles__Scroller-sc-11yjvrp-1']")
        # shop_elems2 = self.driver.find_elements(By.XPATH, "//div[@class='styles__Scroller-sc-11yjvrp-1 dPAMwk']")
        shop_elems3 = self.driver.find_elements(By.CLASS_NAME, "styles__CartItemWrapper-sc-1utvdr0-0")
        # x = shop_elems[1].find_element(By.XPATH, ".//a")
        # print('x.....:', x)
        for elem in shop_elems3:
            try:
                a_elem = elem.find_element(By.XPATH, './/a')
                # pull out the item name
                name = a_elem.get_attribute('href')
                # print('dummy removing link:', name)
                # print('link_details.get("link") ', link_details.get('link'))
                if link_details.get('link') == name:
                    # matched, now remove
                    elem.find_element(By.XPATH, './/button').click()  # removing from cart
                    print('trash remove dummy item cart button clicked!')
                    return True
            except Exception as ee:
                print('2nd: ', ee)
                write_logs(f':Error: :zbot.py: func: do_remove_from_cart; msg: Failed to remove dummy item from cart!;')
        return False

    def cart_timer_handler(self, dummy_products):
        """solves the 20 minutes cart expiry. adds and removes dummy product to keep products in cart"""
        link_details = None
        for product in dummy_products:
            try:
                # print('product: ', product)
                link_details = get_link_details(product)
                self.do_add_to_cart(link_details=link_details)
                write_logs(
                    f':OK: :zbot.py: func: cart_timer_handler; msg: dummy shot product({link_details.get("link")}) added to cart; args:[dummyShot=True, timerResets=True]')
                break  # only using first dummy product for handling, if first ones failes, tries second one.
            except Exception as e:
                print("cart_timer_handler: ", e)
                write_logs(f':Error: :zbot.py: func: cart_timer_handler; msg: Error occurred during adding dummy product for time reset!;')
        time.sleep(0.3)  # waiting to remove the added card
        self.do_remove_from_cart(link_details=link_details)
