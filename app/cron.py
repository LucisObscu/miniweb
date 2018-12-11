from bs4 import BeautifulSoup
from urllib import request as req
import datetime
import pandas as pd
from app.models import Clien
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()





# -*- coding: utf-8 -*-






r = 'https://www.clien.net'
url = 'https://www.clien.net/service/board/park?&od=T31&po={0}'
count = 0
title_list_data = []
hit_list_data = []
time_list_data = []
link_list_data = []
nickname_list_data = []

def hms_cut(data):
    data_str = data
    if type(data_str) != str:
        data_str = str(data_str)
    return datetime.datetime.strptime(data_str[:10], '%Y-%m-%d')

def html_to_str(data):
    return [i.get_text() for i in data]


def urlerro(address):
    try:
        return req.urlopen(address)
    except:
        return urlerro(address)


def hit_to_int(hit_list_data):
    e = []
    for i, v in enumerate(hit_list_data):
        try:
            e.append(int(v))
        except:
            url = urlerro(link_list_data[i])
            soup = BeautifulSoup(url, 'html.parser')
            e.append(int(soup.select('span.view_count')[0].select('strong')[0].get_text().replace(',', '')))
    return e


def get_nick_name(data):
    data_list = []
    for i, v in enumerate(data):
        if v.get_text() != '\n\n':
            data_list.append(v.get_text().replace('\n', ''))
            print(v.get_text())
        else:
            data_list.append(v.find('img')['alt'].replace('\n', ''))
    return data_list


def my_cron_job():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2!!!!!!!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22")

    global count,title_list_data,hit_list_data,time_list_data,link_list_data,nickname_list_data

    sw = False
    while True:
        # print(count)
        if sw:
            break
        urld = urlerro(url.format(count))
        count += 1
        soup = BeautifulSoup(urld, 'html.parser')
        time_list = html_to_str(soup.select('span.timestamp')[1:])
        hit_list = html_to_str(soup.select('span.hit')[1:])
        title_list = html_to_str(soup.select('span.subject_fixed'))
        link_list = [r + i['href'] for i in soup.select('a.list_subject')][1:]
        nickname_list = get_nick_name(soup.select('span.nickname'))[1:]
        today = str(datetime.datetime.now())[:10]
        for i, v in enumerate(time_list):
            print(v[0:10])
            print(today)
            if v[0:10] != today:
                sw = True
                break
            else:
                time_list_data.append(time_list[i])
                hit_list_data.append(hit_list[i])
                title_list_data.append(title_list[i])
                link_list_data.append(link_list[i])
                nickname_list_data.append(nickname_list[i])
    hit_list_data = hit_to_int(hit_list_data)
    data = pd.DataFrame(
        {'title': title_list_data, 'nickname': nickname_list_data, 'hit': hit_list_data, 'time': time_list_data,
         'link': link_list_data})

    jk = int(sum(hit_list_data) / len(hit_list_data))

    data_hit = data[data['hit'] > jk].sort_values(["hit"], ascending=[False]).reset_index()
    del data_hit['index']
    data_hit.index.name='id'
    Clien.objects.all().delete()
    for v in data_hit.get_values():
        Clien.objects.create(title=v[0],nickname=v[1],hit=v[2],time=v[3],link=v[4])
    pymysql.install_as_MySQLdb()
    engine = create_engine("mysql+mysqldb://user:" + "qjtmxjtlfqj!2" + "@tiqmfk950.mysql.pythonanywhere-services.com", encoding='utf-8')
    conn = engine.connect()
    data_hit.to_sql(name='app_clien', con=engine, if_exists='replace')

if __name__ == '__main__':
    my_cron_job()