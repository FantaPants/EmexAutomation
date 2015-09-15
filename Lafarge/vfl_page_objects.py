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

"""VFL Specific Buttons"""
def open_vfl_module(driver):
    common_page_objects.move_to_module(driver, "i.fa.fa-lg.fa-fw.fa-comments")

def add_new_vfl_record(driver):
    common_page_objects.click_button_css(driver, "i.glyphicon.glyphicon-plus")

def edit_latest_vfl_record(driver):
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i")

def view_latest_vfl_record(driver):
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[1]/i")

def delete_latest_vfl_record(driver):
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[3]/i")
    common_page_objects.click_button(driver, "//*[@id='bot2-Msg1']")

def select_all_vfl_records(driver):
    common_page_objects.click_button(driver, "//*[@id='dtVFL']/thead/tr/th[1]/input")

def delete_multiple_vfl_records(driver):
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
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL_info']")
    amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
    time.sleep(1)
    while amount_of_records != '0 to 0 of 0 entries':
        delete_multiple_vfl_records(driver)
        time.sleep(3)
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records

def expand_latest_act(driver):
    common_page_objects.click_button_css(driver, "i.fa.fa-lg.fa-angle-down")

def vfl_next_button(driver):
    common_page_objects.click_button(driver, "//*[@id='btnNextSubmit']")
    #function_module.wait_for_element_XPATH(driver, "//*[@id='bootstrap-wizard-1']/div[2]/div[3]/div/div/ul/li[2]/a", 60)
    
def vfl_finish_button(driver):
    common_page_objects.click_button(driver, "//*[@id='bootstrap-wizard-1']/div[2]/div[3]/div/div/ul/li[2]/a")
    function_module.wait_for_element_CSS(driver, "i.fa.fa-power-off", 60)

def wait_for_vfl_records(driver):
    function_module.wait_for_element_XPATH(driver, "//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i", 60)

"""VFL Details specific fields"""

def vfl_date(driver, date):
    common_page_objects.send_value(driver, "//*[@id='VflDate']", date)

def vfl_workgroup_selector(driver, workgroup):
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen1']", workgroup)

def clear_selected_vfl_workgroup(driver):
    common_page_objects.click_button_css(driver, ".select2-search-choice-close")

def vfl_business_unit(driver, bu):
    common_page_objects.select_dropdown_value(driver, "//*[@id='ProductLine']", bu)

def vfl_location(driver, location):
    common_page_objects.select_dropdown_value(driver, "//*[@id='Location']", location)

def vfl_participants(driver, participant):
    common_page_objects.send_value(driver, "//*[@id='s2id_autogen2']", participant)

def vfl_employees(driver, employee):
    common_page_objects.send_value(driver, "//*[@id='formDetails']/div/section[2]/section[2]/div/div/input", employee)

def vfl_comment(driver, comment):
    common_page_objects.send_value(driver, "//*[@id='Comments']", comment)

def vfl_time(driver, time_in, time_out):
    common_page_objects.send_value(driver, "//*[@id='TimeIn']", time_in)
    common_page_objects.send_value(driver, "//*[@id='TimeOut']", time_out)

"""VFL ACTS"""

def add_vfl_act(driver, radio, act_type):
    radio_string = str(radio)
    function_module.wait_for_element_XPATH(driver, "//*[@id='formActs']/div/section[1]/div/label["+radio_string+"]/i")
    driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label["+radio_string+"]/i").click()
    Select(driver.find_element_by_xpath("//*[@id='Acts']")).select_by_visible_text(act_type)
    common_page_objects.click_button(driver, "//*[@id='btnSubmitFormActs']")
    
def edit_top_act(driver, act_type):
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-pencil")
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-pencil").click()
    Select(driver.find_element_by_xpath("//*[@class='col col-6']/div/div/label/select")).select_by_visible_text(act_type)
    driver.find_element_by_css_selector(".fa.fa-save.glyphicon-size").click()

def delete_top_act(driver):
    function_module.wait_for_element_CSS(driver, "i.glyphicon.glyphicon-trash")
    driver.find_element_by_css_selector("i.glyphicon.glyphicon-trash").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()

def add_conversation(driver, comment):
    function_module.wait_for_element_CSS(driver, "i.fa.fa-comment-o.glyphicon-size")
    driver.find_element_by_css_selector("i.fa.fa-comment-o.glyphicon-size").click()
    function_module.wait_for_element_CSS(driver, "#Comment")
    function_module.field_is_mandatory_css(driver, "#Comment")
    driver.find_element_by_css_selector("#Comment").click()
    driver.find_element_by_css_selector("#Comment").clear()
    driver.find_element_by_css_selector("#Comment").send_keys(comment)
    function_module.wait_for_element_CSS(driver, "#submit_modalConversation")
    driver.find_element_by_css_selector("#submit_modalConversation").click()

def edit_conversation(driver, comment):
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
    """
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
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-times")
    driver.find_element_by_css_selector("i.fa.fa-times").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()

def add_action(driver, duedate, priority, description, assignee):
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
    expand_latest_act(driver)
    function_module.wait_for_element_CSS(driver, "i.fa.fa-times")
    driver.find_element_by_css_selector("i.fa.fa-times").click()
    function_module.wait_for_element_XPATH(driver, "//*[@id='bot2-Msg1']")
    driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()

"""Add standard VFL Records"""

def add_basic_vfl_records(driver, amount, test, workgroup, bu, location, participant):
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

"""VFL Main List View Page"""

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
                     
"""SHOW HIDE COLUMNS PAGE OBJECT"""

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



