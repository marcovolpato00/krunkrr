# krunkrr

Automatically claim KR reward on [krunker.io](https://krunker.io)

## Prerequisites
```
git clone https://github.com/marcovolpato00/krunkrr.git
cd krunkrr/
pip3 install -r requirements.txt
```
Then follow [this guide](https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver?answertab=active#tab-top) to install chromedriver on your system. If you need to change the chromedriver executable path, edit **CHROMEDRIVER_PATH** inside [krunkrr.py](krunkrr.py)


## Authentication

In order for the script to authenticate with your account, you have to manually dump your browser localStorage. **You can do so using the Chrome browser the Developers Tools by pressing F12, then go to the Console tab and type**:

```
JSON.stringify(window.localStorage)
``` 

This will dump the localStorage in JSON format. Copy the output and put it in the **localstorage.json** file.


## Running the script
Manually:
```
python3 krunkrr.py
```

As a cron job, replace **DOWNLOAD_DIR** with the actual directory where you cloned this repo:
```
0 */6 * * * python3 DOWNLOAD_DIR/krunkrr.py   # runs every 6 hours
```

## Running on ARM based devices
For some reason, I wasn't able to run this script on ARM based devices such as Raspberry Pi and even more powerful devices like a Rock64. Instead I am using a small x86 computer, based on a low power Intel Atom processor. If you are able to find a solution, feel free to fork this project and submit a pull request.
