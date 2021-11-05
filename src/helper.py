import datetime
import json
import os


def get_time_difference_in_minute(time_start, time_end):
    time_diff = time_start - time_end
    return time_diff.total_seconds() / 60


def get_link_details(link_key_lst):
    """returns all info about a link in a key value pair"""
    option_dict = {}
    for link in link_key_lst:
        option_dict.update({"link": link})
        link_details = link_key_lst.get(link)
        # print('link: ', link_details)
        options = link_details.get('options')
        size = options.get('size')
        size_XPATH = size.get('XPATH')
        option_dict.update({"sizeXPATH": size_XPATH})

        is_added = link_details.get('history').get('cart').get('added')
        option_dict.update({"is_added": is_added})
    # print('option_dict: ', option_dict)
    return option_dict


def update_cart_info_to_data_json(link_details):
    # print('testing')
    _link = link_details.get('link')
    data = read_dict_from_file('data.json')

    products = data.get("products")
    for product in products:
        # print(product)
        for link_key in product:
            if link_key == _link:
                # now make the changes
                product_info = product.get(link_key)
                history = product_info.get('history')
                # print(history)
                cart = history.get('cart')
                cart['added'] = True
                cart['timestamp'] = str(datetime.datetime.now())
                # print('44')

    write_json_from_dict(new_dict=data, rel_file_path='data.json')


def update_auth_cred(email, password):
    config = read_dict_from_file(file='config.json')
    auth = config.get("auth")
    auth.update({"email": email})
    auth.update({"password": password})

    write_json_from_dict(new_dict=config, rel_file_path="config.json")


def add_new_product_on_data_json(link, size=''):
    data = read_dict_from_file(file='data.json')

    products = data.get("products")
    for product in products:  # iterating through list and getting dict
        for link_key in product:
            product_details = product.get(link_key)
            if link_key == link:
                history = product_details.get('history')
                if not history.get('cart').get('added'):
                    if product_details.get('options').get(
                            'size').get('XPATH') == size:
                        break
                    else:
                        print(
                            "Failed! Not allowed to add the same item with different size. First remove the other size then try again.")
                        return
    products.append(
        {
            link: {
                "options": {
                    "size": {
                        "active": True,
                        "text": "",
                        "XPATH": size,
                        "ID": ""
                    },
                    "quantity": 1
                },
                "history": {
                    "cart": {
                        "added": False,
                        "timestamp": ""
                    },
                    "mail": {
                        "sent": False
                    }
                }
            }
        }
    )

    write_json_from_dict(new_dict=data, rel_file_path='data.json')


def remove_product_from_data_json(link):
    data = read_dict_from_file('data.json')

    products = data.get("products")
    count = 0
    for product in products:
        for link_key in product:
            if link_key == link:
                print('matches!')
                products.pop(count)
        count += 1

    write_json_from_dict(new_dict=data, rel_file_path='data.json')


def show_products(products, already_added=False, to_be_added=False, all_item=False, dummy=False):
    count = 0
    print("ID   URL")
    for product in products:  # iterating through list and getting dict
        for link_key in product:
            product_details = product.get(link_key)
            history = product_details.get('history')
            if to_be_added:
                if history.get('cart').get('added'):
                    # added already
                    pass
                else:
                    print("{}    ".format(count) + link_key + ' ; ', end='')
                    if 'Size-XPATH: ' + product_details.get('options').get('size').get('XPATH'):
                        print('Size-XPATH: ' + product_details.get('options').get(
                            'size').get('XPATH'))
            elif already_added:
                if history.get('cart').get('added'):
                    # added already
                    print("{}    ".format(str(count)) + link_key + ' ; ' + 'Mail-Status: ' + str(
                        product_details.get('history').get(
                            'mail').get('sent')) + ' ; ', end='')
                    if product_details.get('history').get('mail').get('sent'):
                        print('Timestamp:', product_details.get('history').get('mail').get('timestamp'), ' ; ', end='')
                    if 'Size-XPATH: ' + product_details.get('options').get('size').get('XPATH'):
                        print('Size-XPATH: ' + product_details.get('options').get(
                            'size').get('XPATH'))
                else:
                    pass
            elif all_item:
                print("{}    ".format(str(count)) + link_key + ' ; Already-added: ' + str(
                    product_details.get('history').get('cart').get('added')), '; ', end='')
                if not dummy:
                    print('Mail-Status: ' + str(product_details.get('history').get('mail').get('sent')) + ' ; ', end='')
                    if product_details.get('history').get('mail').get('sent'):
                        print('Timestamp:', product_details.get('history').get('mail').get('timestamp'), '; ', end='')
                if 'Size-XPATH: ' + product_details.get('options').get('size').get('XPATH'):
                    print('Size-XPATH: ' + product_details.get('options').get(
                        'size').get('XPATH'))
        count += 1


def show_to_be_added_on_cart_product():
    data = read_dict_from_file('data.json')
    products = data.get("products")  # returning list
    show_products(products=products, to_be_added=True)  # function call to show product
    print()
    while True:
        choice = str(input("Do you want to remove specific link? (Yes/No):"))
        if choice == 'Yes':
            try:
                to_remove = int(input("Type an ID to remove:"))
                products2 = data.get("products")  # returning list
                count2 = 0
                for product2 in products2:  # iterating through list and getting dict
                    if count2 == to_remove:
                        products2.pop(to_remove)
                    count2 += 1

                write_json_from_dict(new_dict=data, rel_file_path='data.json')
                show_products(products=products2)
                break
            except Exception as e:
                print(e)
        else:
            return


def show_already_added_on_cart_product():
    data = read_dict_from_file('data.json')
    products = data.get("products")  # returning list
    show_products(products=products, already_added=True)  # function call to show product
    print()


def show_all_products():
    data = read_dict_from_file('data.json')
    products = data.get("products")  # returning list
    print("Showing all products")
    show_products(products=products, all_item=True)  # function call to show product
    print()
    while True:
        print("    :Submenu:    ")
        print("     1. Remove a specific item ")
        print("     2. Remove all item ")
        print("     3. Go back ")
        choice = int(input("Enter:"))
        if choice == 1:
            try:
                to_remove = int(input("Type an ID to remove:"))
                products2 = data.get("products")  # returning list
                count2 = 0
                for product2 in products2:  # iterating through list and getting dict
                    if count2 == to_remove:
                        products2.pop(to_remove)
                    count2 += 1
                write_json_from_dict(new_dict=data, rel_file_path='data.json')
                print("Showing all products")
                show_products(products=products2, all_item=True)
                continue
            except Exception as e:
                print(e)
        elif choice == 2:
            products2 = data.get("products")  # returning list
            products2.clear()

            write_json_from_dict(new_dict=data, rel_file_path='data.json')
            print('Item list cleared successfully.')
            break
        elif choice == 3:
            return
        else:
            print("Input mismatch! Please enter correct menu number.")
            continue
    return


def add_new_dummy_product_on_data_json(link, size=''):
    data = read_dict_from_file('data.json')

    products = data.get("dummy_products")
    if len(products) > 1:
        print("Failed! Not allowed to add more than two item on dummy product list.")
        return
    for product in products:  # iterating through list and getting dict
        for link_key in product:
            product_details = product.get(link_key)
            if link_key == link:
                history = product_details.get('history')
                if not history.get('cart').get('added'):
                    if product_details.get('options').get(
                            'size').get('XPATH') == size:
                        break
                    else:
                        print(
                            "Failed! Not allowed to add the same item with different size. First remove the other size then try again.")
                        return
    products.append(
        {
            link: {
                "options": {
                    "size": {
                        "active": True,
                        "text": "",
                        "XPATH": size,
                        "ID": ""
                    },
                    "quantity": 1
                },
                "history": {
                    "cart": {
                        "added": False,
                        "timestamp": ""
                    }
                }
            }
        }
    )

    write_json_from_dict(new_dict=data, rel_file_path='data.json')


def remove_dummy_product_from_data_json(link):
    data = read_dict_from_file('data.json')

    products = data.get("dummy_products")
    count = 0
    for product in products:
        for link_key in product:
            if link_key == link:
                print('matches!')
                products.pop(count)
        count += 1
    write_json_from_dict(new_dict=data, rel_file_path='data.json')


def show_all_dummy_products():
    data = read_dict_from_file('data.json')
    products = data.get("dummy_products")  # returning list
    print("Showing all dummy products")
    show_products(products=products, all_item=True, dummy=True)  # function call to show product
    print()
    while True:
        print("    :Submenu:    ")
        print("     1. Remove a specific item ")
        print("     2. Remove all item ")
        print("     3. Go back ")
        choice = int(input("Enter:"))
        if choice == 1:
            try:
                to_remove = int(input("Type an ID to remove:"))
                products2 = data.get("dummy_products")  # returning list
                count2 = 0
                for product2 in products2:  # iterating through list and getting dict
                    if count2 == to_remove:
                        products2.pop(to_remove)
                    count2 += 1

                write_json_from_dict(new_dict=data, rel_file_path='data.json')
                print("Showing all products")
                show_products(products=products2, all_item=True, dummy=True)
                break
            except Exception as e:
                print(e)
        elif choice == 2:
            products2 = data.get("dummy_products")  # returning list
            products2.clear()

            write_json_from_dict(data, 'data.json')
            print('Item list cleared successfully.')
            break
        elif choice == 3:
            return
        else:
            print("Input mismatch! Please enter correct menu number.")
            continue
    return


def write_logs(args='', start=False):
    try:
        from pathlib import Path
        Path("logs").mkdir(parents=True, exist_ok=True)
    except Exception as wl:
        print('Error writing logs! exception:', wl)
        pass
    logs = open("logs/logs.txt", "a")
    if not start:
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        logs.write('[' + dt_string + '] ')
        # logs.write('_ppp' + ':' + 'blah blah args:' + ' -> ' + args + '\n')
    print(args)
    logs.write(args + '\n')
    logs.close()


def read_dict_from_file(file):
    """Reads dict from a json formatted file and returns the dict"""
    import json
    with open(os.path.abspath(os.path.dirname(__file__)) + '/' + file) as f:
        data = f.read()
    js = json.loads(data)
    # print(json.dumps(js, indent=3))
    return js


def write_json_from_dict(new_dict, rel_file_path):
    """Reads dict from a json formatted file and returns the dict"""
    with open(os.path.abspath(os.path.dirname(__file__)) + '/' + rel_file_path, 'w') as updating_json:
        json.dump(new_dict, updating_json)
    # print(json.dumps(js, indent=3))
    return True


def get_config(args=''):
    """
    :param args: takes str (e.g: 'auth').
    :return: returns settings as dict for parameterized args type (e.g: 'auth') from config.json file. if no param supplied returns the whole dict.
    """
    conf = read_dict_from_file("config.json")
    if args:
        d_conf = conf.get(args)
        return d_conf
    else:
        return conf


def do_send_mail(to_mail, sub, msg):
    """Send mail using SMTP"""
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        # print('starting')
        mail_content = msg
        # The mail addresses and password
        config_m = get_config('mail')
        sender_address = config_m.get('from_mail_address')
        sender_pass = config_m.get('password')
        # print('sender_address', sender_address)
        receiver_address = to_mail
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = sub  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        return True
    except Exception as e:
        print(f'Sending mail failed! exception: {e}')
        write_logs(f':Error: :helper.py: func: do_send_mail; msg: Failed to send email!;')  # exception: {e}
        return False
