from CDL.main import *

IDSInstance = IDScraper('wg')
TDInstance = ThreadDownloader('wg')
TDInstance.DL(IDSInstance.ids(pages=1,pless=20))
