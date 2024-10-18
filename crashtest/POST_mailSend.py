import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




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
This is a test mail content:
Hello World
"""
msg.attach(MIMEText(body, "plain"))


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
