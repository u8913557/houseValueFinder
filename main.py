import requests
import random
from bs4 import BeautifulSoup
import urllib
from time import sleep
import datetime

user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+(KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer/v0.94, Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.02785.143 Safari/537.36']

Connections = ['Keep-Alive']
Accepts = ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8']
Accept_Languages = ['zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,ja;q=0.2']
Accept_Encodings = ['gzip, deflate, sdch']

random.seed(datetime.datetime.now())
#index = random.randrange(0, len(user_agents))
index = random.randint(0, len(user_agents)-1)
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

#永慶
communitys_yungching = {'四季紅':'10522', 'MOC移動光城':'11461', '悅桂冠':'9926', '經貿BOSS':'10701',
             '東方晶采':'26262', '風華':'10675', '風範':'11165', '翔譽之心':'26474',
              '大同明日世界':'10816', '長虹菁英':'26630', '康寧城堡':'6825', '民權湖觀':'6892',
              '夆典百富':'10941', '湖水裔':'11370', '清歡':'12460'}

communitys_test = {'MOC移動光城':'11461'}

houseAgents = {'sinyi':communitys_sinyi, 'yungching':communitys_yungching}
#houseAgents_test = {'yungching':communitys_test}


#http://tradeinfo.sinyi.com.tw/community/communityDetail.html?c=0006926&p=1&s2=10311_10510&s4=1&s5=2
#https://community.yungching.com.tw/Building/26630

#==============================================
def getwebcontent(url, header):
    try:
        res = requests.get(url, headers=header, timeout=1000)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    return res

def parsewebcontent(content, xml_format):
    try:
        soup = BeautifulSoup(content, xml_format)
    except AttributeError as e:
        print("BeautifulSoup error:" + e)
        return None
    return soup

#==============================================
def housePrice_sinyi(communitys):
    for name, community in communitys.items():
        #query_data = {'c': community, 'p': '1', 's2': duration, 's4': '1', 's5': '2'}
        query_data = {'c': community, 'p': '1', 's4': '1', 's5': '2'}
        url_data = urllib.parse.urlencode(query_data)
        #print("url_data:" + url_data)
        url = 'http://tradeinfo.sinyi.com.tw/community/communityDetail.html?' + url_data
        print("抓取信義 ====%s==== 實價登錄" % name)
        response = getwebcontent(url, headers)
        if response is None:
            print("get 信義 Web Site Error")
            continue
        else:
            response.encoding = 'utf-8'

            soup = parsewebcontent(response.text, "lxml")
            if soup is None:
                print("Parse 信義 Web Site Error")
                continue
            else:
                #print(soup.select('#tradetable_img'))
                if len(soup.select('#tradetable_img')) is 0:
                    print("信義: %s is empty" % name)
                    sleep(1)
                    continue
                else:
                    #print(soup.select('#tradetable_img')[0].get('src'))
                    img_src = soup.select('#tradetable_img')[0].get('src')
                    tradetable_src = 'http://tradeinfo.sinyi.com.tw' + img_src
                    #print(tradetable_src)
                    sleep(1)                    
                    urlretrieve(tradetable_src, name + '.png')        
    
#===============================
def housePrice_yungching(communitys):
    for name, community in communitys.items():
        url = 'https://community.yungching.com.tw/Building/' + community
        print("抓取永慶 ====%s==== 實價登錄" % name)
        response = getwebcontent(url, headers)
        if response is None:
            print("get 永慶 Web Site Error")
            continue
        else:
            response.encoding = 'utf-8'

            soup = parsewebcontent(response.text, "lxml")
            if soup is None:
                print("Parse 永慶 Web Site Error")
                continue
            else:
                table = soup.find("table", attrs={"class": "tbl-price-trend"})
                trs = table.findAll("tr")
                ths = trs[0].findAll("th")
                count = 0
                filename = name + '.txt'
                file = open(filename, mode='w')

                for tr in trs:
                    file.write("#%d:\n" % count)
                    #print("#%d:" % count)
                    for th, td in zip(ths, tr.findAll("td")):
                        file.write(th.text.strip() + ':' + td.text.strip() + '\n')
                        #print(th.text.strip() + ":" + td.text.strip())
                    count += 1
                    file.write('\n')
                file.close()
    sleep(1)
#=========================

for agent, communitys in houseAgents.items():
#for agent, communitys in houseAgents_test.items():
    if agent == 'sinyi':
        housePrice_sinyi(communitys)
        #print("")
    elif agent == 'yungching':
        housePrice_yungching(communitys)
        #print("")
    else:
        print('No such House Agent')
print("Finished !!")