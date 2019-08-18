#!/usr/bin/env python
#<----------StackDS---------->
#Copyright(C) Emmett Boudreau <http://www.emmettboudreau.com>
#<emmett@emmettboudreau.com>
#|	|	|	|Stack	|   D-S	|	|	|	|
#|			|		|		|			|
#Website: <http://stackds.emmettboudreau,com>
#GNU GPL General License for modification
#			|			and redistribution
#Creative Commons Attribution for open	|
#|			|		|		source uses	|
#Created AUGUST 2019
#<----------StackDS---------->
#--Startup Error Manager--
def errormessage(code,argument):
	print('-----------')
	print('ERROR!')
	print(code,argument)
	print('-----------')
	sys.exit(code)
#<----Dependencies---->
#__GTK__
import os, sys
try:
	from gi.repository import Gtk, GdkPixbuf, Gdk
except:
	errormessage(1,"Missing Dependency: GTK")
#__System__
from IPython.display import clear_output, Image, display
#__Dataframes__
try:
	import pandas as pd
except:
	errormessage(2,"Missing Dependency: Pandas")
#__Mathematics__
try:
	import numpy as np
except:
	errormessage(3,"Missing Dependency: Numpy")
#__Misc__
try:
	import imgkit
except:
	errormessage(4,"Missing Dependency: imagekit")
from shutil import copyfile
from subprocess import Popen, PIPE
from cStringIO import StringIO
#TODO Future Dependencies:
#dependency: Plotly Express
#dependency: Sklearn
#TODO install in install.sh
#Dependency: sudo apt-get install wkhtmltopdf
UI_FILE = "src/stackds.ui"

#<----Dependencies---->
#=====TODO LIST=====
#TODO UI Update? Buttons, better coloring,etc.
#TODO add error GUI for application internal errors
#TODO Preferences
#TODO Add Hotkeys
#TODO Function that places into GUI in treeview, or grid
#TODO DataFrame Menu
#TODO Add saved(ID) as boolean, to tell if DF is saved
#TODO Machine Learning Menu???
#TODO Data Studio Visualization(seperate class and UI file), plotly, w plotly
#																		Dash
#TODO Add confirm overwrite dialog
#TODO Add Pipeline menu, with storable pipelines, maybe put this into ML menu
#TODO Df parser, to place df into grid or treeview
#TODO Add DF saving on tab switch, datablah.tocsv, id before update.
#TODO Export HTML
#TODO Refresh ID, DF, ETC on close, as of right now, you have to switch and
#												Reopen it...
#TODO Change color of df_live_code Textbox
#TODO New DF from series or Txt
#TODO Preferences: Add Head Size
#TODO Preferences: Add Debug mode to make more visible.
#|		|		 || 		|	  |
#=====TODO LIST=====
#<======User Interface======>
class GUI:
	def __init__(self):
		#--GTK BUILDER--
		self.dataopen = 0
		self.datas = 0
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)
		#--Objects--
		window = self.builder.get_object('window')
		self.thenotebook = self.builder.get_object('thenotebook')
		self.id_counter = self.builder.get_object('id_counter')
		self.dfid = 0
		#--/Objects--
		#--Environment-Variables--
		#These Variables are defined on startup, to be
		#Adjusted at the user's pleasure
		self.notebookclosed = False
		self.nbidmultiplier = 0
		self.display_head = 10
		#----Window----
		#Gotta show the window, too
		window.show_all()
		window.connect("destroy", Gtk.main_quit)
		self.original = True
	def on_window_destroy(self, window):
		Gtk.main_quit()
	#|	|	|	|	|	|	|	|	|	|
	#|	|	|Callback Functions	|	|	|
	#|	|	|	|	|	|	|	|	|	|
	#<-------------Notebook ID updater----------------------->
	def notebook_active_update(self,notebook,dataview,index):
		self.dfviewactive = dataview
		if self.notebookclosed == True:
			if index < self.nbpageremoved:
				index = index
				print('Compensation')
			else:
				index = index
				index = (index + self.nbidmultiplier)
				print('No Compensation')
		else:
			print("Loading:")
		self.indexid = index
		self.swapfileactive = ('swap/df'+str(index)+'.csv')
		self.id_counter.set_label(str(index))
		self.dataframe = pd.read_csv('swap/df'+str(index)+'.csv')
		print("Active Tab: "+str(index))
#
#|	|	|	|	|	|	|	|	|	|	|	|	|	|
#|	|	|	|	|	|Menubar	|	|	|	|	|	|
#|	|	|	|	|	|	|	|	|	|	|	|	|	|
#
#<=================File Menu===>
	#<----------Read CSV---------->
	def fm_readcsv_select(self,open_csv):
		self.open_csv = self.builder.get_object('Open_CSV')
		self.open_csv.show()
	#<---------Close Tab--------->
	def fm_closetab_select(self,tabid):
		index = int(self.indexid)
		index = int(self.id_counter.get_label())
		self.thenotebook.remove_page(index)
		self.nbpageremoved = index
		self.nbidmultiplier = (self.nbidmultiplier+1)
		self.notebookclosed = True
		self.id_counter.set_label(str(thenotebook.get_current_page))
	#<----------Render Image--------->
	def fm_renderimage_select(self,img_renderer):
		self.img_renderer = self.builder.get_object('img_renderer')
		self.img_renderer.show()
		self.imghead = False
		self.csstoggler = False
		self.imghead_spin = self.builder.get_object('imghead_spin')
	#<----------Exit-------->
	def fm_exit_click(self,hello):
		Gtk.main_quit()
	#<---------Export HTML-------->
	def fm_exporthtml_cl(self,hhdr):
		print('hi')
	#<---------Save CSV----------->
	def fm_save_csv_select(self,hhe):
		df = self.dataframe
		self.export_csv = self.builder.get_object('export_csv_dialog')
		self.export_csv.show()
#<============DataFrame Menu======>
	#<-------Manual Entry------->
	def df_exec_mb(self,pasghetti):
		self.df_live_code = self.builder.get_object('df_live_code')
		self.df_exec_output = self.builder.get_object('df_exec_output')
		#self.df_exec_output.modify_bg(Gtk.StateType.Normal,
		#							Gdk.Color(20000, 10000, 10000))
		#TODO Change Color^^
		self.df_live_code.show()
		self.dfexeci = self.builder.get_object('df_exec_input')
		self.dfexeco = self.builder.get_object('df_exec_output')
#
#|	|	|	|	|	|	|	|	|	|	|	|	|	|
#|	|	|	|	|	Dialogs	|	|	|	|	|	|	|
#|	|	|	|	|	|	|	|	|	|	|	|	|	|
#
	#<-----Read CSV----->
	def open_csv_cancel_click(self,opene):
		self.open_csv.hide()
		#When user double clicks file selection
	def read_file_activated(self,open_csv):
		window = self.builder.get_object('window')
		filename = self.open_csv.get_uri()
		dflabel1 = self.builder.get_object('Dflabel1')
		self.thenotebook.Scrollable = True
		print('User selected file:')
		print(filename)
		self.filetop = os.path.basename(filename)
		#Tests If Pandas is capable of reading in Data:
		try:
			df = pd.read_csv(filename)
			self.dataopen = self.dataopen+1
		except:
			print(errormessage(21,'File Imported is not a CSV file'))
		print('File ',filename,' Read Successfully.')
		dfforconv = df.head(self.display_head)
		convertimage(dfforconv,css,'swap.png')
		dfimage = Gtk.Image.new_from_file('swap.png')
		#Renders scrollbar with DF as image.
		self.scroller = Gtk.ScrolledWindow.new()
		self.scroller.add(dfimage)
		self.scroller.set_focus_child(dfimage)
		self.notebooklabel = Gtk.Label()
		self.notebooklabel.set_text(self.filetop)
		self.thenotebook.append_page(self.scroller,self.notebooklabel)
		#Checks if the application has just been started,
		#In which case, It then subtracts 1 from the ID
		if self.original == True:
			self.thenotebook.remove_page(0)
			self.original = False
			self.dataopen = self.dataopen-1
		swapper = str('swap/df'+str(self.dataopen)+'.csv')
		self.dataframe = df
		df.to_csv(swapper)
		open_csv.hide()
		window.show_all()
	#<----Image renderer----->
	def custom_csv_toggled(self,customcsvtoggle):
		if self.csstoggler == False:
			self.csstoggler = True
			self.csstypeplace = self.builder.get_object('csstypeplace')
			self.csstypeplace.show()
			self.csstypeplace.No_show_all = False
			self.cssbuffer = Gtk.TextBuffer.new()
			self.cssbuffer.set_text(css)
			self.csstypeplace.set_buffer(cssbuffer)
			self.csstypeplace.set_size_request(300,500)
		else:
			self.csstoggler = False
			self.csstypeplace.hide()
			self.csstypeplace.set_size_request(1,1)
	def img_full_df_toggle(self,loader):
		if self.imghead == False:
			self.imghead = True
			self.imghead.hide()
		else:
			self.imghead = False
	def img_renderer_save(self,dcss):
		self.loadbar = self.builder.get_object('loadbar')
		self.img_renderer = self.builder.get_object('img_renderer')
		self.img_render_save = self.builder.get_object('img_render_save')
		if self.csstoggler == False:
			self.img_render_save.show()
		else:
			css = self.cssbuffer.get_text()
			self.img_render_save.show()
	def close_imrenderer(self,hi):
		self.img_renderer.hide()
	def img_render_folderch(self,folderpath):
		self.img_render_s_prev = self.builder.get_object('img_render_s_prev')
		self.filepath = self.img_render_save.get_current_folder()
		self.img_render_s_prev.set_text('df')
		print
	def img_saved_ok(self,wi):
		self.loadbar.start()
		self.img_render_save.hide()
		filelabel = self.img_render_s_prev.get_text()
		self.filepath = (self.filepath+"/"+filelabel+".png")
		df = pd.read_csv(self.swapfileactive)
		img_full_df_check = self.builder.get_object('img_full_df_check')
		if self.imghead == False:
			hdnum = (self.imghead_spin.get_value_as_int())
			df = df.head(hdnum)
		self.img_renderer.hide()
		self.loadbar.stop()
		convertimage(df,css,self.filepath)
	def	img_savedi_cancel(self,wi):
		self.img_render_save.hide()
	#<--------Save CSV---------->
	def save_csv_cancel(self,hf):
		self.export_csv.hide()
	def save_csv_b_click(self,he):
		swap = ('swap/df'+str(self.indexid)+'.csv')
		filenameentry = self.builder.get_object('filemenuentry')
		userstring = filenameentry.get_text()
		filepath = self.export_csv.get_current_folder()
		svep = (filepath+'/'+userstring+'.csv')
		copyfile(swap,svep)
		self.export_csv.hide()
	#<-------Manual Entry------->
	
	def df_exec_close(self,hel):
		self.df_live_code.hide()
	def df_exec_ex(self,spo):
		outputbuffer = Gtk.TextBuffer.new()
		try:
			df = self.dataframe.copy()
		except:
			outputbuffer.set_text('zIpy Fatal ERROR!: Data not loaded')
		self.dfexeco.set_buffer(outputbuffer)
		userexec = self.dfexeci.get_text()
		sys.stdout = buffer = StringIO()
		print('*********************')
		print('===zIpy Lite 0.0.1===')
		print('*********************')
		try:
			exec userexec
		except:
			print('zIpy Lite has found an error!')
			outputbuffer.set_text(buffer.getvalue())
		outputbuffer.set_text(buffer.getvalue())
		self.dfexeco.set_buffer(outputbuffer)
		self.updatedataview(df)
	#_____________________________________
	#<<<<<<<<<Class Accessories>>>>>>>>>>>
	def updatedataview(self,df):
		df.to_csv(self.swapfileactive)
		dfforconv = df.head(self.display_head)
		scroller = Gtk.ScrolledWindow.new()
		convertimage(dfforconv,css,'swap.png')
		dfimage = Gtk.Image.new_from_file('swap.png')
		scroller.add(dfimage)
		self.notebooklabel.set_text('df'+str(index+1))
		page_num = self.id_counter.get_label()
		scrolleroller = self.thenotebook.get_nth_page(int(page_num))
		dfrealimage = scrolleroller.get_focus_child()
		dfrealimage.set_from_file('swap.png')
#========================================
#<---------Accessory Functions---------->
#TODO DFPARSER FOR NON IMAGE DF
def dfparser(df):
	print('================')
	print('Df Parser Version 2.0')
	print('Programmed by Emmett Boudreau')
	print('================')
	"""Parses Dataframe and places in to GTK Grid, Returns GTK Grid"""
	grid = Gtk.Grid
	parsecolumn = 0
	parserow = 0
	data = Gtk.Label
	for columns in df:
		print('column')
	return(grid)
#
#====================================================================
#|	|	|	DF Converters	|	|	|	|	|	|	|	|	|	|	|
#|	|	|	|	|	|	|	|	|	|	|	|	|	|	|	|	|	|
#Held at swap/swap.html/swap.png
def converthtml(df,css):
	"""Converts Dataframe to HTML"""
	open('swap.html', 'w').close()
	text_file = open("swap.html", "a")
	text_file.write(css)
	text_file.write(df.to_html())
	text_file.close()
	print(df.head(5))
def convertimage(df,css,filepath):
	"""HTML to Image"""
	converthtml(df,css)
	imgkitoptions = {"format": "png","width": 160, "height":600}
	dfprev = Image(imgkit.from_file("swap.html",
									filepath, options=imgkitoptions))
	
#==========Global Default CSS==========
css = """
	<style type=\"text/css\">
	table {
	color: #333;
	font-family: Helvetica, Arial, sans-serif;
	width: 640px;
	border-collapse:
	collapse; 
	border-spacing: 0;
	}imagekit
	td, th {
	border: 1px solid transparent; /* No more visible border */
	height: 30px;
	}
	th {
	background: #DFDFDF; /* Darken header a bit */
	font-weight: bold;
	}
	td {
	background: #FAFAFA;
	text-align: center;
	}
	table tr:nth-child(odd) td{
	background-color: white;
	}
	</style>
	"""
#<======Main======>
class main():
	#This number is used to hold open data
	dataopen = 0
	app = GUI()
	Gtk.main()