selection_config = {
    'max_weight' : 0.1,
    'min_build_vol' : 1000,
}

def get_current_pos():
    pass

def get_price(stock_id):
    pass

def gen_build_pos(pri,avai):
    buildable = []
    for i in tqdm(range(len(pri))):
        stock_id = pri.loc[i,'stock_id']
        now_avai = avai.loc[avai['stkId']==stock_id,:].copy().to_numpy()
        if len(now_avai)>0:
            now_avai = now_avai[0]
            price = get_price(stock_id)
            buildable.append(now_avai)
    buildable = np.array(buildable)
    df_buildable = pd.DataFrame(buildable)
    print(df_buildable)
        

if __name__ == "__main__":
    import argparse
    import pandas as pd
    import numpy as np
    from tqdm import tqdm


    parser = argparse.ArgumentParser(description='piority csv + availble csv + current pos, produce pos.csv')
    parser.add_argument('-p', '--piority', help='1d csv of stocks to build')
    parser.add_argument('-a', '--available', help='Nd csv of available stocks to build')
    parser.add_argument('-c', '--cap', help='cap to build')
    args = parser.parse_args()

    df_pri = pd.read_csv(args.piority)
    df_avai = pd.read_excel(args.available)
    df_pos = get_current_pos()
    cap = args.cap

    print(df_pri)
    print(df_avai)

    df_build = gen_build_pos(df_pri,df_avai,cap)

    

    