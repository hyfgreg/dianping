import re
import requests
from requests.exceptions import ConnectionError
import pymongo

client = pymongo.MongoClient('localhost')
db = client['dianping_shanghai']

menu_url = 'http://www.dianping.com/ajax/json/category/menu?cityId={cityId}'

headers = {
    # 'Referer':'http://www.dianping.com/search/category/1/10/g101',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    # 'Cookie': '_hc.v=3b819f9c-5fa4-7a10-72c5-9babffd8293e.1499262722; __utma=1.1944725669.1499262722.1499262722.1499262722.1; __utmc=1; __utmz=1.1499262722.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _lxsdk_cuid=15d27c4e4f2c8-02b6e35790710b-38710357-1fa400-15d27c4e4f3c8; _lxsdk=15d27c4e4f2c8-02b6e35790710b-38710357-1fa400-15d27c4e4f3c8; s_ViewType=10; JSESSIONID=AA54A8F7AB1EF741A2B4C7CB6E709ADA; aburl=1; cy=2; cye=beijing; _lxsdk_s=15d27c4e4fc-8cd-8f8-d85%7C%7C5'
}

def getCategory(cityId):
    assert type(cityId) == str
    print(menu_url.format(cityId=cityId))
    try:
        response = requests.get(menu_url.format(cityId=cityId),headers=headers)
        # print(response.text)
        if response.status_code == 200:
            # print(response.status_code)
            return response.text
        else:
            # print(response.status_code)
            return response.status_code
    except Exception:
        raise Exception


def retest():
    url = 'http://www.dianping.com/search/category/1/10/g101'
    groups = re.search(r'category\/(.*?)\/(.*?)\/g(.*?)$',url).group()

    url1 = 'http://www.dianping.com/ajax/json/category/menu?cityId=1'

    print(re.search('cityId=(.*?)$',url1).group(1))

    # for group in groups:
    #     print(group)


def getData(id):
    ms = db['category'].find_one({'categoryId':id},{'_id':0})
    print(ms)
    print(ms['categoryName'])
    print(ms.get('children'))

def main():
    # getData(10)
    retest()
if __name__ == '__main__':
    main()