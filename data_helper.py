import requests
import json
import time
import pandas as pd
from collections import defaultdict

class DataHelper:
    def __init__(self, trade_date):
        self.trade_date = trade_date
        self.player_list_base_url = 'https://spdspc.qhrb.com.cn/api/spsread2024/groupBaseFront/getBaseScoreTotalListAdm'
        self.player_detail_base_url = 'https://spdspc.qhrb.com.cn/api/spsread2024/curveFront/getBreedTotalVO'
        self.total_player_list = list()
        self.total_profit_dict = defaultdict(lambda: dict())

    def query_player_list(self):
        for i in range(1, 2):
            res = requests.get(self.player_list_base_url, params={
                'internalAccount': '',
                'playerNickName': '',
                'tradeDate': self.trade_date,
                'deadlineTime': self.trade_date,
                'groupType': 1,
                'rankType': 0,
                'index': i,
                'size': 50,
                'selType': 0,
                'breedCode': ''
            })
            print(res)
            res_json = res.json()
            print(res_json)
            for item in res_json['dataPoints']['list']:
                self.total_player_list.append(item['playerId'])
        print(self.total_player_list)

    def query_player_details(self):
        for player_id in self.total_player_list:
            res = requests.get(self.player_detail_base_url, params={
                'playerId': player_id,
                'tradeDate': self.trade_date,
            })
            res_json = res.json()
            for item in res_json['dataPoints']['totalBreedVOList']:
                self.total_profit_dict[item['breedCode']]['Profit'] += item['tradeClosingProfitAmount']
                self.total_profit_dict[item['breedCode']]['Name'] = item['breedName']
            time.sleep(1)

    def print_all_details():
        data_list = []
        for code, info in self.total_profit_dict.items():
            data_list.append({'Code': code, 'Name': info['Name'], 'Profit': info['Profit']})
        df = pd.DataFrame(data_list)
        df.to_csv('test.csv', index=False)
