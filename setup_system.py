import os
import json

configuration = dict()
configuration = {
    'path' : './trade',
    'latest_data' : '19000101',
    'envpath_win' : 'D:/miniconda3/envs/dsenv/python.exe',
    'envpath_mac' : '/opt/miniconda3/envs/dsenv/bin/python',
    'agents' : 'data_agent',
    'data_storage' : 'market_data',
    'data_agent' : ['Tushare', 'JoinQuant', 'backtrader','futu-api'],
    'data_types' : ['1min','1day'],
    'strategy_agent' : 'strategy',
    'data_update_time': '16:30:00',
    'data_path' : 'd:/trade/market_data',
    'can_update' : 'false',
    'stock_config' : 'stock_config.gzip'
}

with open("config.json", "w") as outfile:
    json.dump(configuration, outfile, indent=4)

#create main path
print('\n>>> checking integrity of main directory...')
if os.path.exists(configuration['path']) == False:
    os.makedirs(configuration['path'])
    print('making directory: %s' % (configuration['path']))
else:
    print("%s already exists..." % (configuration['path']))

#create data_agent path in module
print('\n>>> checking integrity of data agent...')
if os.path.exists(configuration['path'] + '/' +configuration['agents']) == False:
    os.makedirs(configuration['path'] + '/' +configuration['agents'])
    print('making directory: %s' % (configuration['path'] + '/' +configuration['agents']))
else:
    print("%s already exists..." % (configuration['path'] + '/' +configuration['agents']))

for items in configuration['data_agent']:
    if os.path.exists(configuration['path'] + '/' + configuration['agents'] + '/' + items) == False:
        os.makedirs(configuration['path'] + '/' + configuration['agents'] + '/' + items)
        print('making directory: %s' % (configuration['path'] + '/' + configuration['agents'] + '/' + items))
    else:
        print("%s already exists..." % (configuration['path'] + '/' + configuration['agents'] + '/' + items))

#create data_storage path in module
print('\n>>> checking integrity of data storage...')
if os.path.exists(configuration['path'] + '/' + configuration['data_storage']) == False:
    path_name = configuration['path'] + '/' + configuration['data_storage']
    os.makedirs(path_name)
    print('making directory: %s' % (path_name))
else:
    print("%s already exists..." % (configuration['path'] + '/' + configuration['data_storage']))
path_name = configuration['path'] + '/' + configuration['data_storage']
for types in configuration['data_types']:
    if os.path.exists(path_name+ '/'+types) == False:
        os.makedirs(path_name+'/'+types)
        print('making directory: %s' % (path_name+'/'+types))
    else:
        print("%s already exists..." % (path_name+ '/'+types))

#create d
