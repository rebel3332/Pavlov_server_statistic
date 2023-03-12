import json
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json

ddd = list()
app = Flask(__name__)
# FlaskJSON(app)

def GetDateFromLog():
    file_name = "Logs/Pavlov-backup-2023.03.07-01.59.21.log"
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

    # display(count)
    # return json.loads(text_json)

    # Формирую общий DataFrame из Json
    games = pd.json_normalize(statistic)
    # Получаю DataFrame статистики по всем игрокам по всем играм
    players = pd.DataFrame(columns=['game_data', 'uniqueId', 'playerName', 'teamId', 'stats'])
    for row in games.iterrows():
        new_player = pd.DataFrame(row[1]['allStats'])
        new_player['game_data'] = row[1]['date']
        players = pd.concat([players, new_player], axis=0)
    games.drop(['allStats'], axis=1, inplace=True)
    status_list = ['BombPlanted', 'BombDefused', 'Kill', 'Headshot', 'Death', 'Experience', 'TeamKill', 'Assist']
    for row in players.iterrows():
        # display(row[1]['stats'])
        player_stats = row[1]['stats']#.split("},")
        for stat in player_stats:
            # players.loc[row[0],'BombPlanted']
            # display(type(stat))
            for stat_name in status_list:
                if stat['statType'] == stat_name:
                    # display("YES")
                    players.loc[row[0], stat_name] = stat['amount']
    players.drop(['stats'], axis=1, inplace=True)
    # Формирую правильный Json
    new_json = []
    for game in games.iterrows():
        # display(game[1])
        # new_rec_in_json = dict()
        # new_rec_in_json['date'] = game[1]['date']
        new_rec_in_json = game[1]
        # new_rec_in_json = games.iloc[game[0]]
        new_rec_in_json['allStats'] = json.loads(players[players['game_data'] == game[1]['date']].to_json(orient='records'))
        # new_rec_in_json['allStats'] = players[players['game_data'] == game[1]['date']].to_json(orient='records')
        # new_json.append(json.loads(new_rec_in_json.to_json(orient='records')))
        new_json.append(new_rec_in_json)

    # return statistic
    return new_json

def GetDateFromDDD():
    if len(ddd) == 0:
        return ''
    games = pd.json_normalize(ddd)
    # Получаю DataFrame статистики по всем игрокам по всем играм
    players = pd.DataFrame(columns=['game_data', 'uniqueId', 'playerName', 'teamId', 'stats'])
    for row in games.iterrows():
        new_player = pd.DataFrame(row[1]['allStats'])
        new_player['game_data'] = row[1]['date']
        players = pd.concat([players, new_player], axis=0)
    games.drop(['allStats'], axis=1, inplace=True)
    status_list = ['BombPlanted', 'BombDefused', 'Kill', 'Headshot', 'Death', 'Experience', 'TeamKill', 'Assist']
    for row in players.iterrows():
        # display(row[1]['stats'])
        player_stats = row[1]['stats']#.split("},")
        for stat in player_stats:
            # players.loc[row[0],'BombPlanted']
            # display(type(stat))
            for stat_name in status_list:
                if stat['statType'] == stat_name:
                    # display("YES")
                    players.loc[row[0], stat_name] = stat['amount']
    players.drop(['stats'], axis=1, inplace=True)
    # Формирую правильный Json
    new_json = []
    for game in games.iterrows():
        # display(game[1])
        # new_rec_in_json = dict()
        # new_rec_in_json['date'] = game[1]['date']
        new_rec_in_json = game[1]
        # new_rec_in_json = games.iloc[game[0]]
        new_rec_in_json['allStats'] = json.loads(players[players['game_data'] == game[1]['date']].to_json(orient='records'))
        # new_rec_in_json['allStats'] = players[players['game_data'] == game[1]['date']].to_json(orient='records')
        # new_json.append(json.loads(new_rec_in_json.to_json(orient='records')))
        new_json.append(new_rec_in_json)

    # return statistic
    return new_json


# @app.route('/get_value')
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
# @as_json
def get_value():
    # return dict(value=12)
    # return json.loads(text_json)
    # return jsonify(json.loads(text_json))
    return render_template('index.html', data = GetDateFromLog())
    # return render_template('index.html', data = "123")


@app.route('/ddd', methods=['POST', 'GET'])
# @as_json
def get_value_ddd():
    return render_template('index.html', data = GetDateFromDDD())
    # return render_template('index.html', data = "123")


@app.route('/send_data', methods=['POST'])
def SendData():
    if request.method == 'POST':
        global ddd
        # ddd = json.loads(request.data)
        ddd = json.loads(request.data.decode('utf-8'))
    return 'OK'
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5001', debug='True')
    # app.run()