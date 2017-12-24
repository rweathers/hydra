#! /usr/bin/python3

import time
from hydra import *

# TODO - define your program information, all keys are required
program = {
	"name"     :"Program Name",
	"version"  :"0.0.0",
	"date"     :"MM/DD/YYYY",
	"usage"    :"example [-options] --greeting Greeting --name Name", # Separate multiple commands with \n
	"purpose"  :"Purpose of the program.",
	"url"      :"http://www.your-website.com/", # None for no url
	"copyright":"Copyright © YYYY Your Name, All Rights Reserved.",
	"license"  :"This program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.", # None for no license
	"config"   :"{path}example.ini", # None for no config file
	"error"    :"{path}example.err", # None for no error file
	
	# icon-data holds a base64 encoded copy of the icon file, i.e.:
	#	import base64
	#	with open("example.png", "rb") as f: print(base64.b64encode(f.read()))
	# icon-file holds the icon file name
	# icon-data takes precedence over icon-file if icon-data is not None
	# If both are None the default Tk icon will be used
	"icon-data":None, # "base 64 string" for an embeded image
	"icon-file":None # "{path}example.png" for an external image
}

class Configuration(BaseConfiguration):
	def validate(self):
		errors = ""
		
		# TODO - validate your config file
		
		if self.conf.get("example", "") == "": errors += "'example' is required\n"
		
		if errors != "": raise Exception("The following errors occurred when parsing " + self.filename + "\n\n" + errors)

class CLI(BaseCLI):
	def define_arguments(self):
		# TODO - define your arguments
		self.arguments = [
			("help"    , "h", "Show help information"   , "boolean"),
			("version" , "V", "Show version information", "boolean"),
			("license" , "l", "Show license information", "boolean"),
			("quiet"   , "q", "Suppress all output"     , "boolean"),
			("verbose" , "v", "Enable verbose output\n" , "boolean"),
			
			("greeting", "g", "A greeting"              , "value"),
			("name"    , "n", "A name"                  , "value")
			
			#("long-name", "char", "Description", "boolean"),
			#("long-name", "char", "Description", "value"),
			#("long-name", "char", "Description", "multiple"),
		]
		
		# Flags used: g, h, l, n, q, v, V
	
	def get_action(self, inputs):
		# TODO - return the BaseAction subclass to use
		return Action

class GUI(BaseGUI):
	def define_menu(self):
		# TODO - define your menu. This is optional. Don't override define_menu() to have no menu.
		self.menu = [
			("File"    , [("Exit", self.quit)]),
			("Edit"    , [("Reset", self.set_defaults)]),
			("Settings", [("Open Config File", self.open_config)]),
			("Help"    , [("Help", self.show_help), ("About", self.show_about)])
			
			#("Label", [("Label1", callback1), ... ("LabelN", callbackN])
		]
	
	def define_help(self, help):
		# TODO - define your help. help is a tk Text object.
		
		help.insert(tk.END, "Header\n\n", "bold")
		help.insert(tk.END, "Section\n\n", "italic")
		help.insert(tk.END, "Text", "normal")
		
		#help.config(height = 25)
		#help.config(width  = 75)
	
	def create_widgets(self):
		# TODO - create your widgets
		
		self.create_entry(self, "greeting", "Greeting", default=self.conf.get("greeting", ""))
		self.create_entry(self, "name"    , "Name"    , default=self.conf.get("name"    , ""))
		
		#self.create_browse  (self, "inputs"  , "Inputs"  , self.get_inputs, initialdir="/initial/dir", filetypes=[("All Files", ".*")])
		#self.create_browse  (self, "input"   , "Input"   , self.get_input , initialdir="/initial/dir", filetypes=[("All Files", ".*")])
		#self.create_browse  (self, "output"  , "Output"  , self.get_output, initialdir="/initial/dir", initialfile="initial.file", filetypes=[("All Files", ".*")])
		#self.create_browse  (self, "folder"  , "Folder"  , self.get_folder, initialdir="/initial/dir")
		#self.create_entry   (self, "entry"   , "Entry"   , default="Default text")
		#self.create_combobox(self, "combobox", "Combobox", ("", "Option 1", "Option 2", "Option 3"))
		#self.create_listbox (self, "listbox" , "Listbox" , ("Option 1", "Option 2", "Option 3"))
		#self.create_text    (self, "text"    , "Text"    , default="Default\nText")
		#self.create_checkbox(self, "checkbox", "Checkbox", default=0)
		
		#notebook = self.create_notebook(self, "notebook")
		#tab = self.create_tab(notebook, "Tab")
		#self.create_browse  (tab, "inputs"  , "Inputs"  , self.get_inputs, initialdir="/initial/dir", filetypes=[("All Files", ".*")])
		#self.create_browse  (tab, "input"   , "Input"   , self.get_input , initialdir="/initial/dir", filetypes=[("All Files", ".*")])
		#self.create_browse  (tab, "output"  , "Output"  , self.get_output, initialdir="/initial/dir", initialfile="initial.file", filetypes=[("All Files", ".*")])
		#self.create_browse  (tab, "folder"  , "Folder"  , self.get_folder, initialdir="/initial/dir")
		#self.create_entry   (tab, "entry"   , "Entry"   , default="Default text")
		#self.create_combobox(tab, "combobox", "Combobox", ("", "Option 1", "Option 2", "Option 3"))
		#self.create_listbox (tab, "listbox" , "Listbox" , ("Option 1", "Option 2", "Option 3"))
		#self.create_text    (tab, "text"    , "Text"    , default="Default\nText")
		#self.create_checkbox(tab, "checkbox", "Checkbox", default=0)
		
		self.create_button(self, "submit", "Submit", self.action)

	def get_action(self, inputs):
		# TODO - return the BaseAction subclass to use
		return Action

class Action(BaseAction):
	def standardize(self):
		# TODO - standardize your inputs
		
		# self.expand("name") will standardize a single filename or a glob into a list of full filenames
		
		pass
	
	def validate(self):
		errors = ""
		
		# TODO - validate your inputs
		
		if self.inputs["greeting"] == "": errors += "Greeting required\n"
		if self.inputs["name"]     == "": errors += "Name required\n"
		
		if errors != "": raise Exception(errors)
	
	def action(self):
		# TODO - perform the task
		
		# self.open(filename, mode=?, encoding=?) will allow you to use "STDIN" and "STDOUT" for sys.stdin and sys.stdout, respectively
		
		# Dummy code to demonstrate progress
		self.progress("Starting...")
		started = time.time()
		i = 0
		z = 10
		while i < z:
			time.sleep(0.5)
			
			i += 1
			self.progress("Record: " + str(i), started, i, z)
		
		return self.inputs["greeting"] + " " + self.inputs["name"] + "!"

main(program, Configuration, CLI, GUI)
