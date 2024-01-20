import requests
from bs4 import BeautifulSoup as BS
import pymysql
import time

try:
	connection = pymysql.connect(host="localhost", port=3306, user="root", password="12345678", database="news", cursorclass=pymysql.cursors.DictCursor)
	print("Succsessfully connection")

	with connection.cursor() as cursor:
		page = 154721

		while page != 157345:
			try:
				url = "https://gorvesti.ru/sport/rotor-rastrogaet-kontrakty-s-dvumya-igrokami-" + str(page) + ".html"
				r = requests.get(url)
				soup = BS(r.text, "lxml")
				data = soup.find("div", class_="sticky")
				article = data.find("article", class_="item block")
				article_block = article.find("div", class_="article-title-block")
				tags = article.find_all("p")
				time_block = article_block.find("div", class_="summary")

				title = article_block.find("h1", class_="title-block")
				time = time_block.find("span", class_="dt").text
				text = ""
				for tag in tags:
				    text = text + " " + tag.text
				text = text.strip()

				cursor.execute("insert into `records` (name_record, date_record, text_record, url_record) values ('" + title.text + "','" + time + "','" + text + "','" + url + "');")
				connection.commit();

				print(title.text)
				print(time)
				print(text)
				print(url + "\n")
				page += 1

			except AttributeError:
				page += 1
				continue
		
except Exception as ex:
	print("Refused connection")
	print(ex)
