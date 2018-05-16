'''
О том, как подключить авторизацию, читайте тут https://pikabu.ru/story/api_vkontakte_dlya_python_3961240
'''

import vk  # alt enter
import time
import re

# 6469420
access_token = open('vk_key.txt', 'r').read()
session = vk.Session(
    access_token=access_token)
vkapi = vk.API(session, v='5.74')

SELF_ID = 486369485
SLEEP_TIME = 0.3

friends = vkapi('friends.get')  # получение всего списка друзей для текущего пользователя


def get_dialogs():
    dialogs = vkapi.messages.getDialogs()
    return dialogs


def get_all_history(user_id):
    rev = 1
    history = {'count': 0, 'items': []}
    i_offset = 0
    i_count = 200
    historyDic = vkapi.messages.getHistory(user_id=user_id, offset=i_offset, count=i_count, rev=rev)
    history['count'] += historyDic['count']
    history['items'] += historyDic['items']
    i_offset += i_count
    while historyDic['count'] == 200:
        time.sleep(0.3)
        historyDic = vkapi.messages.getHistory(user_id=user_id, offset=i_offset, count=i_count, rev=rev)
        history['count'] += historyDic['count']
        history['items'] += historyDic['items']
        i_offset += i_count
    return history


def get_all_dialogs_histories():
    historyDict = {}
    dialogs = get_dialogs()
    for dialog in dialogs['items']:
        friend_id = dialog['message']['user_id']
        hist = get_all_history(friend_id)
        historyDict[friend_id] = hist
    return historyDict
