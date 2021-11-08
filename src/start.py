import datetime
from helper import update_auth_cred, add_new_product_on_data_json, remove_product_from_data_json, \
    show_to_be_added_on_cart_product, show_already_added_on_cart_product, show_all_products, \
    add_new_dummy_product_on_data_json, remove_dummy_product_from_data_json, show_all_dummy_products, write_logs, \
    read_dict_from_file


def start():
    print("***** Welcome to ZBot *****")
    print()
    truth_table = ['y', 'Y', 'yes', 'YES', 'Yes', 'yEs', 'YeS', 'YES']
    false_table = ['n', 'N', 'no', 'NO', 'No', 'nO']
    while True:
        print("Choose 1, 2 or 3 from below: ")
        print("1. Authentication Menu")
        print("2. Product Menu")
        print("3. Dummy Product Menu")
        print("4. Run Script Now!")
        print("5. Quit")
        selected = int(input("Enter:"))
        print()

        if selected == 1:
            # Authentication Menu

            config = read_dict_from_file(file='config.json')
            print("Choose 1 or 2 from below: ")
            print("1. Show details")
            print("2. Update credentials")
            print("3. Go home")
            selected_11 = int(input("Enter:"))
            if selected_11 == 1:
                print()
                print("Credentials from config.json")
                print("Email: ", config.get("auth").get("email"))
                print("Password: ", config.get("auth").get("password"))
            elif selected_11 == 2:
                print()
                email_input = str(input("Enter new email:"))
                pass_input = str(input("Enter new password:"))
                update_auth_cred(email_input, pass_input)
            elif selected_11 == 3:
                print()
                continue
            else:
                print("Input mismatch! Please enter correct menu number.")
                continue

        elif selected == 2:
            # Product Menu
            while True:
                print("Choose 1 or 2 from below: ")
                print("1. Add a product")
                print("2. Remove a product")
                print("3. Show to-be-added-on-cart products")
                print("4. Show already added-on-cart products")
                print("5. Show all products")
                print("6. Go home")
                selected_21 = int(input("Enter:"))

                if selected_21 == 1:
                    # Add product
                    print()
                    product_link_input = str(input("Enter product link(exactly the color you want): "))
                    size_input_check = str(input("Does the item have any Size option? Yes/No/Exit: "))
                    if size_input_check in truth_table:
                        product_size_input = str(input(
                            "Enter product size XPATH(using chrome inspect tool, copy the correct clickable button xpath): "))
                        if 'button' not in product_size_input:
                            print('Failed! Please insert correct XPATH!')
                            continue
                        add_new_product_on_data_json(link=product_link_input,
                                                     size=product_size_input)  # adding item on data
                        print('Successfully added!')

                    elif size_input_check in false_table:
                        add_new_product_on_data_json(link=product_link_input)  # adding item on data
                        print('Successfully added!')

                    elif size_input_check == 'Exit' or size_input_check == 'exit' or size_input_check == 'ex':
                        print('Going back...')
                        continue
                    else:
                        print("Choice mismatch! Try again!")
                        continue
                elif selected_21 == 2:
                    print()
                    selected_22 = str(input(
                        "Enter product link to remove(exclude all tailing from url such as '/?=blahblah'. Perfect link example, https://www.example.com/abc/123 : "))
                    remove_product_from_data_json(selected_22)
                elif selected_21 == 3:
                    print()
                    show_to_be_added_on_cart_product()
                elif selected_21 == 4:
                    print()
                    show_already_added_on_cart_product()
                elif selected_21 == 5:
                    print()
                    show_all_products()
                elif selected_21 == 6:
                    print()
                    break
                else:
                    print("Input mismatch! Please enter correct menu number.")
                    continue

        elif selected == 3:
            while True:
                print("Choose 1 or 2 from below: ")
                print("1. Add a Dummy product")
                print("2. Remove a Dummy product")
                print("3. Show all dummy products")
                print("4. Show dummy products status")
                print("5. Go home")
                selected_31 = int(input("Enter:"))

                if selected_31 == 1:
                    # Add Dummy product
                    print()
                    product_link_input = str(input("Enter product link(exactly the color you want): "))
                    size_input_check = str(input("Does the item have any Size option? Yes/No/Exit: "))
                    if size_input_check in truth_table:
                        product_size_input = str(input(
                            "Enter product size XPATH(using chrome developer mode, copy the correct clickable button xpath): "))
                        if 'button' not in product_size_input:
                            print('Failed! Please insert correct XPATH!')
                            continue
                        add_new_dummy_product_on_data_json(link=product_link_input,
                                                           size=product_size_input)  # adding item on data
                    elif size_input_check in false_table:
                        add_new_dummy_product_on_data_json(link=product_link_input)  # adding item on data

                    elif size_input_check == 'Exit' or size_input_check == 'exit' or size_input_check == 'ex':
                        print('Going back...')
                        continue
                    else:
                        print("Choice mismatch! Try again!")
                        continue

                elif selected_31 == 2:
                    print()
                    selected_32 = str(input(
                        "Enter product link to remove(exclude all tailing from url such as '/?=blahblah'. Perfect link example, https://www.example.com/abc/123 : "))
                    remove_dummy_product_from_data_json(selected_32)

                elif selected_31 == 3:
                    print()
                    show_all_dummy_products()
                elif selected_31 == 4:
                    print("OK! Dummy Feature Functional")
                elif selected_31 == 5:
                    break
                else:
                    print("Input mismatch! Please enter correct menu number.")
                    continue

        elif selected == 4:
            print('Bot loading....')
            from beta import start_script
            write_logs(
                f'Timestamp {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} :Script: func: None msg: Starting...',
                start=True)
            try:
                start_script()
            except Exception as e:
                print(f'exception - {e}')
                write_logs(
                    f':Error: start.py; func: start^4; msg: Error Occurred during executing the Zbot script;')

        elif selected == 5:
            quit("Thanks for using the bot! Developer https://github.com/cykyy")

        else:
            print("Input mismatch! Please enter correct menu number.")
            continue

        print()


start()
