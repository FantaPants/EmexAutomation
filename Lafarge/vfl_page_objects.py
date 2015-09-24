from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, datetime, re, os
import client_variables, function_module, email_module, common_page_objects


"""This module contains a set of page objects specific to the VFL Module"""

"""ADD VFL RECORDS"""

def add_basic_vfl_records(driver, amount, test, workgroup, bu, location, participant):
    """function is a simple loop that adds basic VFL records"""
    for x in range(amount):
        comment = test + " - Automated VFL#"+str(x)
        add_new_vfl_record(driver)
        vfl_date(driver, function_module.first_day_of_month())
        vfl_workgroup_selector(driver, workgroup)
        vfl_business_unit(driver, bu)
        vfl_location(driver, location)
        vfl_participants(driver, participant)
        vfl_comment(driver, comment)
        vfl_time(driver, "0:00", "1:00")
        vfl_next_button(driver)
        vfl_finish_button(driver)
        print "Added "+comment

"""VFL SPECIFIC BUTTON OBJECTS"""

def open_vfl_module(driver):
    """Select the Open VFL Module button"""
    common_page_objects.move_to_module(driver, "i.fa.fa-lg.fa-fw.fa-comments")

def add_new_vfl_record(driver):
    """Select the Add New VFL button"""
    common_page_objects.click_button_css(driver, "i.glyphicon.glyphicon-plus")

def edit_latest_vfl_record(driver):
    """Select the Edit Latest VFL button"""
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i")

def view_latest_vfl_record(driver):
    """Select the View Latest VFL button"""
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[1]/i")

def delete_latest_vfl_record(driver):
    """Select the Delete Latest VFL button"""
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[3]/i")
    common_page_objects.click_button(driver, "//*[@id='bot2-Msg1']")

def select_all_vfl_records(driver):
    """Select the Select All VFL Records checkbox"""
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/thead/tr/th[1]/input")

def delete_multiple_vfl_records(driver):
    """Function first checks whether the Delete Multiple Records button is enabled. If it
    is currently disabled, it will select all vfl records and then delete them. If you don't
    want this function to delete all records on the page, please use the 'select_multiple_vfl_records'
    object in your script before this one."""
    button_disabled = function_module.field_is_read_only_xpath(driver, "//*[@id='removeVfl']")
    button_enabled = function_module.field_is_not_read_only_xpath(driver, "//*[@id='removeVfl']")
    if button_disabled == True:
        print 'Delete All VFL Records Button currently disabled'
        select_all_vfl_records(driver)
        time.sleep(1)
        print 'Selected all VFL records on current page'
        common_page_objects.click_button(driver, "//*[@id='removeVfl']/i")
        common_page_objects.click_button(driver, "//*[@id='bot2-Msg1']")
        print 'Successfully deleted all existing VFL Records'
    elif button_enabled == True:
        print 'Delete All VFL Records Button already enabled'
        common_page_objects.click_button(driver, "//*[@id='removeVfl']/i")
        common_page_objects.click_button(driver, "//*[@id='bot2-Msg1']")
        print 'Successfully deleted multiple existing VFL Records'

def delete_remaining_vfl_records(driver):
    """Function checks the remaining number of VFL records and will remain in loop
    deleting all records on the current page, until there are no more VFL records."""
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL_info']")
    amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
    time.sleep(1)
    while amount_of_records != '0 to 0 of 0 entries':
        delete_multiple_vfl_records(driver)
        time.sleep(3)
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records

def vfl_next_button(driver):
    """function selects the next button on the Details tab"""
    common_page_objects.click_button(driver, "//*[@id='btnNextSubmit']")
    #function_module.wait_for_element_XPATH(driver, "//*[@id='bootstrap-wizard-1']/div[2]/div[3]/div/div/ul/li[2]/a", 60)
    
def vfl_finish_button(driver):
    """function selects the finish button on the Acts tab"""
    common_page_objects.click_button(driver, "//*[@id='bootstrap-wizard-1']/div[2]/div[3]/div/div/ul/li[2]/a")
    function_module.wait_for_element_CSS(driver, "i.fa.fa-power-off", 60)

def vfl_reports_button(driver):
    """Object selects the VFL Reports button. NOTE - In version 8 this might move to Common Objects as generic open
    Reports Module button"""
    common_page_objects.click_button(driver, "//*[@id='left-panel']/nav/ul/li[3]/a/i")
    function_module.verify_value(driver, "//*[@id='content']/div[1]/div[1]/h1", 'Reports', 'VFL', 'Moving to Reports Module',
    'Asserted that we have successfully moved to the Report section', 'Failed to access to the Report tab')

"""VFL DETAILS OBJECTS"""

def vfl_date(driver, date):
    """Send given date string value to the Date field on the Details tab"""
    common_page_objects.send_value(driver, "//*[@id='VflDate']", date)

def vfl_workgroup_selector(driver, workgroup):
    """Send given WorkGroup string value to the WorkGroup field on the Details tab.
    WorkGroup should always come from Client Variables file."""
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen1']", workgroup)

def clear_selected_vfl_workgroup(driver):
    """Select the X icon of the selected WorkGroup value in the WorkGroup field on the Details tab."""
    common_page_objects.click_button_css(driver, ".select2-search-choice-close")

def vfl_business_unit(driver, bu):
    """Select given Business Unit string value from the Business Unit dropdown on the Details tab.
    Business Unit should always come from Client Variables file."""
    common_page_objects.select_dropdown_value(driver, "//*[@id='ProductLine']", bu)

def vfl_location(driver, location):
    """Select given Location string value from the Location dropdown on the Details tab.
    Location should always come from Client Variables file."""
    common_page_objects.select_dropdown_value(driver, "//*[@id='Location']", location)

def vfl_participants(driver, participant):
    """Send given Participant User string value to the Participants field on the Details tab.
    Participant should be a user taken from Client Variables file. User will have to a different user
    than the one used to login at the beginning of the test"""
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen2']", participant)

def vfl_employees(driver, employee):
    """Send given Employees string value to the Employees Spoken to field on the Details tab.
    Field accepts plain string values, so employee can equal anything you like"""
    common_page_objects.send_value(driver, "//*[@id='formDetails']/div/section[2]/section[2]/div/div/input", employee)

def vfl_comment(driver, comment):
    """Send given Comment string value to the Comment to field on the Details tab.
    Field accepts plain string values, so comment can equal anything you like"""
    common_page_objects.send_value(driver, "//*[@id='Comments']", comment)

def vfl_time(driver, time_in, time_out):
    """Send given Time_in and Time_out values. Ensure that time_out is greater than
    time_in, otherwise the Details form will throw an error as Total Minutes cannot be a negative number"""
    common_page_objects.send_value(driver, "//*[@id='TimeIn']", time_in)
    common_page_objects.send_value(driver, "//*[@id='TimeOut']", time_out)

"""VFL ACTS OBJECTS"""

def add_vfl_act(driver, radio, act_type):
    """Add a VFL act. Object expects "radio" int parameter which is converted to a string to complete the xpath
    locator. 1 = Safe & 2 = Unsafe. Second parameter expects a string and is used to select the act type from the
    dropdown. The act type should be sourced from the client variables file"""
    radio_string = str(radio)
    function_module.wait_for_element_XPATH(driver, "//*[@id='formActs']/div/section[1]/div/label["+radio_string+"]/i")
    driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label["+radio_string+"]/i").click()
    Select(driver.find_element_by_xpath("//*[@id='Acts']")).select_by_visible_text(act_type)
    common_page_objects.click_button(driver, "//*[@id='btnSubmitFormActs']")
    
def edit_top_act(driver, act_type):
    """Object edits the latest act and changes the act type to the one specified. The desired new
    act type should be sourced from the client variables file."""
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-pencil")
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-pencil").click()
    Select(driver.find_element_by_xpath("//*[@class='col col-6']/div/div/label/select")).select_by_visible_text(act_type)
    driver.find_element_by_css_selector(".fa.fa-save.glyphicon-size").click()

def delete_top_act(driver):
    """Object deletes the latest act"""
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-trash")
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-trash").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()

def add_conversation(driver, comment):
    """Object adds a conversation to the latest act, with the given comment string value.
    The object also checks that the comment field is mandatory"""
    function_module.wait_for_element_CSS(driver, "i.fa.fa-comment-o.glyphicon-size")
    driver.find_element_by_css_selector("i.fa.fa-comment-o.glyphicon-size").click()
    function_module.wait_for_element_CSS(driver, "#Comment")
    function_module.field_is_mandatory_css(driver, "#Comment")
    driver.find_element_by_css_selector("#Comment").click()
    driver.find_element_by_css_selector("#Comment").clear()
    driver.find_element_by_css_selector("#Comment").send_keys(comment)
    function_module.wait_for_element_CSS(driver, "#submit_modalConversation")
    driver.find_element_by_css_selector("#submit_modalConversation").click()

def expand_latest_act(driver):
    """Click the expand button for the latest act so as to access the Edit and Delete buttons
    for conversations and actions."""
    common_page_objects.click_button_css(driver, "i.fa.fa-lg.fa-angle-down")

def edit_conversation(driver, comment):
    """Object expands the latest Act and edits the latest conversation, resetting the
    Commnent field to the given string value."""
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-pencil")
    driver.find_element_by_css_selector("i.fa.fa-pencil").click()
    function_module.wait_for_element_CSS(driver, "#Comment")
    driver.find_element_by_css_selector("#Comment").click()
    driver.find_element_by_css_selector("#Comment").clear()
    driver.find_element_by_css_selector("#Comment").send_keys(comment)
    function_module.wait_for_element_CSS(driver, "#update_modalConversation")
    driver.find_element_by_css_selector("#update_modalConversation").click()

def add_image(driver, image):
    """Object expands the latest Act and edits the latest conversation so as to attach
    a specified Image to the converstaion.

    NOTE:
    
    NEED TO RETURN TO THIS ISSUE - TRIED VARIOUS APPROACHES TO EXPLICITY WAIT TILL IMAGE IS FULLY UPLOADED, BUT SO FAR NONE WORKED
        
    #function_module.wait_to_be_clickable_XPATH(driver, "//*[@id='update_modalConversation']", 60)
    #driver.find_element_by_xpath("//*[@id='update_modalConversation']").click()

    #element = WebDriverWait(driver, 60).until((EC.element_to_be_clickable(By.XPATH, "//*[@id='update_modalConversation']")))
    #element.click()

    #function_module.wait_for_element_XPATH(driver, "//*[@id='templateUploaded_Files']/div[1]/button", 60)
    #function_module.wait_for_element_CSS(driver, ".ingPreview", 30)"""
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-pencil")
    driver.find_element_by_css_selector("i.fa.fa-pencil").click()
    driver.find_element_by_xpath("//*[@id='btnAdd_Files']/input[@type='file']").send_keys(image)
    time.sleep(6)
    driver.find_element_by_xpath("//*[@id='update_modalConversation']").click()

def delete_conversation(driver):
    """Object expands the latest act and deletes the latest conversation."""
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-times")
    driver.find_element_by_css_selector("i.fa.fa-times").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()

def add_action(driver, duedate, priority, description, assignee):
    """Object adds an Action to the latest VFL Act. On opening the Action form all mandatory and read only fields, as well as
    default values are checked. Also the object will check that the current user is selected from AssignedBy by default.
    For the purpose of a smooth test run, if the current user is not selected, the object will failed the verification,
    but add the current user so the whole test doesnt fail."""
    function_module.wait_for_element_CSS(driver, "i.fa.fa-file-text-o.glyphicon-size")
    driver.find_element_by_css_selector("i.fa.fa-file-text-o.glyphicon-size").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='DueDate']")
    #Verify all mandatory fields and default values
    function_module.field_is_mandatory_css(driver, "#DueDate")
    function_module.field_is_mandatory_css(driver, "#Priority")
    function_module.field_is_mandatory_css(driver, "#Description")
    function_module.field_is_mandatory_css(driver, "#AssignedTo")
    user_assigned = True
    current_user = driver.find_element_by_xpath("//*[@id='AssignedBy']/option[2]")
    try:
        assert current_user.text == client_variables.fullname1
    except AssertionError:
        function_module.log_to_file('Test_VFL_Module:Page_Object_add_action:Actions AssignedBy field is not automatically populated with current user', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - Actions AssignedBy field was not automatically populated with current user'
        email_module.error_mail('VFL add_action Page Object', 'When creating a new VFL Action, the AssignedBy field was not populated with the current user by default', 'AssertionError')
        user_assigned = False
    else:
        function_module.log_to_file('Test_VFL_Module:Page_Object_add_action:Actions AssignedBy field was automatically populated with current user', 'PASSED')
        print 'Asserted that Actions AssignedBy field is automatically populated with current user'
    time.sleep(1)
    #If Current User is not Assigned already, MAKE IT SO!
    if user_assigned == False:
        driver.find_element_by_xpath("//*[@id='AssignedBy']/option[2]").click()
        driver.find_element_by_xpath("//*[@id='AssignedBy']/option[2]").send_keys(client_variables.fullname1)
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='AssignedBy']/option[2]").send_keys(Keys.RETURN)
        time.sleep(1)
        print "AssignedBy field is now populated with current user"
    else:
        print "AssignedBy field already populated"  
    function_module.field_is_read_only_css(driver, "#Status")
    status = driver.find_element_by_css_selector("#Status")
    status_value = status.get_attribute("value")
    try:
        assert status_value == 'Not Started'
    except AssertionError:
        function_module.log_to_file('Test_VFL_Module:Page_Object_add_action:Actions Status is NOT "Not Started" by default', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - Actions Status is NOT "Not Started" by default'
        email_module.error_mail('VFL add_action Page Object', 'When creating a new VFL Action, the Status field was not set to "Not Started" by default', 'AssertionError')
    else:
        function_module.log_to_file('Test_VFL_Module:Page_Object_add_action:Actions Status is "Not Started" by default', 'PASSED')
        print 'Asserted that Actions Status is "Not Started" by default'
    time.sleep(1)
    common_page_objects.send_value(driver, "//*[@id='DueDate']", duedate)
    common_page_objects.select_dropdown_value(driver, "//*[@id='Priority']", priority)
    common_page_objects.send_value(driver, "//*[@id='Description']", description)
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen1']", assignee)
    time.sleep(1)
    #Assert AssignedTo user added successfully
    assigned_to_user = driver.find_element_by_xpath(".//*[@id='s2id_AssignedTo']/ul/li[1]/div").text
    try:
        assert assigned_to_user == client_variables.fullname2
    except AssertionError:
        function_module.log_to_file('Test_VFL_Module:Page_Object_add_action:AssinedTo user was NOT added successfully', 'FAILED')
        print 'ERROR - ASSERTION EXCEPTION - AssignedTo user was NOT added successfully'
        email_module.error_mail('VFL add_action Page Object', 'When creating a new VFL Action, the test failed to successfully assigned a user to the AssignedTo field', 'AssertionError')
    else:
        function_module.log_to_file('Test_VFL_Module:Page_Object_add_action:AssinedTo user was added successfully', 'PASSED')
        print 'Asserted that AssinedTo user was added successfully'
    time.sleep(1)
    function_module.wait_for_element_XPATH(driver, "//*[@id='submit_modalAction']")
    driver.find_element_by_xpath("//*[@id='submit_modalAction']").click()

def edit_action(driver, duedate, priority, description, assignee):
    """Object expands latest Act and edits the latest Action. All read only fields are checked and then
    Duedate, Priority, Description and AssignedTo are updated."""
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-pencil")
    driver.find_element_by_css_selector("i.fa.fa-pencil").click()
    common_page_objects.send_value(driver, "//*[@id='DueDate']", duedate)
    common_page_objects.select_dropdown_value(driver, "//*[@id='Priority']", priority)
    common_page_objects.send_value(driver, "//*[@id='Description']", description)
    function_module.field_is_read_only_css(driver, "#Status")
    function_module.field_is_read_only_css(driver, "#FullName")
    time.sleep(1)
    function_module.wait_for_element_XPATH(driver, "//*[@id='update_modalAction']")
    driver.find_element_by_xpath("//*[@id='update_modalAction']").click()

def delete_action(driver):
    """Object expands latest Act and edits the latest Action, so as to delete it."""
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-times")
    driver.find_element_by_css_selector("i.fa.fa-times").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()

"""VFL MAIN LIST PAGE OBJECTS"""

def expand_filters(driver):
    """function checks whether the filter panel is currently hidden. If it is hidden then it
    can be expanded. Wait for the required button and then select it in order to expand the filter panel"""
    is_hidden = function_module.field_is_hidden_xpath(driver, "//*[@id='dtFilterFormContainerVfl']")
    if is_hidden == True:
        function_module.wait_for_element_XPATH(driver, "//*[@id='dtFilterHeaderContainerVfl']/div/a[1]")
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        function_module.wait_for_element_XPATH(driver, "//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]")
        print "Filter Panel expanded"
    else:
        print "Filter Panel is not Hidden so therefore must alreay be displayed"

def set_vfl_from_date(driver, date):
    """fucntions assigns a given date to the From Date filter"""
    common_page_objects.send_value(driver, "//*[@id='CreatedOnFrom']", date)

def set_vfl_to_date(driver, date):
    """fucntions assigns a given date to the To Date filter"""
    common_page_objects.send_value(driver, "//*[@id='CreatedOnTo']", date)

def set_vfl_workgroup(driver, workgroup):
    """fucntions assigns a given workGroup to the WorkGroup filter"""
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen3']", workgroup)

def select_vfl_workgroup_subgroups(driver):
    """function clicks the WorkGroup SubGroups checkbox"""
    common_page_objects.click_button(driver, "//*[@id='dtFilterFormContainerVfl']/form/div/div/div[6]/div/label[3]/i")

def set_vfl_location(driver, location):
    """function selects a location from the dropdown location filter"""
    common_page_objects.select_dropdown_value(driver, "//*[@id='Location']", location)

def set_vfl_business_unit(driver, bu):
    """function selects a Business Unit from the dropdown Business Unit filter"""
    common_page_objects.select_dropdown_value(driver, "//*[@id='ProductLine']", bu)

def clear_selected_creator(driver):
    """function selects the X button on the currently selected User in the CreatedBy field"""
    common_page_objects.click_button(driver, "//*[@id='s2id_CreatedBy']/ul/li[1]/a")

def clear_selected_first_participant(driver):
    """function selects the X button on the currently selected User in the Participant field"""
    common_page_objects.click_button(driver, "//*[@id='s2id_Participants']/ul/li[1]/a")

def set_vfl_creator(driver, user):
    """function selects a user for the CreatedBy field"""
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen1']", user)

def set_vfl_participant(driver, user):
    """function selects a user for the Participants field"""
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen2']", user)

def apply_filters(driver):
    """function selects the Apply Filter button and waits for VFL records to load"""
    common_page_objects.click_button(driver, "//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]")
    wait_for_vfl_records(driver)

def clear_filters_main(driver):
    """function selects the primary Clear Filters button (Next to the Expand Filters button)
    and waits for VFL records to load"""
    common_page_objects.click_button(driver, "//*[@id='dtFilterHeaderContainerVfl']/div/a[2]")
    wait_for_vfl_records(driver)

def clear_filters_alt(driver):
    """function selects the alternative Clear Filters button (inside the Filter Panel next to the
    Apply Filters button)and waits for VFL records to load"""
    expand_filters(driver)
    common_page_objects.click_button(driver, "//*[@id='dtFilterFormContainerVfl']/div/div/div/a[1]")
    wait_for_vfl_records(driver)

def check_amount_of_vfl_records(driver, amount):
    """function checks the existing amount of records and prints the amount to the console.
    This function is only used for debugging post test run"""
    amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
    if amount_of_records == amount:
        print amount_of_records
        print 'NICE ONE BRUVA!'
    else:
        print amount_of_records
        print 'SONOFABITCH!'

def pagination_next(driver, expected_amount):
    """function selects the pagination next button"""
    common_page_objects.click_button_css(driver, ".next>a")
    function_module.wait_for_text_to_be_present(driver, "//*[@id='dtVFL_info']", expected_amount, 20)

def pagination_prev(driver, expected_amount):
    """function selects the pagination previous button"""
    common_page_objects.click_button_css(driver, ".prev>a")
    function_module.wait_for_text_to_be_present(driver, "//*[@id='dtVFL_info']", expected_amount, 20)

def pagination_last(driver, expected_amount):
    """function selects the pagination last button"""
    common_page_objects.click_button_css(driver, ".last>a")
    function_module.wait_for_text_to_be_present(driver, "//*[@id='dtVFL_info']", expected_amount, 20)

def pagination_first(driver, expected_amount):
    """function selects the pagination first button"""
    common_page_objects.click_button_css(driver, ".first>a")
    function_module.wait_for_text_to_be_present(driver, "//*[@id='dtVFL_info']", expected_amount, 20)

def pagination_number_of_records(driver, number, expected_amount):
    """function selects the pagination first button"""
    common_page_objects.select_dropdown_value(driver, "//*[@id='dtVFL_length']/span/label/select", number)
    function_module.wait_for_text_to_be_present(driver, "//*[@id='dtVFL_info']", expected_amount, 20)

def vfl_export(driver, file_type, export_type):
    """function that exports all current VFL records in the given file_type and export_type
    where 1 = All, 2 = Current Page and 3 = Selected Records"""
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='formExport']/div[1]/section[1]/div/label["+export_type+"]/i")
    driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label["+export_type+"]/i").click()
    time.sleep(1)
    Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text(file_type)
    if export_type == "1":
        function_module.wait_for_element_CSS(driver, "#submit_modalExport")
        driver.find_element_by_css_selector("#submit_modalExport").click()
        function_module.wait_for_element_CSS(driver, "#bot2-Msg1")
        driver.find_element_by_css_selector("#bot2-Msg1").click()
        time.sleep(2)
    else:
        function_module.wait_for_element_CSS(driver, "#submit_modalExport")
        driver.find_element_by_css_selector("#submit_modalExport").click()
        time.sleep(2)
    if export_type == "1":
        print "Successfully exported all current VFL records - "+file_type+" "
    elif export_type == "2":
        print "Successfully exported current page of VFL records - "+file_type+" "
    else:
        print "Successfully exported all currently selected VFL records - "+file_type+" "

def select_multiple_vfl_records(driver, amount):
    """Object will select the given amount of VFL Records. Where Amount will be an Int value and
    the total records selected will be amount - 1"""
    total = amount - 1
    total_string = str(total)
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i", 60)
    for x in range(1,amount):
        y = str(x)
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr["+y+"]/td[1]/input").click()
    print "Selected top "+total_string+" VFL records on first page of list view"

def wait_for_vfl_records(driver):
    """Object will simply wait for the first VFL records to appear on the list page. Not a full proof
    option, so I might replace at a later date."""
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i", 60)
    

"""VFL SETTINGS OBJECTS"""

def open_vfl_settings(driver):
    """function opens the VFL settings dialog box"""
    common_page_objects.click_button(driver, "//*[@id='content']/div[1]/div[2]/div/a")
    function_module.wait_for_element_XPATH(driver, "//*[@id='Year']")

def submit_vfl_settings(driver):
    """function selects the submit button in the VFL Settings Dialog box"""
    common_page_objects.click_button(driver, "//*[@id='btnSubmitFormSettings']")

def close_vfl_settings(driver):
    """function selects the close button in the VFL Settings Dialog box"""
    common_page_objects.click_button(driver, "//*[@id='cancel_modalSettings']")

def edit_vfl_settings(driver):
    """function selects the first rows edit button in the VFL Settings Dialog box"""
    common_page_objects.click_button(driver, "//*[@id='dtSettingsContainer']/tr/td[3]/div/div/a[1]/i")
    print "Editing VFL Settings - First Row"

def delete_vfl_settings(driver):
    """function selects the first rows delete button in the VFL Settings Dialog box"""
    common_page_objects.click_button(driver, "//*[@id='dtSettingsContainer']/tr/td[3]/div/div/a[2]/i")
    common_page_objects.click_button(driver, "//*[@id='bot2-Msg1']")
    
def cancel_edit_vfl_settings(driver):
    """function selects the cancel button when editing a VFL Settings row,
    in the VFL Settings Dialog box"""
    common_page_objects.click_button(driver, "//*[@id='btnCancelFormSettings']")
    print "Canceled Editing of VFL Settings - First Row"

def update_edit_vfl_settings(driver):
    """function selects the update button when editing a VFL Settings row,
    in the VFL Settings Dialog box"""
    common_page_objects.click_button(driver, "//*[@id='btnUpdateFormSettings']")

def refresh_vfl_settings(driver):
    """function refreshes the webdriver session and then reselects the VFL Settings button"""
    driver.refresh()
    open_vfl_settings(driver)
    
def vfl_year_default_current(driver):
    """function checks that, upon opening the VFL dialog box that the default value for the Year field is the current year. If
    the value is not the current year the verification will fail. However for the purpose of continuing the rest of the VFL
    Settings tests, the function will in this case enter the current year"""
    year_populated = False
    year_field = driver.find_element_by_xpath("//*[@id='Year']")
    year_value = year_field.get_attribute("aria-valuenow")
    current_year = datetime.datetime.now().year
    year_string = str(current_year)
    year_populated = function_module.verify_value_comparison(driver, year_value, year_string, 'VFL', 'Settings Tests',
    'Asserted that the Settings Year field is set to current year by default', 'The Settings Year field is NOT set to current year by default')
    time.sleep(1)
    #If year field is not current year, MAKE IT SO!
    if year_populated == False:
        driver.find_element_by_xpath("//*[@id='Year']").click()
        driver.find_element_by_xpath("//*[@id='Year']").send_keys(year_string)
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='Year']").send_keys(Keys.RETURN)
        time.sleep(2)
        print "Year field is now populated with current year"
    else:
        print "Year field is already populated"

def vfl_visits_default_current(driver):
    """function checks that, upon opening the VFL dialog box that the default value for the Visits field is 0. If
    the value is not 0 the verification will fail. However for the purpose of continuing the rest of the VFL
    Settings tests, the function will in this case enter a value of 0"""
    visits_populated = False
    visits_field = driver.find_element_by_xpath("//*[@id='NoVisits']")
    visits_value = visits_field.get_attribute("aria-valuenow")
    visits_populated = function_module.verify_value_comparison(driver, visits_value, '0', 'VFL', 'Settings Tests',
    'Asserted that the Settings Visits field is set to 0 by default', 'The Settings Visits field is NOT set to 0 by default')
    time.sleep(1)
    #If visits field is not 0, MAKE IT SO!
    if visits_populated == False:
        driver.find_element_by_xpath("//*[@id='NoVisits']").click()
        driver.find_element_by_xpath("//*[@id='NoVisits']").send_keys(visits_string)
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='NoVisits']").send_keys(Keys.RETURN)
        time.sleep(2)
        print "Vists now populated with value = 0"
    else:
        print "Visits field is already populated"

def vfl_year_increment(driver, amount):
    """function will select the increment button next to the year field a given amount. It will then verify that
    the value of the field is as expected"""
    year_field = driver.find_element_by_xpath("//*[@id='Year']")
    year_value = year_field.get_attribute("aria-valuenow")
    for x in range(amount):
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[1]/div/span/a[1]").click()
    year_value_new = year_field.get_attribute("aria-valuenow")
    #year_new = datetime.datetime.now().year + amount
    year_new = int(year_value) + amount
    year_new_string = str(year_new)
    amount_string = str(amount)
    function_module.verify_value_comparison(driver, year_value_new, year_new_string, 'VFL', 'Settings Tests',
    'Asserted that the Settings Year field can be increased by '+amount_string+'', 'Failed to increase the year field by '+amount_string+' as expected')
    time.sleep(1)

def vfl_year_decrement(driver, amount):
    """function will select the decrement button next to the year field a given amount. It will then verify that
    the value of the field is as expected"""
    year_field = driver.find_element_by_xpath("//*[@id='Year']")
    year_value = year_field.get_attribute("aria-valuenow")
    for x in range(amount):
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[1]/div/span/a[2]").click()
    year_value_new = year_field.get_attribute("aria-valuenow")
    year_new = int(year_value) - amount
    year_new_string = str(year_new)
    amount_string = str(amount)
    function_module.verify_value_comparison(driver, year_value_new, year_new_string, 'VFL', 'Settings Tests',
    'Asserted that the Settings Year field can be decreased by '+amount_string+'', 'Failed to decrease the year field by '+amount_string+' as expected')
    time.sleep(1)

def vfl_visits_negative(driver, amount):
    """function will select the decrement button next to the visits field a given amount. It will then verify that
    the value of the field is 0. This page object is designed to test that the visits field cannot be set to a
    negative value"""
    visits_field = driver.find_element_by_xpath("//*[@id='NoVisits']")
    visits_value = visits_field.get_attribute("aria-valuenow")
    for x in range(amount):
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[2]").click()
    visits_value_new = visits_field.get_attribute("aria-valuenow")
    visits_string = str(visits_value_new)
    function_module.verify_value_comparison(driver, visits_string, '0', 'VFL', 'Settings Tests',
    'Asserted that Number of Visits field can NOT be assigned a negative value', 'Number of Visits field can be assigned a negative value')
    time.sleep(1)

def vfl_visits_increment(driver, amount):
    """function will select the increment button next to the visits field a given amount. It will then verify that
    the value of the field is as expected"""
    visits_field = driver.find_element_by_xpath("//*[@id='NoVisits']")
    visits_value = visits_field.get_attribute("aria-valuenow")
    for x in range(amount):
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[1]").click()
    visits_value_new = visits_field.get_attribute("aria-valuenow")
    visits_new = int(visits_value) + amount
    visits_new_string = str(visits_new)
    amount_string = str(amount)
    function_module.verify_value_comparison(driver, visits_value_new, visits_new_string, 'VFL', 'Settings Tests',
    'Asserted that the Settings Visits field can be increased by '+amount_string+'', 'Failed to increase the year field by '+amount_string+' as expected')
    time.sleep(1)

def vfl_visits_decrement(driver, amount):
    """function will select the decrement button next to the visits field a given amount. It will then verify that
    the value of the field is as expected"""
    visits_field = driver.find_element_by_xpath("//*[@id='NoVisits']")
    visits_value = visits_field.get_attribute("aria-valuenow")
    for x in range(amount):
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[2]").click()
    visits_value_new = visits_field.get_attribute("aria-valuenow")
    visits_new = int(visits_value) - amount
    visits_new_string = str(visits_new)
    amount_string = str(amount)
    function_module.verify_value_comparison(driver, visits_value_new, visits_new_string, 'VFL', 'Settings Tests',
    'Asserted that the Settings Visits field can be decreased by '+amount_string+'', 'Failed to decrease the year field by '+amount_string+' as expected')
    time.sleep(1)

def verify_vfl_settings_first_row(driver, year, visits):
    """fucntion will verify whether the first row has the give year and visits values"""
    year_string = str(year)
    visits_string = str(visits)
    function_module.verify_value(driver, "//*[@id='dtSettingsContainer']/tr/td[1]", year_string, 'VFL', 'Settings Tests',
    'Successfully verified that Year for first row is'+year_string+'', 'Could not verify that Year for first row is '+year_string+'')
    time.sleep(1)
    function_module.verify_value(driver, "//*[@id='dtSettingsContainer']/tr/td[2]", visits_string, 'VFL', 'Settings Tests',
    'Successfully verified that Visits for first row is '+visits_string+'', 'Could not verify that Visits for first row is '+visits_string+'')
    time.sleep(1)

def edit_first_row(driver, year, visits):
    """function will edit the first row and set its year and visits field to the given values"""
    year_string = str(year)
    visits_string = str(visits)
    edit_vfl_settings(driver)
    function_module.wait_for_element_XPATH(driver, "//*[@id='Year']")
    driver.find_element_by_xpath("//*[@id='Year']").click()
    driver.find_element_by_xpath("//*[@id='Year']").clear()
    driver.find_element_by_xpath("//*[@id='Year']").send_keys(year_string)
    time.sleep(1)
    #driver.find_element_by_xpath("//*[@id='Year']").send_keys(Keys.RETURN)
    function_module.wait_for_element_XPATH(driver, "//*[@id='NoVisits']")
    driver.find_element_by_xpath("//*[@id='NoVisits']").click()
    driver.find_element_by_xpath("//*[@id='NoVisits']").clear()
    driver.find_element_by_xpath("//*[@id='NoVisits']").send_keys(visits_string)
    time.sleep(1)
    #driver.find_element_by_xpath("//*[@id='NoVisits']").send_keys(Keys.RETURN)
    update_edit_vfl_settings(driver)

"""SHOW HIDE COLUMNS PAGE OBJECTS"""

def click_show_hide_checkbox_xpath(driver, locator):
    """function opens the Show Hide Columns object and selects a checkbox using an XPATH locator"""
    function_module.wait_for_element_XPATH(driver, "//div[@id='dtVFL_wrapper']/div/div/button")
    driver.find_element_by_xpath("//div[@id='dtVFL_wrapper']/div/div/button").click()
    function_module.wait_for_element_XPATH(driver, locator)
    driver.find_element_by_xpath(locator).click()
    main = driver.find_element_by_xpath("//*[@id='main']")
    main.click()
    time.sleep(2)

def click_show_hide_checkbox_css(driver):
    """function opens the Show Hide Columns object and selects a checkbox using a CSS locator"""
    function_module.wait_for_element_XPATH(driver, "//div[@id='dtVFL_wrapper']/div/div/button")
    driver.find_element_by_xpath("//div[@id='dtVFL_wrapper']/div/div/button").click()
    function_module.wait_for_element_CSS(driver, "li > label > input[type=\"checkbox\"]")
    driver.find_element_by_css_selector("li > label > input[type=\"checkbox\"]").click()
    main = driver.find_element_by_xpath("//*[@id='main']")
    main.click()
    time.sleep(2)

def column_hidden(driver, column_object, column_name):
    """function asserts whether the given column is hidden"""
    try:
        assert column_object.is_displayed()
    except StaleElementReferenceException:
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:' +column_name+ ' column successfully hidden', 'PASSED')
        print column_name+' column successfully hidden'
    else:
        function_module.log_to_file('Test_VFL_Module:test024_vfl_show_hide_columns:Failed to hide' +column_name+ ' column', 'FAILED') 
        print 'ERROR WARNING - Failed to hide' +column_name+ ' column'
        email_module.error_mail('VFL Test024', 'Test could not successfully hide the' +column_name+ ' column on the VFL List View page', 'StaleElementReferenceException')
        return False

"""VFL REPORTS OBJECTS"""

def select_vfl_activity_summary_report(driver):
    """selects the VFL Summary Report. NOTE - The existing Report page is most likely due to change in V8
    to incorporate multiple modules. Upon opening the Report form, the object will check mandatory fields."""
    common_page_objects.click_button(driver, "//*[@id='widDtReports']/div/div[2]/div[1]/a")
    function_module.wait_for_element_XPATH(driver, "//*[@id='submit_modalSettings']")
    function_module.field_is_mandatory_xpath(driver, "//*[@class='select required-select2']/input")

def select_vfl_activity_summary_report_submit(driver):
    """object selects the submit button on the VFL summary reports dialog box"""
    common_page_objects.click_button(driver, "//*[@id='submit_modalSettings']")

def generate_basic_vfl_activity_summary_report(driver, workgroup):
    """Object used the select_vfl_summary_report object to open the summary report dialog box, enter a given high level
    workgroup, and don't select the SubGroups checkbox and finally submit the search parameters. NOTE - The given workgroup
    should be sourced from the client variables file"""
    select_vfl_activity_summary_report(driver)
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen2']", workgroup)
    select_vfl_activity_summary_report_submit(driver)
    time.sleep(6)

def generate_basic_vfl_activity_summary_report_with_subgroups(driver, workgroup):
    """Object used the select_vfl_summary_report object to open the summary report dialog box, enter a given high level
    workgroup, and don't select the SubGroups checkbox and finally submit the search parameters. NOTE - The given workgroup
    should be sourced from the client variables file"""
    select_vfl_activity_summary_report(driver)
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen2']", workgroup)
    common_page_objects.click_button(driver, "//*[@id='formSettings']/section[2]/div[2]/label/i")
    select_vfl_activity_summary_report_submit(driver)
    time.sleep(30)

def generate_summary_report_for_vfl_record(driver):
    """Object first verifies that the list page summary report print button is disabled by default. Then the first
    record is selected and the print is selected. We then switch to the window where the report is displaye and
    capture a screenshot for later review"""
    function_module.field_is_read_only_xpath(driver, "//*[@id='printVfl']")
    driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[1]/input").click()
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='printVfl']").click()
    time.sleep(3)
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(2)
    driver.get_screenshot_as_file('V:/QA/Automation/Automation_Resources/Output/summary_report.png')
    time.sleep(2)
    
    
