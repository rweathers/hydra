#! /usr/bin/python3

from hydra import *

program = {
	"name"     :"Hydra Example #2",
	"version"  :"0.3.0",
	"date"     :"04/02/2021",
	"purpose"  :"Demonstrates tabs and multiple actions.",
	"url"      :"https://github.com/rweathers/hydra",
	"copyright":"Copyright © 2017, 2018, 2019, 2020, 2021 Ryan Weathers, All Rights Reserved.",
	"license"  :"This program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.", # None for no license
	"config"   :None,
	"error"    :None
}

class Action1(BaseAction):
	def validate(self):
		if self.inputs["value1"] == "": raise Exception("Value 1 required")
	
	def action(self):
		return "Action 1 Completed Successfully"
		
class Action2(BaseAction):
	def validate(self):
		if self.inputs["value2"] == "": raise Exception("Value 2 required")
	
	def action(self):
		return "Action 2 Completed Successfully"
		
class Action3(BaseAction):
	def validate(self):
		if self.inputs["value3"] == "": raise Exception("Value 3 required")
	
	def action(self):
		return "Action 3 Completed Successfully"

class CLI(BaseCLI):
	def define_arguments(self):
		self.arguments = [
			("help"    , "h", "Show help information"              , "boolean"),
			("version" , "V", "Show version information"           , "boolean"),
			("license" , "l", "Show license information"           , "boolean"),
			("quiet"   , "q", "Suppress all output"                , "boolean"),
			("verbose" , "v", "Enable verbose output"              , "boolean"),
			("action"  , "a", "One of: action1, action2 or action3", "value"),
			("value1"  , "1", "Value #1"                           , "value"),
			("value2"  , "2", "Value #2"                           , "value"),
			("value3"  , "3", "Value #3"                           , "value")
		]
	
	def define_usage(self):
		self.usage = "example2 [-options] --action action# --value# value"
	
	def get_action(self, inputs):
		if inputs["action"] == "action1":
			return Action1
		elif inputs["action"] == "action2":
			return Action2
		elif inputs["action"] == "action3":
			return Action3
		else:
			raise Exception("action required")

class GUI(BaseGUI):
	def create_widgets(self):
		notebook = self.create_notebook(self, "action")
		
		tab1 = self.create_tab(notebook, "Action 1")
		self.create_entry(tab1, "value1" , "Value 1")
		self.create_button(tab1, "submit1", "Action 1", self.action)
		
		tab2 = self.create_tab(notebook, "Action 2")
		self.create_entry(tab2, "value2" , "Value 2")
		self.create_button(tab2, "submit2", "Action 2", self.action)
		
		tab3 = self.create_tab(notebook, "Action 3")
		self.create_entry(tab3, "value3" , "Value 3")
		self.create_button(tab3, "submit3", "Action 3", self.action)

	def get_action(self, inputs):
		if inputs["action"] == "Action 1":
			return Action1
		elif inputs["action"] == "Action 2":
			return Action2
		elif inputs["action"] == "Action 3":
			return Action3
		else:
			raise Exception("An unknown error has occured")

if __name__ == "__main__": main(program, None, CLI, GUI)
