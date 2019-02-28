#! /usr/bin/python3
from urllib.request import urlopen
#from urllib2 import urlopen
from bs4 import BeautifulSoup as bs
import re

from enum import Enum

class PitchersData(Enum):
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

class BattersData(Enum):
    YEARS = 1
    TEAM = 2
    GAME = 3
    DASEKI = 4
    DASUU = 5
    POINT = 6
    HIT = 7
    TWO = 8
    TRIPLE = 9
    HORMRUN = 10
    RUIDA = 11
    DATEN = 12
    STEAL = 13
    MISSSTEAL = 14
    BUNT = 15
    FLY = 16
    FOURBALL = 17
    DEADBALL = 18
    SANSHIN = 19
    DOUBLE = 20
    DARITSU = 21
    SYUTHURUIRITSU = 22
    CHOUDARITSU = 23
    OPS = 24


HIROSHIMA = "hiroshima"
HANSHIN = "hanshin"
YOKOHAMA = "yokohama"
KYOJIN = "kyojin"
CHUNICH = "chunichi"
YAKURUTO = "yakuruto"
SOFTBANK = "softbank"
SEIBU = "seibu"
RAKUTEN = "rakuten"
ORIX = "orix"
NIPPONHAM = "nipponham"
LOTTE = "lotte"

TEAMS = (
    HIROSHIMA,
    HANSHIN,
    YOKOHAMA,
    KYOJIN,
    CHUNICH,
    YAKURUTO,
    SOFTBANK,
    SEIBU,
    RAKUTEN,
    ORIX,
    NIPPONHAM,
    LOTTE
)

TEAMMAP = {
    HIROSHIMA: "c",
    HANSHIN: "t",
    YOKOHAMA: "yb",
    KYOJIN : "g",
    CHUNICH : "d",
    YAKURUTO : "s",
    SOFTBANK : "h",
    SEIBU : "l",
    RAKUTEN : "ip",
    ORIX : "bs",
    NIPPONHAM : "f",
    LOTTE : "m",
}

class ABC(object):
    name = str()
    href = str()

    def __init__(self, name, href):
        self.name = name
        self.href = href

URL = "http://www.pythonscraping.com/pages/page1.html"
URL = "https://baseball-data.com/stats/pitcher-yb/"
URL = "https://baseball-data.com/stats/pitcher-{team}/"
BASEURL = "https://baseball-data.com/stats" # not "base"ball url
BATTERSURL = "https://baseball-data.com/stats/hitter-{team}/"
PICHERSURL = "https://baseball-data.com/stats/pitcher-{team}/"
PLAYERSURL = "https://baseball-data.com/player/{team}/"
TEAM = HANSHIN

# get player data links.
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

def main(pitcher_or_batter="batter", team="hanshin"):
    url = BATTERSURL if (pitcher_or_batter.lower() == "batter") \
                     else PICHERSURL

    html = urlopen(url.format(team=TEAMMAP[team]))
    #print(html.read())
    bsObj = bs(html.read(), "html.parser")
    #print(bsObj)
    setter = getRefURL(bsObj)

    vs = dict()
    for c in setter:
        #print(c)
        getParams(c, vs)
        return

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
    pattern = re.compile("19[0-9]{2}|20[0-1][0-9]")

    url = abc.href # user data link.
    name = abc.name # user display name.
    bsObj = bs(urlopen(url).read(), "html.parser")
    nameList = bsObj.findAll("td") # パラメータ格納部分のタグ
    #nameList = bsObj.findAll("a")
    #print(nameList)
    data = dict()
    params = list()
    Find = False
    for link in nameList:
        '''
        print(link.text)
        if pattern.match(link.text):
            print("find")
        '''
        elem = link.text
        if not len(params) and pattern.match(elem):
            key = elem
            Find = True
            continue
        elif elem == "通算":
            key = elem
            Find = True
            del params[:]
            continue
        if Find:
            print(elem)
            params.append(elem)
            if len(params) >= 23:
                data.update({key:params})
                del params[:]
                Find = False
    data.update({"通算": params})
    if len(params):
        #ret.update({name:int(params[1])})
        ret.update({name:int(data["通算"][4])})
        """
        print(name, params[1])

        """
    '''
    '''

if __name__ == "__main__":
    main()
    #sub()
