import requests
from bs4 import BeautifulSoup as bs4
from lxml import html
from dateutil import parser
from datetime import datetime
import time
import mysql.connector


class Model(object):  # class model untuk konektor ke database
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="", database="prog_test"
        )
        self.sql = "INSERT INTO news_article (title, url, content, summary, article_ts, published_date ) VALUES (%s, %s, %s, %s, %s, %s)"


class Bisnis(
    object
):  # class bisnis berisikan parameter yang nantinya akan digunakan pada fungsi scrap()
    def __init__(self, url=""):
        self.url = url
        self.request = requests.get(url)
        self.bs = bs4(self.request.content, "lxml")
        self.parse = self.bs.find("ul", class_="list-news")
        self.tree = html.fromstring(self.request.content)
        self.get_title = self.tree.xpath("/html/body/div[3]/div/div/div[1]/h1/text()")
        self.get_summary = self.tree.xpath(
            "/html/body/div[3]/div/div/div[1]/div[3]/div/div/div[1]/text()"
        )
        self.get_datetime = self.tree.xpath(
            "/html/body/div[3]/div/div/div[1]/div[1]/br/following::text()[1]"
        )

    def scrap():  # fungsi bisnis untuk mengambil dataset dari website koran.bisnis
        s = Bisnis("https://koran.bisnis.com/")
        m = Model()
        mycursor = m.db.cursor()
        temp = []
        for a in s.parse.find_all("a", class_="icon", href=True):
            if a.text not in temp:
                temp.append(a["href"])
        for x in temp:
            detailed_init = Bisnis(x)

            # DATETIME AND UNIX TIMESTAMP, dibutuhkan beberapa manipulasi data
            get_timestamp = str(detailed_init.get_datetime)
            get_timestamp = get_timestamp.strip("[]''").replace("WIB", "")
            get_timestamp = get_timestamp.split(",")[-1].strip()
            if get_timestamp != "":
                date_time = parser.parse(get_timestamp)
                unix_ts = int(time.mktime(date_time.timetuple()))

                val = [
                    (
                        str(detailed_init.get_title).strip("[]''").strip(),
                        str(x),
                        None,  # konten dari koran.bisnis tidak dapat diambil karena membutuhkan untuk berlangganan premium
                        str(detailed_init.get_summary).strip("[]''"),
                        unix_ts,
                        date_time,
                    )
                ]
                try:
                    mycursor.executemany(m.sql, val)
                    m.db.commit()
                    print(mycursor.rowcount, "inserted.")
                except:
                    pass


class Antaranews(
    object
):  # class antaranews berisikan parameter yang nantinya akan dipakai pada fungsi scrap()
    def __init__(self, url=""):
        self.url = url
        self.request = requests.get(url)
        self.tree = html.fromstring(self.request.content)
        self.get_title = self.tree.xpath(
            "/html/body/div/div/div[2]/div/div[1]/article/div[1]/header/h1/text()"
        )
        self.get_summary = self.tree.xpath(
            "/html/body/div/div/div[2]/div/div[1]/article/div[1]/div[2]/br[1]/preceding-sibling::text()[normalize-space()]"
        )
        self.get_content = self.tree.xpath(
            "/html/body/div/div/div[2]/div/div[1]/article/div[1]/div[2]/br/following-sibling::text()[normalize-space()]"
        )
        self.get_datetime = self.tree.xpath("channel/item//*[3]/text()")
        self.get_link = self.tree.xpath("channel/item/guid/text()")

    def scrap():  # fungsi antaranews untuk mengambil dataset yang ada pada website jambi.antaranews
        s = Antaranews("https://jambi.antaranews.com/rss/terkini.xml")
        m = Model()
        mycursor = m.db.cursor()
        temp = []
        for x in s.get_link:
            if x not in temp:
                detailed_init = Antaranews(x)
                get_title = detailed_init.get_title
                get_summary = [x.strip() for x in detailed_init.get_summary]
                get_content = [x.strip() for x in detailed_init.get_content]
                get_timestamp = [x for x in s.get_datetime[0].split(",")]
                get_timestamp = get_timestamp[1].split(",")
                get_timestamp = str(get_timestamp).strip("[]''")
                date_time = parser.parse(get_timestamp)
                unix_ts = int(time.mktime(date_time.timetuple()))

                val = [
                    (
                        str(get_title).strip("[]''"),
                        str(x),
                        str(get_content).strip("[]''"),
                        str(get_summary).strip("[]''"),
                        unix_ts,
                        date_time,
                    )
                ]
                try:
                    mycursor.executemany(m.sql, val)
                    m.db.commit()
                    print(mycursor.rowcount, "inserted.")
                except:
                    pass
