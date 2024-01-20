import telebot
import time
import pymysql
from telebot import types
import requests
from bs4 import BeautifulSoup as BS



# Инициализация бота и подключение к MySQL
bot = telebot.TeleBot('6985902092:AAEOz7e181FWqb7l2U0kbIQMEbGPiqpe4EM')

@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup()
	btn1 = types.KeyboardButton('Обновить новости')
	markup.row(btn1)
	bot.send_message(message.chat.id, text="Добро пожаловать в чат-бот для просмотра последних новостей", reply_markup=markup)

# Функция для обработки команды
@bot.message_handler(content_types=['text'])
def get_news(message):
	if(message.text == "Обновить новости"):
		while True:
			try:
				url = "https://gorvesti.ru"
				r = requests.get(url)
				soup = BS(r.text, "html5lib")
				column = soup.find("div", class_="col-l-side order-lg-0")
				data = column.find("div", class_="sticky")
				section = data.find("div", class_="section-feed section-feed-sm")
				a = section.find_all("a", class_="card itm")
				link_a = []

				for i in range(10):
					link_a.append(a[i].get("href"))

			except AttributeError as ex:
				print(ex)
				exit(666)

			num_link = len(link_a) - 1
			while num_link != -1:
				try:
					url_current = url + link_a[num_link]
					r = requests.get(url_current)
					soup = BS(r.text, "html5lib")
					data = soup.find("div", class_="sticky")
					article = data.find("article", class_="item block")
					article_block = article.find("div", class_="article-title-block")
					tags = article.find_all("p")
					time_block = article_block.find("div", class_="summary")

					title = article_block.find("h1", class_="title-block")
					time_news = time_block.find("span", class_="dt").text
					text = ""
					for tag in tags:
						text = text + " " + tag.text
					text = text.strip()	
					vip_person = "Отсутствуют"
					attraction = " Отсутствуют"
					
					
					
					connection = pymysql.connect(host="localhost", port=3306, user="root", password="12345678", database="news", cursorclass=pymysql.cursors.DictCursor)					
					with connection.cursor() as cursor:
						cursor.execute("select name_record from records where name_record = '" + title.text + "'")
						news_one = cursor.fetchall()
						if len(news_one) == 0:
							cursor.execute("insert into `records` (name_record, date_record, text_record, url_record) values ('" + title.text + "','" + time_news + "','" + text + "','" + url + "');")
							connection.commit();
					new_news = title.text + time_news + text + url_current + vip_person + attraction 
					if len(new_news) < 4095:
						message_text = "Название: " + title.text + "\n\n" + "Дата: " + time_news + "\n\n" + "Текст: " + text + "\n\n" + "Ссылка: " + url_current + "\n\n" + "ВИП-персоны: " + vip_person + "\n\n" + "Достопримечательности: " + attraction + "\n\n" + "Тональность: "
						bot.send_message(message.chat.id, message_text)
						time.sleep(2)

					num_link -= 1

				except AttributeError:
					num_link-=1
					continue
			break

# Запуск бота
bot.polling(none_stop=True)

# Закрытие подключения к MySQL
conn.close()
