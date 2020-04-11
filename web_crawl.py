import re
import requests
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup as bs


class ConnectionBoursier:

    def __init__(self):

        self.url_main = "https://www.boursier.com/indices/composition/cac-40-FR0003500008,FR.html"
        send_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}
        self.sess = requests.Session()
        self.sess.headers.update(send_headers)

    def download(self):
        try:
            main_page = self.sess.get(self.url_main)
        except requests.exceptions.Timeout:
            print("please check your internet connection or try later.")
        except requests.exceptions.TooManyRedirects:
            print("bad url.")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        main_page = main_page.text
        html = bs(main_page, features="lxml")
        composition_df = self.get_composition_table(html)
        return composition_df

    @staticmethod
    def get_composition_table(html):
        tab_html = html.find("table", {"class":"table"})
        headers = [ele.get_text() for ele in tab_html.find("thead").find_all("th")]
        row_list = tab_html.find("tbody").find_all("tr")
        content = [ele.get_text() for r in row_list for ele in r.find_all("td")]
        pattern = re.compile('(\\r|\\n|\\t|Md|€|\\s+)', re.UNICODE)
        content = [pattern.sub('', c) for c in content]

        resultat = np.reshape(content, (40, 8))
        composition_df = pd.DataFrame(resultat)
        composition_df.columns = headers
        return composition_df




