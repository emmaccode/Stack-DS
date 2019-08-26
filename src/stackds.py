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
from shutil import copyfile
from subprocess import Popen, PIPE
from cStringIO import StringIO
import imp
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

#______Modifications______
print('Checking for zIpy...')
try:
	zIpy = imp.load_source('Myapp', 'extensions/test.py')
	zIpymod = True
except:
	zIpymod = False
	print('Module zIpy is not installed')
print('Checking for Dash-Ly...')
try:
	dashlymod = imp.load_source('Myapp', 'extensions/dashly.py')
	DashLymod = True
except:
	DashLymod = False
	print('Checking for Dash-Ly...')
	print('Module Dash-Ly is not installed')
	if zIpymod == False:
		print('Business as usual')
		print('Running StackDS in Standalone Mode')
#TODO Future Dependencies:
#dependency: Sklearn
#Dependency: sudo apt-get install wkhtmltopdf
UI_FILE = "src/stackds.ui"

#<----Dependencies---->
#=====TODO LIST=====
#TODO UI Update? Buttons, better coloring,etc.
#TODO add error GUI for application internal errors
#TODO Add Hotkeys
#TODO DFParser, for another way to view the DataFrames without rendering images
#TODO Add saved(ID) as boolean, to tell if DF is saved																	Dash
#TODO Add confirm overwrite dialog
#TODO Selectable Df parser, to place df into grid or treeview
#TODO Refresh ID, DF, ETC on close, as of right now, you have to switch and
#												Reopen it...
#TODO Change color of df_live_code Textbox
#TODO UNNAMED- BUG
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
		#==EXTENSIONS!==
		if zIpymod == True:
			pipelinezipy = self.builder.get_object('pipelinezipy')
			self.exbar = self.builder.get_object('extbar')
			zipy = self.builder.get_object('Zipy')
			zipy.show()
			self.exbar.show()
			pipelinezipy.show()
			self.fm_showext = self.builder.get_object('show_extbar')
			self.fm_showext.show()
			self.extbart = True
			creinzip = self.builder.get_object('creinzip')
			creinzip.show()
		if DashLymod == True:
			self.exbar = self.builder.get_object('extbar')
			self.fm_showext = self.builder.get_object('show_extbar')
			self.exbar.show()
			dashly = self.builder.get_object('Dashly')
			dashly.show()
			self.extbart = True
			self.fm_showext.show()
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
	#<--------Export HTML-------->
	def fm_exporthtml_cl(self,dialog):
		htmlsave = self.builder.get_object('Save_HTML')
		htmlsave.show()
#<============DataFrame Menu======>
	#<-------Manual Entry------->
	def df_exec_mb(self,pasghetti):
		self.df_live_code = self.builder.get_object('df_live_code')
		self.df_exec_output = self.builder.get_object('df_exec_output')
		self.df_exec_output.modify_base(Gtk.StateFlags.NORMAL,
										Gdk.color_parse('green'))
		self.df_exec_output.modify_text(Gtk.StateFlags.NORMAL,
										Gdk.color_parse('white'))
		#TODO Change Color^^
		self.df_live_code.show()
		self.dfexeci = self.builder.get_object('df_exec_input')
		self.dfexeco = self.builder.get_object('df_exec_output')
	#<------Drop----->
	def fm_df_drop_cl(self,spaghetti):
		self.dropdialog = self.builder.get_object('drop_dialog')
		self.packbox = self.builder.get_object('packbox')
		self.drop_content_toggle = self.builder.get_object(
													'drop_content_toggle')
		self.drop_row_toggle = self.builder.get_object('drop_row_toggle')
		self.drop_column_toggle = self.builder.get_object('drop_column_toggle')
		self.dropdialog.show()
	#<------Clean------>
	def fm_clean_select(self,clean):
		print('Clean')
	#<-----Replace---->
	def fm_df_replace(self,rep):
		dfrep = self.builder.get_object('df_replace_dialog')
		dfrep.show()
		columnnumber = 1
		df = self.dataframe
		self.repcolrplc = self.builder.get_object('repcolrplc')
		for (columnName, columnData) in df.iteritems():
			columnparse = str(columnName)
			columnnumber = str(columnnumber)
   			self.repcolrplc.append(columnnumber,columnparse)
			columnnumber = int(columnnumber)
			columnnumber = columnnumber+1
#=================Pipelines=======>
	def fm_pipelineshow(self,pip):
		pipelines = self.builder.get_object('Pipelines')
		pipelines.show()
#=================Preferences=====>
	#<------Show Preferences----->
	def show_preferences(self,potat):
		self.pref = self.builder.get_object('preferences')
		verslabel = self.builder.get_object('prefverslabel')
		versidfm = self.builder.get_object('VersionID')
		portfolbut = self.builder.get_object('Portfolbutt')
		docbut = self.builder.get_object('Documentationbut')
		websbut = self.builder.get_object('Websitebut')
		portfolbut.set_label('My Portfolio')
		docbut.set_label('Documentation')
		websbut.set_label('StackDS Website')
		versid = versidfm.get_label()
		verslabel.set_text(versid)
		self.pref.show()
	#<-----Show/Hide Extension bar----->
	def fm_show_extbar(self,main):
		if self.extbart == True:
			self.exbar.hide()
			self.fm_showext.set_label('Show Extensions')
			self.extbart = False
		else:
			self.exbar.show()
			self.fm_showext.set_label('Hide Extensions')
			self.extbart = True

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
			exec(userexec)
		except:
			print('zIpy Lite has found an error!')
			outputbuffer.set_text(buffer.getvalue())
		outputbuffer.set_text(buffer.getvalue())
		self.dfexeco.set_buffer(outputbuffer)
		self.updatedataview(df)
	#<-------Drop-------->
	def df_drop_click(self,ppe):
		df = self.dataframe
		ide = self.packbox.get_active_text()
		if self.columndrop == True:
			df = df.drop(columns=[ide])
		if self.rowdrop == True:
			df = df.drop(df.index[int(ide)])
		if self.contentdrop == True:
			df = df.drop(df.str.contains(ide))
		self.updatedataview(df)
		self.dropdialog.show()
	def Df_Drop_Cancel(self,ppc):
		self.dropdialog.hide()
	def on_drop_row_t(self,wwc):
		columnnumber = 1
		df = self.dataframe
		self.rowdrop = True
		self.contentdrop = False
		self.columndrop = False
		self.drop_content_toggle.set_active(False)
		self.drop_column_toggle.set_active(False)
		self.packbox.remove_all()
		for i in df.index:
			columntitle = str(i)
			columnnumber = str(columnnumber)
			self.packbox.append(columnnumber,columntitle)
			columnnumber = int(columnnumber)
			columnnumber = columnnumber+1
	def on_drop_content_t(self,wwe):
		self.rowdrop = False
		self.contentdrop = True
		self.columndrop = False
		self.drop_row_toggle.set_active(False)
		self.drop_column_toggle.set_active(False)
		self.Content_drop = self.builder.get_object('Content_Drop_Dialog')
		self.Content_drop.show()
		self.packbox.remove_all()
		self.packbox.Has_Entry = True
	def on_drop_column_t(self,wwb):
		self.columndrop = True
		self.contentdrop = False
		self.rowdrop = False
		self.drop_content_toggle.set_active(False)
		self.drop_row_toggle.set_active(False)
		self.packbox.remove_all()
		columnnumber = 1
		df = self.dataframe
		for (columnName, columnData) in df.iteritems():
			columnparse = str(columnName)
			columnnumber = str(columnnumber)
   			self.packbox.append(columnnumber,columnparse)
			columnnumber = int(columnnumber)
			columnnumber = columnnumber+1
	def content_drop_b(self,eat):
		self.contenttodrop = self.builder.get_object('contenttodrop')
		self.packbox.append(str(1),self.contenttodrop.get_text())
		self.Content_drop.hide()
	#<------DF Replace------->
	#TODO Add error dialog for entries not found on axis
	def df_column_replace(self,ricky):
		df = self.dataframe
		toreplace = self.builder.get_object('replcolent')
		hl = toreplace.get_text()
		replme = self.repcolrplc.get_active_text()
		df = df.replace({replme : hl})
		self.updatedataview(df)
	def df_cont_repl(self,jam):
		print('pickles2')
	def df_repl_cancel(self,pot):
		dfrep = self.builder.get_object('df_replace_dialog')
		dfrep.hide()
	#Export To HTML
		
	#<------Preferences------>
	def preference_cl(self,cl):
		self.pref.hide()
	#<------Export HTML------>
	def save_html_conf(self, der):		
		save_html = self.builder.get_object('Save_HTML')
		htmllabel = self.builder.get_object('Save_HTML_Label')
		label = htmllabel.get_text()
		filepath = save_html.get_current_folder
		savefile = str(filepath)+str(label)+'.html'
		dfhtml = self.dataframe.to_html()
		html = css+str(dfhtml)
		open(savefile, 'w').close()
		text_file = open(savefile, "a")
		text_file.write(html)
		text_file.close()
		winder = self.builder.get_object('Save_HTML')
		winder.hide()
	def save_html_Cancel(self, peer):
		winder = self.builder.get_object('Save_HTML')
		winder.hide()
	#_____________________________________
	#<<<<<<<<<Class Accessories>>>>>>>>>>>
	def updatedataview(self,df):
		df.to_csv(self.swapfileactive)
		self.dataframe = pd.read_csv(self.swapfileactive)
		dfforconv = df.head(self.display_head)
		scroller = Gtk.ScrolledWindow.new()
		convertimage(dfforconv,css,'swap.png')
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