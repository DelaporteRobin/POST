import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders

import os



#read password
try:
	with open("D:/WORK/PYTHON/mail_key.dll", "r") as read_file:
		key = read_file.read()
except:
	print("impossible to load key")
else:
	print("key loaded")


smtp_server = "smtp.gmail.com"
port = 587
sender = "robindelaporte1207@gmail.com"
password = key
receiver = "metalleux1207@gmail.com"


msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Test mail"


body = """
Just my python script who wanted to say hello!
"""

msg.attach(MIMEText(body))







#ATTACH FILE TO THE MAIL
filename = "d:/work/personnal/resume/output/resume_delaporterobin_24-11_compressed.pdf"
if os.path.isfile(filename)==True:

	print("external file exists on computer!")

	try:
		with open(filename, "rb") as attach:
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attach.read())

	except Exception as e:
		print("Impossible to load external file and link it to mail\n%s"%e)
	else:
		encoders.encode_base64(part)
		part.add_header(
			"Content-Disposition",
			f"attachment; filename = {filename}",
		)

		msg.attach(part)
		print("External file linked to mail")
else:
	print("External file doesn't exists!")








print("mail created")


try:
	server = smtplib.SMTP(smtp_server, port)
	server.starttls()


	server.login(sender, password)


	server.sendmail(sender, receiver, msg.as_string())



	server.quit()


except Exception as e:
	print("Failed to send email\n%s"%e)

else:
	print("Mail sent")
