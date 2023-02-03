def create_dict(list1,list2):
    result = dict()
    return result

if __name__ == "__main__":
    import os
    import tushare as ts
    import json

    pool = ['000001.SZ', '000002.SZ', '000008.SZ', '000004.SZ', '000005.SZ', ]
    features = []  # the list to store the features of the stocks
    for stock_id in pool:
        pass  # get the start date in the and 

    stock_config = create_dict(pool,features)
    # save the dict as config file..


    with open("stock_config.json", "w") as outfile:
        json.dump(stock_config, outfile, indent=4)
        pass
