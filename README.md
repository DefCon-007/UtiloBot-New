<h1 align="center">Welcome to UtiloBot 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/DefCon-007/UtiloBot-New/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/defcon_007" target="_blank">
    <img alt="Twitter: defcon_007" src="https://img.shields.io/twitter/follow/defcon_007.svg?style=social" />
  </a>
</p>

> A multi-utility bot for Telegram. Make your life easier and get music links to every platform, shorten URLs, etc without ever leaving telegram.

### 🏠 [Homepage](https://utilobot.defcon007.com)

### ✨ [Demo](https://t.me/UtiloBot)

## Build

This bot is hosted on Google cloud functions for better scalability and less maintainance. 

The project is based on Python 3.6, make sure you have the correct python version by using `python --version` or `python3 --version`. 

- ```pip3 install virtualenv```
- Create a new virtual environment for the project.
  ```virtualenv -p python3 ./env```
- Activate the environment created in the last step.
  ```source ./env/bin/activate```
- Install the dependancies. 
  ```pip install -r requirements.txt```
- Now, you can work and add your logic in the `lambda_function.py`. This is the main file which runs when we receive a telegram API webhook. After you are done, just create a zip and upload it to AWS Lambda.
- Create a zip file.
  ```./create_zip.sh```

### Connecting Telegram 

- Use Telegram's BotFather to create a new bot and add the corresponding bot token as environment variable named `BOT_TOKEN`. 
- After the cloud function deployment is done, we need to add a new webhook url to get updates. Copy the cloud function public URL and use the guide [here](https://xabaras.medium.com/setting-your-telegram-bot-webhook-the-easy-way-c7577b2d6f72) to create a new webhook.

## Author

👤 **Ayush Goyal**

* Website: https://www.defcon007.com/
* Twitter: [@defcon_007](https://twitter.com/defcon_007)
* Github: [@DefCon-007](https://github.com/DefCon-007)
* LinkedIn: [@defcon-007](https://linkedin.com/in/defcon-007)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Ayush Goyal](https://github.com/DefCon-007).<br />
This project is [MIT](https://github.com/DefCon-007/UtiloBot-New/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
