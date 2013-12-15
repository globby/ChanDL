from CDL.main import *

IDSInstance = IDScraper('wg')                       #Create an instance of the id scraper on the board 'wg'
TDInstance = ThreadDownloader('wg')                 #Create an instance of the thread downloader on the board 'wg'
TDInstance.DL(IDSInstance.ids(pages=1,pless=20))    #Scrape 'wg' for one page of ids in which the threads have less than 20 pictures and download them
