'''
MIT License

Copyright (c) 2022 fham1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import numpy as np

from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from math import floor

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		
		# default values, change if you hate the gui!
		self.fname = 'stp1.stp'
		self.bit_depth = 128
		self.sample_size = 1024
		self.naqs = 0
		self.ngroups = 0
		self.aqlow_val = 0
		self.aqup_val = 100
		self.group_val = 0
		self.upper_load_aq = 100
		self.lower_load_aq = 0

		self.setWindowTitle("SignalTap Acquisition Viewer")

		####	LOAD BOX	#####
		self.loadlabel = QLabel()
		self.loadlabel.setText("Open only an STP file")
		self.loadfilebutton = QPushButton()
		self.loadfilebutton.clicked.connect(self.openfile)
		self.loadfilebutton.setText("Open .stp")

		#### AQ LOADER BOX #####
		self.num_aqs_label0 = QLabel()
		self.num_aqs_label0.setText("Num aqs found:")
		self.num_aqs_label1 = QLabel()
		self.num_aqs_label1.setText("0")	
  
		self.lower_load_label = QLabel()
		self.lower_load_label.setText("Lower aq to load:")
		self.lower_load_spin = QSpinBox()
		self.lower_load_spin.setMinimum(0)
		self.lower_load_spin.setMaximum(1000000)
		self.lower_load_spin.valueChanged.connect(self.lower_load_change)
		self.lower_load_spin.setValue(0)
  
		self.upper_load_label = QLabel()
		self.upper_load_label.setText("Upper aq to load:")
		self.upper_load_spin = QSpinBox()
		self.upper_load_spin.setMinimum(0)
		self.upper_load_spin.setMaximum(1000000)
		self.upper_load_spin.valueChanged.connect(self.upper_load_change)
		self.upper_load_spin.setValue(0)
   
		####	PARAMS BOX	#####
		self.samplesize_label = QLabel()
		self.samplesize_label.setText("Sample Size:")

		self.samplesize_spin = QSpinBox()
		self.samplesize_spin.setMinimum(0)
		self.samplesize_spin.setMaximum(1000000)
		self.samplesize_spin.valueChanged.connect(self.sample_change)
		self.samplesize_spin.setValue(self.sample_size)

		self.bitdepth_label = QLabel()
		self.bitdepth_label.setText("Bit Depth:")

		self.bitdepth_spin = QSpinBox()
		self.bitdepth_spin.setMinimum(0)
		self.bitdepth_spin.setMaximum(1000000)
		self.bitdepth_spin.valueChanged.connect(self.bitdepth_change)
		self.bitdepth_spin.setValue(self.bit_depth)
  		
		####	PROCESS BOX	#####
		self.process_btn = QPushButton()
		self.process_btn.setText("Process")
		self.process_btn.clicked.connect(self.process)

		self.progress_bar = QProgressBar()

		####	SCRUB BOX #####
		self.num_groups_label0 = QLabel()
		self.num_groups_label0.setText("Groups found:")
		self.num_groups_label1 = QLabel()
		self.num_groups_label1.setText(str(0))
  
		self.group_label = QLabel()
		self.group_label.setText("Group")

		self.group_spin = QSpinBox()
		self.group_spin.setMinimum(0)
		self.group_spin.setMaximum(self.ngroups)
		self.group_spin.valueChanged.connect(self.group_change)
		self.group_spin.setValue(self.group_val)

		self.lowaq_label = QLabel()
		self.lowaq_label.setText("Lower aq")

		self.lowaq_spin = QSpinBox()
		self.lowaq_spin.setMinimum(0)
		self.lowaq_spin.valueChanged.connect(self.aqlow_change)
		self.lowaq_spin.setMaximum(1000000)
		self.lowaq_spin.setValue(self.aqlow_val)

		self.upaq_label = QLabel()
		self.upaq_label.setText("Upper aq")
		
		self.upaq_spin = QSpinBox()
		self.upaq_spin.setMinimum(0)
		self.upaq_spin.setMaximum(1000000)
		self.upaq_spin.valueChanged.connect(self.aqup_change)
		self.upaq_spin.setValue(self.aqup_val)
		
		####	PLOT BOX	#####
		self.playplot_btn = QPushButton()
		self.playplot_btn.setText("Play selection")
		self.playplot_btn.clicked.connect(self.play_plot)

		self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))

		self._dynamic_ax = self.dynamic_canvas.figure.subplots()
		self.t = np.linspace(0, self.sample_size, self.sample_size)
		self._line, = self._dynamic_ax.plot(self.t, self.t)
		self.ind=0		

		####	EXPORT BOX	#####
		self.export_btn = QPushButton()
		self.export_btn.setText("Export to CSV")
		self.export_btn.clicked.connect(self.export_files)

		self.exit_btn = QPushButton()
		self.exit_btn.setText("Exit")
		self.exit_btn.clicked.connect(self.exit)

		###### LAYOUTS ######
		layout_export = QHBoxLayout()
		layout_plot_fig = QVBoxLayout()
		layout_plot = QHBoxLayout()
		layout_scrub = QHBoxLayout()
		layout_process = QHBoxLayout()
		layout_aqloader = QHBoxLayout()
		layout_params = QHBoxLayout()
		layout_load = QHBoxLayout()
		layout_overall = QVBoxLayout()

	
		layout_load.addWidget(self.loadlabel)
		layout_load.addWidget(self.loadfilebutton)

		layout_params.addWidget(self.samplesize_label)
		layout_params.addWidget(self.samplesize_spin)

		layout_params.addWidget(self.bitdepth_label)
		layout_params.addWidget(self.bitdepth_spin)
  
		layout_aqloader.addWidget(self.num_groups_label0)
		layout_aqloader.addWidget(self.num_groups_label1)
		layout_aqloader.addWidget(self.num_aqs_label0)
		layout_aqloader.addWidget(self.num_aqs_label1)
		layout_aqloader.addWidget(self.lower_load_label)
		layout_aqloader.addWidget(self.lower_load_spin)
		layout_aqloader.addWidget(self.upper_load_label)
		layout_aqloader.addWidget(self.upper_load_spin)

		layout_process.addWidget(self.process_btn)
		layout_process.addWidget(self.progress_bar)

		layout_plot.addWidget(self.playplot_btn)
		layout_plot.addLayout(layout_plot_fig)

		layout_plot_fig.addWidget(self.dynamic_canvas)
		layout_plot_fig.addWidget(NavigationToolbar(self.dynamic_canvas, self))		
  
		layout_scrub.addWidget(self.group_label)
		layout_scrub.addWidget(self.group_spin)

		layout_scrub.addWidget(self.lowaq_label)
		layout_scrub.addWidget(self.lowaq_spin)
		layout_scrub.addWidget(self.upaq_label)
		layout_scrub.addWidget(self.upaq_spin)

		layout_export.addWidget(self.export_btn)
		layout_export.addWidget(self.exit_btn)

		layout_overall.addLayout(layout_load)
		layout_overall.addLayout(layout_params)
		layout_overall.addLayout(layout_aqloader)	
		layout_overall.addLayout(layout_process)
		layout_overall.addLayout(layout_scrub)
		layout_overall.addLayout(layout_plot)
		layout_overall.addLayout(layout_export)
		
		container = QWidget()
		container.setLayout(layout_overall)

		self.setCentralWidget(container)


#### METHODS ####
	def openfile(self,s):
		self.fname, _ = QFileDialog.getOpenFileName(self, "Open File","","SignalTap Files (*.stp)")
  		# open the file and read all lines into text
		# TODO: probably faster with mmap
		if self.fname:
			with open(self.fname, mode="r") as f:
				self.text = f.readlines()
			f.close
		else: return
  
		# lines which state what the groups are in sigtap file
		match = [s for s in self.text if "<node is_selected" in s]
		self.ngroups = len(match)

		# instantiation x3
		self.group, self.low_vals, self.hih_vals = (["" for x in range(self.ngroups)] for i in range(3))

		# find the ranges of the groups and split the ranges into pairs
		for x in range(self.ngroups):
			self.group[x] = match[x].split("acq_data_in[",1)[1].split("]\"")[0]
			self.low_vals[x] = self.group[x].split("..",1)[0]
			self.hih_vals[x] = self.group[x].split("..",1)[1]
		del match, self.group

		if not self.low_vals:
			print("WARNING: No groups detected")
		
		# find all lines that have data
		self.tap_lines = [x for x in self.text if "<data name=" in x]
		del self.text
		if not self.tap_lines:
			print("WARNING: No data detected")

		self.naqs = len(self.tap_lines)
		self.orig_naqs = self.naqs
	
		self.num_aqs_label1.setText(str(self.orig_naqs))
  
		self.num_groups_label1.setText(str(self.ngroups))
		self.group_spin.setMaximum(self.ngroups-1)

		print("Open successful!")
  
	def lower_load_change(self, i):
		self.lower_load_aq = i
	def upper_load_change(self, i):
		self.upper_load_aq = i
	def group_change(self, i):
		self.group_val = i
		if 'self.ngroups' in globals():
			if self.group_val>self.ngroups:
				print("WARNING: Group selection", self.group_val , "out of range of groups detected ", self.ngroups)
	def bitdepth_change(self, i):
		self.bit_depth = i
	def sample_change(self,i):
		self.sample_size = i
	def aqup_change(self, i):
		self.aqup_val = i
	def aqlow_change(self, i):
		self.aqlow_val = i

	def _update_canvas(self):
		self._line.set_data(self.t, self.all_aqs[self.ind][self.group_val][:])
		self._dynamic_ax.relim()
		self._dynamic_ax.autoscale_view()
		self._line.figure.canvas.draw()
		
		self.ind = self.ind+1
		if(self.ind >= self.aqup_val):
			self._timer.stop()
			self.ind = 0

	def play_plot(self):
		print("plot!")
		self.ind = self.aqlow_val
		self._timer = self.dynamic_canvas.new_timer(50)
		self._timer.add_callback(self._update_canvas)
		self._timer.start()

	def export_files(self):
		export_filename, _ = QFileDialog.getSaveFileName(self, "Save current group", ".", "CSV (*.csv)")
		if export_filename:
			with open(export_filename,'w') as f:
				np.savetxt(f,self.all_aqs[:,self.group_val,:],delimiter=",")
			f.close()
		else: return

	def exit(self):
		exit()
  
	def process(self):
		print("process!")
		self.process_file()

	def process_file(self):
		bit_depth = self.bit_depth
		sample_size = self.sample_size
		aqstart = self.lower_load_aq
		aqstop = self.upper_load_aq

		if self.group_val>self.ngroups:
			print("WARNING: Group selection", self.group_val , "out of range of groups detected ", self.ngroups)

		if aqstop > self.orig_naqs:
			print("ERROR: Only found ", self.naqs, " acquisitions!")
			return
		else:
			self.naqs = aqstop - aqstart
			if self.naqs < 1 :
				print("ERROR: Can't have negative aqs!")
				return
		# extract all data to tap_aqs
		tap_aqs = ["" for x in range(self.naqs)] 
		for x in range(aqstart,aqstop):
			tap_aqs[x-aqstart] = self.tap_lines[x].split(">",1)[1].split("</data>")[0]

		# convert from lists of strings to numpy array
		arr = np.asarray(tap_aqs,dtype=np.string_)

		del tap_aqs

		# all_aqs is everything
		all_aqs = np.ndarray((self.naqs,self.ngroups,sample_size))

		# Get groups by indexing bit_slice with previously extracted group values
		# Reverse bits, convert to int, convert to float
		breakout=0
		for ind_aq in range(self.naqs):
			for ind_slice in range(sample_size):
				bit_slice = arr[ind_aq][bit_depth*ind_slice:bit_depth*(ind_slice+1)]

				for ind_group in range(self.ngroups):
					# get the current bit slice

					low_ind = int(self.low_vals[ind_group])
					high_ind = int(self.hih_vals[ind_group])
					binary_value = bit_slice[low_ind:high_ind+1]
					binary_value = binary_value[::-1]

					try:
						asnum = int(binary_value[1:], 2)
					except:
						breakout=1
						break
					
					# twos complement conversion
					if binary_value[0] == 49: # individual bytes are in ascii
						asnum ^= 2**(high_ind-low_ind)-1
						asnum += 1
						asnum = -asnum

					all_aqs[ind_aq][ind_group][ind_slice]=asnum
				if breakout:
					breakout =0
					break
			self.progress_bar.setValue(floor(100*ind_aq/self.naqs))
		self.progress_bar.setValue(100)
		self.all_aqs = all_aqs

		del arr

app = QApplication(sys.argv)
window = MainWindow()
window.setFixedSize(800,500)
window.show()
window.activateWindow()
app.exec_()
