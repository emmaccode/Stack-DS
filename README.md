# Stack-DS
Stack-DS is a Python-3-based Integrated Development Environment for Pandas. Stack-DS speeds up the process of wrangling, cleaning, visualizing, manipulating, understanding, and exporting data from Pandas DataFrames. Stack-DS is not intended to be a replacement for Python. The application allows for manipulation and prediction, but only within the reigns of what is plausible, and ideal for the everyday user.
## Introduction
Stack-DS is an expansive-soon-to-be category of apps that bring machine learning and data into the hands of the user. The purpose of Stack is to make predictive assumptions based on what is seen in front of them. The Stack-DS Library will include several applications, currently in development are the following Stack-DS Applications:
zIpy - An IDE capable of editing a multitude of filetypes, and capable of editing ML generated by StackDS
Dashlee - A development environment for HTML Plot.ly dash designed to be used with data opened from Stack-DS
More to come - After Development ensues, eventually, more features will be added to Stack.
### Installation
Version 0.1.0 of Stack-DS will be released for MacOS, Linux, and Windows. However, The unstable releases between full releases ,(i.e. 0.0.5), will be available as source.
#### Stack-DS Dependencies
IPython (clear_output, Image, display)
GTK (Gtk, GdkPixbuf, Gdk)
Numpy
Pandas
imgkit
#### Fix Dependency issues
##### ipython
(sudo) pip install ipython
##### pandas
(sudo) pip install pandas
##### numpy
(sudo) pip install numpy
##### gtk
(sudo) pip install gtk
##### imgkit
sudo apt-get install wkhtmltopdf
## Install StackDS
Snap Install not yet available, unfortunately,
open up source directory with cd ~/
run:
./configure && make && sudo make install
Now:
python stackds.py
## Documentation
Documentation is available on the GitHub Wiki page.
# Changelog
**Version 0.0.3_____________** \
Added Preferences Base \
Added Module menu(Not Visible) \
Added DF - Replace, Drop \
Version 0.0.2_____________
Enabled Debug by Default for Alpha 0.0.2,
Added df refresh function,
Added DataFrame Filemenu,
Added Image Renderer, and CSV export,
Added global CSS,
Added Notebook ID updater,
Version 0.0.1_____________
___Init___
