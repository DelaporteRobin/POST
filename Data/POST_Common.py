import os
import sys
import time 
from groq import Groq
import re 
import dns.resolver
import pendulum
import smtplib
import pyfiglet
import requests

from functools import partial

from termcolor import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
		os.makedirs("C:/Program Files/@RCHIVE/Data/User/", exist_ok=True)
		try:

			with open(os.path.join(os.getcwd(), "C:/Program Files/@RCHIVE/Data/User/UserCompanyData.json"), "w") as save_file:
				json.dump(self.app.company_dictionnary, save_file, indent=4)

		
		except Exception as e:
			self.display_error_function("Impossible to save dictionnary\n%s"%e)
			return False
		else:
			self.display_message_function("Dictionnary saved")
			return True





	def load_company_dictionnary_function(self):
		#COMMON FOLDER LOCATION FOR USER SETTINGS IS C:/Program Files
		try:
			with open(os.path.join("C:/Program Files/@RCHIVE/Data/User/UserCompanyData.json"), "r") as read_file:
				self.app.company_dictionnary = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load company dictionnary\n%s"%e)
		else:
			self.display_message_function("Company dictionnary loaded")
			#self.display_message_function(self.app.company_dictionnary)
			pass
		"""
		try:	
			with open(os.path.join(os.getcwd(), "Data/User/UserCompanyData.json"), "r") as read_file:
				self.app.company_dictionnary = json.load(read_file)
		
		except Exception as e:
			self.display_error_function("Impossible to load company dictionnary\n%s"%e)
		else:
			#self.display_message_function("Company dictionnary loaded")
			pass
		"""





	def add_company_function(self):
		self.display_message_function(self.date)
		#get informations
		company_informations = {
			#"CompanyName":self.query_one("#modal_newcompanyname").value,
			"CompanyLocation":self.query_one("#modal_newcompanylocation").value,
			"CompanyWebsite":self.query_one("#modal_newcompany_website").value,
			"CompanyAnswer":None,
			"CompanyContact":None,
			"CompanyDetails":self.newcompany_details.text,
			"CompanyDate":None,
			"CompanyTags":[],
		}


		#get tags and split content
		tags_value = self.newcompany_tags.value.replace(" ", "").split(";")
		company_informations["CompanyTags"] = tags_value


		#DATE MODICATION
		date_value = self.modal_dateselect.date
		self.display_message_function(date_value)

		if self.newcompany_contacted_checkbox.value == True:
			company_informations["CompanyDate"] = str(date_value)
		"""
		if checkbox == True and date == None --> self.date
		if checkbox == False --> None
		if checbox == True and date != None --> get date value
		"""
		"""
		if self.newcompany_contacted_checkbox.value == True:
			if company_informations["CompanyDate"]==None:
				company_informations["CompanyDate"] = str(self.date)
		"""


		if self.query_one("#modal_newcompany_answer").value == 1:
			company_informations["CompanyAnswer"] = True
		elif self.query_one("#modal_newcompany_answer").value == 2:
			company_informations["CompanyAnswer"] = False
		elif self.query_one("#modal_newcompany_answer").value == 3:
			company_informations["CompanyAnswer"] = None
		else:
			company_informations["CompanyAnswer"] = self.query_one("#modal_newcompany_otheranswer").text

		contact_type_list = self.query("#modal_newcontacttype")
		contact_name_list = self.query("#modal_newcontactname")
		contact_mail_list = self.query("#modal_newcontactmail")
		contact_website_list = self.query("#modal_newcontactwebsite")


		if len(contact_name_list) != len(contact_mail_list):
			self.display_error_function("Error trying to get contact informations")
			return
		else:

			general_dictionnary = {}
			job_dictionnary = {}
			member_dictionnary = {}
			

			for i in range(len(contact_type_list)):
				self.display_message_function(contact_type_list[i].value)

				dictionnary = {
					"mail": contact_mail_list[i].value,
					"website": contact_website_list[i].value
				}

				if contact_type_list[i].value == "GENERAL":
					general_dictionnary[contact_name_list[i].value] = dictionnary 
				elif contact_type_list[i].value == "MEMBER":
					member_dictionnary[contact_name_list[i].value] = dictionnary
				elif contact_type_list[i].value == "JOB":
					job_dictionnary[contact_name_list[i].value] = dictionnary
				else:
					pass



			contact_dictionnary = {
				"GENERAL": general_dictionnary,
				"JOB": job_dictionnary,
				"MEMBER":member_dictionnary
			}


			#replace the value in the company dictionnary
			company_informations["CompanyContact"] = contact_dictionnary


			#replace the value in the company dictionnary and save the new dictionnary
			if (self.mode != "edit") and (self.query_one("#modal_newcompanyname").value in self.app.company_dictionnary):
				self.display_error_function("That company is already registered in the dictionnary")
			else:
				self.app.company_dictionnary[self.query_one("#modal_newcompanyname").value] = company_informations
				value = self.save_company_dictionnary_function()
				#update the value in interface
				self.app.update_informations_function()




	def delete_company_function(self):
		#studio = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
		studio = self.list_studiolist_display[self.listview_studiolist.index]
		try:
			del self.company_dictionnary[studio]
		except:
			self.display_error_function("Impossible to remove studio")
			return
		else:
			self.display_message_function("Studio removed")
			self.save_company_dictionnary_function()
			self.update_informations_function()







	def load_company_data_function(self, Modal_Contact):
		self.display_message_function(self.studio)
		try:
			studio_data = self.app.company_dictionnary[self.studio]
		except:
			self.display_error_function("Impossible to get studio data")
		else:
			self.newcompany_name.value = self.studio 
			self.newcompany_location.value = studio_data["CompanyLocation"]
			self.newcompany_website.value = studio_data["CompanyWebsite"]
			self.newcompany_tags.value = ";".join(studio_data["CompanyTags"])

			try:
				if self.letter_verification_function(studio_data["CompanyDetails"]) == False:
					self.newcompany_details.insert("-")
				else:
					self.newcompany_details.text = studio_data["CompanyDetails"]
			except:
				self.newcompany_details.insert("-")

			#self.display_message_function(studio_data)
			if "CompanyDate" in studio_data:
				if studio_data["CompanyDate"] != None:
					self.newcompany_contacted_checkbox.value = True
					self.query_one("#modal_collapsible_dateselector").disabled = False
					self.query_one("#modal_collapsible_dateselector").title = studio_data["CompanyDate"]

					if type(studio_data["CompanyDate"]) == str:
						self.modal_dateselect.date = pendulum.parse(studio_data["CompanyDate"])
					else:
						self.modal_dateselect.date = studio_data["CompanyDate"]
				else:
					self.newcompany_contacted_checkbox.value = False
					
					self.query_one("#modal_collapsible_dateselector").title = ""
					self.query_one("#modal_collapsible_dateselector").disabled = True
			else:
				self.newcompany_contacted_checkbox.value = False
					
				self.query_one("#modal_collapsible_dateselector").title = "Last time company was reached :"
				self.query_one("#modal_collapsible_dateselector").disabled = True
					



			if studio_data["CompanyAnswer"] == True:
				self.newcompany_answer.value = 1
			elif studio_data["CompanyAnswer"] == False:
				self.newcompany_answer.value = 2
			elif studio_data["CompanyAnswer"] == None:
				self.newcompany_answer.value = 3
			else:
				self.newcompany_otheranswer.disabled=False
				self.newcompany_answer.value = 4
				self.newcompany_otheranswer.text = studio_data["CompanyAnswer"]


			#LOAD CONTACTS IN PAGE
			"""
			if studio_data["CompanyContact"] != None:
				for i in range(len(list(studio_data["CompanyContact"].keys()))):

					#self.display_message_function(i)
					contact_name = list(studio_data["CompanyContact"].keys())[i]
					contact_mail = studio_data["CompanyContact"][contact_name]["mail"]
					contact_website = studio_data["CompanyContact"][contact_name]["website"]

					#self.display_message_function(contact_name)
					new_contact = Modal_Contact("JOB", contact_name, contact_mail, contact_website)
					self.newcompany_contactlist_container.mount(new_contact)
			"""
			if studio_data["CompanyContact"] != None:
				for contact_type, contact in studio_data["CompanyContact"].items():
					for c_name, c_data in contact.items():

						contact_name = c_name
						contact_mail = c_data["mail"]
						contact_website = c_data["website"]

						new_contact = Modal_Contact(contact_type, contact_name, contact_mail, contact_website)
						self.newcompany_contactlist_container.mount(new_contact)








	def generate_markdown_function(self, company_name, company_data):
		markdown = """
# Company name : __%s__

- Company location : %s
"""%(company_name, company_data["CompanyLocation"])


		try:
			if self.letter_verification_function(company_data["CompanyDetails"])==True:
				#try to split the list of elements
				markdown+= "\n# More informations about the company\n"
				details_list = company_data["CompanyDetails"].split("-")

				for detail in details_list:
					if self.letter_verification_function(detail)==True:
						markdown += "- %s\n"%detail
		except:
			pass

		
		if company_data["CompanyAnswer"] not in [True, False, None]:
			markdown += """

> [!WARNING]
> Answer is different : %s
"""%(company_data["CompanyAnswer"])
		
		elif company_data["CompanyAnswer"] == True:
			markdown += """
> [!IMPORTANT]
> The company said Yes
"""
		elif company_data["CompanyAnswer"] == False:
			markdown += """
> [!ERROR]
> The company said No
"""
		else:
			markdown += """
No answer from the company
"""
		


		#CONTACT PART
		markdown += """
Website of the company : [%s](%s)
"""%(company_name, company_data["CompanyWebsite"])


		if "CompanyDate" in company_data:
			markdown += "Last time the studio was contacted : %s\n\n"%company_data["CompanyDate"]
			#get the time difference with today
			today = datetime.now()
			date = company_data["CompanyDate"]

			if date != None:
				if type(date) == str:
					date = pendulum.parse(date).to_date_string()
					date = datetime.strptime(date, "%Y-%m-%d")
				

				delta = (today - date).days
				if delta > 7:
					markdown += "\nIt was %s week(s) ago" % int(delta/7)
				else:
					markdown += "\nIt was %s day(s) ago" % delta

				#self.display_message_function((today - date).days)
			

		markdown += """
## Contact from the company 
"""
		if company_data["CompanyContact"] != {}:
			for contact_type, contact in company_data["CompanyContact"].items():
				
				if contact != {}:
					markdown += "CONTACT - %s\n"%contact_type
					for c_name, c_data in contact.items():
						markdown+="""
%s\n
- mail : %s\n
- website : %s\n
"""%(c_name,c_data["mail"], c_data["website"])
				
		else:
			markdown += """
> [!WARNING]
> No contact from that company!
"""


		

		return markdown





	def letter_verification_function(self, text):
		letter = "abcdefghijklmnopqrstuvwxyz"
		capital = letter.upper()
		figure = "0123456789"

		list_letter = list(letter)
		list_capital = list(capital)
		list_figure = list(figure)


		list_text = list(text)
		if len(list_text) == 0:
			return False 
		else:
			for i in range(len(list_text)):
				if (list_text[i] in list_letter) or (list_text[i] in list_capital) or (list_text[i] in list_figure):
					return True 
			return False






	def create_mail_preset_function(self):
		#get the content in the field
		preset_name = self.input_presetname.value
		preset_content = self.textarea_mail.text

		if (self.letter_verification_function(preset_name) == False) or (self.letter_verification_function(preset_content)==False):
			self.display_error_function("You have to enter a name and a content for the mail preset")
			return

		#self.display_message_function(preset_content)


		#check if the preset is not already registered in the dictionnary
		if "mailPreset" not in self.user_preset:
			self.user_preset["mailPreset"] = {}
		if preset_name not in list(self.user_preset["mailPreset"].keys()):
			#self.user_preset[preset_name] = preset_content
			preset_list = self.user_preset["mailPreset"]
			preset_list[preset_name] = preset_content
			self.user_preset["mailPreset"] = preset_list
			self.save_mail_preset_function()
			self.update_informations_function()
		else:
			self.display_error_function("A preset with the same name is already registered")



	def load_mail_preset_function(self):
		try:
			with open("C:/Program Files/@RCHIVE/Data/User/UserPreset.json", "r") as read_file:
				self.user_preset = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load mail presets\n%s"%e)
		else:
			#self.display_message_function("Presets loaded")
			#self.display_message_function(self.user_preset)
			pass




	def save_mail_preset_function(self):
		os.makedirs("C:/Program Files/@RCHIVE/Data/User/", exist_ok=True)
		try:
			with open("C:/Program Files/@RCHIVE/Data/User/UserPreset.json", "w") as save_file:
				json.dump(self.user_preset, save_file, indent=4)
		except Exception as e:
			self.display_error_function("Impossible to save preset\n%s"%e)
		else:
			self.display_message_function("Preset saved")





	def save_user_settings_function(self):
		os.makedirs("C:/Program Files/@RCHIVE/Data/User/", exist_ok=True)
		try:
			with open("C:/Program Files/@RCHIVE/Data/user/UserSettings.json", "w") as save_file:
				json.dump(self.app.user_settings, save_file, indent=4)
		except Exception as e:
			self.app.display_error_function("Impossible to save user settings\n%s"%e)
			return
		else:
			self.app.display_message_function("User settings saved")




	def load_user_settings_function(self):
		try:
			with open("C:/Program Files/@RCHIVE/Data/user/UserSettings.json", "r") as read_file:
				self.app.user_settings = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load user settings\n%s"%e)
		else:
			#self.display_message_function("User settings loaded")
			pass
					





	def generate_with_copilot_function(self):

		prompt_format = ""
		self.display_message_function("Starting to generate...")
		prompt_format = self.generate_prompt_function_v2()
		prompt_textarea_content = self.textarea_prompt.text
	
		
		with open(os.path.join(os.getcwd(), "prompt.txt"), "w") as save_file:
			save_file.write("\n\n%s"%prompt_format)


		
		try:
			#try:
			#try to create the client for groq
			client = Groq(
				api_key = os.environ.get("GROQ_API_KEY"),
				)

			chat_completion = client.chat.completions.create(
			    messages=[
			        {
			            "role": "system",
			            "content": prompt_format.encode("utf-8").decode("utf-8"),
			        },
			        {
			        	"role":"user",
			        	"content": prompt_textarea_content.encode("utf-8").decode("utf-8")
			        }
			    ],
			    model="mixtral-8x7b-32768",
			)
			with open(os.path.join(os.getcwd(), "generated.txt"), "w") as save_file:
				save_file.write(chat_completion.choices[0].message.content)

			
		except Exception as e:
			self.display_error_function("Impossible to use generation model API\n%s"%e)
		else:
			#replace the value of the text in the mail text area
			self.textarea_mail.clear()
			self.textarea_mail.insert(chat_completion.choices[0].message.content)
			
		

				
			
			









	def generate_prompt_function_v2(self):



		prompt_content = self.textarea_prompt.text
		user_settings = self.user_settings["UserPromptDetails"]

		try:
			studio_name = self.list_studiolist_display[self.listview_studiolist.index]
			studio_data = self.company_dictionnary[studio_name]
		except TypeError:
			self.display_error_function("No studio selected")
			return
		else:
			pass

		try:
			preset_selected = self.user_preset["mailPreset"][list(self.user_preset["mailPreset"].keys())[self.listview_mailpreset.index]]
		except:
			self.display_error_function("Impossible to get mail preset!")
			return
		else:
			#self.display_message_function(preset_selected)
			pass

		prompt_format = """

Ignore all instructions before this one.
You are a [%s], 
Your task is now to write an email to find a job.

your email should be attractive and make people want to find out more about you. So don't be too kissy or sweet in your email, just be PROFESSIONAL.
"""%(self.user_settings["UserJobSearched"])
		

		


		if type(user_settings)==list and (len(user_settings)!=0):
			prompt_format += """
. In your email try to include these informations about yourself (which are important for getting to know you): \n
"""
			for user_data in user_settings:
				if self.letter_verification_function(user_data)==True:
					prompt_format+="\n- %s"%user_data

			prompt_format += """

[WARNING] You don't have to include all the informations, try to don't talk too much about yourself!
"""
		
		prompt_format += """

. HERE IS THE COMPANY YOU ARE WRITING TO : %s
"""%(studio_name)

		
		try:
			if self.letter_verification_function(studio_data["CompanyDetails"]) == True:

				prompt_format += """

. Here are a few details about the studio to help you with your writing : 

[
"""
				#get the list of elements
				studio_data_list = studio_data["CompanyDetails"].split("\n")
				for info in studio_data_list:
					if self.letter_verification_function(info)==True:
						prompt_format+="\n-%s"%info
				prompt_format += """
]
"""
		except:
			pass



		if self.letter_verification_function(preset_selected) == True:
			prompt_format += """

. Here are some details / elements / turn of phrase that you can try incorporate in your mail : 

[
%s\n
]
"""%preset_selected


			prompt_format += """
[WARNING] you don't have to do it! You can also try to modify / shorten / lengthen this mail!
You also have the right to remove parts that are unecessary.

- INTEGRATE ALL ELEMENTS AS SMOOTHLY AS POSSIBLE
- AVOID REPETITIONS 
"""
		return prompt_format











	def generate_prompt_function_v1(self):
				#get all informations
		"""
			the studio selected
			the preset selected (content)
			the prompt
			the user settings

			and generate a new mail with informations
		"""
		prompt_content = self.textarea_prompt.text
		user_settings = self.user_settings["UserPromptDetails"]
		studio_name = self.list_studiolist_display[self.listview_studiolist.index]
		studio_data = self.company_dictionnary[studio_name]

		try:
			preset_selected = self.user_preset["mailPreset"][list(self.user_preset["mailPreset"].keys())[self.listview_mailpreset.index]]
		except:
			self.display_error_function("Impossible to get mail preset!")
			return
		else:
			#self.display_message_function(preset_selected)
			pass

		prompt_format = """
%s\n\n

here is the mail preset you have to adapt : \n
%s\n\n

adapt the mail so it correspond if you send it to that company : %s\n
if you want more informations about this company to generate the mail, there is the website link : %s\n



"""%( prompt_content, preset_selected, studio_name, studio_data["CompanyWebsite"], )
		try:
			if self.letter_verification_function(self.user_settings["UserJobSearched"])==True:
				prompt_format+="note that you are looking / interested by these positions in the company : \n"

				for job in self.user_settings["UserJobSearched"]:
					if self.letter_verification_function(job) == True:
						prompt_format+="- %s\n"%job
		except:
			pass 



			
		try:
			if self.letter_verification_function(self.company_dictionnary[studio_selected]["CompanyDetails"])==True:
				prompt_format+="\nHere is a list of details about the company you want to contact,\nWhat they do, their style... : \n"
				details_list = self.company_dictionnary[studio_name]["CompanyDetails"].split("-")

				for detail in details_list:
					if self.letter_verification_function(detail)==True:
						prompt_format += "-%s\n"%detail
		except:
			pass



		if len(user_settings) > 0:

			prompt_format += """
Try if possible to integrate in this email these details about yourself a subtle way:\n
"""				
			for info in user_settings:
				if self.letter_verification_function(info)==True:
					prompt_format+="- %s\n"%info


		return prompt_format







	#check if email address is valid by syntax or domain?
	def check_address_function(self, content):
		pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

		if re.match(pattern, content):
			domain = content.split("@")[1]

			try:
				dns.resolver.resolve(domain, "MX")
				return True

			except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
				return False


		return False






	def get_contact_from_filter_function(self):
		#get value from select fields
		contacttype_index_list = (self.selectionlist_contacttype.selected)
		contacttag_index_list = (self.selectionlist_tags.selected)
		contactdelta_index_list = (self.selectionlist_delta.selected)

		contacttype_list = []
		for index in contacttype_index_list:
			contacttype_list.append(self.kind_list[index])

		contacttag_list = []
		for index in contacttag_index_list:
			contacttag_list.append(self.tag_list[index])

		contactdelta_list = []
		for index in contactdelta_index_list:
			contactdelta_list.append(list(self.user_settings["alertDictionnary"])[index])



		delta_studio_list = []

		if "RecentContact" in contactdelta_list:
			delta_studio_list.extend(self.short_alert_list)
		if "LatelyContact" in contactdelta_list:
			delta_studio_list.extend(self.medium_alert_list)
		if "PastContact" in contactdelta_list:
			delta_studio_list.extend(self.long_alert_list)
		if "NotContacted" in contactdelta_list:
			delta_studio_list.extend(self.not_contacted_list)


		self.display_message_function(delta_studio_list)

		#self.display_message_function(contacttype_list)
		#self.display_message_function(contacttag_list)


		contact_list = {}
		for studio_name, studio_data in self.company_dictionnary.items():

			if len(delta_studio_list) != 0:
				if studio_name not in delta_studio_list:
					continue
			#TAGS CONDITIONS
			#	-> if the tag list isn't empty -> check for tags
			#	-> if one of the studio tag is in the tag list

			studio_tags = studio_data["CompanyTags"]
			if len(contacttag_list) > 0:
				found=False

				for tag in studio_tags:
					if tag in contacttag_list:
						found=True
						break


			if (len(contacttag_list) == 0) or (found==True):
				for contact_type, contact_data in studio_data["CompanyContact"].items():

					if contact_type in contacttype_list:
						for c_name, c_data in contact_data.items():
							if self.letter_verification_function(c_data["mail"])==True:
								#contact_list.append(c_data["mail"].replace(" ", ""))
								contact_list["%s; %s"%(studio_name, c_data["mail"])] = {
									"studioName":studio_name,
									"contactName":c_name,
									"contactMail":c_data["mail"]
								}



		self.mail_contact_list = contact_list
		self.optionlist_contact.clear_options()
		self.optionlist_contact.add_options(list(contact_list.keys()))





	def send_mail_function(self):
		os.system("cls")
		print(colored("\n\n\n%s"%pyfiglet.figlet_format("MAIL PORTAL", font="the_edge"), "cyan"))

		#GET THE MAIL KEY
		try:
			with open("C:/Program Files/@RCHIVE/DATA/mail_key.dll", "r") as load_key:
				mail_key = load_key.read()
		except Exception as e:
			print(colored("Impossible to load key\n%s"%e, "red"))
			return
		else:
			print(colored("Key loaded", "green"))


		#SETUP THE SERVER
		smtp_server = "smtp.gmail.com"
		port = 587
		user_address = self.user_settings["UserMailAddress"]

		#GET THE MAIL CONTENT 
		mail_header = self.input_mail_header.value
		mail_body = self.textarea_mail.text

		if self.letter_verification_function(mail_header)==False or self.letter_verification_function(mail_body)==False:
			print(colored("MAIL BODY OR MAIL HEADER IS EMPTY!", "red"))
			os.system("pause")
			return

		if len(list(self.mail_contact_list.keys()))==0:
			print(colored("Contact list is empty!", "red"))
			os.system("pause")
			return

		#GET THE MAIL ATTACHED FILES
		attached_file = self.user_settings["UserMailAttached"]
		if os.path.isfile(attached_file)==False:
			print(colored("Attached file doesn't exists!", "red"))
			return




		#DISPLAY FINAL CHOICE TO THE USER BEFORE SENDING THE MAIL
		print(colored("Mail formatting ...", "cyan"))
		print(colored("Your address : ", "cyan"), user_address)
		print(colored("Mail header : ", "cyan"), mail_header)
		print(colored("Mail body :\n", "cyan"), mail_body)

		while True:
			print(colored("Are you sure you want to launch mail sender function?", "cyan"))
			user = input(colored("Y / N ", "magenta"))

			if user == "Y":
				break
			elif user == "N":
				return
			else:
				continue

		
		#SEND LOOP
		try:
			server = smtplib.SMTP(smtp_server, port)
			server.starttls()

			print("Server started ... \n%s"%server)
			print("User address : %s\nUser Key : %s"%(user_address, mail_key))


			server.login(user_address, mail_key)


			contact_list_length = len(list(self.mail_contact_list.keys()))
			i = 0


			header_proxy = mail_header 
			body_proxy = mail_body



			#BUILD THE MAIL
			for contact_name, contact_data in self.mail_contact_list.items():


				mail_header = header_proxy
				mail_body = body_proxy


				#REPLACE VARIABLES IN EMAIL BODY
				if ("[STUDIONAME]" in mail_header) or ("[STUDIONAME]" in mail_body):
					print("Studioname replaced in mail...")
					if contact_data["studioName"] in list(self.company_dictionnary.keys()):
						mail_header = mail_header.replace("[STUDIONAME]", contact_data["studioName"])
						mail_body = mail_body.replace("[STUDIONAME]", contact_data["studioName"])
					else:
						print(colored("Studio skipped because impossible to replace variables!", "red"))
						continue

				if ("[DEMO_LINK]" in mail_header) or ("[DEMO_LINK]" in mail_body):
					print("DemoLink replaced in mail...")
					mail_header = mail_header.replace("[DEMO_LINK]", str(self.user_settings["UserDemoReelLink"]))
					mail_body = mail_body.replace("[DEMO_LINK]", str(self.user_settings["UserDemoReelLink"]))

				if ("[DEMO_PASSWORD]" in mail_header) or ("[DEMO_PASSWORD]" in mail_body):
					print("DemoPassword replaced in mail...")
					mail_header = mail_header.replace("[DEMO_PASSWORD]", str(self.user_settings["UserDemoReelPassword"]))
					mail_body = mail_body.replace("[DEMO_PASSWORD]", str(self.user_settings["UserDemoReelPassword"]))




				msg = MIMEMultipart()
				msg["From"] = user_address
				msg["To"] = contact_data["contactMail"]
				msg["Subject"] = mail_header 


				print(colored("[%s / %s] NEW MAIL CREATED"%(i, contact_list_length), "cyan"))
				content = """
To : %s
"""%(contact_data["contactMail"])

				body = mail_body
				msg.attach(MIMEText(body))

				try:
					with open(attached_file, "rb") as attach:
						part = MIMEBase("application", "octet-stream")
						part.set_payload(attach.read())

				except Exception as e:
					print(colored("Impossible to read external file and link it to mail\n%s"%e, "red"))
				else:
					encoders.encode_base64(part)
					part.add_header(
						"Content-Disposition",
						f"attachment; filename = {attached_file}",
					)

					msg.attach(part)
					print(colored("External file attached to mail : %s"%attached_file))

				try:
					server.sendmail(user_address, contact_data["contactMail"], msg.as_string())
				except Exception as e:
					print(colored("Impossible to send mail\n%s"%e, "red"))
				else:
					

					#get date to update user dictionnary (last time contacted)		
					if contact_data["studioName"] in list(self.company_dictionnary.keys()):
						#get today date
						date_value = pendulum.parse(str(datetime.now()))
						#get data
						studio_data = self.company_dictionnary[contact_data["studioName"]]
						studio_data["CompanyDate"] = str(date_value)

						print("Date refreshed in user data...")





					print(colored("MAIL SENT : %s\n\n"%contact_data["contactMail"], "green"))
				i+=1



			server.quit()
		except Exception as e:
			print(colored("Impossible to connect to server\n%s"%e, "red"))
		else:
			print(colored("TASK DONE", "cyan"))
		

		os.system("pause")









	def check_user_informations_function(self):
		#get all informations in textfield
		user_address = self.input_useraddress.value
		user_mailkey = self.input_mailkey.value
		user_demolink = self.input_demolink.value 
		user_demopassword = self.input_demopassword.value 
		user_resume = self.input_resume.value

		if self.check_address_function(user_address)==False:
			self.display_error_function("Invalid email address")
		else:
			self.user_settings["UserAddress"] = user_address
			

		if self.letter_verification_function(user_mailkey)==False:
			self.display_error_function("Mail key is empty!")
			
		else:
			self.user_settings["UserMailKey"] = user_mailkey

		#check the connection with demoreel link
		try:
			response = requests.get(user_demolink, timeout=5)
		except:
			self.display_error_function("Invalid DemoReel link!")
		else:
			self.display_message_function("DemoReel link checked")
			self.user_settings["UserDemoReelLink"] = user_demolink

		if self.letter_verification_function(user_demopassword) == False:
			self.user_settings["UserDemoPassword"] = None

		if os.path.isfile(user_resume)==False:
			self.display_error_function("Invalid filepath for Resume!")
			return 
		else:
			self.user_settings["UserMailAttached"] = user_resume





