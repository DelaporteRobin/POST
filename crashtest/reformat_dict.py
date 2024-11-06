import os
import colorama
import json

from termcolor import *


colorama.init()







def letter_verification_function(content):
	try:
		list_conttent = list(content)
	except:
		return False

	if len(content) == 0:
		return False

	letter = "abcdefghijklmnopqrstuvwxyz"
	figure = "0123456789"

	list_letter = list(letter)
	list_capital = list(letter.upper())
	list_figure = list(figure)

	

	for i in range(len(content)):
		if (content[i] in list_letter) or (content[i] in list_capital) or (content[i] in list_figure):
			return True


	return False






filename = "c:/Program Files/@RCHIVE/DATA/USER/UserCompanyData.json"


if os.path.isfile(filename)==False:
	print("Impossible to find file")


else:
	print("File found!")



	with open(filename, "r") as read_file:
		data = json.load(read_file)


	for studio_name, studio_data in data.items():
		print(colored("recreating contacts for [%s]"%studio_name, "yellow"))

		company_old_contact = studio_data["CompanyContact"]

		general_dictionnary = {}
		job_dictionnary = {}
		member_dictionnary = {}

		for contact_name, contact_content in company_old_contact.items():
			job_checklist = ["job", "jobs", "careers", "recrutement"]

			found=False

			for job_key in job_checklist:
				if (job_key in contact_name.lower()) or (job_key in contact_content["mail"].lower()):
					found = True
					break


			if found==True:
				print("job contact : %s"%contact_name)
				job_dictionnary[contact_name] = {
					"mail": contact_content["mail"],
					"website": contact_content["website"],
				}
			else:
				if letter_verification_function(contact_name)==True:
					print("general contact : %s"%contact_name)
					general_dictionnary[contact_name] = {
						"mail": contact_content["mail"],
						"website": contact_content["website"],
					}
				else:
					print(colored("Contact skipped because empty!", "red"))


		studio_data["CompanyContact"] = {
			"GENERAL": general_dictionnary,
			"JOB": job_dictionnary, 
			"MEMBER": member_dictionnary
		}


		data[studio_name] = studio_data

	print(colored("\nDone formating dictionnary", "magenta"))




	try:
		with open(filename, "w") as save_file:
			json.dump(data, save_file, indent=4)
	except Exception as e:
		print(colored("Impossible to save\n%s"%e, "red"))
	else:
		print(colored("saved", "yellow"))

			



	"""
	FOR EACH CONTACT IN THE DICTIONNARY
	create a new contact key in the dictionnary
		-> each address containing job, jobs, careers, recrutement -> JOB
		-> contact, hello -> GENERAL
	"""