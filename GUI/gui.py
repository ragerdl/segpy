#!/usr/bin/python2.4
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Small test to demonstrate glade.XML.signal_autoconnect on an instance
#

import pygtk
pygtk.require('2.0')


import matplotlib 
matplotlib.use('GTK') 
from matplotlib.figure import Figure 
from matplotlib.axes import Subplot 
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar 
from matplotlib.numerix import arange, sin, pi 

import Numeric as numpy

import gtk, gtk.glade

import segypy

class SimpleTest:
	def __init__(self):
		# xml = gtk.glade.XML('test2.glade')
#		self.xml = gtk.glade.XML('test/test.glade')
		self.xml = gtk.glade.XML('segygui/segygui.glade')
		self.xml.signal_autoconnect(self)
	
	def on_new1_activate(self, button):
		print 'foo'
		self.segy = segypy.readSegy('../data_4byteINT.segy')
		print 'foo2'
		self.figure = Figure(figsize=(6,4), dpi=72) 
		self.axis = self.figure.add_subplot(111) 
		self.axis.set_xlabel('Trace Header') 
		self.axis.set_ylabel('Time [s]') 
		self.axis.set_title('An Empty Graph') 
		self.axis.grid(True) 
		self.axis.imshow(self.segy[0])
		self.canvas = FigureCanvasGTK(self.figure) # a gtk.DrawingArea 
		self.canvas.show() 
#		self.graphview = self.wTree.get_widget("vbox1") 
#		self.graphview.pack_start(self.canvas, True, True)
		self.graphview = self.xml.get_widget("vbox4") 
		self.graphview.pack_start(self.canvas, True, True)
		print 'PLOTTED'		

		# create a TreeStore with one string column to use as the model
		
		self.liststore = gtk.ListStore(int,str)
		self.treestore = gtk.TreeStore(str)
		# we'll add some data now - 4 rows with 3 child rows each
		for parent in range(4):
			piter = self.treestore.append(None, ['parent %i' % parent])
			for child in range(3):
				self.treestore.append(piter, ['child %i of parent %i' %
					(child, parent)])



		self.treeview = self.xml.get_widget("treeview1")

		self.treeview.set_model(self.liststore)


		renderer1= gtk.CellRendererText()

		self.tvcolumn1 = gtk.TreeViewColumn('Name', renderer1, text=0)
		self.treeview.append_column(self.tvcolumn1)
		self.tvcolumn2 = gtk.TreeViewColumn('Value')
		self.treeview.append_column(self.tvcolumn2)


		# create a CellRendererText to render the data
		self.cell = gtk.CellRendererText()
		# add the cell to the tvcolumn and allow it to expand
		self.tvcolumn1.pack_start(self.cell, True)
		# set the cell "text" attribute to column 0 - retrieve text
		# from that column in treestore
		self.tvcolumn1.add_attribute(self.cell, 'text', 0)
		# make it searchable
		self.treeview.set_search_column(0)
		self.treeview.show_all()


	def on_open1_activate(self, button):
		dialog = gtk.FileChooserDialog("Open..",
			None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		
		dialog.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("SEG-Y files")
		filter.add_pattern("*.segy")
		filter.add_pattern("*.sgy")
		filter.add_pattern("*.seg-y")
		dialog.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("SU files")
		filter.add_pattern("*.su")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			print dialog.get_filename(), 'selected'
			filename  = dialog.get_filename()
			dialog.destroy()
			self.segy = segypy.readSegy(filename)
		
			self.figure = Figure(figsize=(6,4), dpi=72) 
			self.axis = self.figure.add_subplot(111) 
			self.axis.set_xlabel('Yepper') 
			self.axis.set_ylabel('Flabber') 
			self.axis.set_title('An Empty Graph') 
			self.axis.grid(True) 
			self.axis.imshow(self.segy[0])
			self.canvas = FigureCanvasGTK(self.figure) # a gtk.DrawingArea 
			self.canvas.show() 
			self.graphview = self.xml.get_widget_widget("vbox1") 
			print self.graphview
			self.graphview.pack_start(self.canvas, True, True)
#			self.graphview = self.xml.get_widget("hbox2") 
#			self.graphview.pack_start(self.canvas, True, True)
			print 'PLOTTED'		
		
		
		
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
			dialog.destroy()

test = SimpleTest()

gtk.main()