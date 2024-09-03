import os
import sys
import time 

from functools import partial


from textual.app import App, ComposeResult
from textual.widgets import Markdown, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on

from datetime import datetime
from pyfiglet import Figlet
from time import sleep

import threading
import json
import colorama





class POST_CommonApplication:
	def display_message_function(self, message):
		self.notify(str(message), timeout=4)

	def display_error_function(self, message):
		self.notify(str(message), severity="error", timeout=4)





	def save_company_dictionnary_function(self):
		try:
			with open(os.path.join(os.getcwd(), "Data/User/UserCompanyData.json"), "w") as save_file:
				json.dump(self.company_dictionnary, save_file, indent=4)

		
		except:
			self.display_error_function("Impossible to save dictionnary")
			return False
		else:
			self.display_message_function("Dictionnary saved")
			return True





	def load_company_dictionnary_function(self):
		try:
			with open(os.path.join(os.getcwd(), "Data/User/UserCompanyData.json"), "r") as read_file:
				self.company_dictionnary = json.load(read_file)
		except:
			self.display_error_function("Impossible to load company dictionnary")
		else:
			self.display_message_function("Company dictionnary loaded")
		






	def add_company_function(self):
		#get informations
		company_informations = {
			#"CompanyName":self.query_one("#modal_newcompanyname").value,
			"CompanyLocation":self.query_one("#modal_newcompanylocation").value,
			"CompanyWebsite":self.query_one("#modal_newcompany_website").value,
			"CompanyAnswer":None,
			"CompanyContact":None,
		}

		if self.query_one("#modal_newcompany_answer").value == 1:
			company_informations["CompanyAnswer"] = True
		elif self.query_one("#modal_newcompany_answer").value == 2:
			company_informations["CompanyAnswer"] = False
		elif self.query_one("#modal_newcompany_answer").value == 3:
			company_informations["CompanyAnswer"] = None
		else:
			company_informations["CompanyAnswer"] = self.query_one("#modal_newcompany_otheranswer").text

		contact_name_list = self.query("#modal_newcontactname")
		contact_mail_list = self.query("#modal_newcontactmail")
		contact_website_list = self.query("#modal_newcontactwebsite")

		if len(contact_name_list) != len(contact_mail_list):
			self.display_error_function("Error trying to get contact informations")
			return
		else:
			contact_dictionnary = {}
			
			for i in range(len(contact_name_list)):
				contact_dictionnary[contact_name_list[i].value] = {
					"mail": contact_mail_list[i].value,
					"website": contact_website_list[i].value,
				}

			#replace the value in the company dictionnary
			company_informations["CompanyContact"] = contact_dictionnary


			#replace the value in the company dictionnary and save the new dictionnary
			if self.query_one("#modal_newcompanyname").value in self.company_dictionnary:
				self.display_error_function("That company is already registered in the dictionnary")
			else:
				self.company_dictionnary[self.query_one("#modal_newcompanyname").value] = company_informations
				value = self.save_company_dictionnary_function()



