import time, datetime, os, mimetypes, email, smtplib, glob, base64
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.message import Message
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import client_variables, function_module
from datetime import datetime

"""Set of fucntion designed to send emails"""

def summary_mail():
    """Builds and sends a summary email of the latest Automation Test Run. Summary email comprises of
    standard message followed by contents of latest log from clients specific folder. All exports and
    produced during testing should also be attached"""

    #Define email content
    date = datetime.utcnow().strftime('%d-%m-%Y')
    client_name = client_variables.client_name
    sender = 'support@emex.com'
    receiver = 'qateam@emex.com'
    subject = 'HADOUKEN!!! '+client_variables.client_name+' test run Complete - Date: ' + date
    subject_string = str(subject)
    body_intro = 'The latest QA Automation run for ' + client_name + ' was successfully completed on: ' + date + '. The logs created during testing can be found below;'

    #Create Message container
    msg = MIMEMultipart()
    msg['Subject'] = subject_string
    msg['From'] = sender
    msg['To'] = receiver

    #Capture the contents of the latest Log file and store as a string 
    newest = max(glob.iglob(client_variables.folder_path + '\*'), key=os.path.getctime)
    print newest
    f = open(newest,'r')
    log = f.read()
    f.close()

    #build body of email
    body = """%s

    %s"""% (body_intro, log)

    #Record MIME type and attach into container
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)
    #print msg
    
    #Create and attach zipfile of outputs created during test run
    #zipfile = zipfiles.zip_output()
    function_module.zip_output()
    zf = open('outputs.zip', 'rb')
    part2 = MIMEBase('application', "octet-stream")
    part2.set_payload(zf.read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', 'attachment; filename="outputs.zip"')
    msg.attach(part2) 

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    smtpObj = smtplib.SMTP('192.168.2.225')
    smtpObj.sendmail(sender, receiver, msg.as_string())
    smtpObj.quit()



def error_mail(test_number, test_message, exception):
    """Builds and error message email that is send when an assertion throws an exception during testing"""

    #Define email content
    date = datetime.utcnow().strftime('%d-%m-%Y')
    client_name = client_variables.client_name
    sender = 'support@emex.com'
    receiver = 'qateam@emex.com'
    subject = 'POTENTIAL ERROR FOUND IN ' + test_number + ' - CLIENT: ' + client_variables.client_name + ' - DATE: ' + date
    subject_string = str(subject)
    body_intro = 'During the latest Automated Test Run for ' + client_name + ' on: ' + date + '. An exception of type ' + exception + ' was thrown during ' + test_number + '.' 
    body_main = test_message

    #Create Message container
    msg = MIMEMultipart()
    msg['Subject'] = subject_string
    msg['From'] = sender
    msg['To'] = receiver
      
    #build body of email
    body = """%s

    %s"""% (body_intro, body_main)

    #Record MIME type and attach into container
    part1 = MIMEText(body, 'plain')
    msg.attach(part1)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    smtpObj = smtplib.SMTP('192.168.2.225')
    smtpObj.sendmail(sender, receiver, msg.as_string())
    smtpObj.quit()

