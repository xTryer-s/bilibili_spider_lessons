import requests # 发送网络请求
import json # 以json格式读取数据
import os # 本地文件操作
import re # 正则表达式
from pprint import pprint # 输出更加规整
from urllib.parse import unquote # unquote => 解码 url请求  quote => 编码url请求
import time # sleep 函数 暂停程序

# url : https://steamcommunity.com/market/search/render/?query=&start={i}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730

headers_ ={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Host':'steamcommunity.com',
    'connection':'keep-alive',
    'Cookie':'timezoneOffset=28800,0; browserid=3289398278795007560; sessionid=8866d487d0606b8b64cb6dff; steamCountry=US%7Cad7d9ca6e6802923d0c20fd9149bf759'
}
def get_items_json(page_num):
    start_num = (page_num-1)*10
    tar_url = f'https://steamcommunity.com/market/search/render/?query=&start={start_num}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730'
    tar_json_response = requests.get(url=tar_url,headers=headers_)
    tar_json_text = tar_json_response.text

    items_href_get = re.findall(r'href=\\"(.*?)\\"',tar_json_text)
    
    for item_href in items_href_get:
        item_href = str(item_href).replace('\\','')

        item_name_encode = re.findall(r'730/(.*)',item_href)[0]
        item_name_decode = unquote(item_name_encode)
        print(item_name_decode)

        # print(item_href)
        time.sleep(1)
        item_response = requests.get(url=item_href,headers=headers_)

        item_response_text = item_response.text.replace(' ','')

        # with open('item_text.txt','w',encoding='utf-8') as text_output:
        #     text_output.write(item_response_text)
        
        item_id = re.findall(r'Market_LoadOrderSpread\((\d+)\);',item_response_text)[0]

        # print(item_id)
        item_info_href = f'https://steamcommunity.com/market/itemordershistogram?country=US&language=schinese&currency=23&item_nameid={item_id}'

        time.sleep(0.5)
        item_info_response = requests.get(url=item_info_href,headers=headers_)
        item_info_json = json.loads(item_info_response.text)

        # pprint(item_info_json)
        # with open('item_info.json','w',encoding='utf-8') as text_output:
        #     text_output.write(item_info_response.text)
        item_buy_order = item_info_json['buy_order_summary']
        item_sell_order = item_info_json['sell_order_summary']


        result_item_buy_order = re.sub(r'(<.*?>)',r'',item_buy_order)
        result_item_sell_order = re.sub(r'(<.*?>)',r'',item_sell_order)

        print(result_item_buy_order)
        print(result_item_sell_order)
        print(f'item url: {item_href}\n')




def main():
    get_items_json(1)

if __name__=='__main__':
    main()