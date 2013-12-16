import tkFileDialog
import collections

from Tkinter import *
from ttk import *

from CDL.main import *

root = Tk()
root.geometry("400x225")  #176
root.title("4Chan Thread Downloader")

Label(root,text="Download Location:  ").place(x=0,y=0)

location = StringVar()
dlloc = Entry(root,width=29,textvariable=location)
dlloc.place(x=132, y=0)
change = lambda: location.set(tkFileDialog.askdirectory())
Button(root,text="...",width=2,command=change).place(x=372,y=0)

minpics = IntVar()
mpics = Checkbutton(root, text="Minimum Pictures  ", variable=minpics)
mpics.place(x=0,y=30)
#Label(root,text="Minimum Pictures  ").grid(row=2,column=1)
min_ = IntVar()
mpicse = Spinbox(root, from_=1, to=100, state="disabled",textvariable=min_)
mpicse.place(x=150,y=30)
mpe = lambda *a: (minpics.get() and [mpicse.config(state="normal")] or [mpicse.config(state="disabled")])[0]
minpics.trace("w", mpe)

maxpics = IntVar()
mapics = Checkbutton(root, text="Maximum Pictures  ", variable=maxpics)
mapics.place(x=0, y=60)
#Label(root,text="Maximum Pictures  ").grid(row=3,column=1)
max_ = IntVar()
mapicse = Spinbox(root, from_=1, to=100, state="disabled",textvariable=max_)
mapicse.place(x=150,y=60)
mape = lambda *a: (maxpics.get() and [mapicse.config(state="normal")] or [mapicse.config(state="disabled")])[0]
maxpics.trace("w",mape)

boards = collections.OrderedDict([('3', 11), ('a', 11), ('adv', 11), ('an', 11), ('asp', 11), ('b', 16), ('c', 11), ('cgl', 11), ('ck', 11), ('cm', 11), ('co', 11), ('d', 11), ('diy', 11), ('e', 11), ('f', 1), ('fa', 11), ('fit', 11), ('g', 11), ('gd', 11), ('gif', 11), ('h', 11), ('hc', 11), ('hm', 11), ('hr', 11), ('i', 11), ('ic', 11), ('int', 11), ('jp', 11), ('k', 11), ('lgbt', 11), ('lit', 11), ('m', 11), ('mlp', 11), ('mu', 11), ('n', 11), ('o', 11), ('out', 11), ('p', 11), ('po', 11), ('pol', 11), ('r', 16), ('r9k', 11), ('s', 11), ('s4s', 11), ('sci', 11), ('soc', 11), ('sp', 11), ('t', 11), ('tg', 11), ('toy', 11), ('trv', 11), ('tv', 11), ('u', 11), ('v', 11), ('vg', 6), ('vp', 11), ('vr', 11), ('w', 11), ('wg', 11), ('wsg', 11), ('x', 11), ('y', 11)])
bds = {'/{0}/'.format(i) : i for i in boards.keys()}
section = StringVar()
Label(root,text="Board Selection  ").place(x=0, y=90)
sect = Spinbox(root,values=tuple(sorted(bds.keys())),textvariable=section)
section.set('/b/')
sect.place(x=150,y=90)

Label(root, text="Pages to Download  ").place(x=0,y=120)
page = IntVar()
pages = Spinbox(root, from_=1, to=16, textvariable=page)
pages.place(x=150, y=120)

def update(*a):
	x = boards[bds[section.get()]]
	pages.config(to=x)
	page.set(x if page.get()%x==0 else page.get()%x)
section.trace("w",update)

prog = Progressbar(root,length=400)
prog.place(x=0,y=180)
prog2 = Progressbar(root,length=400)
prog2.place(x=0,y=205)
def OnFinish(i,o,f):
	global prog
	global prog2
	global root
	prog.step(100/o)
	prog2['value']=0
	root.update()
def download():
	global prog
	global prog2
	global root
	s = section.get()
	idsi = IDScraper(bds[s])
	if not location.get():
		tdi = ThreadDownloader(bds[s])
	else:
		tdi = ThreadDownloader(bds[s],location.get())
	if maxpics.get() and minpics.get():
		ids = idsi.ids(pages=page.get(),pless=max_.get(),pmore=min_.get())
	elif maxpics.get() and not minpics.get():
		ids = idsi.ids(pages=page.get(),pless=max_.get())
	elif minpics.get() and not maxpics.get():
		ids = idsi.ids(pages=page.get(),pmore=min_.get())
	else:
		ids = idsi.ids(pages=page.get())
	#prog.start()
	but.config(state="disabled")
	prog['value']=0
	prog2['value']=0
	tdi.OnStart = lambda i,o,f: True
	tdi.OnStartp = lambda i,o,f: True
	tdi.OnFinish = OnFinish
	tdi.OnFinishp = lambda i,o,f: (prog2.step(100/o),root.update())
	tdi.DL(ids)
	prog['value'] = 100
	prog2['value'] = 100
	but.config(state="normal")
Label(root).grid(row=7)

but = Button(root,text="Download",command=download,width=49)
#but.config(command=download(but))
but.place(x=0,y=150)
root.mainloop()
