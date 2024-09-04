import os
import sys
import time 
import re
import dns.resolver
import webbrowser

from functools import partial


from textual.app import App, ComposeResult
from textual.widgets import Markdown, MarkdownViewer, DataTable,TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import ScrollableContainer, Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on, work

from rich.text import Text 

from datetime import datetime
from pyfiglet import Figlet
from time import sleep

import threading
import json
import colorama


from Data.POST_Common import POST_CommonApplication




class Modal_Contact(Static):
	

	def __init__(self, name="", mail="", website=""):

		super().__init__()

		#self.app.display_message_function("%s ; %s ; %s"%(name, mail, website))

		self.contact_name = name 
		self.website = website
		self.mail = mail 
		


		


		

		#self.app.display_message_function(name)


	def compose(self) -> ComposeResult:
		with Horizontal(id="modal_newcontact_container"):
			self.modal_newcontactname = Input(placeholder="Name", value = self.contact_name, type="text", id="modal_newcontactname")
			self.modal_newcontactmail = Input(placeholder="Mail", value = self.mail, type="text", id="modal_newcontactmail")
			self.modal_newcontactwebsite = Input(placeholder="Website", value=self.website, type="text", id="modal_newcontactwebsite")

			yield self.modal_newcontactname
			yield self.modal_newcontactmail
			yield self.modal_newcontactwebsite




class POST_AddContact(ModalScreen, POST_CommonApplication): 




	CSS_PATH = ["Data/Styles/Dark_Theme.tcss", "Data/Styles/Global.tcss"]

	def __init__(self, mode, studio=None):
		super().__init__()
		self.mode = mode
		self.studio = studio
		self.app.display_message_function("%s ; %s"%(mode, studio))



	def compose(self) -> ComposeResult:
		self.app.company_dictionnary
		#self.display_message_function = app.display_message_function
		#self.display_error_function = app.display_error_function

		with VerticalScroll(id="modal_createcontact_container"):
			
			self.newcompany_name = Input(placeholder="Company name", type="text", id="modal_newcompanyname")
			self.newcompany_location = Input(placeholder="Company location", type="text", id="modal_newcompanylocation")
			self.newcompany_website = Input(placeholder="Company website", type="text", id="modal_newcompany_website")
			self.newcompany_answer = Select( [("Yes",1), ("No", 2), ("No answer",3), ("Other",4)], id="modal_newcompany_answer")
			self.newcompany_otheranswer = TextArea(id="modal_newcompany_otheranswer", disabled=True)
			self.newcompany_otheranswer.border_title = "Other answer / Details"

			yield self.newcompany_name
			yield self.newcompany_location
			yield self.newcompany_website
			yield self.newcompany_answer

			
			yield self.newcompany_otheranswer

			with Horizontal(id="modal_addcontact_container"):
				yield Button("Add contact", id="modal_addcontacttolist_button")
				yield Button("Remove contact", id="modal_removecontactfromlist_button")
			
			self.newcompany_contactlist_container = ScrollableContainer(id="modal_newcompany_contactlist")
			yield self.newcompany_contactlist_container


			



			yield Rule(line_style="double")

			with Horizontal(id="modal_horizontal_container"):
				yield Button("Create", variant="primary", id="modal_create_contact_button")
				yield Button("Quit", variant="error", id="modal_cancel_contact_button")


		
	

	def on_mount(self) -> None:
		#IF IN EDIT MODE LOAD THE DICTIONNARY OF THE SELECTED COMPANY
		#AND UPDATE THE PAGE
		if self.mode == "edit":
			self.load_company_data_function(Modal_Contact)

		if self.mode == "create":
			new_contact = Modal_Contact()
			self.newcompany_contactlist_container.mount(new_contact)
		
			


	def on_button_pressed(self, event: Button.Pressed) -> None:
		#if event.button.id == "test":
		#	self.display_message_function(self.query("#modal_newcontactname"))

		if event.button.id == "quit":
			self.app.exit()

		elif event.button.id == "modal_cancel_contact_button":
			self.app.pop_screen()

		elif event.button.id == "modal_addcontacttolist_button":
			new_contact = Modal_Contact()
			#self.display_message_function(new_contact)
			self.newcompany_contactlist_container.mount(new_contact)

		elif event.button.id == "modal_removecontactfromlist_button":
			#get children 
			children_list = self.query("Modal_Contact")
			#self.display_message_function(children_list)
			if children_list:
				children_list.last().remove()

		elif event.button.id == "modal_create_contact_button":
			self.add_company_function()


	
	def on_select_changed(self, event: Select.Changed) -> None:
		if event.select.id == "modal_newcompany_answer":
			value = self.query_one("#modal_newcompany_answer").value

			if value == 4:
				self.newcompany_otheranswer.disabled=False
			else:
				self.newcompany_otheranswer.disabled=True
	























class POST_Application(App, POST_CommonApplication):


	CSS_PATH = ["Data/Styles/Dark_Theme.tcss", "Data/Styles/Global.tcss"]


	def __init__(self):
		super().__init__()



		self.company_dictionnary = {}
		self.user_settings = {}


		#self.load_company_dictionnary_function()




	def compose(self) -> ComposeResult:

		yield Header(show_clock=True)


		with Horizontal(id="main_horizontal_container"):

			with Vertical(id="left_vertical_container"):
				yield Button("ADD CONTACT", id="button_addcontact")
				yield Button("EDIT CONTACT", id="button_editcontact")

				self.listview_studiolist = ListView(id="listview_studiolist")
				self.listview_studiolist.border_title = "Studio list"
				yield self.listview_studiolist
				#self.datatable_studiolist = DataTable(id = "datatable_studiolist")
				#yield self.datatable_studiolist


			with Horizontal(id = "right_horizontal_container"):
				with Vertical(id="right_vertical_container1"):
					self.markdown_studio = Markdown("Hello World")
					yield self.markdown_studio

				with Horizontal(id="right_mail_container"):

					with Vertical(id="right_mailpreset_container"):
						self.input_presetname = Input(placeholder="Mail preset name", id="input_presetname")
						yield self.input_presetname
						yield Button("Create preset", id="button_createpreset")
						yield Button("Save preset", id="button_savepreset")
						yield Button("Delete preset", id="button_deletepreset")
						self.checkbox_copilot = Checkbox("Toggle copilot")
						yield self.checkbox_copilot

						self.listview_mailpreset = ListView(id="listview_mailpreset")
						yield self.listview_mailpreset
						self.listview_mailpreset.border_title = "Preset list"
					
					with Vertical(id="right_mailtext_container"):
						with Collapsible(title="Copilot settings", id="right_mailprompt_collapsible"):
							self.textarea_prompt = TextArea(id="textarea_prompt")
							yield self.textarea_prompt
							self.textarea_prompt.border_title = "Copilot prompt"
						self.textarea_mail = TextArea(id="textarea_mail")
						yield self.textarea_mail
						self.textarea_mail.border_title = "Mail"


	def on_mount(self) -> None:
		self.update_informations_function()





	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "button_createpreset":
			self.create_mail_preset_function()


		if event.button.id == "button_addcontact":

			
			#self.display_message_function(value)
			self.push_screen(POST_AddContact("create"))



		if event.button.id == "button_editcontact":

			#studio = list(self.company_dictionnary.keys())[self.query_one("#datatable_studiolist").cursor_coordinate[1]]
			#value = self.company_dictionnary[list(self.company_dictionnary.keys())[(self.query_one("#datatable_studiolist").cursor_coordinate[1])]]
			#get the selection

			studio = list(self.company_dictionnary.keys())[self.listview_studiolist.index]


			self.push_screen(POST_AddContact("edit", studio))
			#self.update_informations_function()







	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":	
			self.exit()

		if event.key == "delete":
			#self.display_message_function("hello")
			#get selected item in list and delete the key from the dictionnary
			value = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
			del self.company_dictionnary[value]
			self.save_company_dictionnary_function()
			self.update_informations_function()
			self.display_message_function("Company removed from dictionnary")



	def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
		link = event.href

		#check if email or internet adress
		email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
		url_regex = r'^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/.*)?$'



		


		#test the dns check
		if re.match(url_regex, link):
			#self.display_message_function("website adress")
			#open the link in a webbrower
			webbrowser.open(link)
		else:
			try:
				domain = link.split("@")[1]
				dns.resolver.resolve(domain, "MX")
			except Exception as e:
				self.display_error_function("Link not recognized\n%s"%e)
			else:
				self.display_message_function("Email adress")

		



	def on_list_view_selected(self, event: ListView.Selected) -> None:
		if event.list_view.id == "listview_studiolist":
			#check the content in the selection by getting the studio name
			index = self.listview_studiolist.index
			#get the content of the dictionnary
			#and fill the markdown viewer with the company informations
			company_name = list(self.company_dictionnary.keys())[index]
			company_data = self.company_dictionnary[company_name]
			
			markdown = self.generate_markdown_function(company_name, company_data)

			self.markdown_studio.update(markdown)





	
	



	def update_informations_function(self):
		
		self.listview_studiolist.clear()
		#self.datatable_studiolist.clear()

		self.load_company_dictionnary_function()
		self.display_message_function(self.company_dictionnary)
		self.display_message_function("UPDATE")


		#rows = ["Location", "Company"]
		#self.datatable_studiolist.add_columns(*rows)

		
		i = 0
		for key, value in self.company_dictionnary.items():

			label = Label("[ %s ] %s"%(value["CompanyLocation"], key))
			#self.datatable_studiolist.add_row(value["CompanyLocation"], key, height=1, key = i,label=Text("hello"))
			self.listview_studiolist.append(ListItem(label))
			i+=1

			
		








#launch the application
if __name__ == "__main__":
	app = POST_Application()
	app.run()