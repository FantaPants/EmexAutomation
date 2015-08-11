import unittest, time, datetime, re, os
"""Set of global variables or key value pairs. The use of the client specific
global variable file, means that generic tests can be written and can be more
easily maintained"""
#Lafarge QA
todays_date = datetime.datetime.now().date()
client_name = 'PPG'
#Log Folder Path
folder_path = 'V:/QA/Automation/Automation_Resources/Logs/PPG'
output_folder = 'V:/QA/Automation/Automation_Resources/Output'
temp_folder = 'V:/QA/Automation/Automation_Resources/temp'
client_folder = 'V:/QA/Automation/Automation_Resources/Output/PPG'
output_zip_folder = 'V:\\QA\\Automation\\Automation_Resources\\Output\\PPG'
#Login Details
base_url = 'http://dub-sv-qa:3035/'
username1 = 'admin'
fullname1 = 'Admin Admin'
pword1 = 'wi1c0x@1'
username2 = ' '
pword2 = ' '
fullname2 = ' '
#Site/WorkGroups  
root_wg = 'PPG Industries'
wg_default_false = ' '
wg_default_true = ' '
wg_parent = ' '
wg_child = ' '
#Business Units/Product Lines
bu1 = ' '
bu2 = ' '
#Locations
location1 = ' '
location2 = ' '
#VFL Acts
act_type1 = ' '
act_type2 = ' '

