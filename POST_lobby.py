import os
import sys
import time 
import re
import dns.resolver
import webbrowser
import pendulum
import pyperclip 

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
				yield Button("Add contact", id="modal_addcontacttolist_button")
				yield Button("Remove contact", id="modal_removecontactfromlist_button")
			
			self.newcompany_contactlist_container = ScrollableContainer(id="modal_newcompany_contactlist")
			yield self.newcompany_contactlist_container



			yield Rule(line_style="double")

			with Horizontal(id="modal_horizontal_container"):
				if self.mode == "create":
					yield Button("Create", variant="primary", id="modal_create_contact_button")
				else:
					yield Button("Save", variant="primary", id="modal_create_contact_button")
				yield Button("Quit", variant="error", id="modal_cancel_contact_button")


		
	

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

		
			self.input_usersettingsjob = Input(placeholder = "What job are you looking for", id="input_usersettingsjob")
			yield self.input_usersettingsjob

			self.textarea_usersettings = ExtendedTextArea(id="textarea_usersettings")
			yield self.textarea_usersettings
			

			yield Rule(line_style="double")

			with Horizontal(id="modal_usersettings_horizontal_container"):
				yield Button("Save", variant="primary", id="modal_usersettings_button_save")
				yield Button("Quit", variant="error", id="modal_usersettings_button_quit")


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
			if self.letter_verification_function(self.input_usersettingsjob.value) == True:
				self.app.user_settings["UserJobSearched"] = self.input_usersettingsjob.value.split("/")

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
			self.input_usersettingsjob.value = "/".join(self.app.user_settings["UserJobSearched"])
		except:
			pass

	
























class POST_Application(App, POST_CommonApplication):


	CSS_PATH = ["Data/Styles/Dark_Theme.tcss", "Data/Styles/Global.tcss"]


	def __init__(self):
		super().__init__()



		self.company_dictionnary = {}
		self.user_settings = {}
		self.user_preset = {}

		self.list_studiolist_display = []

		self.color_theme = "Dark_Theme"
		self.color_dictionnary = {
			"Dark_Theme": {
				"notContacted": "#6a5f83",
				"contactDateShortAlert": "#ad761b",
				"contactDateLongAlert": "#ad361b",
			}
		}


		#self.load_company_dictionnary_function()




	def compose(self) -> ComposeResult:

		yield Header(show_clock=True)


		with Horizontal(id="main_horizontal_container"):

			with Vertical(id="left_vertical_container"):
				yield Button("USER INFOS", id="button_userinfos")
				yield Button("ADD CONTACT", id="button_addcontact")
				yield Button("EDIT CONTACT", id="button_editcontact")
				yield Button("DELETE CONTACT", id="button_deletecontact", variant="error")

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
						yield Button("Use copilot", id="button_usecopilot")

						yield Rule()

						yield Button("Copy content", id="button_copycontent")

						self.listview_mailpreset = ListView(id="listview_mailpreset")
						yield self.listview_mailpreset
						self.listview_mailpreset.border_title = "Preset list"
					
					with Vertical(id="right_mailtext_container"):
						with Collapsible(title="Copilot settings", id="right_mailprompt_collapsible"):
							self.textarea_prompt = TextArea(id="textarea_prompt")
							yield self.textarea_prompt
							self.textarea_prompt.border_title = "Copilot prompt"

							with Horizontal(id="right_mailtext_horizontal"):
								yield Button("Save copilot prompt", id="button_saveprompt")
						self.textarea_mail = TextArea(id="textarea_mail")
						yield self.textarea_mail
						self.textarea_mail.border_title = "Mail"


	def on_mount(self) -> None:
		self.update_informations_function()


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









	async def on_key(self, event: events.Key) -> None:

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
















	
	



	def update_informations_function(self):
		
		self.listview_studiolist.clear()
		self.listview_mailpreset.clear()
		self.textarea_prompt.clear()
		#self.datatable_studiolist.clear()

		self.load_company_dictionnary_function()
		self.load_mail_preset_function()
		self.load_user_settings_function()

		if "CopilotPrompt" in self.user_preset:
			self.textarea_prompt.insert(self.user_preset["CopilotPrompt"])

		#self.display_message_function(self.company_dictionnary)
		self.display_message_function("UPDATE")


		#rows = ["Location", "Company"]
		#self.datatable_studiolist.add_columns(*rows)
		self.list_studiolist_display = []

		if self.user_settings["companyDisplayMode"] != 2:
		
			if ("companyDisplayMode" not in self.user_settings) or (self.user_settings["companyDisplayMode"] == 1):
				studio_list = list(self.company_dictionnary.keys())
				
			elif self.user_settings["companyDisplayMode"] == 0:
				studio_list = list(self.company_dictionnary.keys())
				studio_list.sort(key = str.lower)

			i = 0
			for studio in studio_list:
				studio_data = self.company_dictionnary[studio]

				label = Label("[ %s ] %s"%(studio_data["CompanyLocation"], studio))

				
				if "CompanyDate" not in studio_data:
					label.styles.background = self.color_dictionnary[self.color_theme]["notContacted"]
				else:
					#get the date
					date = studio_data["CompanyDate"]

					if date != None:
						if type(date) == str:
							date = pendulum.parse(date).to_date_string()
							date = datetime.strptime(date, "%Y-%m-%d")
						
						delta = (datetime.now() - date).days
						average_month_day = 365.25 / 12
						delta_month = int(delta / average_month_day)
						
						if delta_month >= self.user_settings["UserContactDateAlert"]:
							label.styles.background = self.color_dictionnary[self.color_theme]["contactDateShortAlert"]
						if delta_month >= int(self.user_settings["UserContactDateAlert"] * 2):
							label.styles.background = self.color_dictionnary[self.color_theme]["contactDateLongAlert"]
					else:
						pass


				#self.datatable_studiolist.add_row(value["CompanyLocation"], key, height=1, key = i,label=Text("hello"))
				self.listview_studiolist.append(ListItem(label))
				self.list_studiolist_display.append(studio)
				i+=1


		else:
			studio_list = list(self.company_dictionnary.keys())

			notcontacted_list = []
			shortalert_list = []
			longalert_list = []
			noalert_list = []

			for studio in studio_list:
				if "CompanyDate" not in self.company_dictionnary[studio]:
					notcontacted_list.append(studio)
					continue

				else:
					date = self.company_dictionnary[studio]["CompanyDate"]


					if date != None:
						if type(date) == str:
							date = pendulum.parse(date).to_date_string()
							date = datetime.strptime(date, "%Y-%m-%d")
						delta = (datetime.now() - date).days
						average_month_day = 365.25 / 12
						delta_month = int(delta / average_month_day)

						if delta_month >= int(self.user_settings["UserContactDateAlert"] * 2):
							longalert_list.append(studio)
						elif delta_month >= self.user_settings["UserContactDateAlert"]:
							shortalert_list.append(studio)
						else:
							noalert_list.append(studio)

					

				

			for studio in longalert_list:
				studio_data = self.company_dictionnary[studio]
				label = Label("[ %s ] %s"%(studio_data["CompanyLocation"], studio))
				label.styles.background = self.color_dictionnary[self.color_theme]["contactDateLongAlert"]
				self.listview_studiolist.append(ListItem(label))
				self.list_studiolist_display.append(studio)

			for studio in shortalert_list:
				studio_data = self.company_dictionnary[studio]
				label = Label("[ %s ] %s"%(studio_data["CompanyLocation"], studio))
				label.styles.background = self.color_dictionnary[self.color_theme]["contactDateShortAlert"]
				self.listview_studiolist.append(ListItem(label))
				self.list_studiolist_display.append(studio)

			for studio in notcontacted_list:
				studio_data = self.company_dictionnary[studio]
				label = Label("[ %s ] %s"%(studio_data["CompanyLocation"], studio))
				label.styles.background = self.color_dictionnary[self.color_theme]["notContacted"]
				self.listview_studiolist.append(ListItem(label))
				self.list_studiolist_display.append(studio)

			for studio in noalert_list:
				studio_data = self.company_dictionnary[studio]
				label = Label("[ %s ] %s"%(studio_data["CompanyLocation"], studio))
				#label.styles.background = self.color_dictionnary[self.color_theme]["notContacted"]
				self.listview_studiolist.append(ListItem(label))
				self.list_studiolist_display.append(studio)





		
		


		try:
			for key, value in self.user_preset["mailPreset"].items():
				self.listview_mailpreset.append(ListItem(Label(key)))
		except:
			pass


			
		








#launch the application
if __name__ == "__main__":
	app = POST_Application()
	app.run()