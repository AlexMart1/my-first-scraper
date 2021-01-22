import requests
import lxml.html as html
import numpy as np
#este modulo se importa para poder crear carpetas desde el script
import os
#este modulo para traer la fecha de hoy y asociarlas con las noticias
import datetime

home_url = 'https://www.larepublica.co/'

dummy_xpath = '//h2/a/@href'

xpath_links= '//div[@class="news V_Title_Img" or @class="V_Title"]/a/@href'

xpath_title = '//div[@class="mb-auto"]//a/text()'

xpath_summary = '//div[@class="lead"]/p/text()'

xpath_body = '//div[@class="html-content"]/p/text()'

def parse_article(link, today):
	try:
		#entro al link dado utilizando requests.get()
		response = requests.get(link)
		if response.status_code == 200:
			#decodeo el contenido del articulo usando utf-8
			article = response.content.decode('utf-8')
			#lo convierto a un objeto html
			parsed = html.fromstring(article)
			
			try:
				#porque parsed.xpath() entrega una lista
				title = parsed.xpath(xpath_title)[0]
				title = title.replace('\"','')
				file_title = title.replace(' ','_')
				summary = parsed.xpath(xpath_summary)[0]
				#body mas bien es una lista de parrafos
				body = parsed.xpath(xpath_body)
			
			#si hay una noticia que carezca de un resumen, por ejemplo
			#yo voy a salirme de la función
			#esto es una salida fácil pues lo que hago con esto es evitarme
			#procesar las noticias que carezcan de un resumen, tal vez 
			#una versión más elaborada de este scraper debería ser capaz
			#de también guardar esas noticias
			except IndexError:
				return 
			
			#voy a abrir la carpeta creada en parse_home()
			#y luego voy a crear un archivo txt que lleve de nombre
			#el titulo de la noticia
			#'w' = modo escritura
			# encoding = 'utf-8' para no tener problemas con carácteres especiales
			# as f para referirnos al archivo abierto
			with open(f'{today}/{file_title}.txt', 'w', encoding='utf-8') as f:
				 f.write(title)
				 f.write('\n\n')
				 f.write(summary)
				 f.write('\n\n')
				 for p in body:
				 	f.write(p)
				 	f.write('\n')
			
		else:
			raise ValueError(f'Error: {response.status_code}')
	except ValueError as ve:
		print(ve)


def parse_home():
	try:
		response = requests.get(home_url)
		
		if response.status_code == 200:
			#response.content se trae el contenido html de la pagina
			#decode con utf-8 resuelve problemas de lectura de caracteres raros
			home = response.content.decode('utf-8')
			#en parsed almaceno un objeto hecho desde home
			#sobre el que voy a poder hacer busquedas de tipo xpath
			parsed = html.fromstring(home)
			
			links_to_news = parsed.xpath(xpath_links)
			links_to_news = np.unique(links_to_news)
			
			dummy = parsed.xpath(dummy_xpath)
			
			#print(links_to_news)
			#print(len(links_to_news))
			
			today = datetime.date.today().strftime('%d-%m-%Y')
			#si no existe una carpeta con la fecha de hoy
			if not os.path.isdir(today):
				#vamos a crear esa carpeta
				os.mkdir(today)
				
			for link in links_to_news:
				parse_article(link, today)
			
		else:
			raise ValueError(f'Error:{response.status_code}')
			
			
	except ValueError as ve:
		print(ve)
	
	
def run():
	parse_home()

#defino el entry-point
if __name__ == '__main__':
	run()


	
	
