import unittest, time, datetime, re, os, shutil, zipfile, glob, client_variables
from datetime import date
from datetime import datetime

"""This module contains a set of custom built modules that are designed to be imported
and used throughout all test modules"""

"""Set of functions used to return dates required for use in other
scripts"""

def today():
    """function returns todays date"""
    today_object = datetime.utcnow()
    today_string = today_object.strftime('%m/%d/%Y')
    return today_string

def first_day_of_month():
    """function returns first day of the current month"""
    first_object = datetime.utcnow()
    first_string = first_object.strftime('%m/01/%Y')
    return first_string

"""Set of functions used to delete various outputs and files that
may have been created during a test run. Delete functions should be
placed at the end of each test run, so as to ensure a clean slate is
is available when running a similar or identical test run in future."""

def remove_outputs_zip():
    """function removes the outputs zip file created by zipfiles.zip_output"""
    os.remove("outputs.zip")

def clear_client_outputs():
    """function clears out the clients output folder of all files created
    during the test run. These files should have already been zipped up and
    emails to QA"""
    directory = client_variables.output_zip_folder
    for name in glob.glob(directory + '\\*'):
        os.remove(name)

"""Set of functions used to create log file during test run"""

def timestamp():
    """timestamp function used to add current time to log file name"""
    my_date_object = datetime.utcnow()
    my_date_string = my_date_object.strftime('%d-%m-%Y %H:%M:%S')
    return my_date_string

LogName = client_variables.folder_path + '\ ' + 'AUTOMATED TEST RUN LOG - ' + datetime.utcnow().strftime('%d-%m-%Y')

def log_to_file(text, status='INFO'):
    """function that creates and appends to log for given date. By default, lines in log will have
    Status = INFO. However when this function is called from within other scripts, the user can
    set Status = whatever they want. I.E. PASS, FAIL etc"""
    outfile = open(LogName, 'a')
    outfile.write(timestamp()+' - '+status+' - '+str(text)+'\n')
    outfile.close()

"""Set of functions for moving files that have been created during test run"""

def move_file():
    """Move file function to be used at any point where file created
    from download needs to be moved to client specific folder"""
    source = client_variables.output_folder
    destination = client_variables.client_folder
    copyfiles = os.listdir(source)
    ext = (".xlsx", ".csv", ".pdf", ".png")

    for copyfile in copyfiles:
        if copyfile.endswith(ext):
            copyfile = source + "/" + copyfile
            print "copying", copyfile
            shutil.move(copyfile, destination)
        elif copyfile.startswith('GetTotalByYearReport'):
            copyfile = source + "/" + copyfile
            print "copying", copyfile
            shutil.move(copyfile, destination)


def rename_file(str):
    """Generic Rename function that is intended to allow string input of new filename.
    Currently not in use as consistent windows errors claiming could not find new file
    drove me bonkers. Functions code is currently being used directly in tests with
    "newname" given a specific value in each case"""
    source = client_variables.output_folder
    renamefiles = os.listdir(source)
    ext = (".xlsx", ".csv", ".pdf", ".png")
    for renamefile in renamefiles:
        if renamefile.endswith(ext):
            renamefile = source + "/" + renamefile
            print "renaming:", renamefile
            newname = source + "/" + str
            print "newname:", newname
            os.rename(renamefile, newname)
        elif renamefile.startswith('GetTotalByYearReport'):
            renamefile = source + "/" + renamefile
            print "renaming:", renamefile
            newname = source + "/" + str
            print "newname:", newname
            os.rename(renamefile, newname)

"""set of functions designed to create zip files that can be
attached to emails etc."""

def zip_output():
   """function creates a zip file comprising of files currently in client
   specific output folder. The resulting zip file will reside will test runs local
   directory, but each test run should delete this zip folder before finishing"""
   directory = client_variables.output_zip_folder
   #create the zip archive
   zip = zipfile.ZipFile('outputs.zip', 'w')

   # add all files in specified folder
   for name in glob.glob(directory + '\\*'):
       zip.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
   zip.close()

"""Verification functions to use in Test Scripts when using an assertion would be overkill"""

def field_is_mandatory(str):
    """Function used for checking that fields that use aria-required parameter are correctly set to
    mandatory as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    if str == 'true':
        print "Mandatory field = true"
    else:
        log_to_file('Mandatory field test failed', 'WARNING')

def field_is_read_only(str):
    """Function used for checking that fields that use disabled parameter are correctly set to
    read only as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    if str == 'true':
        print "Read Only field = true"
    else:
        log_to_file('Read Only field test failed', 'WARNING')

def field_is_not_read_only(str):
    """Function used for checking that fields that use disabled parameter are correctly set to
    read only as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    if str == 'true':
        log_to_file('Read Only field enabled test failed', 'WARNING')
    else:
        print "Read Only field enabled = true"

def field_is_hidden(str):
    """Function used for checking that fields that use display parameter are correctly set to
    none/hidden as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    if str == 'display: none;':
        print "Hidden field = true"
    else:
        log_to_file('Hidden field test failed', 'WARNING')

def field_is_not_hidden(str):
    """Function used for checking that fields that use display parameter are correctly set to
    none/hidden as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    if str == 'display: none;':
        log_to_file('Hidden field displayed test failed', 'WARNING')
    else:
        print "Hidden field displayed = true"
                
