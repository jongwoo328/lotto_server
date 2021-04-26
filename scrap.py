import csv
import datetime

data = []
field_names = ['round','date','1st_count','1st_price','2nd_count','2nd_price','3rd_count','3rd_price','4th_count','4th_price','5th_count','5th_price','num1','num2','num3','num4','num5','num6','bonus']

with open('lotto.csv', 'r') as f, open('lotto_data.csv', 'w') as f2:
    writer = csv.DictWriter(f2, fieldnames=field_names)
    lottos = csv.DictReader(f)
    for lotto in lottos:
        lotto['date'] = datetime.date(*map(int, lotto['date'].split('.')))
        lotto['1st_count'] = int(lotto['1st_count'].replace(',', ''))
        lotto['2nd_count'] = int(lotto['2nd_count'].replace(',', ''))
        lotto['3rd_count'] = int(lotto['3rd_count'].replace(',', ''))
        lotto['4th_count'] = int(lotto['4th_count'].replace(',', ''))
        lotto['5th_count'] = int(lotto['5th_count'].replace(',', ''))
        lotto['1st_price'] = int(lotto['1st_price'].replace(',', ''))
        lotto['2nd_price'] = int(lotto['2nd_price'].replace(',', ''))
        lotto['3rd_price'] = int(lotto['3rd_price'].replace(',', ''))
        lotto['4th_price'] = int(lotto['4th_price'].replace(',', ''))
        lotto['5th_price'] = int(lotto['5th_price'].replace(',', ''))
        writer.writerow(lotto)