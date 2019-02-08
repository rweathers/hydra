#! /usr/bin/python3

import time
from hydra import *

program = {
	"name"     :"Hydra Example #3",
	"version"  :"0.2.0",
	"date"     :"02/08/2019",
	"purpose"  :"Demonstrates custom widget placement.",
	"url"      :"https://github.com/rweathers/hydra",
	"copyright":"Copyright © 2017, 2018, 2019 Ryan Weathers, All Rights Reserved.",
	"license"  :"This program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.", # None for no license
	"config"   :None,
	"error"    :None,
	"icon-data":None,
	"icon-file":None
}

class Configuration(BaseConfiguration):
	pass

class CLI(BaseCLI):
	def get_action(self, inputs):
		return Action

class GUI(BaseGUI):
	def create_widgets(self):
		# The create_widget functions have largs and wargs paramaters that are passed to the label and widget constructors, respectively
		# They also have lgrid and wgrid paramaters that are passed to their respective grid() function calls
		# create_browse and create_button have bargs and bgrid that serve the same purpose
		# These can be used to fully customize the widget layout
		
		self.create_entry(self, "first-name", "First Name", wargs={"width":25}, lgrid={"row":1, "column":0}, wgrid={"row":2, "column":0})
		self.create_entry(self, "last-name" , "Last Name" , wargs={"width":25}, lgrid={"row":1, "column":1}, wgrid={"row":2, "column":1})
		
		self.create_button(self, "submit", "Submit", self.action)

	def get_action(self, inputs):
		return Action

class Action(BaseAction):
	def action(self):
		return "Completed Successfully"

if __name__ == "__main__": main(program, Configuration, CLI, GUI)
