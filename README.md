[![status workflow test](https://github.com/cirebon-dev/notification_bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/cirebon-dev/notification_bot/actions) 

With [@sendh_bot](https://t.me/sendh_bot) you can easy send notification/message to telegram from anywhere (Terminal, CI/CD pipeline, IoT device etc)

![Screenshot 1](Screenshots/Screenshot_1.png)

![Screenshot 2](Screenshots/Screenshot_2.png)

![Screenshot 3](Screenshots/Screenshot_3.png)

This service is stateless, so your privacy is highly protected, and you can deploy it in your own instance.

## Run Locally

1. type command `poetry self add poetry-dotenv-plugin`.

2. type command `poetry update`.

3. edit `.env.example` and renamed to `.env`.

4. type command `poetry run python app.py`
 
5. open browser `https://your-host/update_webhook`

now you can start chatting with your bot :)
