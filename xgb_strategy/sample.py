
def get_1day_path():
    with open('config.json', 'r') as j:
        config_df = json.loads(j.read())
    datapath = config_df['path']+ '/' + config_df['data_storage'] +'/' + '1day'
    #print('Using Storage at: %s' % datapath)
    return datapath

def get_stockconfig():
    datapath = 'stock_config.gzip'
    df = pd.read_parquet(datapath)
    #print('Using Storage at: %s' % datapath)
    return df

# to be run in root directory
if __name__ == "__main__":
    import pandas as pd
    import sklearn as sk
    import nltk
    import json

    print(get_1day_path())
    print(get_stockconfig())