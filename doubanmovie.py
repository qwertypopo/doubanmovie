# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import json

class get_movie(object):
    # 初始化
    def __init__(self):
        self.begin_url = 'https://movie.douban.com/chart'
        self.post_urls = []
        self.headers = {'user-agent': 'Mozilla/5.0'}

    # 获取各个分类排行榜的url
    def get_url(self):

        web = requests.get(self.begin_url, headers=self.headers)
        soup = BeautifulSoup(web.text, "html.parser", from_encoding='utf-8')
        links = soup.find('div', class_="types").findAll("a")
        for link in links:
            self.post_urls.append("https://movie.douban.com/" + link['href'])

    # 获取排行榜数据
    def get_data(self, url):
        typeurl = requests.get(url, headers=self.headers)
        typenum = url.split('&')[1].split('=')[1]
        soup = BeautifulSoup(typeurl.text, "html.parser", from_encoding='utf-8')
        dataurl = requests.get('https://movie.douban.com/j/chart/top_list?type='+typenum+
                               '&interval_id=100%3A90&action=&start=0&limit=20')
        movie_data = {'movie_info': dataurl.text, 'movie_type': soup.find('div', id='content').h1}
        return movie_data

    def outputer(self, movie_datas):
        fout = open('movie_list.txt', 'w')
        for movie_data in movie_datas:
            fout.write(
                '====================' + '%s' % movie_data['movie_type'].encode('utf-8').strip('<h1>').strip('</h1>')
                + '==================\n\n')
            datas = json.loads(movie_data['movie_info'])
            for data in datas:
                fout.write('%d' % data['rank']+ '\t%s' % data['title'].encode('utf-8')+ '\t豆瓣评分：'
                           + '%s' % data['score'].encode('utf-8') + '分\n''%s' % data['release_date'].encode(
                            'utf-8')+'\t'+''.join(data['regions']).encode('utf-8')+'\t'+
                           ' / '.join(data['types']).encode('utf-8')+'\n\n')
        fout.close()

    def start(self):
        self.get_url()
        movie_datas = []
        for url in self.post_urls:
            movie_datas.append(self.get_data(url))
        self.outputer(movie_datas)

mov = get_movie()
mov.start()
