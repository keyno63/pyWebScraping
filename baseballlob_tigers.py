#! /usr/bin/python3
from urllib.request import urlopen
#from urllib2 import urlopen
from bs4 import BeautifulSoup as bs
import re

from enum import Enum

HIROSHIMA = "hiroshima"
HANSHIN = "hanshin"

class Pitchers(Enum):
    YEARS = 1
    TEAM = 2
    GAME = 3
    WIN = 4
    LOSE = 5
    HOLD = 6
    HP = 7
    ALL = 8
    CLOSE = 9
    NOFOAR = 10
    BATTER = 11
    INN = 12
    HIT = 13
    HORM = 14
    FOAR = 15
    DEAD = 16
    SAN = 17
    WILD = 18
    BOAK = 19
    MISS = 20
    JISEKI = 21
    BOU = 22
    WHIP = 23

TEAMMAP = {
    "hiroshima": "c",
    "hanshin": "t",
    "yokohama": "yb",

}

TEAMS = [
    "hiroshima",
    "hamshin",
    "yokohama",
    "kyojin",
    "chunichi",
    "yakuruto",
    "softbank",
    "seibu",
    "rakuten",
    "orix",
    "nipponham",
    "lotte"
]

class ABC(object):
    name = str()
    href = str()

    def __init__(self, name, href):
        self.name = name
        self.href = href

URL = "http://www.pythonscraping.com/pages/page1.html"
URL = "https://baseball-data.com/stats/pitcher-yb/"
URL = "https://baseball-data.com/stats/pitcher-t/"
URL = "https://baseball-data.com/stats/pitcher-{team}/"
TEAM = "hanshin"


def getRefURL(bsObj):
    print("======================")
    #nameList = bsObj.findAll(tag="href")
    #nameList = bsObj.findAll(lambda tag: len(tag.attrs) == 2)
    nameList = bsObj.findAll("a", href=re.compile("^(\/|.*"+"https://baseball-data.com/player/{team}/"
        .format(team=TEAMMAP[TEAM])+")"))
    #nameList = bsObj.findAll("a")
    #print(nameList)
    addLink = set()
    for link in nameList:
        #print(link)
        if link.attrs["href"] is None:
            continue
        href = link.attrs["href"]
        elem = link.text
        #print (href, elem)
        #print(link)
        if href.startswith("/"):
            player = ABC(elem, href)
            addLink.add(player)
        else:
            player = ABC(elem, href)
            addLink.add(player)
    return addLink

def main():
    html = urlopen(URL.format(team=TEAMMAP[TEAM]))
    #print(html.read())
    bsObj = bs(html.read(), "html.parser")
    #print(bsObj)
    setter = getRefURL(bsObj)

    vs = dict()
    for c in setter:
        #print(c)
        getParams(c, vs)

    """
    # 昇順
    for k, v in sorted(vs.items(), key=lambda x: x[1]):
            print(str(k) + ": " + str(v))
    """
    # 降順
    for k, v in sorted(vs.items(), key=lambda x: -x[1]):
            print(str(k) + ": " + str(v))

def sub():
    pass

def getParams(abc, ret):
    #obj = bs(urlopen("https://baseball-data.com/player/yb/%E6%9D%B1%E3%80%80%E5%85%8B%E6%A8%B9").read())
    #bsObj = bs(urlopen("https://baseball-data.com/player/yb/%E4%BB%8A%E6%B0%B8%E3%80%80%E6%98%87%E5%A4%AA").read())
    url = abc.href
    name = abc.name
    bsObj = bs(urlopen(url).read(), "html.parser")
    nameList = bsObj.findAll("td")
    #nameList = bsObj.findAll("a")
    #print(nameList)
    params = list()
    Find = False
    for link in nameList:
        #print(link)
        elem = link.text
        #print(elem)
        #print(link)
        if elem == "通算":
            Find = True
            continue
        if Find:
            params.append(elem)
    if len(params):
        ret.update({name:int(params[1])})
        """
        print(name, params[1])

        """

if __name__ == "__main__":
    main()
    #sub()
