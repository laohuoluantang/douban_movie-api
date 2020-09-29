import pymysql
import requests, json
from bs4 import BeautifulSoup
import time, random,re
conn = pymysql.connect(
    host = '172.17.0.3',
    port=3306,
    user='root',
    password='root',
    db = 'doubantop250',
    charset = 'utf8'
)
cursor = conn.cursor()


my_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'}
douban_movie_top250_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=5&page_start=100'

r = requests.get(douban_movie_top250_url, headers = my_headers)
r.encoding = 'utf-8'
top250_json = json.loads(r.text)
top250_list = top250_json['subjects']

top250_movie_url_list = []
top250_movie_image_url_list = []
top250_movie_title_list = []
top250_movie_rate_list =[]
top250_movie_report_list=[]
top250_movie_looked_list=[]
top250_movie_wantlook_list=[]

for i in top250_list:
    top250_movie_url_list.append(i['url'])
    top250_movie_image_url_list.append(i['cover'])
    top250_movie_rate_list.append(i['rate'])
    top250_movie_title_list.append(i['title'])


for i in top250_movie_url_list:
    r = requests.get(i, headers = my_headers)
    time.sleep(random.randint(1, 10))
    soup = BeautifulSoup(r.text, 'lxml')
    top250_movie_report_list.append(soup.find(id='link-report').span.get_text("|", strip=True).replace('"', ''))
    print(soup.find(id='link-report').span.get_text("|", strip=True))
    temp = soup.find('div', class_='subject-others-interests-ft').find_all('a')
    top250_movie_looked_list.append(re.sub('\D', '', temp[0].get_text("|", strip=True)))
    top250_movie_wantlook_list.append(re.sub('\D', '', temp[1].get_text("|", strip=True)))     
    for j in temp:
        print(re.sub('\D', '', j.get_text("|", strip=True)))

sql_base = 'insert into movie_messages (title, imageurl, rate, report, looked, wantlook) values '

for i in range(0, len(top250_list)):
    sql = '(' + '"' + str(top250_movie_title_list[i])+'"' + ', ' + '"' +  str(top250_movie_image_url_list[i])+ '"'  + ', ' + '"' + str(top250_movie_rate_list[i]) + '"' + ', ' + '"'  + str(top250_movie_report_list[i]) + '"' + ', ' + '"' + str(top250_movie_looked_list[i])+ '"'  + ', ' + '"'  + str(top250_movie_wantlook_list[i])+ '"'  + ')'
    sql_temp = sql_base + sql
    print(sql_temp)
    cursor.execute(sql_temp)
    conn.commit()

cursor.close()
conn.close()




