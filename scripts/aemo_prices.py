import pandas as pd

import glob


def process_file(year, month, region):

    df = pd.read_csv("http://nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{}/MMSDM_{}_{}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_TRADINGPRICE_{}{}010000.zip".format(year, year, month, year, month,), header=1, skiprows=0, skipfooter=1, engine='python')
    df = df[['SETTLEMENTDATE', 'REGIONID', 'PERIODID', 'RRP', 'LASTCHANGED', 'RAISE6SECRRP', 'RAISE60SECRRP', 'RAISE5MINRRP',
    'LOWER6SECRRP', 'LOWER60SECRRP', 'LOWER5MINRRP', 'PRICE_STATUS']]
    df = df[(df.REGIONID==region)]
    df= df.sort_values(by=['SETTLEMENTDATE'])

    df.to_csv('{}_{}_{}.csv'.format(region , year, month), header=True)


years = ['2016', '2017', '2018', '2019', '2020']
months  = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
regions = ['SA1', 'NSW1', 'VIC1', 'QLD1']
for y in years:
    for m in months:
        for r in regions:
            process_file(y, m, r)



for state in regions:
    data_frames = []
    files = glob.glob('{}*.csv'.format(state[:-1]))
    combined_csv = pd.concat([pd.read_csv(f) for f in files ])
    combined_csv = combined_csv.sort_values(by=['SETTLEMENTDATE'])
    combined_csv = combined_csv.drop(combined_csv.columns[[0]], axis=1)
    combined_csv.to_csv('{}2016-2020.csv'.format(state))


