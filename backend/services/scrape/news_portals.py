from bs4 import BeautifulSoup as BS
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import sqlite3 as sql
import requests
from datetime import datetime

class ScrapeKathmanduPost:
    
    def __init__(self):
        self.kathmandupost_url = "https://kathmandupost.com//"
        print("Scraping Kathmandu Post")
        web_page_kathmandupost = requests.get(self.kathmandupost_url)
        self.soup_kathmandupost = BS(web_page_kathmandupost.content,'html.parser')
        
        self.CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.scraped_dict = {}
        
        self.con = sql.connect('database_scrapy.db')
        self.cursor_obj = self.con.cursor()
            
    def cleanhtml(self,raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext

    def clean_text(self,text):
        clean_str = ""
        text_str = str(text)
        text_str = self.cleanhtml(text_str)
        text_str = text_str.replace("\xa0","")
        text_str = text_str.replace("\u202f","")
        clean_str += " "
        clean_str += text_str 
        clean_str = clean_str.replace(".,",".")  
        clean_str = clean_str.replace(". ,",". ")
        clean_str = clean_str.replace("[","")
        clean_str = clean_str.replace("]","")  
        return clean_str
    
    def get_kathmandupost_news_url(self):
        scrape_link = []
        
        main_container = self.soup_kathmandupost.find("main")
        web_links = main_container.find_all("a") 

        for links in web_links:
            links = links['href']
            if links.find("https://kathmandupost.com/") == -1:
                links = "https://kathmandupost.com" + links
            scrape_link.append(links)

        #removing duplicate links
        scrape_link = list(dict.fromkeys(scrape_link))
        return scrape_link
    
    def get_kathmandupost_scraped_news(self,scrape_link):
        count = 0
        for link in scrape_link[0:3]:
            try:
                url = link
                response = requests.get(url)
                soup = BS(response.content, "html.parser")
                title = soup.find(attrs={"style": "margin-bottom:0.1rem;"}).get_text()
                temp_container=soup.find("section",class_='story-section')
                news_str = temp_container.find_all('p')
                news_str = self.clean_text(news_str)
                
                date = datetime.now().strftime("%Y/%m/%d")                
                source = "KathmanduPost"
                split_index = len(url.split('/')) - 1
                news_id = url.split('/')[split_index]
                news_id = int(''.join(str(ord(c)) for c in news_id)[0:10])
                
            except:
                continue
                  
    def create_table(self):
        table = " CREATE TABLE IF NOT EXISTS english_news(news_id INTEGER(20) PRIMARY KEY ,title VARCHAR(100), news VARCHAR(2000), source VARCHAR(100), link VARCHAR(100),category VARCHAR(15),date VARCHAR(25),confidence BIGINT,summary VARCHAR(2000))"
        self.cursor_obj.execute(table)
    
    def update_table(self,key):
        try:
            self.cursor_obj.execute("INSERT INTO english_news (news_id,title,news,source,link,category,date,confidence,summary) VALUES (?,?,?,?,?,?,?,?,?)",(self.scraped_dict[key]['news_id'],self.scraped_dict[key]['title'],self.scraped_dict[key]['news'],self.scraped_dict[key]['source'],self.scraped_dict[key]['link'],self.scraped_dict[key]['category'],self.scraped_dict[key]['date'],self.scraped_dict[key]['confidence'],self.scraped_dict[key]['summary']) )
            self.con.commit()
        except sql.Error as er:
            print(er)
        #self.cursor_obj.execute(query)

    def scrape_news(self):
        if self.kathmandupost_url != "":
            scrape_link = self.get_kathmandupost_news_url()
            self.get_kathmandupost_scraped_news(scrape_link)
            self.create_table()
            for key in self.scraped_dict:
                self.update_table(key)
        self.con.close()    