"""A framework for developing hybrid CLI/GUI programs."""

################################################################################
# Hydra Framework
#
# Copyright © 2017 Ryan Weathers, All Rights Reserved.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Version: 0.1.2-alpha (2017-12-24)
################################################################################

import csv
import configparser
import decimal
import glob
import os
import sys
import time
import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class BaseConfiguration:
	"""Base class for loading and validating configuration files.
	
	Attributes:
		filename - Path to a configuration file.
		conf - Dictionary storing the option/value pairs. 
	"""
	
	def __init__(self, filename):
		"""Initalize the object.
		
		Paramaters:
			filename - Path to a configuration file.
		"""
		self.filename = filename
		self.conf = {}
		
		if self.filename is not None:
			self.load()
			self.validate()
	
	def load(self):
		"""Load the configuration file into self.conf."""
		try:
			open(self.filename, "r").close()
		except Exception as e:
			raise Exception(self.filename + " not found.")
		
		cp = configparser.ConfigParser()
		cp.read(self.filename)
		for s in cp.sections():
			for o in cp.options(s):
				self.conf[o] = cp.get(s, o)
	
	def validate(self):
		"""Raise an exception if any configuration values are invalid."""
		pass

class BaseCLI:
	"""Base class for defining the command line interface.
	
	Attributes:
		prog - Program constants dictionary.
		conf - Configuration dictionary.
		arguments - Command line arguments (sys.argv).
		last_update - Unix timestamp of last user progress update.
		inputs - User input dictionary.
	"""
	
	def __init__(self, prog, conf, argv):
		"""Initialize the object.
		
		Paramaters:
			prog - Program constants dictionary.
			conf - Configuration dictionary.
			argv - Command line arguments (sys.argv).
		"""
		self.prog = prog
		self.conf = conf
		self.arguments = []
		self.last_update = 0
		
		self.define_arguments()
		self.inputs = self.parse_arguments(argv, conf)
		
		self.action()
	
	def define_arguments(self):
		"""Define the command line arguments."""
		pass
	
	def parse_arguments(self, argv, defaults):
		"""Parse the command line arguments and return them in a dictionary.
			
		Paramaters:
			argv - Command line arguments (sys.argv).
		"""
		flags = self.conf
		map = {}
		count = 0
		
		# Initialize flags
		boolean = []
		value = []
		multiple = []
		for (long, short, desc, type) in self.arguments:
			if short != "": map[short] = long
			if type == "boolean":
				flags[long] = False
				boolean.append(long)
			elif type == "value":
				flags[long] = defaults.get(long, "")
				value.append(long)
			elif type == "multiple":
				flags[long] = [] if defaults.get(long, "") == "" else [defaults.get(long, "")]
				multiple.append(long)
			else:
				raise Exception("Invalid argument type: " + type)
		
		# Convert all flags to their long version
		long_args = []
		for val in argv:
			if val.startswith("--"):
				# Cut off "--"
				val = val[2:]
				
				# `--flag=value` or `--flag value`?
				extra = None
				if "=" in val:
					tmp = val.split("=")
					val = tmp[0]
					extra = tmp[1]
				
				# Is this a valid flag?
				if val in flags:
					long_args.append("--" + val)
					if extra is not None: long_args.append(extra)
					count += 1
				else:
					raise Exception("Unknown argument: " + val)
			elif val.startswith("-"):
				# Split and convert short flags
				i = 1
				while i < len(val):
					f = val[i:i+1]
					
					# Is this a valid flag?
					if f in map:
						long_args.append("--" + map[f])
						count += 1
					else:
						raise Exception("Unknown argument: " + f)
						
					i+=1
			else:
				# Copy over any remaining values
				long_args.append(val)
		
		# Process user input
		expecting_value = ""
		for val in long_args:
			# Process flags and inputs
			if val.startswith("--"):
				# Cut off leading "--"
				val = val[2:]
				
				# Boolean flag or value flag?
				if val in boolean:
					flags[val] = True
					expecting_value = ""
				else:
					# The next value is the value for this flag
					expecting_value = val
					
					# Clear the default for mutliple types
					if val in multiple: flags[expecting_value] = []
			elif expecting_value != "":
				# Save the input value
				if expecting_value in value:
					flags[expecting_value] = val
				elif expecting_value in multiple:
					flags[expecting_value].append(val)
				
		flags["_count"] = count
		
		return flags
	
	def print_help(self):
		"""Print the help information to standard out."""
		width = 40

		print("")
		print(self.prog["name"], self.prog["version"])
		print(self.prog["purpose"])
		
		usage = self.prog["usage"].strip().split("\n")
		prefix = "Usage:"
		for u in usage:
			print(prefix, u.strip())
			prefix = "      "
		
		for (long, short, desc, type) in self.arguments:
			desc = desc.replace("\n", "\n " + " " * width)
			if type == "boolean":
				if short != "": short = "-" + short + ", "
				print(("    " + short + "--" + long).ljust(width)[0:width] + " " + desc)
			elif type == "value":
				if short != "": short = "-" + short + " VALUE, "
				print(("    " + short + "--" + long + " VALUE").ljust(width)[0:width] + " " + desc)
			elif type == "multiple":
				if short != "": short = "-" + short + " VALUE(S), "
				print(("    " + short + "--" + long + " VALUE(S)").ljust(width)[0:width] + " " + desc)

		print("")
		
		if self.prog["config"] is not None:
			print("See " + self.prog["config"] + " for default values")
			print("")
		
		if self.prog["url"] is not None:
			print(self.prog["url"])
			print("")
	
	def print_version(self):
		"""Print the program name and version."""
		print("")
		print(self.prog["name"], self.prog["version"], self.prog["date"])
		print("")
	
	def print_license(self):
		"""Print the program's license information."""
		print("")
		print(self.prog["name"], self.prog["version"])
		print("")
		print(self.prog["copyright"])
		print("")
		if self.prog["license"] is not None:
			print(self.prog["license"])
			print("")
	
	def output_progress(self, text, started=None, processed=None, total=None):
		"""Print progress information to standard out.
		
		Paramaters:
			text - Progress text.
			started - Unix timestamp of when the program started.
			processed - Counter of processed items.
			total - Total number of items to process.
		"""
		if not self.inputs["quiet"]:
			p = progress(self.last_update, text, started, processed, total)
			if p is not None:
				self.last_update = p[0]
				print(p[1].ljust(80)[0:80-1] + "\r", end="", flush=True)
	
	def get_action(self, inputs):
		"""Return the BaseAction subclass to use.
		
		Paramaters:
			inputs - User input dictionary.
		"""
		pass
	
	def action(self):
		"""Validate the user's input and perform the action."""
		try:
			if (self.inputs["help"]) or ((self.inputs["_count"] == 0) and ((sys.stdin is not None) and sys.stdin.isatty())):
				self.print_help()
			elif self.inputs["version"]:
				self.print_version()
			elif self.inputs["license"]:
				self.print_license()
			else:
				if not self.inputs["quiet"]: print("")
				
				action = self.get_action(self.inputs)(self.inputs, self.output_progress)
				action.standardize()
				action.validate()
				message = action.action()
				
				if not self.inputs["quiet"]:
					self.output_progress("")
					print(message)
					print("")
		except Exception as e:
			print(("ERROR: " + str(e)).ljust(80))
			if self.inputs.get("verbose", False):
				import traceback
				print(traceback.format_exc())
			
			error_output(e, self.prog["error"])

class BaseGUI(tk.Frame):
	"""Base class for defining the graphical user interface.
	
	Attributes:
		prog - Program constants dictionary.
		conf - Configuration dictionary.
		menu - List of tuples defining the menu.
		help - List of dictionaries defining the help.
		widgets - Dictionary of the widget objects.
		row - The next row to use in the grid layout.
		padding - Padding to use for all widgets.
		text_width - Width of text boxes.
		last_update - Unix timestamp of last user progress update.
	"""
	
	def __init__(self, master, prog, conf):
		"""Initialize the object.
		
		Paramaters:
			master - Tk Root object.
			prog - Program constants dictionary.
			conf - Configuration dictionary.
		"""
		tk.Frame.__init__(self, master)
		self.grid(padx=10, pady=10)
		
		self.prog = prog
		self.conf = conf
		self.menu = []
		self.help = []
		self.widgets = {}
		self.row = 1
		self.padding = 4
		self.text_width = 40
		self.last_update = 0
		
		self.define_menu()
		self.create_menu()
		
		self.create_widgets()
		self.create_title(self.prog["name"])
		self.create_progress()
		self.set_defaults()
		
		self.start()
	
	def define_menu(self):
		"""Define the menu."""
		pass
	
	def create_menu(self):
		"""Create the menu and add it to the root window."""
		if len(self.menu) > 0:
			menubar = tk.Menu(self)
			for label, items in self.menu:
				menu = tk.Menu(menubar, tearoff=0)
				for label2, command2 in items: menu.add_command(label=label2, command=command2)
				menubar.add_cascade(label=label, menu=menu)
			self.master.config(menu=menubar)
	
	def open_config(self):
		"""Open the configuration file."""
		webbrowser.open(self.prog["config"])

	def define_help(self, help):
		"""Define the help information."""
		pass
	
	def show_help(self):
		"""Show the help window."""
		
		window = tk.Toplevel(self)
		window.wm_title("Help")
		
		help = tk.Text(window, height=25, width=75, borderwidth=0, highlightthickness=0, pady=10, padx=10, wrap=tk.WORD)
		scroll = tk.Scrollbar(window, command=help.yview)
		help.configure(yscrollcommand=scroll.set)
		
		help.tag_configure("title" , font=("Arial", 18, "bold"), justify="center")
		help.tag_configure("normal", font=("Arial", 10))
		help.tag_configure("bold"  , font=("Arial", 12, "bold"))
		help.tag_configure("italic", font=("Arial", 10, "italic"))
		
		help.insert(tk.END, self.prog["name"] + " Help\n", "title")
		help.insert(tk.END, "\n" + self.prog["purpose"] + "\n\n", "normal")
		
		self.define_help(help)
		
		help.config(state=tk.DISABLED)
		
		help.pack(side=tk.LEFT)
		scroll.pack(side=tk.RIGHT, fill=tk.Y)
		
		self.set_icon(window)
		self.center(window)
		
	def show_about(self):
		"""Open the about window."""
		p1=(10, 10, 10, 10)
		p2=(10, 0, 10, 10)
		p3=(10, 0, 10, 0)
		
		window = tk.Toplevel(self)
		window.wm_title("About")

		labels = []
		labels.append({"text":self.prog["name"], "padding":p1, "font":("Arial", 18, "bold")})
		labels.append({"text":"Version " + self.prog["version"], "padding":p3})
		labels.append({"text":self.prog["date"]})
		labels.append({"text":self.prog["purpose"]})
		if self.prog["url"] is not None: labels.append({"text":self.prog["url"], "foreground":"blue", "cursor":"hand2"})
		labels.append({"text":self.prog["copyright"], "font":("Arial", 10, "italic")})
		
		if self.prog["license"] is not None:
			license = self.prog["license"].split("\n\n")
			for l in license:
				l = l.replace("\n", " ")
				labels.append({"text":l, "anchor":tk.W, "font":("Arial", 10, "italic")})
		
		default = {"padding":p2, "anchor":tk.CENTER, "wraplength":500, "font":("Arial", 10)}
		for l in labels:
			d = default.copy()
			d.update(l)
			l = ttk.Label(window, **d)
			l.pack(fill="x")
			
			if d["text"][0:5] == "http:": l.bind("<Button-1>", lambda e, url=d["text"]: webbrowser.open(url))
		
		self.set_icon(window)
		self.center(window)
	
	def create_widgets(self):
		"""Create the widgets."""
		pass
	
	def set_defaults(self):
		"""Set all widgets to their default value."""
		for c in self.widgets: self.widgets[c].setval(self.widgets[c].default)
	
	def create_title(self, text):
		"""Add a title label to the root window.
		
		Paramaters:
			text - Title text.
		"""
		label = ttk.Label(self, text=text, padding=(0, 0, 0, 10), font=("Arial", 18, "bold"))
		label.grid(row=0, column=0, columnspan=self.grid_size()[0])
	
	def create_entry(self, parent, name, text, default="", largs={}, wargs={}, lgrid={}, wgrid={}):
		"""Add an entry to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the label.
			default - Default value of the widget.
			largs - Constructor arguments for the label.
			wargs - Constructor arguments for the widget.
			lgrid - grid() arguments for the label.
			wgrid - grid() arguments for the widget.
		"""
		label = ttk.Label(parent, text=text, **largs)
		label.grid(**setdefaults(lgrid, {"row":parent.row, "column":0, "padx":self.padding, "pady":self.padding, "sticky":"W"}))
		
		value = tk.StringVar()		
		entry = ttk.Entry(parent, textvariable=value, **setdefaults(wargs, {"width":self.text_width}))
		entry.label = label
		entry.value = value
		entry.default = default
		entry.getval = value.get
		entry.setval = value.set
		entry.grid(**setdefaults(wgrid, {"row":parent.row, "column":1, "padx":self.padding, "pady":self.padding, "sticky":"W"}))
		
		self.widgets[name] = entry
		
		parent.row += 1
	
	def create_browse(self, parent, name, text, command, initialdir=None, initialfile=None, filetypes=[], default="", largs={}, wargs={}, bargs={}, lgrid={}, wgrid={}, bgrid={}):
		"""Add a file browser to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the label.
			command - Function callback (one of self.get_inputs, self.get_input, self.get_output or self.get_folder)
			initialdir - Starting directory for the file dialog.
			initialfile - Starting filename for the file dialog.
			filetypes - List of allowed file types.
			default - Default value of the widget.
			largs - Constructor arguments for the label.
			wargs - Constructor arguments for the widget.
			bargs - Constructor arguments for the browse button.
			lgrid - grid() arguments for the label.
			wgrid - grid() arguments for the widget.
			bgrid - grid() arguments for the browse button.
		"""
		self.create_entry(parent, name, text, default=default, largs=largs, wargs=wargs, lgrid=lgrid, wgrid=wgrid)
		
		if (initialdir is None) or (initialdir == ""): initialdir = os.path.expanduser("~")
		
		text = "Browse…"
		value = tk.StringVar()
		value.set(text)
		button = ttk.Button(parent, textvariable=value, command=lambda: command(self.widgets[name], initialdir, initialfile, filetypes), **bargs)
		button.value = value
		button.default = text
		button.getval = value.get
		button.setval = value.set
		button.grid(**setdefaults(bgrid, {"row":parent.row-1, "column":2, "sticky":"W"}))
		
		self.widgets[name + "-browse"] = button
	
	def create_combobox(self, parent, name, text, values, default=None, largs={}, wargs={}, lgrid={}, wgrid={}):
		"""Add a combobox to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the label.
			values - List of values to use.
			default - Default value of the widget.
			largs - Constructor arguments for the label.
			wargs - Constructor arguments for the widget.
			lgrid - grid() arguments for the label.
			wgrid - grid() arguments for the widget.
		"""
		label = ttk.Label(parent, text=text, **largs)
		label.grid(**setdefaults(lgrid, {"row":parent.row, "column":0, "padx":self.padding, "pady":self.padding, "sticky":"W"}))
		
		value = tk.StringVar()
		value.set(values[0])
		combobox = ttk.Combobox(parent, textvariable=value, values=values, state="readonly", **wargs)
		combobox.label = value
		combobox.value = value
		combobox.default = values[0] if default == None else default
		combobox.getval = value.get
		combobox.setval = value.set
		combobox.grid(**setdefaults(wgrid, {"row":parent.row, "column":1, "padx":self.padding, "pady":self.padding, "sticky":"EW"}))
		
		self.widgets[name] = combobox
		
		parent.row += 1
		
	def create_listbox(self, parent, name, text, values, selectmode=tk.EXTENDED, largs={}, wargs={}, lgrid={}, wgrid={}):
		"""Add a listbox to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the label.
			values - List of values to use.
			selectmode - Listbox selectmode argument.
			largs - Constructor arguments for the label.
			wargs - Constructor arguments for the widget.
			lgrid - grid() arguments for the label.
			wgrid - grid() arguments for the widget.
		"""
		label = ttk.Label(parent, text=text, **largs)
		label.grid(**setdefaults(lgrid, {"row":parent.row, "column":0, "padx":self.padding, "pady":self.padding, "sticky":"NW"}))
		
		def getsel():
			nonlocal listbox
			l = []
			t = eval(listbox.value.get())
			for i in listbox.curselection(): l.append(t[i])
			return l
			
		def setval(val):
			nonlocal listbox
			listbox.value.set("")
			listbox.value.set(val)
		
		value = tk.StringVar()
		value.set(values)
		listbox = tk.Listbox(parent, listvariable=value, selectmode=selectmode, exportselection=0, **wargs)
		listbox.label = label
		listbox.value = value
		listbox.default = values	
		listbox.getval = getsel
		listbox.setval = setval
		listbox.grid(**setdefaults(wgrid, {"row":parent.row, "column":1, "padx":self.padding, "pady":self.padding, "sticky":"EW"}))
		
		self.widgets[name] = listbox
		
		parent.row += 1
		
	def create_text(self, parent, name, text, height=10, wrap="none", default="", largs={}, wargs={}, lgrid={}, wgrid={}):
		"""Add a text to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the label.
			height - Height in number of lines.
			wrap - Text wrap argument.
			default - Default value of the widget.
			largs - Constructor arguments for the label.
			wargs - Constructor arguments for the widget.
			lgrid - grid() arguments for the label.
			wgrid - grid() arguments for the widget.
		"""
		label = ttk.Label(parent, text=text, **largs)
		label.grid(**setdefaults(lgrid, {"row":parent.row, "column":0, "padx":self.padding, "pady":self.padding, "sticky":"NW"}))
		
		def getval():
			nonlocal text
			return text.get(1.0, tk.END)
			
		def setval(val):
			nonlocal text
			text.delete(1.0, tk.END)
			text.insert(tk.INSERT, val)
		
		wrapper = tk.Frame(parent, borderwidth=1, relief="sunken")
		
		text = tk.Text(wrapper, height=height, width=1, wrap=wrap, borderwidth=0, **wargs)
		text.label = label
		text.default = default
		text.getval = getval
		text.setval = setval
		text.grid(row=0, column=0, sticky="NSEW")
		
		scrollV = tk.Scrollbar(wrapper, orient="vertical", command=text.yview)
		scrollV.grid(row=0, column=1, sticky="NS")
		scrollH = tk.Scrollbar(wrapper, orient="horizontal", command=text.xview)
		scrollH.grid(row=1, column=0, sticky="EW")
		text.configure(yscrollcommand=scrollV.set, xscrollcommand=scrollH.set)
		
		wrapper.grid(**setdefaults(wgrid, {"row":parent.row, "column":1, "padx":self.padding, "pady":self.padding, "sticky":"NSEW"}))
		wrapper.grid_rowconfigure(0, weight=1)
		wrapper.grid_columnconfigure(0, weight=1)
		
		self.widgets[name] = text
		
		parent.row += 1
	
	def create_checkbox(self, parent, name, text, default=0, wargs={}, wgrid={}):
		"""Add a checkbox to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the label.
			default - Default value of the widget.
			wargs - Constructor arguments for the widget.
			wgrid - grid() arguments for the widget.
		"""
		value = tk.IntVar()
		checkbox = ttk.Checkbutton(parent, variable=value, text=text, **wargs)
		checkbox.value = value
		checkbox.default = default
		checkbox.getval = value.get
		checkbox.setval = value.set
		checkbox.grid(**setdefaults(wgrid, {"row":parent.row, "column":1, "padx":self.padding, "pady":self.padding, "sticky":"W"}))
		
		self.widgets[name] = checkbox
		
		parent.row += 1
	
	def create_button(self, parent, name, text, command, bargs={}, bgrid={}):
		"""Add a button to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			text - Text for the widget.
			command - Function to call when clicked.
			bargs - Constructor arguments for the button.
			bgrid - grid() arguments for the button.
		"""
		value = tk.StringVar()
		value.set(text)
		button = ttk.Button(parent, textvariable=value, command=command, **bargs)
		button.value = value
		button.default = text
		button.getval = value.get
		button.setval = value.set
		button.grid(**setdefaults(bgrid, {"row":parent.row, "column":0, "columnspan":3, "pady":(10, 0)}))
		self.widgets[name] = button
		
		parent.row += 1
	
	def create_notebook(self, parent, name, nargs={}):
		"""Add a notebook to the given parent.
		
		Paramaters:
			parent - A Tk frame.
			name - Name of the widget.
			nargs - Constructor arguments for the notebook.
		"""
		value = tk.StringVar()
		value.set("")
		notebook = ttk.Notebook(parent, **nargs)
		notebook.grid(row=parent.row, column=0, columnspan=3, sticky="EW")
		notebook.value = value
		notebook.default = ""
		notebook.getval = value.get
		notebook.setval = value.set
		notebook.bind("<<NotebookTabChanged>>", self.notebook_tab_changed)
		self.widgets[name] = notebook
		
		parent.row += 1
		
		return notebook
		
	def notebook_tab_changed(self, event):
		"""Tab changed event callback for the notebook.
		
		Paramaters:
			event - Tk event object.
		"""
		tab = event.widget.tab(event.widget.index("current"),"text")
		event.widget.defaut = tab
		event.widget.setval(tab)
	
	def create_tab(self, parent, text):
		"""Add a tab to the given notebook.
		
		Paramaters:
			parent - A notebook.
			text - Text to display on tab.
		"""
		tab = ttk.Frame(padding=10)
		tab.grid()
		tab.columnconfigure(0, weight=1)
		tab.row = 0
		
		parent.add(tab, text=text)
		
		return tab
	
	def create_progress(self):
		"""Add a progress label to the root window."""
		value = tk.StringVar()
		progress = ttk.Label(self, textvariable=value, padding=(0, 10, 0, 0))
		progress.value = value
		progress.default = ""
		progress.getval = value.get
		progress.setval = value.set
		progress.config(foreground="green")
		progress.config(font=("Arial", 10, "bold"))
		progress.grid(row=self.row, column=0, columnspan=self.grid_size()[0])
		
		self.widgets["progress"] = progress
		
		self.row += 1
	
	def enable_widgets(self):
		"""Enable all widgets."""
		for name in self.widgets:
			if not isinstance(self.widgets[name], ttk.Notebook):
				self.widgets[name].config(state = tk.NORMAL if not isinstance(self.widgets[name], ttk.Combobox) else "readonly")
		
		self.update()
	
	def disable_widgets(self):
		"""Disable all widgets."""
		for name in self.widgets:
			if not isinstance(self.widgets[name], ttk.Notebook):
				self.widgets[name].config(state = tk.DISABLED)
		
		self.update()
	
	def hide_widget(self, name):
		"""Hide the given widget.
		
		Paramaters:
			name - Name of the widget to hide.
		"""
		self.widgets[name].grid_remove()
		if hasattr(self.widgets[name], "label"): self.widgets[name].label.grid_remove()
		if name + "-browse" in self.widgets: self.widgets[name + "-browse"].grid_remove()
	
	def show_widget(self, name):
		"""Show the given widget.
		
		Paramaters:
			name - Name of the widget to hide.
		"""
		self.widgets[name].grid()
		if hasattr(self.widgets[name], "label"): self.widgets[name].label.grid()
		if name + "-browse" in self.widgets: self.widgets[name + "-browse"].grid()
	
	def get_input(self, widget, initialdir, initialfile, filetypes):
		"""Show the open file (singular) dialog.
		
		Paramaters:
			widget - Widget in which to save the user's selection.
			initialdir - Starting directory for the file dialog.
			initialfile - Starting filename for the file dialog.
			filetypes - List of allowed file types.
		"""
		if widget.value.get() != "": initialdir = os.path.dirname(widget.value.get())
		
		result = tk.filedialog.askopenfilename(initialdir=initialdir, initialfile=initialfile, filetypes=filetypes)
		if result: widget.setval(result)
		
		# Hack for windows bug - if you double-click the second click is passed to the form, this sends the event to a disabled widget causing it to have no effect
		self.disable_widgets()
		self.enable_widgets()
	
	def get_inputs(self, widget, initialdir, initialfile, filetypes):
		"""Show the open files (plural) dialog.
		
		Paramaters:
			widget - Widget in which to save the user's selection.
			initialdir - Starting directory for the file dialog.
			initialfile - Starting filename for the file dialog.
			filetypes - List of allowed file types.
		"""
		if widget.value.get() != "": initialdir = os.path.dirname(list(csv.reader([widget.value.get()]))[0][0])
				
		result = tk.filedialog.askopenfilenames(initialdir=initialdir, initialfile=initialfile, filetypes=filetypes)
		if len(result) == 1:
			result = result[0]
		else:
			result = map(lambda f: "\"" + f.replace("\"", "\\\"") + "\"", result)
			result = ",".join(result)
		widget.setval(result)
		
		# Hack for windows bug - if you double-click the second click is passed to the form, this sends the event to a disabled widget causing it to have no effect
		self.disable_widgets()
		self.enable_widgets()
	
	def get_output(self, widget, initialdir, initialfile, filetypes):
		"""Show the save file dialog.
		
		Paramaters:
			widget - Widget in which to save the user's selection.
			initialdir - Starting directory for the file dialog.
			initialfile - Starting filename for the file dialog.
			filetypes - List of allowed file types.
		"""
		if widget.value.get() != "": initialdir = os.path.dirname(widget.value.get())
		
		result = tk.filedialog.asksaveasfilename(initialdir=initialdir, initialfile=initialfile, filetypes=filetypes)
		if result: widget.setval(result)
	
	def get_folder(self, widget, initialdir, ignored1=None, ignored2=None):
		"""Show the open folder dialog.
		
		Paramaters:
			widget - Widget in which to save the user's selection.
			initialdir - Starting directory for the file dialog.
			ignored1 - Stub paramater just to be compatible with the other file dialog functions.
			ignored2 - Stub paramater just to be compatible with the other file dialog functions.
		"""
		if widget.value.get() != "": initialdir = widget.value.get()
		
		result = tk.filedialog.askdirectory(initialdir=initialdir)
		if result: widget.setval(result)
	
	def center(self, window):
		"""Center the given window.
		
		Paramaters:
			window - TK frame.
		"""
		window.attributes("-alpha", 0.0) # Prevent flashing of empty frame on Windows
		window.resizable(0,0)
		window.withdraw() # Prevent flashing of empty frame on Linux
		window.update_idletasks() 
		window.geometry("+{0}+{1}".format(int((window.winfo_screenwidth() - window.winfo_reqwidth())/2), int((window.winfo_screenheight() - window.winfo_reqheight())/4)))
		window.deiconify() # Prevent flashing of empty frame on Linux
		window.attributes("-alpha", 1.0) # Prevent flashing of empty frame on Windows
		
	def set_icon(self, window):
		"""Set the icon for the given window.
		
		Paramaters:
			window - TK frame.
		"""
		if self.prog["icon-data"] is not None:
			img = tk.PhotoImage(data=self.prog["icon-data"])
			window.tk.call("wm", "iconphoto", window._w, img)
		elif self.prog["icon-file"] is not None:
			img = tk.PhotoImage(file=self.prog["icon-file"])
			window.tk.call("wm", "iconphoto", window._w, img)
	
	def start(self):
		"""Start the GUI."""
		self.master.wm_title(self.prog["name"] + " " + self.prog["version"])
		self.set_icon(self.master)
		self.center(self.master)
		self.mainloop()
	
	def set_progress(self, text, started=None, processed=None, total=None):
		"""Set the progress text.
		
		Paramaters:
			text - Progress text.
			started - Unix timestamp of when the program started.
			processed - Counter of processed items.
			total - Total number of items to process.
		"""
		p = progress(self.last_update, text, started, processed, total)
		if p is not None:
			self.last_update = p[0]
			self.widgets["progress"].setval(p[1])
			self.update()
	
	def get_action(self, inputs):
		"""Return the BaseAction subclass to use.
		
		Paramaters:
			inputs - User input dictionary.
		"""
		pass
	
	def action(self):
		"""Validate the user's input and perform the action."""
		try:
			self.config(cursor="watch")
			self.disable_widgets()
			
			inputs = self.conf.copy()
			for name in self.widgets: inputs[name] = self.widgets[name].getval()
			
			action = self.get_action(inputs)(inputs, self.set_progress)
			action.standardize()
			action.validate()
			message = action.action()
			
			self.config(cursor="")
			tk.messagebox.showinfo("Success", message)
			self.widgets["progress"].setval("")
		except Exception as e:
			self.config(cursor="")
			self.widgets["progress"].setval("")
			tk.messagebox.showerror("ERROR", str(e))
			
			error_output(e, self.prog["error"])
		finally:
			self.config(cursor="")
			self.enable_widgets()

class BaseAction:
	"""Base class for defining actions.
	
	Attributes:
		inputs - User input dictionary.
		progress - Callback function for user progress updates.
	"""
	
	def __init__(self, inputs, progress):
		"""Initialize the object.
		
		Paramaters:
			inputs - User input dictionary.
			progress - Callback function for user progress updates.
		"""
		self.inputs = inputs
		self.progress = progress
	
	def standardize(self):
		"""Standardize the user's inputs."""
		pass
	
	def validate(self):
		"""Raise an exception if any of the user's inputs are invalid."""
		pass
	
	def action(self):
		"""Perform the task and return a message for the user."""
		return ""
	
	def expand(self, field):
		"""Convert a CSV string into a list of filenames and expand wildcard filenames.
		
		Paramaters:
			field - Field name to modify.
		"""
		if not isinstance(self.inputs[field], list): self.inputs[field] = list(csv.reader([self.inputs[field]]))[0]
		tmp = []
		for i in self.inputs[field]:
			if i == "STDIN":
				tmp.append(i)
			else:
				for g in glob.glob(i): tmp.append(g)
		self.inputs[field] = tmp
	
	def open(self, filename, mode="r", encoding="utf-8"):
		"""Return sys.stdin (for filename == "STDIN"), sys.stdout (for filename == "STDIN") or a file handle.
		
		Paramaters:
			filename - "STDIN", "STDOUT" or a filename.
			mode - File open mode.
			encoding - File encoding.
		"""
		if self.inputs.get("verbose", False): self.progress("Opening " + filename + "\n")
		
		if filename == "STDIN":
			if (sys.stdin is not None) and sys.stdin.isatty(): raise Exception("Empty STDIN")
			return sys.stdin
		elif filename == "STDOUT":
			return sys.stdout
		else:
			return open(filename, mode=mode, encoding=encoding)

def progress(last_update, text, started=None, processed=None, total=None):
	"""Return progress text with optional time elapsed and estimated time to complete.
	
	Paramaters:
		text - Progress text.
		started - Unix timestamp of when the program started.
		processed - Counter of processed items.
		total - Total number of items to process.
	"""
	now = time.time()
	ms = int(round(now * 1000))
	if ((ms - last_update) > 100) or (started is None):
		if started is not None:
			elapsed = now - started
			remaining = (0 if processed == 0 else (elapsed/processed)) * (total - processed)
			
			hh_mm_ss = lambda t: (str(int(t/3600.0)) + ":" if t >= 3600 else "") + str(int(t/60.0)%60).zfill(2) + ":" + str(int(t%60)).zfill(2)
			text += " | Time: " + hh_mm_ss(elapsed) + "/" + hh_mm_ss(remaining) + " | Progress: " + str(int((0 if total == 0 else (processed/total)) * 100.0)) + "%"
		
		return (ms, text)
	else:
		return None

def setdefaults(primary, secondary):
	"""Return a dictionary with the values of primary and secondary merged, with primary taking precedence over secondary.
	
	Paramaters:
		primary - The primary dictionary.
		secondary - The secondary dictionary.
	"""
	primary = primary.copy()
	for key in secondary: primary.setdefault(key, secondary[key])
	return primary

def error_output(ex, error_path):
	"""Write error details to a file.
	
	Paramaters:
		ex - An exception object.
		error_path - Error filename.
	"""
	import traceback
	
	if error_path is not None:
		try:
			with open(error_path, mode="w") as f: f.write(str(ex) + "\n\n" + traceback.format_exc())
		except Exception as e:
			print("ERROR: " + str(e))
			print(traceback.format_exc())

def main(prog, configuration_class, cli_class, gui_class):
	"""Run the program.
	
	Paramaters:
		prog - Program constants dictionary.
		configuration_class - A BaseConfiguration subclass.
		cli_class - A BaseCI subclass.
		gui_class - A BaseGUI subclass.
	"""
	path = os.path.dirname(sys.executable) if hasattr(sys, "frozen") else sys.path[0]
	path += os.sep
	if prog["config"]    is not None: prog["config"]    = prog["config"].format(path=path)
	if prog["error"]     is not None: prog["error"]     = prog["error"].format(path=path)
	if prog["icon-file"] is not None: prog["icon-file"] = prog["icon-file"].format(path=path)
	
	try:
		if ("gui" not in sys.argv) and ((len(sys.argv) > 1) or ((sys.stdin is not None) and not sys.stdin.isatty())):
			try:
				conf = configuration_class(prog["config"])
				cli = cli_class(prog, conf.conf, sys.argv)
			except Exception as e:
				print("ERROR: " + str(e))
				raise
		else:
			root = tk.Tk()
			try:
				conf = configuration_class(prog["config"])
				gui = gui_class(root, prog, conf.conf)
			except Exception as e:
				root.withdraw()
				tk.messagebox.showerror("ERROR", str(e))
				raise
	except Exception as e:
		error_output(e, prog["error"])
