from flask_mail import Message
from flask import render_template,current_app




def confirmation_mail(mail,codeping,mail_instance):
  msg = Message('MAIL DE CONFIRMATION', 
                sender='melainenkeng@gmail.com',
                recipients=[mail])
  msg.html = render_template('confirmMail.html', codeping = codeping)
  mail_instance.send(msg)



def reset_password_mail(mail,password,mail_instance):
  msg = Message('Reset Password', 
                sender='melainenkeng@gmail.com',
                recipients=[mail])
  msg.html = render_template('resetPasswordMail.html', password = password)
  mail_instance.send(msg)



# def welcome_mail(full_name, email):
#   msg = Message('Welcome to Collabinnovate', 
#                 sender='melainenkeng@gmail.com',
#                 recipients=[email])
#   msg.html = render_template('welcome.html', full_name = full_name)
  
#   mail.send(msg)