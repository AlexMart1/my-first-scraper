import requests
import lxml.html as html
import numpy as np

home_url = 'https://www.larepublica.co/'

dummy_xpath = '//h2/a/@href'

xpath_links= '//div[@class="news V_Title_Img" or @class="V_Title"]/a/@href'

xpath_title = '//div[@class="mb-auto"]//a/text()'

xpath_summary = '//div[@class="lead"]/p/text()'

xpath_body = '//div[@class="html-content"]/p/text()'

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
			
			print(links_to_news)
			print(len(links_to_news))
			
		else:
			raise ValueError(f'Error:{response.status_code}')
			
			
	except ValueError as ve:
		print(ve)
	
	
def run():
	parse_home()

#defino el entry-point
if __name__ == '__main__':
	run()


	
	
