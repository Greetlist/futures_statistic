import os
import argh
from data_helper import DataHelper

def get_data(trade_date):
    dh = DataHelper(trade_date)
    dh.query_player_list()
    #dh.query_player_details()
    #dh.print_all_details()

if __name__ == '__main__':
    argh.dispatch_commands([get_data])
