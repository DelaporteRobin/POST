import imaplib
import email
import colorama

from termcolor import *
from email.header import decode_header

colorama.init()




#read password
try:
    with open("D:/WORK/PYTHON/mail_key.dll", "r") as read_file:
        key = read_file.read()
except:
    print("impossible to load key")
else:
    print("key loaded")



# Configuration des détails de connexion
imap_server = "imap.gmail.com"  # Serveur IMAP de Gmail
email_user = "robindelaporte1207@gmail.com"
password = key  # Utilisez un mot de passe d'application

# Se connecter au serveur IMAP
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(email_user, password)

# Sélectionner la boîte de réception (INBOX)
mail.select("inbox")

# Rechercher les emails (Ici on récupère tous les emails non supprimés)
status, messages = mail.search(None, "ALL")

# Convertir la liste d'emails reçus en une liste de numéros d'ID d'emails
mail_ids = messages[0].split()



# Récupérer un nombre limité de mails récents (par exemple, les 5 derniers)
for i in mail_ids[-50:]:
    print(colored("\n\n\nREADING NEW MAIL", "yellow"))
    # Récupérer l'email par son ID
    status, msg_data = mail.fetch(i, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Décoder l'email
            msg = email.message_from_bytes(response_part[1])
            
            # Décoder l'objet de l'email
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Obtenir l'expéditeur
            sender = msg.get("From")
            
            print("Mail from : %s"%sender)
            
           
            #READ THE CONTENT OF THE MAIL
            """
            # Si l'email a un contenu multiple (texte, HTML)
            if msg.is_multipart():
                #
                
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":  # Affiche uniquement le texte brut
                        body = part.get_payload(decode=True).decode("utf-8")
                        print("Contenu:\n", body)
                
            else:
                # Si le contenu est directement en texte simple
                #body = msg.get_payload(decode=True).decode("utf-8")
               # print("Contenu:\n", body)

                print(colored("html content in the mail", "red"))
            """

# Fermer la connexion à la boîte mail
mail.close()
mail.logout()