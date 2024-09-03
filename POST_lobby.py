import os
import sys
import time 

from functools import partial


from textual.app import App, ComposeResult
from textual.widgets import Markdown, TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import ScrollableContainer, Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on

from datetime import datetime
from pyfiglet import Figlet
from time import sleep

import threading
import json
import colorama


from Data.POST_Common import POST_CommonApplication




class Modal_Contact(Static):
	def compose(self) -> ComposeResult:
		with Horizontal(id="modal_newcontact_container"):
			self.modal_newcontactname = Input(placeholder="Name", type="text", id="modal_newcontactname")
			self.modal_newcontactmail = Input(placeholder="Mail", type="text", id="modal_newcontactmail")
			self.modal_newcontactwebsite = Input(placeholder="Website", type="text", id="modal_newcontactwebsite")

			yield self.modal_newcontactname
			yield self.modal_newcontactmail
			yield self.modal_newcontactwebsite




class POST_AddContact(ModalScreen, POST_CommonApplication): 




	CSS_PATH = ["Data/Styles/Dark_Theme.tcss", "Data/Styles/Global.tcss"]




	def compose(self) -> ComposeResult:
		self.company_dictionnary = app.company_dictionnary
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
			
			self.newcompany_contactlist_container = ScrollableContainer(Modal_Contact(), id="modal_newcompany_contactlist")
			yield self.newcompany_contactlist_container


			yield Rule(line_style="double")

			with Horizontal(id="modal_horizontal_container"):
				yield Button("Create", variant="primary", id="modal_create_contact_button")
				yield Button("Quit", variant="error", id="modal_cancel_contact_button")
			


	def on_button_pressed(self, event: Button.Pressed) -> None:
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


		self.load_company_dictionnary_function()




	def compose(self) -> ComposeResult:

		yield Header(show_clock=True)


		with Horizontal(id="main_horizontal_container"):

			with Vertical(id="left_vertical_container"):
				yield Button("ADD CONTACT", id="button_addcontact")
				yield Button("EDIT CONTACT", id="button_editcontact")

				self.listview_studiolist = ListView(id="listview_studiolist")
				self.listview_studiolist.border_title = "Studio list"
				yield self.listview_studiolist



			with Vertical(id="right_vertical_container"):
				self.markdown_studio = Markdown("""INFORMATIONS...""")
				yield self.markdown_studio


		self.update_informations_function()





	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":
			self.exit()



	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "button_addcontact":
			self.push_screen(POST_AddContact())




	def update_informations_function(self):
		self.listview_studiolist.clear()

		for key, value in self.company_dictionnary.items():
			label = Label(key)

			self.listview_studiolist.append(ListItem(label))







#launch the application
if __name__ == "__main__":
	app = POST_Application()
	app.run()