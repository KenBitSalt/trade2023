
def update_daily():
    # read the 'can_update' parameter in the config json file
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())

    with open('stock_config.json', 'r') as j:
        stocklist_df = json.loads(j.read())

    ud = config_df['can_update']
    runner =config_df["envpath"]
    if ud:
        for stock_id in ['000001.SZ', '000002.SZ', '000008.SZ', '000004.SZ', '000005.SZ', ]:
            subprocess.call(('%s tushare_get_stock_updates_today.py -s %s' % (runner, stock_id)), shell=True)
    


def check_can_update():
    pass

def change_can_update():
    pass

if __name__ == "__main__":
    import os
    import time
    import subprocess
    import json
    import tushare as ts
    import pandas as pd
    import json
    import datetime
    from datetime import datetime
    import argparse

    # 初始化pro接口
    token = 'edde8271b419fde9edbb0cfba7e223476af8286db034fc4f7ae10556'
    ts.set_token(token)
    pro = ts.pro_api(token)

    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())

    env_path = config_df['envpath']
    can_update = False

    update_daily()

    
                
