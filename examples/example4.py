#! /usr/bin/python3

from hydra import *

program = {
	"name"     :"Hydra Example #4",
	"version"  :"0.1.0",
	"date"     :"05/05/2024",
	"purpose"  :"Demonstrates user input and messages.",
	"url"      :"https://github.com/rweathers/hydra",
	"copyright":"Copyright © 2024 Ryan Weathers, All Rights Reserved.",
	"license"  :"This program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.", # None for no license
	"config"   :None,
	"error"    :None
}

class Action(BaseAction):
	def action(self):
		
		self.user_message("Example message")
		self.user_warning("Example warning")
		self.user_error("Example error")
		
		response = self.user_confirm("Are you sure?", True)
		
		response = self.user_input("Enter text", "foo")
		
		# self.interface contains either "gui" or "cli"
		
		return "Task Successful"
		
class CLI(BaseCLI):
	def define_arguments(self):
		self.arguments = [
			("help"    , "h", "Show help information"   , "boolean"),
			("version" , "V", "Show version information", "boolean"),
			("license" , "l", "Show license information", "boolean"),
			("quiet"   , "q", "Suppress all output"     , "boolean"),
			("verbose" , "v", "Enable verbose output"   , "boolean"),
			("cli"     , "" , "Force cli"               , "boolean")
		]
		
	def define_usage(self):
		self.usage = "example4 --cli"
	
	def get_action(self, inputs):
		return Action

class GUI(BaseGUI):
	def create_widgets(self):
		self.create_button(self, "submit", "Start", self.action)

	def get_action(self, inputs):
		return Action

if __name__ == "__main__": main(program, None, CLI, GUI)
