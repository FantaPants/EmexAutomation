import unittest, time, datetime, re, os
"""Set of global variables or key value pairs. The use of the client specific
global variable file, means that generic tests can be written and can be more
easily maintained"""
#PPG QA
todays_date = datetime.datetime.now().date()
client_name = 'Lafarge'
#Log Folder Path
folder_path = 'V:/QA/Automation/Automation_Resources/Logs/Lafarge_HS'
output_folder = 'V:/QA/Automation/Automation_Resources/Output'
temp_folder = 'V:/QA/Automation/Automation_Resources/temp'
client_folder = 'V:/QA/Automation/Automation_Resources/Output/Lafarge_HS'
output_zip_folder = 'V:\\QA\\Automation\\Automation_Resources\\Output\\Lafarge_HS'
#Login Details
base_url = 'http://dub-sv-qa:3030/'
username1 = 'admin'
fullname1 = 'Admin Admin'
pword1 = 'wi!c0x@1'
username2 = 'buuser'
pword2 = 'password@1'
fullname2 = 'buuser user'
#Site/WorkGroups  
root_wg = 'Lafarge Group'
wg_default_false = 'France'
wg_default_true = 'La Malle'
wg_parent = 'Agence Les Antilles Readymix'
wg_child = 'Petit-Canal'
#Business Units/Product Lines
bu1 = 'Aggregates'
bu2 = 'Cement'
#Locations
location1 = 'AGGREGATES'
location2 = 'CEMENT'
#VFL Acts
act_type1 = 'Access / Egress'
act_type2 = 'Confined Spaces'

