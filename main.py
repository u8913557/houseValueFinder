import requests
import random
from bs4 import BeautifulSoup
import urllib
from PIL import Image
from io import BytesIO
from time import sleep

user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+(KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer/v0.94, Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.02785.143 Safari/537.36']

Connections = ['Keep-Alive']
Accepts = ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']
Accept_Languages = ['zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2']
Accept_Encodings = ['gzip, deflate, sdch']

index = random.randrange(0, len(user_agents))
user_agent = user_agents[index]
Connection = Connections[0]
Accept = Accepts[0]
Accept_Language = Accept_Languages[0]
Accept_Encoding = Accept_Encodings[0]
headers = {'user-agent':user_agent, 'Connection':Connection, 'Accept':Accept,
           'Accept_Language':Accept_Language, 'Accept-Encoding':Accept_Encoding}

#信義房屋
communitys_sinyi = {'四季紅':'0009238', 'MOC移動光城':'0011553', '悅桂冠':'0006926', '經貿BOSS':'0011152',
             '東方晶采':'0013605', '風華':'0007150', '風範':'Y001253', '翔譽之心':'0015380',
              '大同明日世界':'G0000194', '長虹菁英':'0019322', '康寧城堡':'0006300', '民權湖觀':'0001143',
              '夆典百富':'0016097', '湖水裔':'0009710', '清歡':'Y000987', '捷韻LAVIE':'0019289'}
startDate_s2 = ['103', '11']
stopDate_s2 = ['105', '10']
duration = startDate_s2[0] + startDate_s2[1] + '_' + stopDate_s2[0] + stopDate_s2[1]

communitys_yungching = {'四季紅':'10522', 'MOC移動光城':'11461', '悅桂冠':'9926', '經貿BOSS':'10701',
             '東方晶采':'26262', '風華':'10675', '風範':'11165', '翔譽之心':'26474',
              '大同明日世界':'10816', '長虹菁英':'26630', '康寧城堡':'6825', '民權湖觀':'6892',
              '夆典百富':'10941', '湖水裔':'11370', '清歡':'12460'}

houseAgents = {'sinyi':communitys_sinyi, 'yungching':communitys_yungching}

#http://tradeinfo.sinyi.com.tw/community/communityDetail.html?c=0006926&p=1&s2=10311_10510&s4=1&s5=2
#https://community.yungching.com.tw/Building/27444

def housePrice_sinyi(communitys):
    for name, community in communitys.items():
        query_data = {'c': community, 'p': '1', 's2': duration, 's4': '1', 's5': '2'}
        url_data = urllib.parse.urlencode(query_data)
        url = 'http://tradeinfo.sinyi.com.tw/community/communityDetail.html?' + url_data
        response = requests.get(url, headers=headers, timeout=1000)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        sleep(1)
        tradetable_src = 'http://tradeinfo.sinyi.com.tw' + soup.select('#tradetable_img')[0].get('src')
        #print(tradetable_src)
        print("抓取信義 ====%s==== 實價登錄" % name)
        response = requests.get(tradetable_src, headers=headers, timeout=1000)
        img = Image.open(BytesIO(response.content))
        img.save(name + '_' + duration + '.png', 'PNG')
        # img.show()
        sleep(1)

def housePrice_yungching(communitys):
    for name, community in communitys.items():
        url = 'https://community.yungching.com.tw/Building/' + community
        response = requests.get(url, headers=headers, timeout=1000)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")
        print("抓取永慶 ====%s==== 實價登錄" % name)
        table = soup.find("table", attrs={"class": "tbl-price-trend"})
        tds = table.findAll("td")
        ths = table.findAll("th")
        count = 1
        filename = name + '.txt'
        file = open(filename, mode='w')
        for x in tds:
            file.write("#%d:\n" % count)
            #print("#%d:" % count)
            for td, th in zip(tds, ths):
                file.write(th.text.strip() + ':' + td.text.strip() + '\n')
                #print(th.text.strip() + ":" + td.text.strip())
            count += 1
            file.write('\n')
        file.close()
        sleep(1)

try:
    for agent, communitys in houseAgents.items():
        if agent == 'sinyi':
            housePrice_sinyi(communitys)
        elif agent == 'yungching':
            housePrice_yungching(communitys)
        else:
            print('No such House Agent')
except:
    print('get web error')