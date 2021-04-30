# Dependencies
from bs4 import BeautifulSoup as soup
from splinter import Browser
import requests
import pymongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)

	#Define a function to perform the repeated calls for 
	def retrievehtml(url, target):
		browser.visit(url)
		html = browser.html
		html_soup = soup(html, 'html.parser')
		return html_soup.select_one(target)
	
	# URL of first page to be scraped
	url = 'https://redplanetscience.com/'
	slide_elem = retrievehtml(url, 'div.list_text')

	news_title = slide_elem.find('div', class_='content_title').get_text()
	news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

	#Finding the Featured Image of the Day for https://spaceimages-mars.com
	url2 = 'https://spaceimages-mars.com'
	mars_pic_elem = retrievehtml(url2, 'div.header')
	img = mars_pic_elem.find('img', class_='headerimage fade-in')
	featured_image_url=(f"{url2}/{img['src']}")

	#Get the URL of the full images from Marshemispheres.com
	url3 = 'https://marshemispheres.com/'
	astropedia_elem = retrievehtml(url3, 'div.result-list')
	products = astropedia_elem.find_all('a', class_='itemLink')
	subpages = []
	for product in products:
		productURL = f"{url3}{product['href']}"
		if (productURL not in subpages):
			subpages.append(productURL)

	hemispheres = []
	for page in subpages:
		hspage = retrievehtml(page,'div.cover')
		pagetitle = hspage.h2.get_text()
		hspage = retrievehtml(page,'div.container')
		imgurl = hspage.find('img', class_="wide-image")['src']
		hemispheres.append({"Title": pagetitle ,"Image URL" : f"{url3}{imgurl}"})
	
	browser.quit()
	return {
		"NewsTitle1": news_title,
		"NewsDesc": news_p,
		"FeaturedURL": featured_image_url,
		"Hemispheres": hemispheres
	}

if __name__ == "__main__":
	print(scrape())
