import requests
from bs4 import BeautifulSoup


# https://movie.douban.com/top250?start=0&filter=
film_cnt = 0
for n in range(0,250,25):
    tar_url = f'https://movie.douban.com/top250?start={n}&filter='

    headers_ = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    response = requests.get(url=tar_url,headers=headers_)

    if not response.ok:
        print('访问失败')
        exit()
    else:
        print('访问成功')

    web_text = response.text

    # print(web_text)

    web_soup = BeautifulSoup(web_text,'html.parser')

    # print(web_soup)

    grid_view = web_soup.find('ol',attrs={'class':'grid_view'})

    # print(grid_view)

    films_lis =grid_view.findAll('li')

    # print(len(films_lis))

    with open('douban.txt','a',encoding='utf-8') as douban_output:
        for film_li in films_lis:
            film_title = film_li.find('span',attrs={'class':'title'})
            film_cnt+=1
            output_text= f'{film_cnt}.{film_title.text}\n'
            # print(output_text)
            douban_output.write(output_text)