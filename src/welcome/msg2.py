import os
import requests
import json
import datetime as dt
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime


client = WebClient(token=os.environ['HR_BOT_TOKEN'])
channel_id = 'U017RGMB70S'

today = dt.datetime.now()
# date = today - dt.timedelta(days=37)
# test_date = date.strftime('%Y-%m-%d')
today = today.strftime('%Y-%m-%d')

headers = {
    "Authorization": "Bearer " + os.environ['TOKEN'],
    "Content-Type": "application/json ",
    "Notion-Version": "2021-08-16"}

info = []

cursor = None
while True:
    readUrl = f"https://api.notion.com/v1/databases/{os.environ['DATABASE_MOSCOW']}/query"
    if cursor:
        query = {'start_cursor': cursor}
        res = requests.post(readUrl, headers=headers, data=json.dumps(query))
    else:
        res = requests.post(readUrl, headers=headers)

    query = res.json()
    result_map = query.get('results')
    cursor = query.get('next_cursor')

    for k in result_map:
        info.append(k)

    if query.get('has_more') is False:
        break


for i in info:
    pers = i.get('properties')
    # if pers.get('ФИО').get('rich_text') == []:
    #     continue
    # name = pers.get('ФИО').get('rich_text')[0]['text']['content']
    if pers.get('Должность').get('rich_text') == []:
        continue
    position = pers.get('Должность').get('rich_text')[0]['text']['content']
    start_date = pers.get('Start Date').get('date').get('start')
    email = pers.get('Почта MySky').get('email')
    # print(email, position, start_date, start_date==test_date)

    if position == 'Стажер':
        continue

    try:

        response_1 = client.users_lookupByEmail(email=email)
        slack_id = response_1.get('user').get('id')

        text0_msk = 'Привет, <@' + slack_id + '>! :wave_hello:\n\nВ продолжение нашей адаптации, мы просим тебя:\n\n1. Разместить фото профиля в Slack и Gmail :bust_in_silhouette:\n2. Написать свою должность и номер телефона в Slack :telephone_receiver:\n3. Установить корпоративную <https://www.notion.so/mysky/Signatures-for-the-E-mail-5b8192e417e040b18f88ceafb1238e66|подпись> в Gmail  :mailbox_with_mail:\n\nЧтобы адаптация прошла легко, советуем изучить наш корпоративный портал: он дополнит знания, приобретенные на Welcome презентации.\n\n:computer: <https://www.notion.so/mysky/Home-Page-ef5ac1c7b5b64161b7155923c8fb640e|Корпоративный портал> - это единое информационное поле для всех сотрудников.\nТам ты сможешь найти:\n    • информацию о компании и продуктах;\n    • организационную структуру и профиль каждого сотрудника с контактными данными, включая календарь дней рождений, чтобы не пропустить поздравление коллеги;\n    • информацию о зарплатных и социальных проектах компании;\n    • самые часто задаваемые вопросы от того, как уйти в отпуск, до того, как получить справку с места работы (пожалуйста, удели этому пункту особое внимание, он ответит на многие твои будущие вопросы).\n\nНе стесняйся задавать вопросы!\nТвой руководитель поможет тебе со всеми рабочими моментами, любую IT-поддержку ты получишь в канале <#C0355MLB2E4>, а команда HR постарается сделать твою адаптацию максимально комфортной!\n\nДобро пожаловать, мы тебя ждали! :pig-hello-door:'

        message = ''

        if start_date == today:
            message = text0_msk

        if message != '':

            try:
                response_2 = client.chat_postMessage(
                    channel=slack_id,
                    text=message)

            except SlackApiError as e:
                assert e.response["ok"] is False  # The server responded with: {'ok': False, 'error': 'not_in_channel'}
                assert e.response["error"]
                print(f"Got an error: {e.response['error']}")

            date = (datetime.strptime(today, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d'))

            try:
                response_3 = client.chat_postMessage(
                    channel=channel_id,
                    text='Сообщение отправлено <@' + slack_id + '> - ' + str(date.days) + '-й день')

            except SlackApiError as e:
                assert e.response["ok"] is False
                assert e.response["error"]
                print(f"Got an error: {e.response['error']}")

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error missing info from Notion: {e.response['error']}")


info = []

cursor = None
while True:
    readUrl = f"https://api.notion.com/v1/databases/{os.environ['DATABASE_BELGOROD']}/query"
    if cursor:
        query = {'start_cursor': cursor}
        res = requests.post(readUrl, headers=headers, data=json.dumps(query))
    else:
        res = requests.post(readUrl, headers=headers)

    query = res.json()
    result_map = query.get('results')
    cursor = query.get('next_cursor')

    for k in result_map:
        info.append(k)

    if query.get('has_more') is False:
        break

for i in info:
    pers = i.get('properties')
    # if pers.get('ФИО').get('rich_text') == []:
    #     continue
    # name = pers.get('ФИО').get('rich_text')[0]['text']['content']
    if pers.get('Должность').get('rich_text') == []:
        continue
    position = pers.get('Должность').get('rich_text')[0]['text']['content']
    start_date = pers.get('Первый день').get('date').get('start')
    email = pers.get('Почта MySky').get('email')
    # print(email, position, start_date)

    if position == 'Стажер':
        continue

    try:

        response_1 = client.users_lookupByEmail(email=email)
        slack_id = response_1.get('user').get('id')

        text0_blg = 'Привет, <@' + slack_id + '>! :wave_hello:\n\nВ продолжение нашей адаптации, мы просим тебя:\n\n1. Разместить фото профиля в Slack и Gmail :bust_in_silhouette:\n2. Написать свою должность и номер телефона в Slack :telephone_receiver:\n3. Установить корпоративную <https://www.notion.so/mysky/Signatures-for-the-E-mail-5b8192e417e040b18f88ceafb1238e66|подпись> в Gmail  :mailbox_with_mail:\n\nЧтобы адаптация прошла легко, советуем изучить наш корпоративный портал: он дополнит знания, приобретенные на Welcome презентации.\n\n:computer: <https://www.notion.so/mysky/Home-Page-ef5ac1c7b5b64161b7155923c8fb640e|Корпоративный портал> - это единое информационное поле для всех сотрудников.\nТам ты сможешь найти:\n    • информацию о компании и продуктах;\n    • организационную структуру и профиль каждого сотрудника с контактными данными, включая календарь дней рождений, чтобы не пропустить поздравление коллеги;\n    • информацию о зарплатных и социальных проектах компании;\n    • самые часто задаваемые вопросы от того, как уйти в отпуск, до того, как получить справку с места работы (пожалуйста, удели этому пункту особое внимание, он ответит на многие твои будущие вопросы).\n\nНе стесняйся задавать вопросы!\nТы всегда можешь обращаться:\n    • к своему руководителю по всем рабочим моментам;\n    • к <@U5AL1N6NL> для оформления курьерского отправления или заказа необходимой для работы канцелярии;\n    • в канал <#C0355MLB2E4> за любой IT-поддержкой;\n    • к <@UH703GVL2> по всем кадровым вопросам.\n\nДобро пожаловать, мы тебя ждали! :pig-hello-door:'

        message = ''

        if start_date == today:
            message = text0_blg

        if message != '':

            try:
                response_2 = client.chat_postMessage(
                    channel=slack_id,
                    text=message)

            except SlackApiError as e:
                assert e.response["ok"] is False  # The server responded with: {'ok': False, 'error': 'not_in_channel'}
                assert e.response["error"]
                print(f"Got an error: {e.response['error']}")

            date = (datetime.strptime(today, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d'))

            try:
                response_3 = client.chat_postMessage(
                    channel=channel_id,
                    text='Сообщение отправлено <@' + slack_id + '> - ' + str(date.days) + '-й день')

            except SlackApiError as e:
                assert e.response["ok"] is False
                assert e.response["error"]
                print(f"Got an error: {e.response['error']}")

    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error missing info from Notion: {e.response['error']}")