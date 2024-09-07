import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

headers_ = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

target_book_url = input('请输入目标小说url')

book_response = requests.get(url=target_book_url,headers=headers_)

book_html_text = book_response.text

book_html_soup = BeautifulSoup(book_html_text,'html.parser')

# print(book_html_soup)

book_info = book_html_soup.find('div',attrs={'class':'info'})

book_name = book_info.find('h1').text
book_author = book_info.find('div',attrs={'class':'small'}).find('span').text
book_latest_href = book_info.find('div',attrs={'class':'small'}).find('a').get('href')

latest_chapter = re.findall(r'/book/\d+/(\d+).html',book_latest_href)[0]
print(book_name)
print(book_author)
# print(book_latest_href)
# print(latest_chapter)

base_url = target_book_url

with open(f'{book_name},{book_author}.txt','w',encoding='utf-8') as book_output:
    for i in tqdm(range(1,int(latest_chapter)+1,1)):
        tar_chapter_url = base_url+f'{i}.html'
        chapter_response = requests.get(url=tar_chapter_url,headers=headers_)
        # print(chapter_response.text)
        chapter_soup = BeautifulSoup(chapter_response.text,'html.parser')
        
        chapter_name = chapter_soup.find('h1',attrs={'class':'wap_none'})
        # print(chapter_name.text)

        chapter_content = chapter_soup.findAll('div',attrs={'id':'chaptercontent'})[0]

        chapter_content_str = str(chapter_content)

        if '本章由于字数太少，暂不显示。' in chapter_content_str:
            continue

        content_re = re.findall(r'id="chaptercontent">(.*)<br\/><br\/>.*<br\/><br\/>',chapter_content_str)[0]

        clean_content = str(content_re).replace('<br/><br/>','\n')

        # print(clean_content)

        book_output.write(str(chapter_name.text)+'\n')
        book_output.write(clean_content+'\n'+'\n')
        


