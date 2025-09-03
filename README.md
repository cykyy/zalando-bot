# Zalando Bot 🛒

This Python script is designed to bypass the 20-minute cart expiry timer on `zalando-prive.it`. It helps you keep desired items in your shopping cart indefinitely, so you don't lose them to other customers while you continue browsing.

---

## How It Works

Zalando Privé reserves items in a cart for only 20 minutes. If you don't check out within that time, the items are released and become available to others.

This bot automates the process of "refreshing" your cart's timer. It periodically performs a "dummy shot"—a background action that interacts with your cart. This action resets the 20-minute expiry timer for all items, effectively holding them for you until you're ready to make a purchase.

---

## Features

-   **Cart Timer Bypass**: Keeps items in your cart beyond the standard 20-minute limit.
-   **Email Notifications**: Sends you a warning email when it's time to purchase your items before the bot stops refreshing.
-   **Detailed Logging**: Creates a `logs/logs.txt` file with detailed runtime information for easy debugging.
-   **Interactive CLI**: A simple command-line menu to configure credentials, manage products, and run the script.
-   **Robust Error Handling**: Manages common issues, such as a product going out of stock.

---

## Prerequisites

Before you begin, ensure you have the following installed and set up:

-   **Python 3.9+**
-   **Google Chrome** browser
-   A **Zalando Privé** account

---

## Setup & Usage

Follow these steps to get the bot up and running.

### 1. Installation

First, clone the repository and install the required Python packages.

```bash
# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd <your-repo-directory>

# Install dependencies
pip install -r requirements.txt
```

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
