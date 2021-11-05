import time
import datetime
from zbot import ZBot
from helper import get_link_details, get_time_difference_in_minute, write_logs, read_dict_from_file, get_config, \
    do_send_mail

zbot = ZBot()


def start_script():
    write_logs(f':OK: :beta.py: func: start_script; msg: script fired!;')
    last_fired_time = datetime.datetime.now()  # - datetime.timedelta(minutes=20)
    dummy_shot_count = 0  # keeps tracks of dummy shot.
    while True:
        time.sleep(0.3)
        # zbot.add_cookies()
        print('before login()')
        zbot.login()
        print("zbot.logged_in: ", zbot.logged_in)

        # driver = zbot.get_driver()
        # driver.refresh()

        data = read_dict_from_file('data.json')
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
            # print('last dummy fired:', difference, 'minutes ago')
            config_f = get_config(args='setting')
            if dummy_shot_count >= config_f.get('dummy_shots_max_count'):
                _msg = 'Please order the product as soon as possible. Cart timer adder aka "Dummy Shot" may not work anymore at this point!'
                try:
                    do_send_mail(to_mail=get_config(args='mail').get('to_mail_address'),
                                 sub='Warning Cart Timer Expiry',
                                 msg=_msg + ' Timestamp:' + str(datetime.datetime.now()))
                except Exception as emx:
                    print('Error sending mail', emx)
                    write_logs(
                        f':Error: :zbot.py: func: start_script; msg: Error occurred during sending mail for exceeding dummy shot counter;')  # exception: {emx}
                write_logs(
                    f':Warning: :beta.py: func: start_script; msg: {_msg} ;')
            if float(difference) >= config_f.get("dummy_interval_minutes"):  # interval minutes e.g. 9
                # fire the dummy cart function and update last fired time
                print('Firing Dummy Shot')
                zbot.cart_timer_handler(data.get('dummy_products'))
                print('end of dummy shot')
                last_fired_time = datetime.datetime.now()
                dummy_shot_count += 1

        difference = get_time_difference_in_minute(datetime.datetime.now(), last_fired_time)
        print('last dummy fired:', round(difference, 2), 'minutes ago')

        print('**program end**')
        print()
        time.sleep(0.2)  # define the intervals ( eg 2 mins or 5mins or any for script to re run )
        # break
    # time.sleep(50000)
