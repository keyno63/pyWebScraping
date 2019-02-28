# codinf: utf-8
#list_hist = ["スパークス高","マーリンズ","ジャイアンツ","マリナーズ"]
list_hist = ["タイガース"]

string = str()
for c in list_hist:
    if len(string):
        string += (" - ")
    string += c

print(string)
