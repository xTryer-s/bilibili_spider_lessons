import requests # requests库用于向目标网站发送请求
from bs4 import BeautifulSoup # 用于解析HTML界面
from tqdm import tqdm
film_cnt = 0
 
with open("lesson1/films_top250.txt","w",encoding='utf-8') as films_w:
    for i in tqdm(range(0,250,25),desc='Catch top250...'):
 
        target_url = f"https://movie.douban.com/top250?start={i}"
 
        headers_ = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
 
        response_header = requests.get(target_url,headers=headers_)
 
        html_text = response_header.text
 
        html_soup = BeautifulSoup(html_text,"html.parser") # 把获取的网页源代码文本数据按html去解析
 
        films_ol = html_soup.find("ol",attrs={"class":"grid_view"})
 
        film_li_list = films_ol.findAll("li")
 
        for film_li in film_li_list:
            # print(film_li)
            film_title = film_li.find("span",attrs={"class":"title"})
 
            # print(film_title.text)
 
            film_cnt += 1
 
            films_w.write(f"{film_cnt}.{film_title.text}\n")
 
 