import requests
from bs4 import BeautifulSoup
import pandas as pd

teams = ['281', '31', '631', '148', '11', '985','543', '29', '1003', '379', '1010', '873', '762', '989', '1132',
         '180', '1237', '603', '931', '1110']
headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


def get_num(str1):
    i = list(str1)
    total = ''
    len1 = len(i)
    b = 0
    while b < len1:
        if '0' <= i[b] <= '9':
            total = total + i[b]
        b = b + 1
    if "Th." in str1:
        total = total[:-1]
    return total


for tms in teams:
    page = 'https://www.transfermarkt.com/manchester-city/startseite/verein/'+ tms + '/saison_id/2018'
    pt = requests.get(page, headers=headers)
    soup = BeautifulSoup(pt.content, 'html.parser')
    team = soup.find("h1", itemprop='name')
    table = soup.find_all("td", itemprop="athlete")

    names = [tb.get_text() for tb in table]

    marketvalue = soup.find_all(class_="rechts hauptlink")

    value = [mv.get_text() for mv in marketvalue]

    lenv = len(value) - 1
    while lenv >= 0:
        value[lenv] = get_num(value[lenv])
        lenv = lenv - 1


    squad = pd.DataFrame({"names": names, "value": value})
    pa = team.get_text() + "1.xlsx"

    with pd.ExcelWriter(pa) as writer:
        squad.to_excel(writer)
