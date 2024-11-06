import os
import sys
import subprocess
import ctypes


lib_list = [
	"re",
	"unidecode",
	"Levenshtein",
	"termcolor",
	"re",
	"dnspython",
	"pyperclip",
	"rich",
	"threading",
	"datetime",
	"textual_datepicker",
	"groq",
	"ast",
	"time",
	"sys",
	"colorama",
	"pyfiglet",
	"pendulum",
	"json",
	"textual"
	]


for lib in lib_list:
	try:
		__import__(lib)
	except ImportError:
		print("Impossible to load library : %s --> Download running...\n"%lib)
		subprocess.check_call([sys.executable, "-m", "pip", "install", lib])


import time 
import re
import dns.resolver
import webbrowser
import pendulum
import pyperclip 
import pyfiglet
import unidecode
import re
import Levenshtein

from functools import partial


from textual.suggester import SuggestFromList, Suggester
from textual.app import App, ComposeResult
from textual.widgets import Markdown, MarkdownViewer, DataTable,TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import ScrollableContainer, Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on, work

from textual_datepicker import DateSelect, DatePicker

from rich.text import Text 

from datetime import datetime
from pyfiglet import Figlet
from time import sleep

import threading
import json
import colorama


from Data.POST_Common import POST_CommonApplication






# EXTENDED CLASS OF TEXTUAL WITH ADDITIONNAL FEATURES
class ExtendedTextArea(TextArea):
	"""A subclass of TextArea with parenthesis-closing functionality."""

	def _on_key(self, event: events.Key) -> None:
		if event.key == "enter":
			self.insert("\n-")
			#self.move_cursor_relative(columns=-1)
			event.prevent_default()









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
		self.date = str(datetime.now())
		self.app.display_message_function("%s ; %s"%(mode, studio))



	def compose(self) -> ComposeResult:
		self.app.company_dictionnary
		#self.display_message_function = app.display_message_function
		#self.display_error_function = app.display_error_function

		with VerticalScroll(id="modal_createcontact_container"):
			
			self.newcompany_name = Input(placeholder="Company name", type="text", id="modal_newcompanyname")
			self.newcompany_location = Input(placeholder="Company location", type="text", id="modal_newcompanylocation")
			self.newcompany_website = Input(placeholder="Company website", type="text", id="modal_newcompany_website")

			

			

			self.newcompany_details = ExtendedTextArea(id="modal_newcompany_details")
			self.newcompany_details.border_title = "Company details"

			self.newcompany_answer = Select( [("Yes",1), ("No", 2), ("No answer",3), ("Other",4)], id="modal_newcompany_answer")
			self.newcompany_otheranswer = TextArea(id="modal_newcompany_otheranswer", disabled=True)
			self.newcompany_otheranswer.border_title = "Other answer / Details"



			yield self.newcompany_name
			yield self.newcompany_location
			yield self.newcompany_website
			#yield Button("Last time company was reached", id="modal_newcompany_datebutton")

			self.newcompany_contacted_checkbox = Checkbox("I have already contacted the company", id="modal_contacted_checkbox")
			self.newcompany_contacted_checkbox.value = False
			yield self.newcompany_contacted_checkbox
			with Collapsible(title = "Last time company was reached : ", id="modal_collapsible_dateselector"):
				
				self.modal_dateselect = DateSelect(placeholder="please select",format="YYYY-MM-DD",picker_mount="#modal_collapsible_dateselector",date=pendulum.parse(str(datetime.now())), id="modal_date")
				yield self.modal_dateselect


				   
				
			yield self.newcompany_details
			yield self.newcompany_answer

			
			yield self.newcompany_otheranswer


			with Horizontal(id="modal_addcontact_container"):
				yield Button("Add contact", id="modal_addcontacttolist_button", classes="darken_button primary_button")
				yield Button("Remove contact", id="modal_removecontactfromlist_button", classes="darken_button error_button")
			
			self.newcompany_contactlist_container = ScrollableContainer(id="modal_newcompany_contactlist")
			yield self.newcompany_contactlist_container



			yield Rule(line_style="double")

			with Horizontal(id="modal_horizontal_container"):
				if self.mode == "create":
					yield Button("Create", variant="primary", id="modal_create_contact_button", classes="darken_button primary_button")
				else:
					yield Button("Save", variant="primary", id="modal_create_contact_button", classes="darken_button primary_button")
				yield Button("Quit", variant="error", id="modal_cancel_contact_button", classes="darken_button error_button")


		


	

	def on_mount(self) -> None:
		#IF IN EDIT MODE LOAD THE DICTIONNARY OF THE SELECTED COMPANY
		#AND UPDATE THE PAGE
		if self.mode == "edit":
			self.load_company_data_function(Modal_Contact)

		if self.mode == "create":
			self.query_one("#modal_collapsible_dateselector").disabled = True
			new_contact = Modal_Contact()
			self.newcompany_contactlist_container.mount(new_contact)



	def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
		if event.checkbox.id == "modal_contacted_checkbox":
			self.query_one("#modal_collapsible_dateselector").disabled = not self.newcompany_contacted_checkbox.value





	def on_date_picker_selected(self, event: DatePicker.Selected) -> None:
		self.date = event.date
		
		if datetime.strptime(self.date.to_date_string(), "%Y-%m-%d") > datetime.now():
			self.display_error_function("This date is in the futur!")
			return
		widget = self.query_one("#modal_collapsible_dateselector").title = "Last time company was reached : %s"%pendulum.parse(str(self.date))
		self.display_message_function("UPDATED")


		
			


	def on_button_pressed(self, event: Button.Pressed) -> None:
		#if event.button.id == "test":
		#	self.display_message_function(self.query("#modal_newcontactname"))

		if event.button.id == "quit":
			self.app.exit()

		elif event.button.id == "modal_cancel_contact_button":
			self.app.pop_screen()

		elif event.button.id == "modal_newcompany_datebutton":
			date = self.app.push_screen(POST_DateSelector())
			self.display_message_function(date)

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






























class POST_UserInfos(ModalScreen, POST_CommonApplication):


	CSS_PATH = ["Data/Styles/Dark_Theme.tcss", "Data/Styles/Global.tcss"]


	def __init__(self):
		super().__init__()
	

	def compose(self) -> ComposeResult:

		with VerticalScroll(id="modal_usersettings_vertical_container"):


			self.input_usersettingsjob = Input(placeholder = "What is your job", id="input_usersettingsjob")
			yield self.input_usersettingsjob
		
			self.input_usersettingsskills = Input(placeholder = "What are your skills", id="input_usersettingsskills")
			yield self.input_usersettingsskills

			

			self.textarea_usersettings = ExtendedTextArea(id="textarea_usersettings")
			yield self.textarea_usersettings
			
			

			yield Rule(line_style="double")

			with Horizontal(id="modal_usersettings_horizontal_container"):
				yield Button("Save", variant="primary", id="modal_usersettings_button_save", classes="darken_button primary_button")
				yield Button("Quit", variant="error", id="modal_usersettings_button_quit", classes="darken_button error_button")


	def on_button_pressed(self, event: Button.Pressed) -> None:
		#if event.button.id == "test":
		#	self.display_message_function(self.query("#modal_newcontactname"))

		if event.button.id == "modal_usersettings_button_quit":
			self.app.pop_screen()

		if event.button.id == "modal_usersettings_button_save":
			content = self.textarea_usersettings.text
			splited_content = content.split("-")

			#for line in splited_content:
			#	self.app.display_message_function(line)
			self.app.user_settings["UserPromptDetails"] = splited_content
			if self.letter_verification_function(self.input_usersettingsskills.value) == True:
				self.app.user_settings["UserSkillSearched"] = self.input_usersettingsskills.value.split("/")

			if self.letter_verification_function(self.input_usersettingsjob.value)==True:
				self.app.user_settings["UserJobSearched"] = self.input_usersettingsjob.value

			self.save_user_settings_function()


	def on_mount(self) -> None:
		#apply user settings in the text area
		#self.display_message_function(self.app.user_settings)
		content = self.app.user_settings["UserPromptDetails"]
		
		#self.app.display_message_function(type(content))


		for line in content:
			if self.letter_verification_function(line)==True:
				#self.app.display_message_function("-%s"%line)
				self.textarea_usersettings.insert("-%s"%line)

		try:
			self.input_usersettingsskills.value = "/".join(self.app.user_settings["UserSkillSearched"])
			self.input_usersettingsjob.value = self.app.user_settings["UserJobSearched"]
		except:
			pass

	
























class POST_Application(App, POST_CommonApplication):


	CSS_PATH = ["Data/Styles/Dark_Theme.tcss", "Data/Styles/Global.tcss"]


	def __init__(self):
		super().__init__()



		self.company_dictionnary = {}
		self.contact_list = {}


		self.studio_suggest_list = []
		self.mail_contact_list = []


		self.user_settings = {
			"colorTheme":"DarkTheme",
			"companyDisplayMode":1,
			"colorDictionnary": {
				"UserContactShortAlert": {
					"Color": "#fff03a",
					"Delta": 3,
				},
				"UserContactMediumAlert": {
					"Color": "#ff7c3a",
					"Delta": 5,
				},
				"UserContactLongAlert": {
					"Color": "#ff3a3a",
					"Delta": 7,
				},
				"UsernotContacted": {
					"Color":"#ffffff"
				},
			
			}
		}
		
		self.user_preset = {}

		self.list_studiolist_display = []

		self.font_title = "ansi_shadow"

		self.color_theme = "Dark_Theme"



		#COLORS FOR CONTACTED STUDIO
		"""
		FONT COLOR
			Not contacted yet --> no color
			Already contacted --> Lighter color?
			Short time alert --> orange
			Long time alert --> Red
		"""
		self.color_dictionnary = {
			"Dark_Theme": {
				"notContacted": "white",
				"contactDateShortAlert": "#e59818",
				"contactDateMediumAlert": "#e55a1a",
				"contactDateLongAlert": "#d81b57",
			}
		}


		#self.load_company_dictionnary_function()




	def compose(self) -> ComposeResult:

		yield Header(show_clock=True)
		


		with Horizontal(id="main_horizontal_container"):
			with Vertical(id = "main_title_container"):

				yield Label(pyfiglet.figlet_format("_@rchive_",font=self.font_title, width=200), id="label_title")


				with Horizontal(id = "main_left_center_container_horizontal"):
					with Vertical(id = "main_left_container"):
						
						

						with Vertical(id="left_vertical_container"):

							
							with Grid(id = "left_horizontal_option_bar"):
				
								
								yield Button("USER INFOS", id="button_userinfos", classes="button_bar")
								yield Button("ADD CONTACT", id="button_addcontact", classes="button_bar")
								yield Button("EDIT CONTACT", id="button_editcontact", classes="button_bar")
								yield Button("DELETE CONTACT", id="button_deletecontact", variant="error", classes="error_button button_bar")
								

							with Collapsible(id = "collapsible_studiolist_settings", title="COMPANY LIST SETTINGS"):
								with RadioSet(id = "radioset_studiolist_settings"):
									yield RadioButton("By alphabetic order")
									yield RadioButton("By chronologic order")
									yield RadioButton("By priority order")



							self.input_studiolist_searchbar = Input(placeholder = "Studio name...", id = "input_studiolist_searchbar")
							yield self.input_studiolist_searchbar

							self.listview_studiolist = ListView(id="listview_studiolist")
							self.listview_studiolist.border_title = "Studio list"
							yield self.listview_studiolist
							#self.datatable_studiolist = DataTable(id = "datatable_studiolist")
							#yield self.datatable_studiolist
					with Vertical(id = "main_center_container"):

						#with Horizontal(id = "right_horizontal_container"):
						with Vertical(id="right_vertical_container1"):
							self.markdown_studio = Markdown("Hello World")
							yield self.markdown_studio


			with Vertical(id = "main_right_container"):
				with TabbedContent(id="main_righttab_container"):


					with TabPane("Mail editor"):
						with Horizontal(id="main_righthorizontal_container"):
							with Vertical(id="right_mailpreset_container"):
								self.input_presetname = Input(placeholder="Mail preset name", id="input_presetname")
								yield self.input_presetname
								yield Button("Create preset", id="button_createpreset", classes="button_preset")
								yield Button("Save preset", id="button_savepreset", classes="button_preset")
								yield Button("Delete preset", id="button_deletepreset", classes="button_preset")
								yield Button("Use copilot", id="button_usecopilot", classes="primary_button button_preset")

								yield Rule()

								yield Button("Copy content", id="button_copycontent", classes="button_preset")

								self.listview_mailpreset = ListView(id="listview_mailpreset")
								yield self.listview_mailpreset
								self.listview_mailpreset.border_title = "Preset list"
							
							with Vertical(id="right_mailtext_container"):
								
								


								with Collapsible(title="Contact list", id="collapsible_mail_contact_list"):
									self.input_mailcontact = Input(placeholder="Mail contact list", id="input_mailcontact", suggester=SuggestFromList(self.studio_suggest_list, case_sensitive=False))
									yield self.input_mailcontact
									
									with Horizontal(id = "mail_contact_horizontal_container"):
										with Vertical(id = "mail_contact_left_column"):
											yield Button("hello")

										with Vertical(id = "mail_contact_right_column"):
											self.optionlist_contact = OptionList(id = "optionlist_contact")
											self.optionlist_contact.border_title = "Mail contact list"
											yield self.optionlist_contact


								yield Rule()

								

								self.textarea_mail = TextArea(id="textarea_mail")
								yield self.textarea_mail
								self.textarea_mail.border_title = "Mail"



					with TabPane("Mail Settings"):
						with Vertical(id = "main_settings_container"):
							with Collapsible(title="Copilot settings", id="right_mailprompt_collapsible"):
								self.textarea_prompt = TextArea(id="textarea_prompt")
								yield self.textarea_prompt
								self.textarea_prompt.border_title = "Copilot prompt"



								with Horizontal(id="right_mailtext_horizontal"):
									yield Button("Save copilot prompt", id="button_saveprompt")




					with TabPane("Mail watcher"):
						self.listview_contactlist = ListView(id = "listview_contactlist")
						yield self.listview_contactlist

		


	def on_mount(self) -> None:
		
		self.update_informations_function()







	def on_input_changed(self, event: Input.Changed) -> None:
		#EVENT FOR THE SEARCHBAR
		#call the searchbar system function
		if event.input.id == "input_studiolist_searchbar":
			#get the value of the searchbar at that moment
			#self.display_message_function(self.input_studiolist_searchbar.value)
			self.searchbar_function(self.input_studiolist_searchbar.value)


	def on_input_submitted(self, event: Input.Submitted) -> None:
		if event.input.id == "input_mailcontact":
			#get the value of the input field
			#check if the name is in the studio list
			#otherwise check if it is an email adress
			if self.letter_verification_function(self.input_mailcontact.value)!=True:
				self.display_error_function("You have to enter a studio name or email adress!")
				return
			else:
			

				if self.input_mailcontact.value not in list(self.company_dictionnary.keys()):
					if (self.check_adress_function(self.input_mailcontact.value)) != True:
						self.display_error_function("This is not a valid studio name or email adress!")
						return 
				
				if self.input_mailcontact.value in self.mail_contact_list:
					self.display_error_function("Contact already in list!")
					return 

				self.mail_contact_list.append(self.input_mailcontact.value)
				self.optionlist_contact.add_option(self.input_mailcontact.value)
				self.display_message_function("Contact added to list")



	def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
		if event.option_list.id == "optionlist_contact":
			
			#get the index of the selected item
			#remove it from the list
			#refresh the option list
			self.mail_contact_list.pop(self.optionlist_contact.highlighted)
			self.optionlist_contact.clear_options()
			self.optionlist_contact.add_options(self.mail_contact_list)


						





			

	"""
	async def on_key(self, event: events.Key):
		if (self.focused.id == "input_mailcontact") and (event.key == "right"):
			self.input_mailcontact.value = "%s;"%self.input_mailcontact.value
	"""


	def on_radio_set_changed(self, event:RadioSet.Changed) -> None:
		if event.radio_set.id == "radioset_studiolist_settings":
			#get index
			index = event.index
			self.user_settings["companyDisplayMode"] = index
			self.save_user_settings_function()
			self.update_informations_function()


	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "button_createpreset":
			self.create_mail_preset_function()


		if event.button.id == "button_saveprompt":
			content = self.textarea_prompt.text 
			self.display_message_function(content)

			
			self.user_preset["CopilotPrompt"] = content

			self.save_mail_preset_function()


		if event.button.id == "button_usecopilot":
			#self.display_message_function(self.company)
			generate = self.generate_with_copilot_function()


		if event.button.id == "button_copycontent":
			if self.letter_verification_function(self.textarea_mail.selected_text)==True:
				pyperclip.copy(self.textarea_mail.selected_text)
			else:
				pyperclip.copy(self.textarea_mail.text)
			self.display_message_function("copied")
			


		if event.button.id == "button_addcontact":
			
			#self.display_message_function(value)
			self.push_screen(POST_AddContact("create"))


		if event.button.id == "button_userinfos":
			self.push_screen(POST_UserInfos())

		if event.button.id == "button_deletecontact":
			

			self.delete_company_function()



		if event.button.id == "button_savepreset":
			#get the content of the list selection
			#get the content of the text
			#replace in the dictionnary and save the new dictionnary
			index = self.listview_mailpreset.index
			preset_list = self.user_preset["mailPreset"]
			preset_name = list(preset_list.keys())[index]

			new_preset_content = self.textarea_mail.text 
			preset_list[preset_name] = new_preset_content
			self.user_preset["mailPreset"]
			self.save_mail_preset_function()
			self.update_informations_function()



		if event.button.id == "button_editcontact":

			#studio = list(self.company_dictionnary.keys())[self.query_one("#datatable_studiolist").cursor_coordinate[1]]
			#value = self.company_dictionnary[list(self.company_dictionnary.keys())[(self.query_one("#datatable_studiolist").cursor_coordinate[1])]]
			#get the selection

			try:
				#studio = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
				studio = self.list_studiolist_display[self.listview_studiolist.index]

				self.push_screen(POST_AddContact("edit", studio))
			except TypeError:
				self.display_error_function("No studio selected")
				
			#self.update_informations_function()






















	def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
		link = event.href

		#check if email or internet adress
		
		#email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
		#url_regex = r'^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/.*)?$'
		


		#remove the beginning of the link copied if it starts with mailto:
		if link.startswith("mailto:"):
			link = link.replace("mailto:", "")

		pyperclip.copy(link)
		self.display_message_function("Link copied in clipboard\n%s"%link)


		
		"""

		#test the dns check
		if re.match(url_regex, link):
			#self.display_message_function("website adress")
			#open the link in a webbrower
			
			#OPEN THE WEBBROWSER WITH THE LINK
			#webbrowser.open(link)

			#COPY THE LINK IN THE CLIPBOARD
			pyperclip.copy(link)
			self.display_message_function("Link copied in clipboard\n%s"%link)
		else:
			try:
				domain = link.split("@")[1]
				dns.resolver.resolve(domain, "MX")
			except Exception as e:
				self.display_error_function("Link not recognized\n%s"%e)
			else:
				self.display_message_function("Email adress")
		"""

		



	def on_list_view_selected(self, event: ListView.Selected) -> None:
		if event.list_view.id == "listview_studiolist":
			#check the content in the selection by getting the studio name
			index = self.listview_studiolist.index
			#get the content of the dictionnary
			#and fill the markdown viewer with the company informations
			
			#company_name = list(self.company_dictionnary.keys())[index]
			company_name = self.list_studiolist_display[index]
			company_data = self.company_dictionnary[company_name]
			
			markdown = self.generate_markdown_function(company_name, company_data)

			self.markdown_studio.update(markdown)


		if event.list_view.id == "listview_mailpreset":

			#clear the content of the text area
			#and fill it with the content of that mail preset if possible
			index = self.listview_mailpreset.index
			preset_name = list(self.user_preset["mailPreset"].keys())[index]
			self.textarea_mail.clear()

			#self.display_message_function(preset_name)
			#self.display_message_function(self.user_preset["mailPreset"])
			try:
				self.textarea_mail.insert(self.user_preset["mailPreset"][preset_name],(0,0))
			except:
				pass








	def searchbar_function(self, content):

		if self.letter_verification_function(content) == True:
			#remove all capital letter and accent in the content
			content = unidecode.unidecode(content.lower())
			#self.display_message_function(content)



			self.list_studiolist_display = []



			for i in range(len(self.list_studiolist_filtered)):

				studio_name = self.list_studiolist[i]
				studio_filtered = self.list_studiolist_filtered[i]


				if content in studio_filtered:
					self.list_studiolist_display.append(studio_name)
				else:
					distance = Levenshtein.distance(content, studio_filtered)
					length = max(len(content), len(studio_filtered))
					similitude = ((length - distance) / length) * 100

					if similitude > 70:
						self.list_studiolist_display.append(studio_name)


			#self.list_studiolist_display = self.searchbar_studio_list
			self.listview_studiolist.clear()
			self.update_studiolist_view()




		else:
			#append to the studiolist the studiolist
			self.update_informations_function()















	def update_informations_function(self):






		#self.display_message_function("Refresh informations")


		#LOAD ALL INFORMATIONS CONTAINED IN USER SETTINGS FILES
		self.listview_studiolist.clear()
		self.listview_mailpreset.clear()
		self.textarea_prompt.clear()

		self.load_company_dictionnary_function()
		self.load_mail_preset_function()
		self.load_user_settings_function()




		#create the studio suggest list for mail contact
		self.studio_suggest_list.clear()
		self.studio_suggest_list = list(self.company_dictionnary.keys())
		self.input_mailcontact.suggester=SuggestFromList(self.studio_suggest_list, case_sensitive=False)

		self.listview_contactlist.clear()
		for suggest in self.studio_suggest_list:
			self.listview_contactlist.append(ListItem(Label(suggest)))



		#CREATE THE CONTACT LIST
		"""
		for studio_name, studio_data in self.company_dictionnary.items():
			for contact_name, contact_data in studio_data["CompanyContact"].items():
				if self.letter_verification_function(contact_data["mail"])==True:
					self.contact_list[contact_data["mail"]] = {
						"studioName":studio_name,
						"studioContactName":contact_name
						}
		for contact_adress, contact_data in self.contact_list.items():
			label = Label("[ %s ] - %s"%(contact_adress, contact_data["studioName"]))
			self.listview_contactlist.append(ListItem(label)) 
		"""







		if "CopilotPrompt" in self.user_preset:
			self.textarea_prompt.insert(self.user_preset["CopilotPrompt"])


		if "mailPreset" in self.user_preset:
			preset_list = list(self.user_preset["mailPreset"].keys())

			for preset in preset_list:
				self.listview_mailpreset.append(ListItem(Label(preset)))




		self.list_studiolist = list(self.company_dictionnary.keys())
		self.list_studiolist_filtered = []

		for studio in self.list_studiolist:
			self.list_studiolist_filtered.append(unidecode.unidecode(studio.lower()))

		self.list_studiolist_display = []
		#self.list_studiolist_filtered = []

		
		#NOT BY PRIORITY ORDER
		if self.user_settings["companyDisplayMode"] != 2:
			try:
				self.display_message_function("NOT PRIORITY ORDER")
				if self.user_settings["companyDisplayMode"] != 2:


					self.list_studiolist_display = list(self.company_dictionnary.keys())

					#BY ALPHABETIC ORDER
					if  (self.user_settings["companyDisplayMode"] == 0):
						self.list_studiolist_display.sort(key = str.lower)
			except KeyError:
				pass





		#BY PRIORITY ORDER
		else:	
			self.display_message_function("PRIORITY ORDER")

			not_contacted_list = []
			no_alert_list = []
			short_alert_list = []
			medium_alert_list = []
			long_alert_list = []


			for studio_name, studio_data in self.company_dictionnary.items():
				if ("CompanyDate" not in studio_data) or (studio_data["CompanyDate"] == None):
					not_contacted_list.append(studio_name)

				else:
					date = self.company_dictionnary[studio_name]["CompanyDate"]

					if type(date) == str:
						date = pendulum.parse(date).to_date_string()
						date = datetime.strptime(date, "%Y-%m-%d")

					delta = (datetime.now() - date).days
					average_month_day = 365.25 / 12
					delta_month = int(delta / average_month_day)
					delta_week = int(delta / 7)



					"""
					if delta_week >= self.user_settings["colorDictionnary"]["UserContactLongAlert"]["Delta"]:
						long_alert_list.append(studio_name)

					if (delta_week >= self.user_settings["colorDictionnary"]["UserContactMediumAlert"]["Delta"]) and (delta_week < self.user_settings["colorDictionnary"]["UserContactLongAlert"]["Delta"]):
						medium_alert_list.append(studio_name)

					if (delta_week >= self.user_settings["colorDictionnary"]["UserContactShortAlert"]["Delta"]) and (delta_week < self.user_settings["colorDictionnary"]["UserContactMediumAlert"]["Delta"]):
						short_alert_list.append(studio_name)

					else:
						no_alert_list.append(studio_name)
					"""



					#CREATION OF ALERT LIST
					alert_data = self.user_settings["colorDictionnary"]

					if delta_week < alert_data["UserContactShortAlert"]["Delta"]:
						no_alert_list.append(studio_name)

					elif (delta_week >= alert_data["UserContactShortAlert"]["Delta"]) and (delta_week < alert_data["UserContactMediumAlert"]["Delta"]):
						short_alert_list.append(studio_name)

					elif (delta_week >= alert_data["UserContactMediumAlert"]["Delta"]) and (delta_week < alert_data["UserContactLongAlert"]["Delta"]):
						medium_alert_list.append(studio_name)

					else:
						long_alert_list.append(studio_name)

					



			#concatenate all list
			self.list_studiolist_display = long_alert_list + medium_alert_list + short_alert_list + no_alert_list + not_contacted_list


		self.update_studiolist_view()








	def update_studiolist_view(self):


		#FOR EACH STUDIO IN THE STUDIO LIST ADD IT TO THE LIST WITH THE RIGHT COLOR
		for studio in self.list_studiolist_display:



			#UPDATE THE FILTERED STUDIO LIST 
			#remove unwanted informations from studio
			#remove capital letters / accents
			#self.list_studiolist_filtered.append(unidecode.unidecode(studio).lower())
			#self.display_message_function(self.list_studiolist_filtered[-1])




			studio_data = self.company_dictionnary[studio]

			label = Label(studio)

			self.listview_studiolist.append(ListItem(label))


			#CHECK FOR COLORS
			if ("CompanyDate" not in studio_data) or (studio_data["CompanyDate"] == None):
				#label.styles.color = self.color_dictionnary[self.color_theme]["notContacted"]
				label.classes = "label_primary"
			else:
				date = self.company_dictionnary[studio]["CompanyDate"]

				if type(date) == str:
					date = pendulum.parse(date).to_date_string()
					date = datetime.strptime(date, "%Y-%m-%d")

				delta = (datetime.now() - date).days
				average_month_day = 365.25 / 12
				delta_month = int(delta / average_month_day)
				delta_week = int(delta / 7)




				alert_data = self.user_settings["colorDictionnary"]
					
				if delta_week < alert_data["UserContactShortAlert"]["Delta"]:
					pass

				elif (delta_week >= alert_data["UserContactShortAlert"]["Delta"]) and (delta_week < alert_data["UserContactMediumAlert"]["Delta"]):
					label.styles.color = self.user_settings["colorDictionnary"]["UserContactShortAlert"]["Color"]

				elif (delta_week >= alert_data["UserContactMediumAlert"]["Delta"]) and (delta_week < alert_data["UserContactLongAlert"]["Delta"]):
					label.styles.color = self.user_settings["colorDictionnary"]["UserContactMediumAlert"]["Color"]

				else:
					label.styles.color = self.user_settings["colorDictionnary"]["UserContactLongAlert"]["Color"]

					
				

				

			#app.refresh_css()




			


















		




	
	



			
		




#check if admin function
def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False











#launch the application
if __name__ == "__main__":


	#check if the program is launched as admin
	if is_admin():
		print("Admin rights checked")
		app = POST_Application()
		app.run()
	else:
		print("Asking for admin rights...")

		ctypes.windll.shell32.ShellExecuteW(
			None, "runas", sys.executable, " ".join(sys.argv), None, 1
		)