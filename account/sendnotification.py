import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from decouple import config
import requests
import json

# Initialize the default Firebase app
cred = credentials.Certificate("firebasekey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def send_push_notification(push_token, title, message_body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=message_body),
            token=push_token,
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)
    except Exception as e:
        print(e)

# Initialize another Firebase app with a different name
cred_user = credentials.Certificate("firebasekeyuser.json")
if 'user_app' not in firebase_admin._apps:
    user_app = firebase_admin.initialize_app(cred_user, name='user_app')

def send_push_notification_user(push_token, title, message_body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=message_body),
            token=push_token,
        )
        response = messaging.send(message, app=firebase_admin.get_app('user_app'))
        print('Successfully sent message:', response)
    except Exception as e:
        print(e)
