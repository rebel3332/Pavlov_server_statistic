from read_env import read_env
import os
import pandas as pd
import json
import schedule
import time
import requests
import ast

def GetDateFromLog():
    file_name = LOG_PATH + "/Pavlov-backup-2023.03.07-01.59.21.log"
    count = 0
    found_json = False
    text_json = ""
    statistic = []

    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            if not found_json:
                if "StatManagerLog" in line:
                    if "{" in line:
                        found_json = True
                        text_json = "{\"date\": \"" + line.split(":")[0].replace("[", "") + "\",\n"
                        count += 1
            elif found_json:
                if "StatManagerLog: End Stat Dump" in line:
                    # print(text_json)
                    # text_json += "}"
                    found_json = False
                    # display(text_json)
                    statistic.append(json.loads(text_json))
                else:
                    text_json = text_json + line

    return statistic


def PutDate(data):
    requests.post(PUT_URL, data=data)


def worker():
    # Получаю данные из файла
    data = GetDateFromLog()
    # Передаю на сервер
    PutDate(json.dumps(data))
    # PutDate(json.dumps('123'))
    # PutDate({'data': '123'})
    # PutDate('123123213213123213213')
    # print(json.dumps(data))
    # для восстановления обратно в JSON
    # print(json.loads(json.dumps(data)))

if __name__  == '__main__':
    read_env()
    global PUT_URL
    global LOG_PATH
    LOG_PATH = os.getenv('LOG_PATH')
    TIME_FROM_WORKER = int(os.getenv('TIME_FROM_WORKER'))
    PUT_URL = os.getenv('PUT_URL')
    print('Read pavlov logs from path %s' % os.getenv('LOG_PATH'))
    print('worker runs every {0} minutes'.format(os.getenv('TIME_FROM_WORKER')))
    schedule.every(TIME_FROM_WORKER).minutes.do(worker)
    while True:
        schedule.run_pending()
        time.sleep(10)
    # worker()