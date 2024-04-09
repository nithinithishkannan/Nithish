from bs4 import BeautifulSoup as bs
import requests
import html5lib
url="https://en.wikipedia.org/wiki/2023_Karnataka_Legislative_Assembly_election"
d1=requests.get(url)
# print(r)
bs1=bs(d1.text,'html5lib')
const_tab=bs1.findAll("table",attrs={"class":"wikitable sortable"})
# print(table)
# for tb in  const_tab:
#     print(tb)
#     print("\n")
row_no=0
const_result={}
for tr in const_tab[0].findAll("tr"):
    row_no += 1
    dist_cheak=0
    if row_no < 3:
        continue

    td = [x.text for x in tr.findAll("td")]
    if len(td) == 0:
        continue
# print(tr)

    const_no,const_name='',''
    if len(td)==12:
        const_no,const_name=td[1].strip(),td[2].strip()
    else:
        const_no, const_name = td[0].strip(), td[1].strip()
    # print(const_no,const_name)
    const_result[const_no]=const_name

    # print(const_result)

for const_no,const_name in const_result.items():
    url=f"https://results.eci.gov.in/ResultAcGenMay2023/ConstituencywiseS10{const_no}.htm?ac={const_no}"
    if int(const_no)==0:
        break

    dt=requests.get(url)
    bs_dt=(dt.text,'html5lib')

    data_table = bs_dt.findAll("table",attrs={
        "style":"margin: auto; width: 100%; font-family: Verdana; border: solid 1px black;font-weight:lighter"})
    if len(data_table)==0:
        continue
    row_content=data_table[0].findAll('tr',attrs={"style":"font-size:12px;"})
    if len(row_content)==0:
        continue

    for t in row_content[:5]:
        td = [x.text for x in t.findAll("td")]
        print(td)
    break