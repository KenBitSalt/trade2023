
def read_config_param(path, param):
    pass

def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        #timer = '{:02d}:{:02d}'.format(mins, secs)
        #print(timer, end="\r")
        time.sleep(1)
        t -= 1
    
    update_daily()

def update_daily():

    # read the 'can_update' parameter in the config json file
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    ud = config_df['can_update']

    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    if '17:48:58'<= time < '17:49:00':
        ud = True  # change config.json:can_update to true
        print("Perparing for daily update, Setting can_update to: True")
    if '17:49:00'<= time <= '17:50:00':
        for stock_id in ['000001.SZ', '000002.SZ', '000008.SZ', '000004.SZ', '000005.SZ', ]:
            subprocess.call(('D:/miniconda3/envs/dsenv/python.exe d:/trade/tushare_get_stock_updates_today.py -s %s' % stock_id), shell=True)
        print('Finish updating daily data, Setting can_update to: False')
        ud = False


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

    update_data = True

    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())

    env_path = config_df['envpath']
    can_update = False

    while True:
        countdown(1)

    
                

