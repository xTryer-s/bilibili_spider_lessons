import requests # 发送网络请求
from bs4 import BeautifulSoup # 分析网页 爬取信息
import re # 正则表达式 文本定位 文本处理
from tqdm import tqdm # 进度条


book_url = input('请输入目标小说url:\n')

# 为了保证url以 / 结尾
if book_url[-1] !='/':
    book_url+='/'

headers_ = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

book_main_response = requests.get(url=book_url,headers=headers_)

book_html_text = book_main_response.text

book_html_soup = BeautifulSoup(book_html_text,'html.parser')

book_info_find = book_html_soup.find('div',attrs={'class':'info'})

# print(book_info_find)

book_title = book_info_find.find('h1').text
book_author = book_info_find.find('div',attrs={'class':'small'}).find('span').text
book_latest_href = book_info_find.find('div',attrs={'class':'small'}).find('a').get('href')

book_latest_num = int(re.findall(r'/book/\d+/(\d+).html',str(book_latest_href))[0])

print(book_title)
print(book_author)
print(f'共需爬取{book_latest_num}章')

with open(f'{book_title},{book_author}.txt','w',encoding='utf-8') as book_output:
    for i in tqdm(range(1,book_latest_num+1,1),desc=f'正在爬取:{book_title},{book_author}'):
        chapter_url = book_url+f'{i}.html'
        # print(chapter_url)
        chapter_response = requests.get(url=chapter_url,headers=headers_)
        chapter_html_text = chapter_response.text

        chapter_html_soup = BeautifulSoup(chapter_html_text,'html.parser')


        chapter_title = chapter_html_soup.find('h1',attrs={'class':'wap_none'}).text

        chapter_content_find = chapter_html_soup.find('div',attrs={'id':'chaptercontent'})
        chapter_content_str = str(chapter_content_find)

        
        re_chapter_content = str(re.findall(r'id="chaptercontent">(.*)<br/><br/>.*<br/><br/>',chapter_content_str)[0])

        clean_chapter_content = re_chapter_content.replace('<br/><br/>','\n')
        # with open('chapter_get_1.txt','w',encoding='utf-8') as chapter_out:

        #     chapter_out.write(clean_chapter_content)

        # print(clean_chapter_content)
        book_output.write(chapter_title+'\n')
        book_output.write(clean_chapter_content+'\n\n')




