import requests
import json
import os
import re
from pprint import pprint
from urllib.parse import unquote
import time

headers_ ={
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
'Referer':'https://steamcommunity.com/market/search?appid=730',
'Host':'steamcommunity.com',
'connection':'keep-alive',
'Cookie':''
}

def get_items_json(page_num):

        
    start_num = (page_num-1)*10
    tar_url = f'http://steamcommunity.com/market/search/render/?query=&start={start_num}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730'
    
    tar_json_response = requests.get(url=tar_url,headers=headers_)
    tar_json_text = tar_json_response.text.replace('\\','')
    # print(tar_json_text)

    # with open(f'tmp_page{page_num}.txt','w',encoding='utf-8') as tmp_output:
    #     tmp_output.write(tar_json_text)

    # tar_items_json = json.loads(tar_json_text)
    # pprint(tar_items_json)

    tar_items_hrefs = re.findall(r'href="(.*?)"',tar_json_text)
    for item_href in tar_items_hrefs:
        time.sleep(0.5)
        # print(item_href)
        item_name_href = re.findall(r'730/(.*)',item_href)[0]
        item_name = unquote(item_name_href)
        print(item_name)


        time.sleep(0.5)
        item_response = requests.get(url=item_href,headers=headers_)

        # item界面也是通过js刷新得到的 不能这么做
        # true_href:https://steamcommunity.com/market/itemordershistogram?language=schinese&currency=23&item_nameid=176288467
        # currency=23表示人民币 item_nameid 对应 具体item

        item_html_text =  item_response.text.replace(' ','')
        # with open('item_text.txt','w',encoding='utf-8') as item_output:
        #     item_output.write(item_html_text)

        item_nameid = re.findall(r'Market_LoadOrderSpread\((\d+)\)',item_html_text)[0]
        # print(item_nameid)
        


        item_shop_data_url = f'http://steamcommunity.com/market/itemordershistogram?language=schinese&currency=23&item_nameid={item_nameid}'

        item_shop_data_response = requests.get(url=item_shop_data_url,headers=headers_)

        item_shop_data_text = item_shop_data_response.text

        item_shop_data_json = json.loads(item_shop_data_text)

        # pprint(item_shop_data_json)

        item_buy_order = item_shop_data_json['buy_order_summary']
        item_sell_order = item_shop_data_json['sell_order_summary']

        # print(item_buy_order)
        # print(item_sell_order)

        result_item_buy_order = re.sub(r'(<.*?>)',r'',item_buy_order)
        result_item_sell_order  = re.sub(r'(<.*?>)',r'',item_sell_order)

        print(result_item_buy_order)
        print(result_item_sell_order)
        print('')
        # break

def main():
    for i in range(1,11,1):
        get_items_json(i)

if __name__=='__main__':
    main()