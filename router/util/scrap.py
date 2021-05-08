import datetime

import requests
from bs4 import BeautifulSoup


url = 'https://dhlottery.co.kr/gameResult.do?method=byWin'

def is_lotto_number(n):
    try:
        n = int(n)
    except:
        raise Exception('Value Error')
        
    is_integer = type(n) == type(0)
    is_bigger_then_0 = n > 0
    is_smaller_then_46 = n < 46
    if not (is_integer and is_bigger_then_0 and is_smaller_then_46):
        raise Exception('Number error')

def get_html_through_bs():
    response = requests.get(url).text
    bs = BeautifulSoup(response, 'html.parser')
    return bs

def get_round():
    bs = get_html_through_bs()
    return int(bs.select_one('h4 strong').text[:-1])

def get_new_data():
    bs = get_html_through_bs()
    win_result = bs.select_one('div.win_result')
    table_data = bs.select_one('table.tbl_data')

    try:
        num_data = win_result.select('.num')

        n = map(lambda x:x.text ,num_data[0].select('span'))
        num1, num2, num3, num4, num5, num6 = n
        bonus = num_data[1].select_one('span').text
    except Exception as exc:
        print(exc)
        return -1

    try:
        for num in n:
            is_lotto_number(num)
        is_lotto_number(bonus)
    except Exception as exc:
        print(exc)
        return -2

    round = int(win_result.select_one('h4 strong').text[:-1])
    
    date_string = win_result.select_one('p.desc').text.strip('(').strip(')').strip('추첨').strip().split()
    date_elements = map(lambda x:int(x[:-1]), date_string)
    date = datetime.date(*date_elements)
    
    first, second, third, fourth, fifth = map(lambda x: x.select('td') ,table_data.select('tbody tr'))
    
    first_count = int(''.join(first[2].text.split(',')))
    first_price = int(''.join(first[3].text.strip('원').split(',')))
    
    second_count = int(''.join(second[2].text.split(',')))
    second_price = int(''.join(second[3].text.strip('원').split(',')))
    
    third_count = int(''.join(third[2].text.split(',')))
    third_price = int(''.join(third[3].text.strip('원').split(',')))

    fourth_count = int(''.join(fourth[2].text.split(',')))
    fourth_price = int(''.join(fourth[3].text.strip('원').split(',')))
    
    fifth_count = int(''.join(fifth[2].text.split(',')))
    fifth_price = int(''.join(fifth[3].text.strip('원').split(',')))

    result_data = {
        'round': round,
        'date': date,
        'first_count': first_count,
        'first_price': first_price,
        'second_count': second_count,
        'second_price': second_price,
        'third_count': third_count,
        'third_price': third_price,
        'fourth_count': fourth_count,
        'fourth_price': fourth_price,
        'fifth_count': fifth_count,
        'fifth_price': fifth_price,
        'num1': num1,
        'num2': num2,
        'num3': num3,
        'num4': num4,
        'num5': num5,
        'num6': num6,
        'bonus': bonus
    }

    return result_data
