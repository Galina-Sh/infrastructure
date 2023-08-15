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
a = today - dt.timedelta(days=1)
b = today - dt.timedelta(days=14)
c = today - dt.timedelta(days=30)
d = today - dt.timedelta(days=60)
e = today - dt.timedelta(days=80)
f = today - dt.timedelta(days=95)
date1 = a.strftime('%Y-%m-%d')
date2 = b.strftime('%Y-%m-%d')
date3 = c.strftime('%Y-%m-%d')
date4 = d.strftime('%Y-%m-%d')
date5 = e.strftime('%Y-%m-%d')
date6 = f.strftime('%Y-%m-%d')

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
    # print(email, position, start_date)

    if position == 'Стажер':
        continue

    try:

        response_1 = client.users_lookupByEmail(email=email)
        slack_id = response_1.get('user').get('id')

        text1 = 'Привет :pig-hello-front:\nНадеемся, твой первый день прошел хорошо.\nМы понимаем, что у каждого из нас свой опыт за плечами и стараемся сделать все, чтобы наши ожидания от адаптации совпали.\nДля этого предлагаем пройти тебе <http://forms.gle/cZ3FXVKMgezPerfu6|опрос ожиданий> – он поможет нам создать для тебя максимально комфортные условия для быстрого ввода.\nСкорее проходи!'
        text2 = 'Привет :pig-hello-door:\nЮхуу, ты с нами уже 14 дней!\nНам важно понимать, как проходит твоя адаптация, поэтому предлагаем пройти <http://forms.gle/1rsFeLJvhewwyiZj6|мини опрос>. Он не займет больше 5 минут твоего времени.\nВперед!'
        text3 = 'Привет!\nСуперклассные новости – ты с нами уже целый месяц!\n\nСейчас самое время провести встречу 1:1 со своим руководителем для дополнительной прозрачности в ожиданиях обеих сторон. На всякий случай отправляем ссылку <http://docs.google.com/document/d/1JSPInrCcAb4mFb4eEzyhk51P3OQ9M5ZKXqLiQG3uyo4|подсказки, как провести разговор 1:1 с максимальной пользой>.\n\nТакже, нам важно услышать твое мнение о компании, работе в целом, адаптации, команде и понять, что мы делаем хорошо, а что с твоей точки зрения можно еще улучшить. Предлагаем прогуляться и поговорить! Возможно, у тебя будут вопросы, которые ты захочешь обсудить лично.\n\nЕсли тебе нужна помощь в назначении встреч – смело обращайся к любому сотруднику отдела HR&Admin.\n\nОтличного тебе настроения и до встречи!'
        text4 = 'Привет!\nТвой испытательный срок близится к завершению. Надеемся, что ты успешно пройдешь его :meow_highfive:\nНа данном этапе мы бы хотели узнать, как тебе работается в команде, к которой ты присоединился.\nБудем очень благодарны за <http://forms.gle/hLr87BbJM5YoouaY6|обратную связь>!'
        text5 = 'Привет!\nСовсем скоро закончится твой испытательный срок :clapping2:\n\nНам очень важно, чтобы твои ожидания от нашей компании оправдались. Прохождение <http://forms.gle/G6WRZfpJdq8aShau7|опроса> поможет нам поддержать процесс адаптации на высоком уровне и устранить возможные сложности, которые могли возникнуть в первые месяцы работы. Давай поможем будущим новичкам вместе :blush:\nБлагодарим и желаем успешного завершения испытательного срока!\n\nP.S. Если в анкете нет вопросов, которые ты хотел бы обсудить, но не хочешь об этом говорить с руководителем – ты всегда можешь рассчитывать на помощь HR – просто обратись с просьбой о личной беседе.'
        text6_msk = 'Привет, <@' + slack_id + '>!\nПоздравляем тебя с успешным официальным прохождением испытательного срока! (тут звучат радостные визги твоего рекрутера и звон бокалов твоей HR команды)\n\nТеперь тебе доступны новые дары богов:\n    • ДМС;\n    • Ежегодные медицинские чекапы;\n    • Возможность включить в страховку Стоматологию;\n    • Страхование при выезде за рубеж;\n    • Английский язык (внутреннее офлайн обучение и корпоративные скидки в SkyEng);\n    • Корпоративные скидки на обучение детей школьным предметам в онлайн-школе SkySmart.\n\nНадеемся, твоя адаптация проходила отлично!\nЗаходи в гости в наш HR кабинет :meow_party:'
        text6_nn = 'Привет, <@' + slack_id + '>!\nПоздравляем тебя с успешным официальным прохождением испытательного срока! (тут звучат радостные визги твоего рекрутера и звон бокалов твоей HR команды)\n\nТеперь тебе доступны новые дары богов:\n    • Корпоративные скидки на изучение английского языка в SkyEng;\n    • Корпоративные скидки на обучение детей школьным предметам в онлайн-школе SkySmart.\n\nНадеемся, твоя адаптация проходила отлично!\nЖелаем успехов :meow_party:'

        message = ''

        if start_date == date1:
            message = text1
        elif start_date == date2:
            message = text2
        elif start_date == date3:
            message = text3
        elif start_date == date4:
            message = text4
        elif start_date == date5:
            message = text5
        elif start_date == date6 and position == 'Специалист-оператор базы данных':
            message = text6_nn
        elif start_date == date6 and position != 'Специалист-оператор базы данных':
            message = text6_msk

        if message != '':

            try:
                response_2 = client.chat_postMessage(
                    channel=slack_id,
                    text=message)

            except SlackApiError as e:
                assert e.response["ok"] is False  # The server responded with: {'ok': False, 'error': 'not_in_channel'}
                assert e.response["error"]
                # print(f"Got an error: {e.response['error']}")
                print(f"Got an error: {e.response['error']}", email)

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

        text1 = 'Привет :pig-hello-front:\nНадеемся, твой первый день прошел хорошо.\nМы понимаем, что у каждого из нас свой опыт за плечами и стараемся сделать все, чтобы наши ожидания от адаптации совпали.\nДля этого предлагаем пройти тебе <http://forms.gle/cZ3FXVKMgezPerfu6|опрос ожиданий> – он поможет нам создать для тебя максимально комфортные условия для быстрого ввода.\nСкорее проходи!'
        text2 = 'Привет :pig-hello-door:\nЮхуу, ты с нами уже 14 дней!\nНам важно понимать, как проходит твоя адаптация, поэтому предлагаем пройти <http://forms.gle/1rsFeLJvhewwyiZj6|мини опрос>. Он не займет больше 5 минут твоего времени.\nВперед!'
        text3 = 'Привет!\nСуперклассные новости – ты с нами уже целый месяц!\n\nСейчас самое время провести встречу 1:1 со своим руководителем для дополнительной прозрачности в ожиданиях обеих сторон. На всякий случай отправляем ссылку <http://docs.google.com/document/d/1JSPInrCcAb4mFb4eEzyhk51P3OQ9M5ZKXqLiQG3uyo4|подсказки, как провести разговор 1:1 с максимальной пользой>.\n\nТакже, нам важно услышать твое мнение о компании, работе в целом, адаптации, команде и понять, что мы делаем хорошо, а что с твоей точки зрения можно еще улучшить. Предлагаем прогуляться и поговорить! Возможно, у тебя будут вопросы, которые ты захочешь обсудить лично.\n\nЕсли тебе нужна помощь в назначении встреч – смело обращайся к любому сотруднику отдела HR&Admin.\n\nОтличного тебе настроения и до встречи!'
        text4 = 'Привет!\nТвой испытательный срок близится к завершению. Надеемся, что ты успешно пройдешь его :meow_highfive:\nНа данном этапе мы бы хотели узнать, как тебе работается в команде, к которой ты присоединился.\nБудем очень благодарны за <http://forms.gle/hLr87BbJM5YoouaY6|обратную связь>!'
        text5 = 'Привет!\nСовсем скоро закончится твой испытательный срок :clapping2:\n\nНам очень важно, чтобы твои ожидания от нашей компании оправдались. Прохождение <http://forms.gle/G6WRZfpJdq8aShau7|опроса> поможет нам поддержать процесс адаптации на высоком уровне и устранить возможные сложности, которые могли возникнуть в первые месяцы работы. Давай поможем будущим новичкам вместе :blush:\nБлагодарим и желаем успешного завершения испытательного срока!\n\nP.S. Если в анкете нет вопросов, которые ты хотел бы обсудить, но не хочешь об этом говорить с руководителем – ты всегда можешь рассчитывать на помощь HR – просто обратись с просьбой о личной беседе.'
        text6 = 'Привет, <@' + slack_id + '>!\nПоздравляем тебя с успешным официальным прохождением испытательного срока! (тут звучат радостные визги твоего рекрутера и звон бокалов твоей HR команды)\n\nТеперь тебе доступны новые дары богов:\n    • Корпоративные скидки на изучение английского языка в SkyEng;\n    • Корпоративные скидки на обучение детей школьным предметам в онлайн-школе SkySmart.\n\nНадеемся, твоя адаптация проходила отлично!\nЖелаем успехов :meow_party:'

        message = ''

        if start_date == date1:
            message = text1
        elif start_date == date2:
            message = text2
        elif start_date == date3:
            message = text3
        elif start_date == date4:
            message = text4
        elif start_date == date5:
            message = text5
        elif start_date == date6:
            message = text6

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