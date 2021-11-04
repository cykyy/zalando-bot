# Script

The script's starting point is (main function lives on) src/start.py. You can rename the start.py file (only this file). But you cannot change other file names, doing so will throw import error and break the script.

- start.py: This is the interective starting point of the script.
- beta.py : This file is the actual root point for the bot. You can call start_script function on this file from anywhere(such as terminal) and try it out.
- zbot.py: This file contains zalando-prive selinium APIs functions. All the magic happens here.
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
    "user_data_dir": "user-data-dir=/Users/rayhanmia/Library/Application Support/Google/Chrome/Profile 1/",
    "dummy_interval_minutes": 9,
    "dummy_shots_max_count": 14
  },
  "mail": {
    "enable": true,
    "from_mail_address": "rayhan17c@gmail.com",
    "password": "gzjqfozjfygqnvyh",
    "to_mail_address": "kbir.opr@gmail.com"
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

-- mail:
* `enable` - Bool - Enable mail feature or not. If **true**, sends mail.
* `from_mail_address` - String - From where the email will be sent. Also the Gmail SNMP username.
* `password` - String - SNMP Login password. Also supports gmail app password.
* `to_mail_address` - String - Where all the mail will be sent

#### start.py interective bot menu:
-- menus: 
1 `Authentication Menu` - Where you can record your zalando-prive email and password.
2 `Product Menu` - All about products. Actions such as adding to cart, removing can be done here.
3 `Dummy Product Menu` - All about dummy products. Currently supports only two dummy product adding at a time. One for primary if primary fails then secodanry takes the fall.
4 `Logs Menu` - Logs viewing and all. Currently not implemented. For future update.
5 `Run Script Now` - Executes the script.
6 `Quit` - Exits the script.

### Notes:
Use url format like this when adding a url of a priduct using the interective tool, **https://www.zalando-prive.it/campaigns/ZZO1865/articles/AD541A1ZG-K11**
`do not use url which has categories inside them.`

## Features

- This script helps to purchase products on zalando-prive site.
- logs.txt file which contains all the information about the script runtime.
- Erorr handling such as if a product is not available anymore have been implemented. And many more error handling like this also implemented.

## How to start?
Great, now that we understand who does what and all the required fields, let's jump on to how we can execute the script successfully. Before executing the script make sure you create an account with the zalando-prive site. Now make ready your environment, install all the requirements (pip install -r requirements.txt) and chrome browser on your machine. This script runs perfectly on **python version 3.9.7**
At this point you can go ahead and run the **start.py** file and the script should start. To debug any error please go to logs/logs.txt and you will find script's runtime errors/success logs and other information.
* To run the script, type
```
python src/start.py or python start.py
```

One more important thing, **Please don't use your computer during script runtime**(atleast when a script loads a new item on the broswer to add to cart, doing so will interept script clicking mechanism on the browser which may ultimly lead failer to add a product to cart on time.)

**Thanks**
