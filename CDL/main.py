import urllib
import urllib2
import json
import os
import sys


__AUTHOR__ = "Catalyst"
__LICENSE__ = "GNU GPL"
__DOCSTRING__ = """

CDL or ChanDL is a 4chan thread downloading and thread id scraping library.
Usage and parmater explaination is as follows:

#Scrape thread ids:
instance = IDScraper('b')	 													#Parameter is section ID
instance.ids(pages=5,start=2,pmore=5,pless=20) 									#Gets all thread ids from pages 2-6 inclusive with more than 5 posts with images, and less than 20 posts with images
instance.ids() 																	#If parameters omitted, it will default to (pages=1,start=0,pmore=0,pless=False)

#Download threads:
instance = ThreadDownloader(board='b',path="/home/me/4chanimages") 				#First parameter is section ID, second is path to download to (defaults to current working directory if omitted)
instance.DL(['id1','id2'])														#Input a list of thread ids to download
"Called on start of thread download"
instance.OnStart = (lambda increment,outof,fname: sys.stdout.write("{0} {1}/{2}\n".format(fname,increment,outof)))
"Called on end of thread download"
instance.OnFinish = (lambda increment,outof,fname: sys.stdout.write("{0} {1}/{2}\n").format(fname,increment,outof)))
"Called on start of image download"
instance.OnStartp = (lambda increment,outof,fname: sys.stdout.write("{0} {1}/{2}\n").format(fname,increment,outof)))
"Called on end of image download"
instance.OnFinishp = (lambda increment,outof,fname: sys.stdout.write("{0} {1}/{2}\n").format(fname,increment,outof)))
"""

#EXCEPTIONS
class FCDL(Exception):
	pass
class InvalidBoard(FCDL):
	pass
class ParameterError(FCDL):
	pass

class IDScraper(object):
	def __init__(self,board,outfile=False):
		self.outfile = outfile
		if board not in ['3','a','adv','an','asp','b','c','cgl','ck','cm','co','d','diy','e','f','fa','fit','g','gd','gif','h','hc','hm','hr','i','ic','int','jp','k','lgbt','lit','m','mlp','mu','n','o','out','p','po','pol','q','r','r9k','s','s4s','sci','soc','sp','t','tg','toy','trv','tv','u','v','vg','vp','vr','w','wg','wsg','x','y']:
			raise InvalidBoard("{0} is an invalid board id.".format(board))
		self.board = board
	def ids(self,pages=1,start=0,pmore=0,pless=False):
		ids = []
		if pages < 1:
			raise ParameterError("Pages can not be < 1.")
		if start > 0:
			raise ParameterError("Start can not be > 0.")
		for i in range(start,pages):
			try:
				ids += self.getPage(i,pmore,pless)
			except urllib2.URLError:
				break
			except urllib2.HTTPError:
				break		
		return ids
	def getPage(self,page,pmore,pless):
		ids = []
		baseurl = "http://api.4chan.org/{0}/{1}.json".format(self.board,page)
		dat = json.loads(urllib2.urlopen(baseurl).read())
		for i in dat['threads']:
			tv = i['posts']
			if int(tv[0]['images'])+1 >= pmore:
				if pless:
					if int(tv[0]['images'])+1 <= pless:
						ids.append(tv[0]['no'])
				else:
					ids.append(tv[0]['no'])
		return ids

class ThreadDownloader(object):
	def __init__(self,board,path=os.getcwd()):
		self.path = path
		if board not in ['3','a','adv','an','asp','b','c','cgl','ck','cm','co','d','diy','e','f','fa','fit','g','gd','gif','h','hc','hm','hr','i','ic','int','jp','k','lgbt','lit','m','mlp','mu','n','o','out','p','po','pol','q','r','r9k','s','s4s','sci','soc','sp','t','tg','toy','trv','tv','u','v','vg','vp','vr','w','wg','wsg','x','y']:
			raise InvalidBoard("{0} is an invalid board id.".format(self.board))
		self.board = board
	def DL(self,threads):
		if not type(threads) == type([]):
			raise ParameterError("Thread ids must be list, not {0}".format(type(threads)))
		self.mine(self.path+"/{0}".format(self.board))
		increment = 0
		for i in threads:
			increment += 1
			self.OnStart(increment,len(threads),i)
			try:
				self.getThread(i)
			except urllib2.URLError:
				pass
			except urllib2.HTTPError:
				pass
			self.OnFinish(increment,len(threads),i)
	def OnStart(self,increment,outof,id_):												#Method called on start of each thread download
		print "Getting thread {0}/{1} ({2})...".format(increment,outof,id_)
	def OnFinish(self,increment,outof,id_):					 							#Method called on completion of each thread download
		pass
	def OnStartp(self,increment,outof,fname):											#Method called on start of each picture download
		print "\t- {0} (Image: {1}/{2})".format(fname,increment,outof)
	def OnFinishp(self,increment,outof,fname):											#Method called on completion of each picture download
		pass
	def getThread(self,id_):
		baseurl = "http://api.4chan.org/{0}/res/{1}.json".format(self.board,id_)
		dat = json.loads(urllib2.urlopen(baseurl).read())
		self.mine(self.path+"/{0}/{1}".format(self.board,id_))
		pics = []
		for i in dat['posts']:
			try:
				pics.append(str(i['tim'])+str(i['ext']))
			except:
				pass
		increment = 0
		for i in pics:
			increment += 1
			self.OnStartp(increment,len(pics),i)
			urllib.urlretrieve("http://images.4chan.org/{0}/src/{1}".format(self.board,i),self.path+"/{0}/{1}/{2}".format(self.board,id_,i))
			self.OnFinishp(increment,len(pics),i)
	def mine(self,path):
		if not os.path.exists(path):
			os.mkdir(path)
