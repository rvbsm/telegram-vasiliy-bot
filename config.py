from os import getenv

APP_NAME = getenv('APP_NAME')
BOT_TOKEN = getenv('BOT_TOKEN')
MONGODB_URI = getenv('MONGODB_URI')

WEBHOOK_HOST = f'https://{APP_NAME}.herokuapp.com'
WEBHOOK_PATH = '/webhook/' + BOT_TOKEN
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = getenv('PORT', 5000)
