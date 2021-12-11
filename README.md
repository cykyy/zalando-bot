# Zalando-bot
zalando-prive.it is a different type of eCommerce than the popular ones such as amazon, eBay. Zalando-prive has this feature that allows the products curently on the cart to get expired after 20 minutes of idle. And their possibility of adding to cart for other customers work just like the cart system in a grocery store. For example, say on a shelf there's only 2 packet available for a product "A". Now two customer comes with their cart and takes each, now if any third person comes to buy the same product he/she can't because the product is still in someone else's cart regardless of the product being checked out or not. Now let's say the first two persons walk the store for another half an hour or an hour and maybe later decide he/she will not buy it and puts it away from the cart. What if the store somehow could've put a mechanism to detect how long a product is in a cart and at a certain time an employee comes and asks for checking out otherwise the employee puts away the product! This same mechanism is implemented on the Zalando-prive.it site. This script bypasses their mechanism. This script allows keeping products in the cart even after their cart expiry time which is 20 minutes of not checking out. This script uses selenium and Python 3.9

## Script

The script's starting point is (main function lives on) src/start.py. You can rename the start.py file (only this file). But you cannot change other file names, doing so will throw import error and break the script.

- start.py: This is the interactive starting point of the script.
- beta.py : This file is the actual root point for the bot. You can call start_script function on this file from anywhere(such as terminal) and try it out.
- zbot.py: This file contains zalando-prive selenium APIs functions. All the magic happens here.
- helper.py: Helper file contains all the helper functions for the script. Problem such as parsing and sortings are coded here.
- data.json: This is the local json based database. All information gets saved here. Don't edit anything on this file manually.
- conf.json: This is the config file. A very important one.

### conf.json
```{
  "auth": {
    "email": "",
    "password": ""
  },
  "setting": {
    "user_data_dir": "",
    "dummy_interval_minutes": 9,
    "dummy_shots_max_count": 14,
    "initial_implicitly_wait": 2,
    "response_rate": 0.10
  },
  "mail": {
    "enable": true,
    "from_mail_address": "",
    "password": "",
    "to_mail_address": ""
  }
}
```
#### Keys:
-- auth: 
* `email` - String - Email of zalando-prive
* `password` - String - Username of zalando-prive.

-- setting:
* `user_data_dir` - String - Chrome profile **user_data_dir** (visit chrome://version from chrome and copy profile path).
* `dummy_interval_minutes` - Int - Interval minutes between a dummy shot (A dummy shot resets the timer of all existing added to cart products to default 20minutes - Default 9
* `dummy_interval_minutes` - Int - How many times the dummy shot should get fired without sending any warning message (through email, terminal and log) to purchase the product. - Default 14
* `initial_implicitly_wait` - Float - Initial load time value. Waits for js,css,html to load on the initial run.
* `response_rate` - Float - Refresh rate, clicking response rate. Less is fast.

-- mail:
* `enable` - Bool - Enable mail feature or not. If **true**, sends mail.
* `from_mail_address` - String - From where the email will be sent. Also the Gmail SNMP username.
* `password` - String - SNMP Login password. Also supports gmail app password.
* `to_mail_address` - String - Where all the mail will be sent

#### start.py interactive bot menu:
-- menus: 
* `Authentication Menu` - Where you can record your zalando-prive email and password.
* `Product Menu` - All about products. Actions such as adding to cart, removing can be done here.
* `Dummy Product Menu` - All about dummy products. Currently, supports only two dummy product adding at a time. One for primary if primary fails then secondary takes the fall.
* `Logs Menu` - Logs viewing and all. Currently, not implemented. For future update.
* `Run Script Now` - Executes the script.
* `Quit` - Exits the script.

### Notes:
Use url format like this when adding a url of a product using the interactive tool, **https://www.zalando-prive.it/campaigns/ZZO1865/articles/AD541A1ZG-K11**
`do not use url which has categories inside them.`

## Features

- This script helps to purchase products on zalando-prive site.
- logs.txt file which contains all the information about the script runtime.
- Error handling such as if a product is not available anymore have been implemented. And many more error handling like this also implemented.

## How to start?
Great, now that we understand who does what and all the required fields, let's jump on to how we can execute the script successfully. Before executing the script make sure you create an account with the zalando-prive site. Now make ready your environment, install all the requirements (pip install -r requirements.txt) and Chrome browser on your machine. This script runs perfectly on **python version 3.9.7**.
At this point you can go ahead and run the **start.py** file, and the script should start. To debug any error please go to logs/logs.txt, and you will find script's runtime errors/success logs and other information.
* To run the script, type
```
python src/start.py or python start.py
```

One more important thing, **Please don't use your computer during script runtime**(atleast when the script loads a new item on the browser to add to cart, doing so will intercept script clicking mechanism on the browser which may ultimately lead failure to add a product to cart on time.)

**Thanks**
