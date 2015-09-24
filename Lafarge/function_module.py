from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotSelectableException
import unittest, time, datetime, re, os, shutil, zipfile, glob
import client_variables, email_module
from datetime import date
from datetime import datetime

"""This module contains a set of custom built functions that are designed to be imported
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

def move_file(source, destination):
    """Move file function to be used at any point where file created
    from download needs to be moved to client specific folder"""
    #source = client_variables.output_folder
    #destination = client_variables.client_folder
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


def rename_file(source, oldname, newname):
    """Generic Rename function that is intended to allow string input of new filename.
    Currently not in use as consistent windows errors claiming could not find new file
    drove me bonkers. Functions code is currently being used directly in tests with
    "new_name" given a specific value in each case"""
    #source = client_variables.output_folder
    renamefiles = os.listdir(source)
    ext = (".xlsx", ".csv", ".pdf", ".png")
    for renamefile in renamefiles:
        if renamefile.endswith(ext):
            renamefile = source + "/" + renamefile
            print "renaming:", renamefile
            newname = source + "/" + newname
            print "newname:", newname
            os.rename(renamefile, newname)
        elif renamefile.startswith(oldname):
            renamefile = source + "/" + renamefile
            print "renaming:", renamefile
            newname = source + "/" + newname
            print "newname:", newname
            os.rename(renamefile, newname)

"""set of functions designed to create zip files that can be
attached to emails etc."""

def zip_output(directory):
   """function creates a zip file comprising of files currently in client
   specific output folder. The resulting zip file will reside will test runs local
   directory, but each test run should delete this zip folder before finishing"""
   #directory = client_variables.output_zip_folder
   #create the zip archive
   zip = zipfile.ZipFile('outputs.zip', 'w')

   # add all files in specified folder
   for name in glob.glob(directory + '\\*'):
       zip.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
   zip.close()

"""Verification functions to use in Test Scripts when using an assertion would be overkill"""

def field_is_mandatory_css(driver, locator):
    """Function used for checking that fields that use aria-required parameter are correctly set to
    mandatory as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_css_selector(locator)
    is_mandatory = elem.get_attribute("aria-required")
    if is_mandatory == 'true':
        print "Mandatory field = true"
    else:
        log_to_file('Mandatory field test failed', 'WARNING')

def field_is_mandatory_xpath(driver, locator):
    """Function used for checking that fields that use aria-required parameter are correctly set to
    mandatory as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_xpath(locator)
    is_mandatory = elem.get_attribute("aria-required")
    if is_mandatory == 'true':
        print "Mandatory field = true"
    else:
        log_to_file('Mandatory field test failed', 'WARNING')

def field_is_read_only_css(driver, locator):
    """Using a CSS Selector Locator, this function is used for checking that fields that use disabled parameter are correctly set to
    read only as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_css_selector(locator)
    is_disabled = elem.get_attribute("disabled")
    if is_disabled == 'true':
        print "Read Only field = true"
        return True
    else:
        log_to_file('Expected Read Only field to be disabled, but was still enabled', 'WARNING')
        return False

def field_is_read_only_xpath(driver, locator):
    """Using an XPath Locator, this function is used for checking that fields that use disabled parameter are correctly set to
    read only as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_xpath(locator)
    is_disabled = elem.get_attribute("disabled")
    if is_disabled == 'true':
        print "Read Only field = true"
        return True
    else:
        log_to_file('Expected Read Only field to be disabled, but was still enabled', 'WARNING')
        return False

def field_is_not_read_only_css(driver, locator):
    """Using a CSS Selector Locator, this function used for checking that fields that use disabled parameter are correctly set to
    read only as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_css_selector(locator)
    is_disabled = elem.get_attribute("disabled")
    if is_disabled == 'true':
        log_to_file('Expected Read Only field to be enabled, but was still disabled', 'WARNING')
        return False
    else:
        print "Read Only field enabled = true"
        return True
def field_is_not_read_only_xpath(driver, locator):
    """Using an XPath Locator, this function is used for checking that fields that use disabled
    parameter are currently enabled. This verification can be used to warn the tester when the
    field is incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_xpath(locator)
    is_disabled = elem.get_attribute("disabled")
    if is_disabled == 'true':
        log_to_file('Expected Read Only field to be enabled, but was still disabled', 'WARNING')
        return False
    else:
        print "Read Only field enabled = true"
        return True

def field_is_hidden_css(driver, locator):
    """Function used for checking that fields that use display parameter are correctly set to
    none/hidden as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_css_selector(locator)
    is_hidden = elem.get_attribute("style")
    if is_hidden == 'display: none;':
        print "Hidden field = true"
        return True
    else:
        log_to_file('Hidden field test failed', 'WARNING')
        return False

def field_is_hidden_xpath(driver, locator):
    """Function used for checking that fields that use display parameter are correctly set to
    none/hidden as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_xpath(locator)
    is_hidden = elem.get_attribute("style")
    if is_hidden == 'display: none;':
        print "Hidden field = true"
        return True
    else:
        log_to_file('Hidden field test failed', 'WARNING')
        return False

def field_is_not_hidden_css(driver, locator):
    """Function used for checking that fields that use display parameter are correctly set to
    none/hidden as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_css_selector(locator)
    is_hidden = elem.get_attribute("style")
    if is_hidden == 'display: none;':
        log_to_file('Hidden field displayed test failed', 'WARNING')
        return False
    else:
        print "Hidden field displayed = true"
        return True

def field_is_not_hidden_xpath(driver, locator):
    """Function used for checking that fields that use display parameter are correctly set to
    none/hidden as expected. This verification can be used to warn the tester when the field is
    incorrectly configured, but won't disturb the flow of the overall test."""
    elem = driver.find_element_by_xpath(locator)
    is_hidden = elem.get_attribute("style")
    if is_hidden == 'display: none;':
        log_to_file('Hidden field displayed test failed', 'WARNING')
        return False
    else:
        print "Hidden field displayed = true"
        return True

"""Explicit Wait functions for use with controlling webdriver and for catching timeouts"""

def wait_for_text_to_be_present(driver, locator, text, time=30):
    """Function is used to wait for the given text to be present in the given located element"""
    wait = WebDriverWait(driver, time)
    try:
        wait.until(EC.text_to_be_present_in_element((By.XPATH, locator), text))
    except NoSuchElementException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate given text and/or element', 'FAILED')
        print 'ERROR - TIMEOUT - Failed to locate given text and/or element'
        email_module.wait_error_mail('Text Present in Element', locator, 'NoSuchElementException')
        return False

def wait_for_element_ID(driver, locator, time=30):
    """Function used to Explicitly Wait for an element to be displayed. The Element is located
    using its ID"""
    try:
        WebDriverWait(driver, time).until(lambda s: s.find_element(By.ID, locator).is_displayed())
    except NoSuchElementException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate required ID element within requirement timeframe', 'FAILED')
        print 'ERROR - TIMEOUT - Failed to locate required ID element within requirement timeframe'
        email_module.wait_error_mail('ID', locator, 'NoSuchElementException')
        return False
    
def wait_for_element_Link_Text(driver, locator, time=30):
    """Function used to Explicitly Wait for an element to be displayed. The Element is located
    using its ID"""
    try:
        WebDriverWait(driver, time).until(lambda s: s.find_element(By.LINK_TEXT, locator).is_displayed())
    except NoSuchElementException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate required ID element within requirement timeframe', 'FAILED')
        print 'ERROR - TIMEOUT - Failed to locate required ID element within requirement timeframe'
        email_module.wait_error_mail('LINK TEXT', locator, 'NoSuchElementException')
        return False

def wait_for_element_CSS(driver, locator, time=30):
    """Function used to Explicitly Wait for an element to be displayed. The Element is located
    using its CSS_SELECTOR"""
    try:
        WebDriverWait(driver, time).until(lambda s: s.find_element(By.CSS_SELECTOR, locator).is_displayed())
    except NoSuchElementException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate required CSS element within requirement timeframe', 'FAILED')
        print 'ERROR - TIMEOUT - Failed to locate required CSS element within requirement timeframe'
        email_module.wait_error_mail('CSS SELECTOR', locator, 'NoSuchElementException')
        return False

def wait_for_element_XPATH(driver, locator, time=30):
    """Function used to Explicitly Wait for an element to be displayed. The Element is located
    using its XPATH"""
    wait = WebDriverWait(driver, time)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
        #WebDriverWait(driver, time).until(lambda s: s.find_element(By.XPATH, locator).is_displayed())
        return True
    except NoSuchElementException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate required XPATH element within requirement timeframe', 'FAILED')
        print 'ERROR - NO SUCH ELEMENT - Failed to locate required XPATH element within requirement timeframe'
        email_module.wait_error_mail('XPATH', locator, 'NoSuchElementException')
        return False
    except TimeoutException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate required XPATH element within requirement timeframe', 'FAILED')
        print 'ERROR - TIMEOUT - Failed to locate required XPATH element within requirement timeframe'
        email_module.wait_error_mail('XPATH', locator, 'TimeoutException')
        return False

def wait_to_be_clickable_XPATH(driver, locator, time=30):
    """Function used to Explicitly Wait for an element to be clickable. The Element is located
    using its XPATH"""
    wait = WebDriverWait(driver, time)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
        return True
    except NoSuchElementException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate clickable XPATH element', 'FAILED')
        print 'ERROR - NO SUCH ELEMENT - Failed to locate clickable XPATH element within requirement timeframe'
        email_module.wait_error_mail('XPATH', locator, 'NoSuchElementException')
        return False
    except ElementNotSelectableException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate clickable XPATH element', 'FAILED')
        print 'ERROR - ELEMENT NOT CLICKABLE - Failed to locate clickable XPATH element within requirement timeframe'
        email_module.wait_error_mail('XPATH', locator, 'ElementNotSelectableException')
        return False
    except TimeoutException:
        log_to_file('Test_VFL_Module:TIMEOUT:Failed to locate clickable XPATH element', 'FAILED')
        print 'ERROR - TIMEOUT - Failed to locate clickable XPATH element within requirement timeframe'
        email_module.wait_error_mail('XPATH', locator, 'TimeoutException')
        return False

"""Verifications"""

def verify_element_not_present_XPATH(driver, locator, module, test, pass_message, fail_message):
    """Verify whether an element is NOT present using an XPath locator. If the element is NOT present
    handle the resulting NoSuchElementException and pass the verification. However if the element is present
    and no exception is thrown, the verification fails. Print a fail message, log a fail message and send
    an appropriate fail email notification"""
    try:
        driver.find_element_by_xpath(locator)
    except NoSuchElementException:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message
    else:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR WARNING - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'NoSuchElementException')

def verify_element_not_present_CSS(driver, locator, module, test, pass_message, fail_message):
    """Verify whether an element is NOT present using an CSS Selector locator. If the element is NOT present
    handle the resulting NoSuchElementException and pass the verification. However if the element is present
    and no exception is thrown, the verification fails. Print a fail message, log a fail message and send
    an appropriate fail email notification"""
    try:
        driver.find_element_by_css_selector(locator)
    except NoSuchElementException:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message
    else:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR WARNING - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'NoSuchElementException')

def verify_element_is_present_XPATH(driver, locator, module, test, pass_message, fail_message):
    """Verify whether an element is present using an CSS Selector locator. If the element is NOT present
    throw a NoSuchElementException and fail the verification. However if the element is present
    and no exception is thrown, the verification passes."""
    try:
        driver.find_element_by_xpath(locator)
    except NoSuchElementException:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR WARNING - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'NoSuchElementException')
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message

def verify_element_is_present_CSS(driver, locator, module, test, pass_message, fail_message):
    """Verify whether an element is present using an CSS Selector locator. If the element is NOT present
    throw a NoSuchElementException and fail the verification. However if the element is present
    and no exception is thrown, the verification passes."""
    try:
        driver.find_element_by_css_selector(locator)
    except NoSuchElementException:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR WARNING - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'NoSuchElementException')
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message

def verify_value(driver, locator, value, module, test, pass_message, fail_message):
    """Wait for the element to appear using an xpath locator. Create a variable to store the located element.
    Verify that the stated string value is the same as the fields text attribute"""
    wait_for_element_XPATH(driver, locator)
    elem = driver.find_element_by_xpath(locator)
    text = elem.text
    try:
        assert text == value
    except AssertionError:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'AssertionError')
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message

def verify_dropdown_value(driver, locator, value, module, test, pass_message, fail_message):
    """Wait for the dropdown element to appear using an xpath locator. Create a variable to store the selected
    dropdown value. Verify that the stated string value is the same as the values text attribute"""
    wait_for_element_XPATH(driver, locator)
    elem = Select(driver.find_element_by_xpath(locator))
    text = elem.first_selected_option.text
    try:
        assert text == value
    except AssertionError:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'AssertionError')
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message

def verify_value_comparison(driver, first_value, second_value, module, test, pass_message, fail_message):
    try:
        assert first_value == second_value
    except AssertionError:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'AssertionError')
        return False
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message
        return True

def verify_radio_dropdown_element_is_disabled(driver, locator, value, module, test, pass_message, fail_message):
    """VFL Specific Example - Selecting Safe or UnSafe activates dropdown. Function waits for radio button to
    appear and selects the correct one. Then verifies that the given dropdown value is present in the list but
    currently set to read only"""
    wait_for_element_XPATH(driver, locator)
    driver.find_element_by_xpath(locator).click()
    elem = driver.find_element_by_xpath(value)
    is_disabled = elem.get_attribute("disabled")
    try:
        assert is_disabled == 'true'
    except AssertionError:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'AssertionError')
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message

def verify_tool_tip_value(driver, locator, value, module, test, pass_message, fail_message):
    """Verifies the title of the given tool-tip"""
    wait_for_element_XPATH(driver, locator)
    elem = driver.find_element_by_xpath(value)
    tool_tip = elem.get_attribute("data-original_title")
    try:
        assert tool_tip == value
    except AssertionError:
        log_to_file(''+module+':'+test+':'+fail_message+'', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - ' + fail_message
        email_module.error_mail(module, test, fail_message, 'AssertionError')
    else:
        log_to_file(''+module+' Module:'+test+':'+pass_message+'', 'PASSED')
        print pass_message
