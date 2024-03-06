[![status workflow test](https://github.com/cirebon-dev/notification_bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/cirebon-dev/notification_bot/actions) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

With [@sendh_bot](https://t.me/sendh_bot) you can easy to send file or text message to telegram from anywhere (Terminal, CI/CD pipeline, IoT device etc)

![Screenshot 1](Screenshots/Screenshot_1.png)

![Screenshot 2](Screenshots/Screenshot_2.png)

![Screenshot 3](Screenshots/Screenshot_3.png)

This service is stateless, so your privacy is highly protected, and you can deploy it in your own instance.

## Run Locally (self hosted)

1. install dependency with `pip install -r requirements.txt`.

2. generate key with `python keygen.py`.

3. edit `.env.example` file and renamed to `.env`.

4. type command `gunicorn --bind 0.0.0.0:80 wsgi`
 
5. open browser `https://your-host/update_webhook`

now you can start chatting with your bot :)
