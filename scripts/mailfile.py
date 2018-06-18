# code from http://codecomments.wordpress.com/2008/01/04/python-gmail-smtp-example/
import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
import config
import email_logger

def sendMail(recipient,subject, text,  *attachmentFilePaths, **kwargs):
  from_account=None
  from_account_pass=None
  if 'from_account' in kwargs.keys():
    from_account = kwargs['from_account']
  if 'from_account_pass' in kwargs.keys():
    from_account_pass = kwargs['from_account_pass']
    
    
  if from_account == None:
    from_account = config.gmailUser
  if from_account_pass == None:
    from_account_pass = config.gmailPassword
  msg = MIMEMultipart()
  msg['From'] = from_account
  msg['To'] = recipient
  msg['Subject'] = subject
  msg.attach(MIMEText(text))
  for attachmentFilePath in attachmentFilePaths:
    msg.attach(getAttachment(attachmentFilePath))
  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(from_account, from_account_pass)
  mailServer.sendmail(from_account, recipient, msg.as_string())
  mailServer.close()
  print('Sent email to %s' % recipient)
  
  ### log email address
  email_logger.log("", recipient)

def getAttachment(attachmentFilePath):
  contentType, encoding = mimetypes.guess_type(attachmentFilePath)
  if contentType is None or encoding is not None:
    contentType = 'application/octet-stream'
  mainType, subType = contentType.split('/', 1)
  file = open(attachmentFilePath, 'rb')
  if mainType == 'text':
    attachment = MIMEText(file.read())
  elif mainType == 'message':
    attachment = email.message_from_file(file)
  elif mainType == 'image':
    attachment = MIMEImage(file.read(),_subType=subType)
  elif mainType == 'audio':
    attachment = MIMEAudio(file.read(),_subType=subType)
  else:
    attachment = MIMEBase(mainType, subType)
  file.close()
  attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
  return attachment
