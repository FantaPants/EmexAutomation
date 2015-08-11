# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, datetime, re, os
import client_variables, function_module

    
class Test_001_VFL_Forms(unittest.TestCase):
    """Set of tests responsible for testing the functionality of
    VFL Details and Acts forms. Used with Creating and Editing
    VFL Records"""                
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_001_add_new_vfl_test_details(self):
        """Testing the VFL details form when adding a new VFL Record.
        Test includes asserts to ensure each particular field adheres
        to expected behaviour"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        print "Moved to VFL Module"
        time.sleep(5)
        #Choose to add a new VFL Record
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        print "Found new VFL button successfully"
        #Verify Due Date is Mandatory
        elem = driver.find_element_by_css_selector("#VflDate")
        date_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(date_mandatory)
        #Verify WorkGroup is Mandatory
        elem = driver.find_element_by_css_selector("#WorkGroup")
        workgroup_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(workgroup_mandatory)
        #Verify Product Line is Read Only
        elem = driver.find_element_by_css_selector("#ProductLine")
        product_line_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(product_line_disabled)
        #Verify Product Line is Mandatory
        elem = driver.find_element_by_css_selector("#ProductLine")
        product_line_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(product_line_mandatory)
        #Verify TimeIn is Mandatory
        elem = driver.find_element_by_css_selector("#TimeIn")
        time_in_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(time_in_mandatory)
        #Verify TimeOut is Mandatory
        elem = driver.find_element_by_css_selector("#TimeOut")
        time_out_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(time_out_mandatory)
        #Verify Minutes is Read Only
        elem = driver.find_element_by_css_selector("#minutes")
        minutes_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(minutes_disabled)
        function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Successfully verified all mandatory and/or read only fields', 'PASSED')
        print "All mandatory and read only fields verfied"
        #Select the 1st day of the month. Selecting the 1st day will help ensure test doesn't fail for wrong reasons
        driver.find_element_by_id("VflDate").send_keys(function_module.first_day_of_month())
        driver.find_element_by_id("VflDate").send_keys(Keys.RETURN)
        print "Selected first day of the month for VFL Date field"
        #Select Site with NO Default Product Line & Allow Data = NO
        driver.find_element_by_id("s2id_autogen1").click()
        driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.root_wg)
        time.sleep(2)
        elem = driver.find_element_by_xpath("//*[@id='select2-drop']/ul/li").text
        try:
            assert elem == 'No matches found'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Workgroup with Allow Data = NO was selected', 'FAILED')
            print 'Assertion Exception - Managed to select a WorkGroup with Allow Data = NO'
        else:
            function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Workgroup with Allow Data = NO cannot be selected', 'PASSED')
            print 'Asserted that WorkGroups with Allow Data = NO cannot be selected'
        time.sleep(1)
        driver.find_element_by_id("s2id_autogen1").clear()
        time.sleep(1)
        #Select Site with NO Default Business Unit & Allow Data = YES
        driver.find_element_by_id("s2id_autogen1").click()
        driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_default_false)
        time.sleep(1)
        driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
        time.sleep(1)
        #Select Business Unit
        driver.find_element_by_id("ProductLine").click()
        Select(driver.find_element_by_id("ProductLine")).select_by_visible_text(client_variables.bu2)
        driver.find_element_by_id("ProductLine").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Selected a WorkGroup with no Default Business Unit, but Allow Data = Yes"
        #Clear Site field and select a new Site with a Default Business Unit & Allow Data = YES
        driver.find_element_by_css_selector(".select2-search-choice-close").click()
        driver.find_element_by_id("s2id_autogen1").click()
        driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_default_true)
        time.sleep(1)
        driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
        time.sleep(1)
        #Assert that Business Unit field has been automatically populated
        default_business_unit = driver.find_element_by_css_selector("#ProductLine")
        try:
            assert default_business_unit != None
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Business Unit field was not automaticallly populated by WGs default Product Line', 'FAILED')
            print 'Assertion Exception - Default Business Unit was not selected automatically'
        else:
            function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Default Business Unit was selected automatically', 'PASSED')
            print 'Asserted that Business Unit field was automatically populated when WG was selected'
        time.sleep(1)
        #Select Location
        Select(driver.find_element_by_id("Location")).select_by_visible_text(client_variables.location1)
        time.sleep(1)
        print "Selected Location successfully"
        #Assert Participants field is automatically populated with current user
        current_participant = driver.find_element_by_css_selector(".select2-search-choice.select2-locked>div")
        try:
            assert current_participant.text == client_variables.fullname1
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Participants field not automatically populated with current user', 'FAILED')
            print 'Assertion Exception - Participants field was not automatically populated with current user'
        else:
            function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Participants field was automatically populated with current user', 'PASSED')
            print 'Asserted that Participants field is automatically populated with current user'
        time.sleep(1)
        #Add second user to Participants field
        driver.find_element_by_id("s2id_autogen2").click()
        driver.find_element_by_id("s2id_autogen2").send_keys(client_variables.fullname2)
        time.sleep(5)
        driver.find_element_by_id("s2id_autogen2").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Added second user to Participants field"
        """
        Add value to Employees Spoken to field
        driver.find_element_by_css_selector(".bootstrap-tagsinput").click()
        driver.find_element_by_css_selector(".bootstrap-tagsinput").clear()
        driver.find_element_by_css_selector(".bootstrap-tagsinput").send_keys("Richie Test")
        time.sleep(1)
        driver.find_element_by_css_selector(".bootstrap-tagsinput").send_keys(Keys.RETURN)
        time.sleep(1)
        """
        #Enter a string into the Comments field
        driver.find_element_by_id("Comments").clear()
        driver.find_element_by_id("Comments").send_keys("testing automated VFL creation")
        time.sleep(1)
        print "Entered value into Comments field"
        #Set Time In = 0:00 
        driver.find_element_by_css_selector("#TimeIn").click()
        driver.find_element_by_css_selector("#TimeIn").clear()
        time.sleep(1)
        driver.find_element_by_css_selector("#TimeIn").send_keys("0:00")
        time.sleep(1)
        #Set Time In = 1:00 
        driver.find_element_by_css_selector("#TimeOut").click()
        driver.find_element_by_css_selector("#TimeOut").clear()
        time.sleep(1)
        driver.find_element_by_css_selector("#TimeOut").send_keys("1:00")
        time.sleep(1)
        print "Set the Time In and Time Out fields"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:Successfully saved new VFL record')
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test001_add_new_VFL_record_test_details:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test001_add_new_VFL_record_test_details:TEST COMPLETED"

    def test_002_edit_existing_vfl_record(self):
        """Test to ensure that existing VFL records can be edited successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test002_edit_existing_vfl_record:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Edit the latest VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Change value of Comments field
        driver.find_element_by_id("Comments").clear()
        driver.find_element_by_id("Comments").send_keys("testing automated VFL creation - EDITED")
        time.sleep(1)
        print "Successfullt edited Comments field"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Assert that the changes to the VFL record have been saved
        changes_saved = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[7]").text
        try:
            assert changes_saved == "testing automated VFL creation - EDITED"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test002_edit_existing_vfl_record:Changes made to VFL record were not saved successfully', 'FAILED')
            print 'Assertion Exception - Changes to VFL Record have not been saved successfully'
        else:
            function_module.log_to_file('Test_VFL_Module:test002_edit_existing_vfl_record:Changes made to VFL record were saved successfully', 'PASSED')
            print 'Asserted that VFL record was edited and saved'
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test002_edit_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test002_edit_existing_vfl_record:TEST COMPLETED"

    def test_003_add_edit_delete_safe_acts(self):
        """Test to add a new Safe Act on the Acts tab. The newly created
        Act is then edited and also deleted. The Act is deleted so as to
        to simplify following tests."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test003_add_edit_delete_safe_acts:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Add a Safe Act of type 1
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[1]/i").click()
        Select(driver.find_element_by_id("Acts")).select_by_visible_text(client_variables.act_type1)
        driver.find_element_by_id("btnSubmitFormActs").click()
        time.sleep(2)
        print "Added Safe Act - First option in dropdown"
        #Assert that Safe Act of type 1 cannot be selected again, hence asserting that it has been successfully added
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[1]/i").click()
        elem = driver.find_element_by_xpath("//*[@id='Acts']/option[2]")
        selected_act_disabled = elem.get_attribute("disabled")
        try:
            assert selected_act_disabled == 'true'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test003_add_edit_delete_safe_acts:User can select the same Safe Act Twice', 'FAILED')
            print 'Assertion Exception - Was able to add to Safe Acts of the same type (1)'
        else:
            function_module.log_to_file('Test_VFL_Module:test003_add_edit_delete_safe_acts:Successfully asserted Safe Act type 1 cannot be added twice (1)', 'PASSED')
            print 'Asserted that Safe Acts of the same type cannot be added twice (1)'
        time.sleep(2)
        #Edit a Safe Act of type 1 and change to type 2
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-pencil").click()
        Select(driver.find_element_by_xpath("//*[@class='col col-6']/div/div/label/select")).select_by_visible_text(client_variables.act_type2)
        driver.find_element_by_css_selector(".fa.fa-save.glyphicon-size").click()
        time.sleep(2)
        print "Edited Safe Act - Second option in dropdown"
        #Assert that Safe Act of type 2 cannot be selected again, hence asserting the act has been successfully edited
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[1]/i").click()
        elem = driver.find_element_by_xpath("//*[@id='Acts']/option[3]")
        selected_act_disabled_2 = elem.get_attribute("disabled")
        try:
            assert selected_act_disabled_2 == 'true'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test003_add_edit_delete_safe_acts:User can select the same Safe Act twice', 'FAILED')
            print 'Assertion Exception - Was able to add to Safe Acts of the same type (2)'
        else:
            function_module.log_to_file('Test_VFL_Module:test003_add_edit_delete_safe_acts:Successfully asserted Safe Act type 2 cannot be added twice (2)', 'PASSED')
            print 'Asserted that Safe Acts of the same type cannot be added twice (2)'
        time.sleep(2)
        #Delete Safe Act
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-trash").click()
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        time.sleep(1)
        print "Successfully deleted Safe Act"
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test003_add_edit_delete_safe_acts:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test003_add_edit_delete_safe_acts:TEST COMPLETED"

    def test_004_add_edit_unsafe_acts(self):
        """Test to add a new Unsafe Act on the Acts tab. The newly created
        Act is then edited but not deleted. At least one Act needs to remain
        in order to successfully complete tests for comments and actions"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test004_add_edit_unsafe_acts:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Add an Unsafe Act of type 1
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[2]/i").click()
        Select(driver.find_element_by_id("Acts")).select_by_visible_text(client_variables.act_type1)
        driver.find_element_by_id("btnSubmitFormActs").click()
        time.sleep(2)
        print "Added Unsafe Act - First option in dropdown"
        #Assert that Unsafe Act of type 1 cannot be selected again, hence asserting that it has been successfully added
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[2]/i").click()
        elem = driver.find_element_by_xpath("//*[@id='Acts']/option[2]")
        selected_act_disabled = elem.get_attribute("disabled")
        try:
            assert selected_act_disabled == 'true'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test004_add_edit_unsafe_acts:User can select the same Unsafe Act Twice', 'FAILED')
            print 'Assetion Exception - Was able to add to Unsafe Acts of the same type (1)'
        else:
            function_module.log_to_file('Test_VFL_Module:test004_add_edit_unsafe_acts:Successfully asserted Unsafe Act type 1 cannot be added twice (1)', 'PASSED')
            print 'Asserted that Unsafe Acts of the same type cannot be added twice (1)'
        time.sleep(2)
        #Edit an Unsafe Act of type 1 and change to type 2
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-pencil").click()
        Select(driver.find_element_by_xpath("//*[@class='col col-6']/div/div/label/select")).select_by_visible_text(client_variables.act_type2)
        driver.find_element_by_css_selector(".fa.fa-save.glyphicon-size").click()
        time.sleep(2)
        print "Edited Unsafe Act - Second option in dropdown"
        #Assert that Safe Act of type 2 cannot be selected again, hence asserting the act has been successfully edited
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[2]/i").click()
        elem = driver.find_element_by_xpath("//*[@id='Acts']/option[3]")
        selected_act_disabled_2 = elem.get_attribute("disabled")
        try:
            assert selected_act_disabled_2 == 'true'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test004_add_edit_unsafe_acts:User can select the same Unsafe Act Twice', 'FAILED')
            print 'Assetion Exception - Was able to add to Unsafe Acts of the same type (2)'
        else:
            function_module.log_to_file('Test_VFL_Module:test004_add_edit_unsafe_acts:Successfully asserted Unsafe Act type 2 cannot be added twice (2)', 'PASSED')
            print 'Asserted that Unsafe Acts of the same type cannot be added twice (2)'
        time.sleep(2)
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test004_add_edit_unsafe_acts:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test004_add_edit_unsafe_acts:TEST COMPLETED"

    def test_005_add_conversations(self):
        """Test to add conversation to an existing Act"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test005_add_conversations:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Add a Conversation & assert that Comment field is mandatory
        driver.find_element_by_css_selector("i.fa.fa-comment-o.glyphicon-size").click()
        time.sleep(1)
        elem = driver.find_element_by_id("Comment")
        comment_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(comment_mandatory)
        time.sleep(1)
        print "Verified that Conversation Comment field is mandatory"
        driver.find_element_by_id("Comment").click()
        driver.find_element_by_id("Comment").clear()
        driver.find_element_by_id("Comment").send_keys("Testing adding conversations")            
        driver.find_element_by_id("submit_modalConversation").click()
        time.sleep(1)
        #Assert that Conversation has been added correctly
        elem = driver.find_element_by_xpath("//*[@class='col col-8']/label[1]").text
        try:
            assert elem == 'Testing adding conversations'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test005_add_conversations:Failed to add a conversation to an existing act', 'FAILED')
            print 'Assetion Exception - Conversation has not been added correctly'
        else:
            function_module.log_to_file('Test_VFL_Module:test005_add_conversations:Successfully asserted conversation was added', 'PASSED')
            print 'Asserted Conversation has been successfully added'
        time.sleep(1)
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test005_add_conversations:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test005_add_conversations:TEST COMPLETED"

    def test_006_edit_conversations(self):
        """Test to ensure that exisitng conversations can be edited successfully and
        that image files can be successfully attached to a conversation"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test006_edit_conversations:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Edit the Conversation & attach an Image
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-angle-down").click()
        time.sleep(1)
        driver.find_element_by_css_selector("i.fa.fa-pencil").click()
        driver.find_element_by_id("Comment").click()
        driver.find_element_by_id("Comment").clear()
        driver.find_element_by_id("Comment").send_keys("Testing adding conversations - EDITED")
        driver.find_element_by_xpath("//*[@id='btnAdd_Files']/input[@type='file']").send_keys("V:\QA\Automation\Automation_Resources\Attachments\Conversation Image\PM5544_with_non-PAL_signals.png")
        time.sleep(5)  
        driver.find_element_by_id("update_modalConversation").click()
        time.sleep(1)
        print "Attached image file to conversation correctly"
        #Assert that Conversation has been edited correctly
        elem = driver.find_element_by_xpath("//*[@class='col col-8']/label[.='Testing adding conversations - EDITED']").text
        try:
            assert elem == 'Testing adding conversations - EDITED'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test006_edit_conversations:Failed to edit an existing conversation', 'FAILED')
            print 'Assetion Exception - Conversation has not been edited correctly'
        else:
            function_module.log_to_file('Test_VFL_Module:test006_edit_conversations:Successfully edited an existing conversation and attached an image', 'PASSED')
            print 'Asserted Conversation has been successfully edited'
        time.sleep(1)
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test006_edit_conversations:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test006_edit_conversations:TEST COMPLETED"

    def test_007_delete_conversations(self):
        """Test to ensure that existing conversations can be successfully deleted"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test007_delete_conversations:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Delete the Conversation
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-angle-down").click()
        time.sleep(1)
        driver.find_element_by_css_selector("i.fa.fa-times").click()
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        time.sleep(2)
        #Verify Conversation was deleted by confirming that the edit conversation button is not present
        try:
            driver.find_element_by_css_selector("i.fa.fa-pencil")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test007_delete_conversations:Successfully deleted conversation', 'PASSED')
            print 'Asserted Conversation has been successfully deleted'
        else:
            function_module.log_to_file('Test_VFL_Module:test007_delete_conversations:Failed to delete conversation', 'FAILED') 
            print 'WARING - Failed to Delete Conversation'
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test007_delete_conversations:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test007_delete_conversations:TEST COMPLETED"

    def test_008_add_action(self):
        """Test to ensure that VFL Corrective Actions can be added to existin Acts
        All fields with mandatory requirements on the action from are tested with assertions
        NOTE: Test is unfinished as would like to add SQL based assertion to ensure Action was
        synced with main application correctly"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test008_add_action:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Add an Action
        driver.find_element_by_css_selector("i.fa.fa-file-text-o.glyphicon-size").click()
        time.sleep(1)
        print "Found Add Action button"
        #Verify DueDate is mandatory
        elem = driver.find_element_by_xpath("//*[@id='DueDate']")
        duedate_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(duedate_mandatory)
        #Verify Priority is mandatory
        elem = driver.find_element_by_xpath("//*[@id='Priority']")
        priority_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(priority_mandatory)
        #Verify Description is mandatory
        elem = driver.find_element_by_xpath("//*[@id='Description']")
        description_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(description_mandatory)
        #Verify AssignedTo is mandatory
        elem = driver.find_element_by_xpath("//*[@id='AssignedTo']")
        assigned_to_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(assigned_to_mandatory)
        print "Verified that all expected fields are mandatory"
        #Assert Action AssignedBy Current User
        current_user = driver.find_element_by_xpath("//*[@id='AssignedBy']/option[2]")
        try:
            assert current_user.text == client_variables.fullname1
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test008_add_action:Actions AssignedBy field is not automatically populated with current user', 'FAILED')
            print 'Assertion Error - Actions AssignedBy field was not automatically populated with current user'
        else:
            function_module.log_to_file('Test_VFL_Module:test008_add_action:Actions AssignedBy field was automatically populated with current user', 'PASSED')
            print 'Asserted that Actions AssignedBy field is automatically populated with current user'
        time.sleep(1)
        #Verify Status is read only and Assert default value = Not Started
        elem = driver.find_element_by_xpath("//*[@id='Status']")
        status_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(status_disabled)
        time.sleep(1)
        print "Verified that Actions Status field is read only"
        status_value = elem.get_attribute("value")
        try:
            assert status_value == 'Not Started'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test008_add_action:Actions Status is NOT "Not Started" by default', 'FAILED')
            print 'Assertion Error - Actions Status is NOT "Not Started" by default'
        else:
            function_module.log_to_file('Test_VFL_Module:test008_add_action:Actions Status is "Not Started" by default', 'PASSED')
            print 'Asserted that Actions Status is "Not Started" by default'
        time.sleep(1)
        #Select Due Date
        driver.find_element_by_xpath("//*[@id='DueDate']").send_keys(function_module.today())
        driver.find_element_by_xpath("//*[@id='DueDate']").send_keys(Keys.RETURN)
        time.sleep(2)
        print "Selected Due Date = Todays Date"
        #Select Priority
        Select(driver.find_element_by_xpath("//*[@id='Priority']")).select_by_visible_text("Low")
        time.sleep(2)
        print "Set Actions Priority = Low"
        #Add a Description
        driver.find_element_by_xpath("//*[@id='Description']").clear()
        driver.find_element_by_xpath("//*[@id='Description']").send_keys("testing automated VFL Corrective Actions")
        time.sleep(1)
        print "Gave the Action a description"
        #Select an AssignedTo user
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").click()
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(client_variables.username2)
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(Keys.RETURN)
        time.sleep(1)
        function_module.log_to_file('Test_VFL_Module:test008_add_action:Successfully selected user2 as Actions AssignedTo user', 'PASSED')
        print "Successfully found as selected an AssignedTo user"
        #Save the Action
        driver.find_element_by_xpath("//*[@id='submit_modalAction']").click()
        time.sleep(5)
        #Assert that Action has been added correctly
        elem = driver.find_element_by_xpath("//*[@class='col col-6']/label[1]").text
        try:
            assert elem == 'testing automated VFL Corrective Actions'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test008_add_action:Failed to add a action to an existing act', 'FAILED')
            print 'Assetion Exception - Action has not been added correctly'
        else:
            function_module.log_to_file('Test_VFL_Module:test008_add_action:Successfully asserted action was added', 'PASSED')
            print 'Asserted Action has been successfully added'
        time.sleep(1)
        
        #Research & Add SQL Based Assertions to check that Action has been added correctly. Alternatively, check Actions presence in Action Module
        
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test008_add_action:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test008_add_action:TEST COMPLETED"

    def test_009_edit_action(self):
        """Test to ensure that existing actions can be edited successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test009_edit_action:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Edit an Action
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-angle-down").click()
        time.sleep(1)
        driver.find_element_by_css_selector("i.fa.fa-pencil").click()
        time.sleep(1)
        print "Found Edit Action button successfully"
        #Change Priority
        Select(driver.find_element_by_xpath("//*[@id='Priority']")).select_by_visible_text("High")
        time.sleep(2)
        print "Priority of Action changed to High"
        #Add a Description
        driver.find_element_by_xpath("//*[@id='Description']").clear()
        driver.find_element_by_xpath("//*[@id='Description']").send_keys("testing automated VFL Corrective Actions - EDITED")
        time.sleep(1)
        print "Edited Actions Description"
        #Save the Action
        driver.find_element_by_xpath("//*[@id='update_modalAction']").click()
        time.sleep(5)
        #Assert that Action has been added correctly
        elem = driver.find_element_by_xpath("//*[@class='col col-6']/label[1]").text
        try:
            assert elem == 'testing automated VFL Corrective Actions - EDITED'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test009_edit_action:Failed to save changes to Action correctly', 'FAILED')
            print 'Assertion Exception - Failed to save changes to Action correctly'
        else:
            function_module.log_to_file('Test_VFL_Module:test009_edit_action:Successfully saved changes Action', 'PASSED')
            print 'Asserted that changes to Action have been saved correctly'
        time.sleep(1)
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test009_edit_action:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test009_edit_action:TEST COMPLETED"

    def test_010_delete_action(self):
        """Test to ensure that existing VFL Corrective Actions can be deleted successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test010_delete_action:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Choose to edit existing VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        print "Found Edit VFL button for latest VFL Record"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Delete an Action
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-angle-down").click()
        time.sleep(1)
        driver.find_element_by_css_selector("i.fa.fa-times").click()
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        time.sleep(1)
        #Verify Action was deleted by confirming that the edit Action button is not present
        try:
            driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test010_delete_action:Successfully deleted Action', 'PASSED')
            print 'Verified Action has been successfully deleted'
        else:
            function_module.log_to_file('Test_VFL_Module:test010_delete_action:Failed to delete Action', 'FAILED') 
            print 'WARNING - Failed to verify Action was deleted'
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test010_delete_action:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test010_delete_action:TEST COMPLETED"

    def test_011_view_existing_vfl_record(self):
        """Test to ensure that VFL records behave as expected when in view mode.
        All fields on the first tab have assertions to verify that they are disabled
        and various checks are performed on the Acts tab to ensure that controls for
        adding/editing acts are not present"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #View the latest VFL Record (READ-ONLY)
        #driver.find_element_by_css_selector("i.glyphicon.glyphicon-eye-open").click()
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[1]/i").click()
        print "Found View VFL button for latest VFL Record"
        #Verify that VflDate field is currently readonly/disabled
        elem = driver.find_element_by_id("VflDate")
        VflDate_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(VflDate_disabled)
        #Verify that WorkGroup field is currently readonly/disabled
        elem = driver.find_element_by_id("WorkGroup")
        WorkGroup_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(WorkGroup_disabled)
        #Verify that Business Unit/Product Line field is currently readonly/disabled
        elem = driver.find_element_by_id("ProductLine")
        Business_Unit_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(Business_Unit_disabled)
        #Verify that Location field is currently readonly/disabled
        elem = driver.find_element_by_id("Location")
        Location_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(Location_disabled)
        #Verify that Time In field is currently readonly/disabled
        elem = driver.find_element_by_id("TimeIn")
        TimeIn_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(TimeIn_disabled)
        #Verify that Time Out field is currently readonly/disabled
        elem = driver.find_element_by_id("TimeOut")
        TimeOut_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(TimeOut_disabled)
        #Verify that Minutes Spent field is currently readonly/disabled
        elem = driver.find_element_by_id("minutes")
        Minutes_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(Minutes_disabled)
        #Verify that Participants field is currently readonly/disabled
        elem = driver.find_element_by_id("Participants")
        Participants_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(Participants_disabled)
        #Verfiy that Employees Spoken To field is currently readonly/disabled
        elem = driver.find_element_by_id("PersonsSpokenTo")
        PersonsSpokenTo_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(PersonsSpokenTo_disabled)
        #Verify that Comments To field is currently readonly/disabled
        elem = driver.find_element_by_id("Comments")
        Comments_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(Comments_disabled)
        print "Verified that all fields on the VFL Details tab are set to read only when in View Mode"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Verify that Safe Acts radio button is not present on page
        try:
            driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[1]/i")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Safe Acts cannot be selected in View Mode', 'PASSED')
            print 'Verified that Safe Acts cannot be selected in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Safe Acts cannot be selected in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Safe Acts cannot be selected in View Mode'
        #Verify that UnSafe Acts radio button is not present on page
        try:
            driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[2]/i")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Unsafe Acts cannot be selected in View Mode', 'PASSED')
            print 'Verified that Unsafe Acts cannot be selected in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Unsafe Acts cannot be selected in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Unsafe Acts cannot be selected in View Mode'
        #Verify that Add Acts button is not present on page
        try:
            driver.find_element_by_id("btnSubmitFormActs")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Acts cannot be added in View Mode', 'PASSED')
            print 'Verified that Acts cannot be added in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Acts cannot be added in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Acts cannot be added in View Mode'
        #Verify that Add Comments button is not present on page
        try:
            driver.find_element_by_css_selector("i.fa.fa-comment-o.glyphicon-size")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Comments cannot be added in View Mode', 'PASSED')
            print 'Verified that Comments cannot be added in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Comments cannot be added in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Comments cannot be added in View Mode'
        #Verify that Add Actions button is not present on page
        try:
            driver.find_element_by_css_selector("i.fa.fa-file-text-o.glyphicon-size")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Actions cannot be added in View Mode', 'PASSED')
            print 'Verified that Actions cannot be added in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Actions cannot be added in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Actions cannot be added in View Mode'
        #Verify that Edit Act button is not present on page
        try:
            driver.find_element_by_css_selector("i.glyphicon.glyphicon-pencil")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Acts cannot be edited in View Mode', 'PASSED')
            print 'Verified that Acts cannot be edited in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Acts cannot be edited in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Acts edited be added in View Mode'
        #Verify that Delete Act button is not present on page
        try:
            driver.find_element_by_css_selector("i.glyphicon.glyphicon-trash")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that Acts cannot be deleted in View Mode', 'PASSED')
            print 'Verified that Acts cannot be deleted in View Mode'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that Acts cannot be deleted in View Mode', 'FAILED')
            print 'WARNING - Could not verify that Acts deleted be added in View Mode'
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test011_view_existing_vfl_record:TEST COMPLETED"

    def test_012_delete_existing_vfl_record(self):
        """Simple test to ensure that individual VFL record under test can be deleted successfully"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test012_delete_existing_vfl_record:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Delete the latest VFL Record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[3]/i").click()
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        time.sleep(3)
        print "Successfully found the Delete VFL Record button"
        #Assert that the VFL Record has been deleted correctly
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        try:
            assert amount_of_records == '0 to 0 of 0 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test012_delete_existing_vfl_record:Failed to delete VFL Record', 'FAILED')
            print 'Assertion Exception - Failed to delete VFL Record'
        else:
            function_module.log_to_file('Test_VFL_Module:test012_delete_existing_vfl_record:Successfully deleted VFL Record', 'PASSED')
            print 'Asserted that VFL Record has been successfully deleted'
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test012_delete_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test012_delete_existing_vfl_record:TEST COMPLETED"
    
    """
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    """
    
    def tearDown(self):
        """basic test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class Test_002_VFL_Main(unittest.TestCase):
    """Set of tests responsible for testing the functionality of
    the main VFL view/landing page"""
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_013_verify_default_filters(self):
        """Test to ensure that on initial page load the default filters of Creator = Current User
        and Participant = Current User are selected and applied as expected"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Verify Filter Panel is hidden by default
        elem = driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']")
        filter_panel_hidden = elem.get_attribute("style")
        function_module.field_is_hidden(filter_panel_hidden)
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        #Verify Filter Panel is now displayed
        elem = driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']")
        filter_panel_active = elem.get_attribute("style")
        function_module.field_is_not_hidden(filter_panel_active)
        #Assert creator field is automatically populated with current user
        current_user1 = driver.find_element_by_xpath("//*[@id='s2id_CreatedBy']/ul/li[1]/div")
        try:
            assert current_user1.text == client_variables.fullname1
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:Creator field is not automatically populated with current user', 'FAILED')
            print 'Assertion Error - Creator field was not automatically populated with current user'
        else:
            function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:Creator field was automatically populated with current user', 'PASSED')
            print 'Asserted that Creator field is automatically populated with current user'
        time.sleep(1)
        #Assert Participants field is automatically populated with current user
        current_user2 = driver.find_element_by_xpath("//*[@id='s2id_Participants']/ul/li[1]/div")
        try:
            assert current_user2.text == client_variables.fullname1
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:Participants field is not automatically populated with current user', 'FAILED')
            print 'Assertion Error - Participants field was not automatically populated with current user'
        else:
            function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:Participants field was automatically populated with current user', 'PASSED')
            print 'Asserted that Participants field is automatically populated with current user'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test013_verify_default_filters:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test013_verify_default_filters:TEST COMPLETED"

    def test_014_delete_multiple_VFL_records(self):
        """Test creates three new VFL records. After records are successfully created we verify that
        the delete multiple VFL records button is disabled by default. We then select all three
        records and delete them simultaneously. A safety check is included to delete all other
        records, if any."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test014_delete_multiple_VFL_records:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        for x in range(3):
            driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
            driver.find_element_by_id("VflDate").click()
            driver.find_element_by_link_text("1").click()
            driver.find_element_by_id("s2id_autogen1").click()
            driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_default_false)
            time.sleep(1)
            driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("ProductLine").click()
            Select(driver.find_element_by_id("ProductLine")).select_by_visible_text(client_variables.bu2)
            driver.find_element_by_id("ProductLine").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("Comments").clear()
            driver.find_element_by_id("Comments").send_keys("TEST 014 - Automated VFL#"+str(x))
            time.sleep(1)        
            driver.find_element_by_css_selector("#TimeIn").click()
            driver.find_element_by_css_selector("#TimeIn").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeIn").send_keys("0:00")
            time.sleep(1)      
            driver.find_element_by_css_selector("#TimeOut").click()
            driver.find_element_by_css_selector("#TimeOut").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeOut").send_keys("1:00")
            time.sleep(1)
            driver.find_element_by_id("btnNextSubmit").click()
            time.sleep(3)
            driver.find_element_by_link_text("Finish").click()
            time.sleep(3)
            print "Added TEST 014 - Automated VFL#"+str(x)
        print "Total number of Test VFL Records now = 3"
        #Verifiy Multi-Delete button is diabled by default
        elem = driver.find_element_by_xpath("//*[@id='removeVfl']")
        multi_delete_disabled = elem.get_attribute("disabled")
        time.sleep(1)
        function_module.field_is_read_only(multi_delete_disabled)
        #Select All VFL records on first page
        driver.find_element_by_xpath("//*[@id='dtVFL']/thead/tr/th[1]/input").click()
        time.sleep(1)
        #Verify that Multi-Delete button is now enabled
        elem = driver.find_element_by_xpath("//*[@id='removeVfl']")
        multi_delete_enabled = elem.get_attribute("disabled")
        function_module.field_is_not_read_only(multi_delete_enabled)
        driver.find_element_by_xpath("//*[@id='removeVfl']/i").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        function_module.log_to_file('Test_VFL_Module:test014_delete_multiple_VFL_records:All existing VFL Records have been deleted', 'PASSED')
        print "Successfully deleted all existing VFL Records"
        #If any records still exist, delete these also
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        time.sleep(1)
        while amount_of_records != '0 to 0 of 0 entries':
            driver.find_element_by_xpath("//*[@id='dtVFL']/thead/tr/th[1]/input").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='removeVfl']/i").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
            time.sleep(3)
            amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
            print amount_of_records
        print "Total number of Test VFL Records now = 0"    
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test014_delete_multiple_VFL_records:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test014_delete_multiple_VFL_records:TEST COMPLETED"

    def test_015_filter_by_date_range(self):
        """Test adds three new VFL records. After adding the records successfully, the default
        filters are cleared and a date range added instead. On applying the filters we verify that
        our three VFL records are returned as they exist within the specified date range. Calendar
        interactions are control by functions taken from the function_module.py file. The WorkGroup used in
        this test will be the parent of the WorkGroup used in test_016"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test015_filter_by_date_range:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        for x in range(3):
            driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
            driver.find_element_by_id("VflDate").click()
            driver.find_element_by_link_text("1").click()
            driver.find_element_by_id("s2id_autogen1").click()
            driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_parent)
            time.sleep(1)
            driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("ProductLine").click()
            Select(driver.find_element_by_id("ProductLine")).select_by_visible_text(client_variables.bu1)
            driver.find_element_by_id("ProductLine").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("Comments").clear()
            driver.find_element_by_id("Comments").send_keys("TEST 015 - Automated VFL#"+str(x))
            time.sleep(1)        
            driver.find_element_by_css_selector("#TimeIn").click()
            driver.find_element_by_css_selector("#TimeIn").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeIn").send_keys("0:00")
            time.sleep(1)      
            driver.find_element_by_css_selector("#TimeOut").click()
            driver.find_element_by_css_selector("#TimeOut").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeOut").send_keys("1:00")
            time.sleep(1)
            driver.find_element_by_id("btnNextSubmit").click()
            time.sleep(3)
            driver.find_element_by_link_text("Finish").click()
            time.sleep(3)
            print "Added TEST 015 - Automated VFL#"+str(x)
        print "Total number of Test VFL Records now = 3"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully"
        #Set From Date
        driver.find_element_by_xpath("//*[@id='CreatedOnFrom']").send_keys(function_module.first_day_of_month())
        driver.find_element_by_xpath("//*[@id='CreatedOnFrom']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Set From Date equals the first day of the current month"
        #Set To Date
        driver.find_element_by_xpath("//*[@id='CreatedOnTo']").send_keys(function_module.today())
        driver.find_element_by_xpath("//*[@id='CreatedOnTo']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Set To Date equals todays date"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button"
        #Verify expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 3 of 3 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test015_filter_by_date_range:Failed to successfully filter by Date Range', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by Date Range'
        else:
            function_module.log_to_file('Test_VFL_Module:test015_filter_by_date_range:Successfully filtered by Date Range', 'PASSED')
            print 'Asserted that filtering by Date Range works as expected'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test015_filter_by_date_range:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test015_filter_by_date_range:TEST COMPLETED"

    def test_016_filter_by_workgroup_no_subgroups(self):
        """Another three VFL records are added. They are added to a workgroup that is a child of the
        workgroup used in test_015. We also specifically select a Location for these three WorkGroups
        for use in test_018. We now have 6 VFL records to work. After successfully creating the new
        VFL records we clear the default filters and select the parent workgroup used in test_015.
        My unticking the SubWorkGroups checkbox and applying the filters we get three VFL recrods
        returned in the list view"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        for x in range(3):
            driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
            driver.find_element_by_id("VflDate").click()
            driver.find_element_by_link_text("1").click()
            driver.find_element_by_id("s2id_autogen1").click()
            driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_child)
            time.sleep(1)
            driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("ProductLine").click()
            Select(driver.find_element_by_id("ProductLine")).select_by_visible_text(client_variables.bu2)
            driver.find_element_by_id("ProductLine").send_keys(Keys.RETURN)
            time.sleep(1)
            Select(driver.find_element_by_id("Location")).select_by_visible_text(client_variables.location1)
            time.sleep(1)
            driver.find_element_by_id("Comments").clear()
            driver.find_element_by_id("Comments").send_keys("TEST 016 - Automated VFL#"+str(x))
            time.sleep(1)        
            driver.find_element_by_css_selector("#TimeIn").click()
            driver.find_element_by_css_selector("#TimeIn").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeIn").send_keys("0:00")
            time.sleep(1)      
            driver.find_element_by_css_selector("#TimeOut").click()
            driver.find_element_by_css_selector("#TimeOut").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeOut").send_keys("1:00")
            time.sleep(1)
            driver.find_element_by_id("btnNextSubmit").click()
            time.sleep(3)
            driver.find_element_by_link_text("Finish").click()
            time.sleep(3)
            print "Added TEST 015 - Automated VFL#"+str(x)
        print "Total number of Test VFL Records now = 6"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully"
        #Select a WorkGroup
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys(client_variables.wg_parent)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Parent WorkGroup selected"
        #Disable SubGroups
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/form/div/div/div[6]/div/label[3]/i").click()
        time.sleep(1)
        print "Disabled SubGroups checkbox"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 3 of 3 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:Failed to successfully filter by WorkGroup (No SubGroup)', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by WorkGroup (No SubGroup)'
        else:
            function_module.log_to_file('Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:Successfully filtered by WorkGroup (No SubGroup)', 'PASSED')
            print 'Asserted that filtering by WorkGroup (No SubGroup) works as expected'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test016_filter_by_workgroup_no_subgroups:TEST COMPLETED"

    def test_017_filter_by_workgroup_with_subgroups(self):
        """We remove the default filters and select WorkGroup equals the same parent WorkGroup selected
        in test_016. However this time we leave the SubWorkGroups checkbox selected and hence will get
        6 VFL records returned in the list view when the filters are applied"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully"
        #Select a WorkGroup
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys(client_variables.wg_parent)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen3']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Parent WorkGroup selected with SubGroups checkbox left checked"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 6 of 6 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:Failed to successfully filter by WorkGroup (With SubGroup)', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by WorkGroup (With SubGroup)'
        else:
            function_module.log_to_file('Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:Successfully filtered by WorkGroup (With SubGroup)', 'PASSED')
            print 'Asserted that filtering by WorkGroup (With SubGroup) works as expected'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test017_filter_by_workgroup_with_subgroups:TEST COMPLETED"

    def test_018_filter_by_location(self):
        """We clear the default filters and then select the same Location used when
        creating VFL records in test_016. After applying the Location filter we will
        have three VFL records returned"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test018_filter_by_location:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully"
        #Select Location
        Select(driver.find_element_by_xpath("//*[@id='Location']")).select_by_visible_text(client_variables.location1)
        time.sleep(2)
        print "Selected a value for Location filter"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 3 of 3 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test018_filter_by_location:Failed to successfully filter by Location', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by Location'
        else:
            function_module.log_to_file('Test_VFL_Module:test018_filter_by_location:Successfully filtered by Location', 'PASSED')
            print 'Asserted that filtering by Location works as expected'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test018_filter_by_location:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test018_filter_by_location:TEST COMPLETED"

    def test_019_filter_by_business_unit(self):
        """We clear the default filters and then select the same business unit used when
        creating VFL records in test_016. After applying the business unit filter we will
        have three VFL records returned"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test019_filter_by_business_unit:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully"
        #Select business unit
        Select(driver.find_element_by_xpath("//*[@id='ProductLine']")).select_by_visible_text(client_variables.bu2)
        time.sleep(2)
        print "Select a value from the Business Unit filter"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 3 of 3 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test019_filter_by_business_unit:Failed to successfully filter by Business Unit', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by Business Unit'
        else:
            function_module.log_to_file('Test_VFL_Module:test019_filter_by_business_unit:Successfully filtered by Business Unit', 'PASSED')
            print 'Asserted that filtering by Business Unit works as expected'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test019_filter_by_business_unit:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test019_filter_by_business_unit:TEST COMPLETED"

    def test_020_filter_by_creator_or_participant(self):
        """We login to the application using the user2 credentials and delete any records that currently
        exist that are associated to this user. We then add a single VFL record with this user, assigning
        user1 as a participant. Then we clear the default filters and test various combinations of the
        Creator & Participant fields. When all tests are finished we delete the record created using
        user2"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username2)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword2)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Successfully logged in (as User2) and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Delete all, if any, existing user2 records
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        time.sleep(2)
        while amount_of_records != '0 to 0 of 0 entries':
            driver.find_element_by_xpath("//*[@id='dtVFL']/thead/tr/th[1]/input").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='removeVfl']/i").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
            time.sleep(3)
            amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
            print amount_of_records
        print "Amount of VFL Records created by user2 = 0"
        #Add a single VFL record with Admin as a participant
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        driver.find_element_by_id("VflDate").click()
        driver.find_element_by_link_text("1").click()
        driver.find_element_by_id("s2id_autogen1").click()
        driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_default_false)
        time.sleep(1)
        driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_id("ProductLine").click()
        Select(driver.find_element_by_id("ProductLine")).select_by_visible_text(client_variables.bu2)
        driver.find_element_by_id("ProductLine").send_keys(Keys.RETURN)
        time.sleep(1)
        Select(driver.find_element_by_id("Location")).select_by_visible_text(client_variables.location1)
        time.sleep(1)
        driver.find_element_by_id("s2id_autogen2").click()
        driver.find_element_by_id("s2id_autogen2").send_keys(client_variables.fullname1)
        time.sleep(5)
        driver.find_element_by_id("s2id_autogen2").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_id("Comments").clear()
        driver.find_element_by_id("Comments").send_keys("TEST 020 - Buuser's Automated VFL")
        time.sleep(1)        
        driver.find_element_by_css_selector("#TimeIn").click()
        driver.find_element_by_css_selector("#TimeIn").clear()
        time.sleep(1)
        driver.find_element_by_css_selector("#TimeIn").send_keys("0:00")
        time.sleep(1)      
        driver.find_element_by_css_selector("#TimeOut").click()
        driver.find_element_by_css_selector("#TimeOut").clear()
        time.sleep(1)
        driver.find_element_by_css_selector("#TimeOut").send_keys("1:00")
        time.sleep(1)
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(3)
        driver.find_element_by_link_text("Finish").click()
        time.sleep(3)
        print "Amount of VFL Records created by user2 = 1"
        print "Total number of Test VFL Records now = 7"
        #FILTER BY CREATOR = USER1 ONLY
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully (1)"
        #Remove Default Filters
        driver.find_element_by_xpath("//*[@id='s2id_CreatedBy']/ul/li[1]/a").click()
        driver.find_element_by_xpath("//*[@id='s2id_Participants']/ul/li[1]/a").click()
        print "All default filters have been cleared (1)"
        #Filter by just Creator = user1
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(client_variables.fullname1)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "User1 selected for just Creator filter"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button (1)"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 6 of 6 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Failed to successfully filter by just Creator', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by just Creator'
        else:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Successfully filtered by just Creator', 'PASSED')
            print 'Asserted that filtering by just Creator works as expected'
        time.sleep(1)
        #FILTER BY PARTICIPANT = USER1 ONLY
        #Clear filters
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[2]").click()
        time.sleep(1)
        print "Existing filters have been cleared (1)"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully (2)"
        #Remove Default Filters
        driver.find_element_by_xpath("//*[@id='s2id_CreatedBy']/ul/li[1]/a").click()
        driver.find_element_by_xpath("//*[@id='s2id_Participants']/ul/li[1]/a").click()
        print "All default filters have been cleared (2)"
        #Filter by just Participant = user1
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(client_variables.fullname1)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "User1 selected for Participant filter"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button (2)"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 7 of 7 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Failed to successfully filter by just Participant (1)', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by just Participant (1)'
        else:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Successfully filtered by just Participant (1)', 'PASSED')
            print 'Asserted that filtering by just Participant works as expected (1)'
        time.sleep(1)
        #FILTER BY PARTICIPANT = USER2 ONLY
        #Clear filters
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[2]").click()
        time.sleep(1)
        print "Existing filters have been cleared (2)"
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully (3)"
        #Remove Default Filters
        driver.find_element_by_xpath("//*[@id='s2id_CreatedBy']/ul/li[1]/a").click()
        driver.find_element_by_xpath("//*[@id='s2id_Participants']/ul/li[1]/a").click()
        print "All default filters have been cleared (3)"
        #Filter by just Participant = user2
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(client_variables.fullname2)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "User2 selected for Participant filter"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button (3)"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 1 of 1 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Failed to successfully filter by just Participant (2)', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by just Participant (2)'
        else:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Successfully filtered by just Participant (2)', 'PASSED')
            print 'Asserted that filtering by just Participant works as expected (2)'
        time.sleep(1)
        #FILTER BY CREATOR = USER2 & PARTICIPANT = USER1
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        #Clear filters using alternative button
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[1]").click()
        time.sleep(1)
        print "Existing filters have been cleared (3)(ALTERNATIVE METHOD)"
        #Expand Filter Panel again
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully again (4)"
        #Remove Default Filters
        driver.find_element_by_xpath("//*[@id='s2id_CreatedBy']/ul/li[1]/a").click()
        driver.find_element_by_xpath("//*[@id='s2id_Participants']/ul/li[1]/a").click()
        print "All default filters have been cleared (4)"
        #Filter by Creator = user2 and participant = user1
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(client_variables.fullname2)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(client_variables.fullname1)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "User2 selected for Creator filter AND User1 selected for Participant filter"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button (4)"
        #Assert expected amount of rows returned
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        try:
            assert amount_of_records == 'Showing 1 to 7 of 7 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Failed to successfully filter by Creator AND Participant', 'FAILED')
            print 'Assertion Exception - Failed to successfully filter by Creator AND Participant'
        else:
            function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:Successfully filtered by Creator AND Participant', 'PASSED')
            print 'Asserted that filtering by Creator AND Participant works as expected'
        time.sleep(1)
        #DELETE RECORD ADDED BY USER2
        #Clear filters
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[2]").click()
        time.sleep(1)
        print "Existing filters have been cleared (4)"
        #Delete record
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[3]/i").click()
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        time.sleep(3)
        print "Amount of VFL Records created by user2 = 0"
        print "Total number of Test VFL Records now = 6"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test020_filter_by_creator_or_participant:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test020_filter_by_creator_or_participant:TEST COMPLETED"

    def test_021_pagination(self):
        """This test takes a long time as we first have to loop through the creation of 49 VFL Records.
        After all records have been added we should have a total of 55 VFL records. Using the pagination
        controls and assertions based on the string at the bottom left of the view, we verify that we
        are moving to the expected pages"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Add multiple VFL records for test
        for x in range(50):
            driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
            driver.find_element_by_id("VflDate").click()
            driver.find_element_by_link_text("1").click()
            driver.find_element_by_id("s2id_autogen1").click()
            driver.find_element_by_id("s2id_autogen1").send_keys(client_variables.wg_default_false)
            time.sleep(1)
            driver.find_element_by_id("s2id_autogen1").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("ProductLine").click()
            Select(driver.find_element_by_id("ProductLine")).select_by_visible_text(client_variables.bu2)
            driver.find_element_by_id("ProductLine").send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_id("Comments").clear()
            driver.find_element_by_id("Comments").send_keys("TEST 021 - Automated VFL#"+str(x))
            time.sleep(1)        
            driver.find_element_by_css_selector("#TimeIn").click()
            driver.find_element_by_css_selector("#TimeIn").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeIn").send_keys("0:00")
            time.sleep(1)      
            driver.find_element_by_css_selector("#TimeOut").click()
            driver.find_element_by_css_selector("#TimeOut").clear()
            time.sleep(1)
            driver.find_element_by_css_selector("#TimeOut").send_keys("1:00")
            time.sleep(1)
            driver.find_element_by_id("btnNextSubmit").click()
            time.sleep(3)
            driver.find_element_by_link_text("Finish").click()
            time.sleep(3)
            print "Added TEST 021 - Automated VFL#"+str(x)
        print "Total number of Test VFL Records now = 56"
        amount_of_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print amount_of_records
        time.sleep(1)
        #Move to next page
        driver.find_element_by_css_selector(".next>a").click()
        time.sleep(5)
        page_two = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print page_two
        try:
            assert page_two == 'Showing 11 to 20 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to move to the next page', 'FAILED')
            print 'Assertion Exception - Failed to move to the next page'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully moved to the next page', 'PASSED')
            print 'Asserted that we can successfully navigate to the next page'
        time.sleep(1)
        #Move to previous page
        driver.find_element_by_css_selector(".prev>a").click()
        time.sleep(5)
        page_one = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print page_one
        try:
            assert page_one == 'Showing 1 to 10 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to move to the previous page', 'FAILED')
            print 'Assertion Exception - Failed to move to the previous page'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully moved to the previous page', 'PASSED')
            print 'Asserted that we can successfully navigate to the previous page'
        time.sleep(1)
        #Move to last page
        driver.find_element_by_css_selector(".last>a").click()
        time.sleep(5)
        page_last = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print page_last
        try:
            assert page_last == 'Showing 51 to 56 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to move to the last page', 'FAILED')
            print 'Assertion Exception - Failed to move to the last page'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully moved to the last page', 'PASSED')
            print 'Asserted that we can successfully navigate to the last page'
        time.sleep(1)
        #Move to first page
        driver.find_element_by_css_selector(".first>a").click()
        time.sleep(5)
        page_first = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print page_first
        try:
            assert page_first == 'Showing 1 to 10 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to move to the first page', 'FAILED')
            print 'Assertion Exception - Failed to move to the first page'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully moved to the first page', 'PASSED')
            print 'Asserted that we can successfully navigate to the first page'
        time.sleep(1)
        #Change to display 5 records
        Select(driver.find_element_by_xpath("//*[@id='dtVFL_length']/span/label/select")).select_by_visible_text('5')
        time.sleep(5)
        five_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print five_records
        try:
            assert five_records == 'Showing 1 to 5 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to display 5 records', 'FAILED')
            print 'Assertion Exception - Failed to display 5 records'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully displayed 5 records', 'PASSED')
            print 'Asserted that we can successfully display 5 records'
        time.sleep(1)
        #Change to display 10 records
        Select(driver.find_element_by_xpath("//*[@id='dtVFL_length']/span/label/select")).select_by_visible_text('10')
        time.sleep(5)
        ten_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print ten_records
        try:
            assert ten_records == 'Showing 1 to 10 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to display 10 records', 'FAILED')
            print 'Assertion Exception - Failed to display 10 records'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully displayed 10 records', 'PASSED')
            print 'Asserted that we can successfully display 10 records'
        time.sleep(1)
        #Change to display 25 records
        Select(driver.find_element_by_xpath("//*[@id='dtVFL_length']/span/label/select")).select_by_visible_text('25')
        time.sleep(10)
        twenty_five_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print twenty_five_records
        try:
            assert twenty_five_records == 'Showing 1 to 25 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to display 25 records', 'FAILED')
            print 'Assertion Exception - Failed to display 25 records'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully displayed 25 records', 'PASSED')
            print 'Asserted that we can successfully display 25 records'
        time.sleep(1)
        #Change to display 50 records
        Select(driver.find_element_by_xpath("//*[@id='dtVFL_length']/span/label/select")).select_by_visible_text('50')
        time.sleep(20)
        fifty_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print fifty_records
        try:
            assert fifty_records == 'Showing 1 to 50 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to display 50 records', 'FAILED')
            print 'Assertion Exception - Failed to display 50 records'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully displayed 50 records', 'PASSED')
            print 'Asserted that we can successfully display 50 records'
        time.sleep(1)
        #Change to display 100 records
        Select(driver.find_element_by_xpath("//*[@id='dtVFL_length']/span/label/select")).select_by_visible_text('100')
        time.sleep(25)
        hundred_records = driver.find_element_by_xpath("//*[@id='dtVFL_info']").text
        print hundred_records
        try:
            assert hundred_records == 'Showing 1 to 56 of 56 entries'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Failed to display 100 records', 'FAILED')
            print 'Assertion Exception - Failed to display 100 records'
        else:
            function_module.log_to_file('Test_VFL_Module:test021_pagination:Successfully displayed 100 records', 'PASSED')
            print 'Asserted that we can successfully display 100 records'
        time.sleep(1)
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test021_delete_existing_vfl_record:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test021_delete_existing_vfl_record:TEST COMPLETED"

    def test_022_tool_tips(self):
        """Test includes a set of basic assertions to ensure that various elements on the main
        page have the expected tool-tip text that will be displayed on Mouse Over"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test022_tool_tips:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Assert Information text is correct
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[1]/label/i")
        information_text = elem.get_attribute("data-content")
        assert information_text == '<div>Total Minutes <br /><b>60</b></div><div>Site <br /><b>France</b></div><div>No. Conversations <br /><b>0</b></div><div>Safe Act(s) <br /><b>None</b></div><div>Unsafe Act(s) <br /><b>None</b></div>'
        print "Information Tool Tip for first VFL Record displays correct data"
        #Assert View ToolTip
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[1]")
        view_tool_tip = elem.get_attribute("data-original-title")
        assert view_tool_tip == 'View VFL'
        print "Tool Tip for View button is correct"
        #Assert Edit ToolTip
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]")
        view_tool_tip = elem.get_attribute("data-original-title")
        assert view_tool_tip == 'Edit VFL'
        print "Tool Tip for Edit  button is correct"
        #Assert Delete ToolTip
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[3]")
        view_tool_tip = elem.get_attribute("data-original-title")
        assert view_tool_tip == 'Delete VFL'
        print "Tool Tip for Delete button is correct"
        #Assert Add ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[1]")
        add_tool_tip = elem.get_attribute("data-original-title")
        assert add_tool_tip == 'Add New VFL'
        print "Tool Tip for Add button is correct"
        #Assert Delete All ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[2]")
        delete_all_tool_tip = elem.get_attribute("data-original-title")
        assert delete_all_tool_tip == 'Delete Selected VFL'
        print "Tool Tip for Delete Selected button is correct"
        #Assert Print ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[3]")
        print_tool_tip = elem.get_attribute("data-original-title")
        assert print_tool_tip == 'VFL Print Reports'
        print "Tool Tip for Print Reports button is correct"
        #Assert Export ToolTip
        elem = driver.find_element_by_xpath("//*[@id='widDtVFLs']/div/div[2]/div[1]/div/div[2]/div/div/a[4]")
        export_tool_tip = elem.get_attribute("data-original-title")
        assert export_tool_tip == 'Export Selected VFL'
        print "Tool Tip for Export button is correct"
        function_module.log_to_file('Test_VFL_Module:test022_tool_tips:All Tool Tips are correct', 'PASSED')
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test022_tool_tips:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test022_tool_tips:TEST COMPLETED"

    def test_023_creator_participant_rights(self):
        """All previous tests have proven that a Creator can view, edit and delete their own records.
        By adding User2 as a participant to the first record in the view and then logging in as User2,
        we can proceed to verify that as participants User2 can edit and view a record, but not delete it.
        We tend filter the view to only display issues where User1 is the exclusive participant. User2
        will therefore be limited to only viewing these records."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:Successfully logged in (as User1) and started test')
        print "Logged in as User1 successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Edit first Record and add User2 as Participant
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        time.sleep(1)
        driver.find_element_by_id("s2id_autogen2").click()
        driver.find_element_by_id("s2id_autogen2").send_keys(client_variables.fullname2)
        time.sleep(5)
        driver.find_element_by_id("s2id_autogen2").send_keys(Keys.RETURN)
        time.sleep(1)
        print "User 2 added as Participant to first VFL Record"
        #Move successfully to the next tab, close and log out
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        driver.find_element_by_link_text("Finish").click()
        time.sleep(1)
        print "Successfully saved VFL Record and returned to list view"
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        time.sleep(1)
        print "Logged out of application as User 1"
        #Login as User2
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username2)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword2)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:Successfully logged in (as User2) and started test')
        print "Logged in as User2 successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Verify Delete button is disabled for Participant
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr/td[8]/div[2]/div/a[3]")
        cannot_delete = elem.get_attribute("disabled")
        function_module.field_is_read_only(cannot_delete)
        print "User2 does not have permission to delete VFL Records where they are not the creator"
        #FILTER BY CREATOR & PARTICIPANT = USER1 ONLY
        #Expand Filter Panel
        driver.find_element_by_xpath("//*[@id='dtFilterHeaderContainerVfl']/div/a[1]").click()
        time.sleep(1)
        print "Expanded filter panel successfully"
        #Remove Default Filters
        driver.find_element_by_xpath("//*[@id='s2id_CreatedBy']/ul/li[1]/a").click()
        driver.find_element_by_xpath("//*[@id='s2id_Participants']/ul/li[1]/a").click()
        print "All default filters have been cleared"
        #Select Creator = user1
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(client_variables.fullname1)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Selected User1 as Creator"
        #Select Participant = user1
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(client_variables.fullname1)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(Keys.RETURN)
        time.sleep(1)
        print "Selected User1 as Participant"
        #Apply Filters
        driver.find_element_by_xpath("//*[@id='dtFilterFormContainerVfl']/div/div/div/a[2]").click()
        time.sleep(3)
        print "Have selected the Apply Filters button"
        #Verify Delete button is disabled for any user
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[2]/td[8]/div[2]/div/a[3]")
        cannot_delete2 = elem.get_attribute("disabled")
        function_module.field_is_read_only(cannot_delete2)
        print "User2 does not have permission to delete VFL Records where they are neither the creator or the participant"
        time.sleep(1)
        #Verify Edit button is disabled for any user
        elem = driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[2]/td[8]/div[2]/div/a[2]")
        cannot_edit = elem.get_attribute("disabled")
        function_module.field_is_read_only(cannot_edit)
        print "User2 does not have permission to edit VFL Records where they are neither the creator or the participant"
        time.sleep(1)
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:Successfully verified limited permissions for non creators AND/OR participants', 'PASSED')
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test023_creator_participant_rights:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test023_creator_participant_rights:TEST COMPLETED"


        """NOTE: test_024 is missing at the moment. This test will be responsible for testing the
        functionality of the Show/Hide columns control. This control is a javascript control and I
        need to first research how to locate javascript elements with webdriver"""

    def tearDown(self):
        """Standard test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)



class Test_003_VFL_Settings(unittest.TestCase):
    """Set of tests responsible for testing the functionality of
    VFL Settings dialog box"""
    def setUp(self):
        """Standard test setup method"""
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_025_add_year(self):
        """Test opens the VFL Setting dialog and a row with Year = Current Year and
        # of Visits = 3. Various assertions are used to ensure the increase and decrease
        buttons function correctly for both fields"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test025_add_year:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Open the VFL Settings Window
        driver.find_element_by_xpath("//*[@id='content']/div[1]/div[2]/div/a").click()
        time.sleep(3)
        print "Successfully opened VFL Settings dialog"
        #Assert that Year field is automatically populated with current year
        year_field = driver.find_element_by_xpath("//*[@id='Year']")
        year_value = year_field.get_attribute("aria-valuenow")
        current_year = datetime.datetime.now().year
        year_string = str(current_year)
        try:
            assert year_value == year_string
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year field is NOT set to current year by default', 'FAILED')
            print 'Assertion Error - The Settings Year field is NOT set to current year by default'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year field is set to current year by default', 'PASSED')
            print 'Asserted that the Settings Year field is set to current year by default'
        time.sleep(1)
        #Increase Year by 1 and assert change
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[1]/div/span/a[1]").click()
        year_field_new = driver.find_element_by_xpath("//*[@id='Year']")
        year_value_new = year_field_new.get_attribute("aria-valuenow")
        next_year = datetime.datetime.now().year + 1
        next_year_string = str(next_year)
        try:
            assert year_value_new == next_year_string
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year field was not increased by 1 as expected', 'FAILED')
            print 'Assertion Error - Failed to increase the year field by 1 as expected'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year field increased by 1', 'PASSED')
            print 'Asserted that the Settings Year field can be increased by 1'
        time.sleep(1)
        #Decrease Year by 1 and assert change
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[1]/div/span/a[2]").click()
        year_field_set = driver.find_element_by_xpath("//*[@id='Year']")
        year_value_set = year_field_set.get_attribute("aria-valuenow")
        this_year = datetime.datetime.now().year
        this_year_string = str(this_year)
        try:
            assert year_value_set == this_year_string
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year field was not decreased by 1 as expected', 'FAILED')
            print 'Assertion Error - Failed to decrease the year field by 1 as expected'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year field decreased by 1', 'PASSED')
            print 'Asserted that the Settings Year field can be decreased by 1'
        time.sleep(1)
        #Assert that No. Visits field is automatically populated value = 0
        visits_field = driver.find_element_by_xpath("//*[@id='NoVisits']")
        visits_value = visits_field.get_attribute("aria-valuenow")
        visits_string = str(visits_value)
        try:
            assert visits_string == "0"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field was NOT set to 0 by default', 'FAILED')
            print 'Assertion Error - Number of Visits field was not set to 0 by default'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field was set to 0 by default', 'PASSED')
            print 'Asserted that Number of Visits field was set to 0 by default'
        time.sleep(1)
        #Ensure that No. Visits can not have negative value entered
        for x in range(3):
            driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[2]").click()
        visits_field_neg = driver.find_element_by_xpath("//*[@id='NoVisits']")
        visits_value_neg = visits_field_neg.get_attribute("aria-valuenow")
        visits_string_neg = str(visits_value_neg)
        try:
            assert visits_string_neg == "0"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field can be assigned a negative value', 'FAILED')
            print 'Assertion Error - Number of Visits field can be assigned a negative value'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field can NOT be assigned a negative value', 'PASSED')
            print 'Asserted that Number of Visits field can NOT be assigned a negative value'
        time.sleep(1)
        #Increase No. Visits by 5 and assert change
        for x in range(5):
            driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[1]").click()
        visits_field_new = driver.find_element_by_xpath("//*[@id='NoVisits']")
        visits_value_new = visits_field_new.get_attribute("aria-valuenow")
        visits_string_new = str(visits_value_new)
        try:
            assert visits_string_new == "5"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field failed to increase to a value of 5', 'FAILED')
            print 'Assertion Error - Number of Visits field failed to increase to a value of 5'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field was increased to 5', 'PASSED')
            print 'Asserted that Number of Visits field was increased to 5'
        time.sleep(1)
        #Decrease No. Visits by 2 and assert change
        for x in range(2):
            driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[2]").click()
        visits_field_set = driver.find_element_by_xpath("//*[@id='NoVisits']")
        visits_value_set = visits_field_set.get_attribute("aria-valuenow")
        visits_string_set = str(visits_value_set)
        try:
            assert visits_string_set == "3"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field failed to decrease to a value of 3', 'FAILED')
            print 'Assertion Error - Number of Visits field failed to decrease to a value of 3'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits field was decreased to 3', 'PASSED')
            print 'Asserted that Number of Visits field was decreased to 3'
        time.sleep(1)
        #Add a row with Current Year and No. Visits = 3
        driver.find_element_by_xpath("//*[@id='btnSubmitFormSettings']").click()
        time.sleep(1)
        print "Have submitted the current year with 3 visits"
        #Assert first row has year = current year
        first_row_year = driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[1]").text
        first_row_year2 = datetime.datetime.now().year
        first_row_year2_string = str(first_row_year)
        try:
            assert first_row_year == first_row_year2_string
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year for first row is NOT set to the current year', 'FAILED')
            print 'Assertion Error - Year for first row is not set to the current year'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Year for first row is set to the current year', 'PASSED')
            print 'Asserted that Year for first row is set to the current year'
        time.sleep(1)
        #Assert first row No. Visits = 3
        first_row_visits = driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[2]").text
        try:
            assert first_row_visits == "3"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits for first row is NOT set to expected value of 3', 'FAILED')
            print 'Assertion Error - Number of Visits for first rowd is NOT set to expected value of 3'
        else:
            function_module.log_to_file('Test_VFL_Module:test025_add_year:Number of Visits for first row is set to expected value of 3', 'PASSED')
            print 'Asserted that Number of Visits for first row is set to expected value of 3'
        time.sleep(1)
        #Close the VFL Settings window
        driver.find_element_by_xpath("//*[@id='cancel_modalSettings']").click()
        time.sleep(1)
        print "Closed VFL Settings dialog box"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test025_add_year:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test025_add_year:TEST COMPLETED"

    def test_026_update_year(self):
        """Test verifies the various methods a user can update an existing row.
        A row can be updated by either attempting to add a value for a year that
        already exists OR by selecting the edit button for an existing row"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test026_update_year:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Open the VFL Settings Window
        driver.find_element_by_xpath("//*[@id='content']/div[1]/div[2]/div/a").click()
        time.sleep(3)
        print "Successfully opened VFL Settings dialog"
        #Assert that Year field is automatically populated with current year
        year_field = driver.find_element_by_xpath("//*[@id='Year']")
        year_value = year_field.get_attribute("aria-valuenow")
        current_year = datetime.datetime.now().year
        year_string = str(current_year)
        try:
            assert year_value == year_string
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Year field is NOT set to current year by default', 'FAILED')
            print 'Assertion Error - The Settings Year field is NOT set to current year by default'
        else:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Year field is set to current year by default', 'PASSED')
            print 'Asserted that the Settings Year field is set to current year by default'
        time.sleep(1)
        #Assert first row No. Visits = 3
        first_row_visits = driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[2]").text
        try:
            assert first_row_visits == "3"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Number of Visits for first row is NOT set to expected value of 3', 'FAILED')
            print 'Assertion Error - Number of Visits for first row is NOT set to expected value of 3'
        else:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Number of Visits for first row is set to expected value of 3', 'PASSED')
            print 'Asserted that Number of Visits for first row is set to expected value of 3'
        time.sleep(1)
        #Change Current Years No. Visits = 1 using fields at top of form
        driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[1]").click()
        driver.find_element_by_xpath("//*[@id='btnSubmitFormSettings']").click()
        time.sleep(1)
        print "Changed current years number of Visits from 3 to 1"
        #Assert first row No. Visits = 1
        first_row_visits_update1 = driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[2]").text
        try:
            assert first_row_visits_update1 == "1"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Number of Visits for first row is NOT set to expected value of 1', 'FAILED')
            print 'Assertion Error - Number of Visits for first row is NOT set to expected value of 1'
        else:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Number of Visits for first row is set to expected value of 1', 'PASSED')
            print 'Asserted that Number of Visits for first row is set to expected value of 1'
        time.sleep(1)
        #Change Current Years No. Visits = 4 using edit button
        driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[3]/div/div/a[1]/i").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='btnCancelFormSettings']").click()
        time.sleep(1)
        #function_module.log_to_file('Test_VFL_Module:test026_update_year:Successfully verified cancel update button works')
        driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[3]/div/div/a[1]/i").click()
        for x in range(3):
            driver.find_element_by_xpath("//*[@id='formSettings']/div/section[2]/div/span/a[1]").click()
        driver.find_element_by_xpath("//*[@id='btnUpdateFormSettings']").click()
        time.sleep(1)
        print "Changed current years number of Visits from 1 to 4"
        #Assert first row No. Visits = 4
        first_row_visits_update2 = driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[2]").text
        try:
            assert first_row_visits_update2 == "4"
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Number of Visits for first row is NOT set to expected value of 4', 'FAILED')
            print 'Assertion Error - Number of Visits for first row is NOT set to expected value of 4'
        else:
            function_module.log_to_file('Test_VFL_Module:test026_update_year:Number of Visits for first row is set to expected value of 4', 'PASSED')
            print 'Asserted that Number of Visits for first row is set to expected value of 4'
        time.sleep(1)
        #Close the VFL Settings window
        driver.find_element_by_xpath("//*[@id='cancel_modalSettings']").click()
        time.sleep(1)
        print "Closed VFL Settings dialog box"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test026_update_year:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test026_update_year:TEST COMPLETED"

    def test_027_delete_year(self):
        """Simple test is used to delete the row to the VFL Settings table
        that was just added and edited."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test027_delete_year:Successfully logged in and started test')
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Open the VFL Settings Window
        driver.find_element_by_xpath("//*[@id='content']/div[1]/div[2]/div/a").click()
        time.sleep(3)
        print "Successfully opened VFL Settings dialog"
        #Delete first row for current year
        driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[3]/div/div/a[2]/i").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='bot2-Msg1']").click()
        print "Deleting the first row"
        time.sleep(3)
        #Verify that first row has been deleted
        try:
            driver.find_element_by_xpath("//*[@id='dtSettingsContainer']/tr/td[1]")
        except NoSuchElementException:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Verified that the first row has been deleted', 'PASSED')
            print 'Verified that the first row has been deleted'
        else:
            function_module.log_to_file('Test_VFL_Module:test011_view_existing_vfl_record:Could not verify that the first row has been deleted', 'FAILED')
            print 'WARNING - Could not verify that the first row has been deleted'
        #Close the VFL Settings window
        driver.find_element_by_xpath("//*[@id='cancel_modalSettings']").click()
        time.sleep(1)
        print "Closed VFL Settings dialog box"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test027_delete_year:TEST COMPLETED', 'PASSED')
        print 'Test_VFL_Module:test027_delete_year:TEST COMPLETED'

    def tearDown(self):
        """Standard test tear down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


class Test_004_VFL_Export(unittest.TestCase):
    """Set of tests responsible for testing the export function for the VFL List View."""
    def setUp(self):
        """Setup edited so that its uses a specific firefox profile called 'auto_test_profile'.
        When using this firefox profile the user will not be prompted when downloading specific
        file types, such as .xlsx and .csv. Lines were left in but commented out that control
        the setup and tear down of a temp directory to be used for downloads. This approach might
        be revisited at a later stage."""
        auto_test_profile = webdriver.FirefoxProfile("C:/Users/rhoward.EMEX/AppData/Roaming/Mozilla/Firefox/Profiles/kz6phe2o.auto_test_profile")
        self.driver = webdriver.Firefox(firefox_profile=auto_test_profile)
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_028_export_all_excel(self):
        """Test creates .xlsx file which includes all current 55 VFL records. After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test028_export_all_excel:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #export all current records
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label[1]/i").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text("Excel")
        time.sleep(1)
        driver.find_element_by_id("submit_modalExport").click()
        time.sleep(2)
        driver.find_element_by_id("bot2-Msg1").click()
        time.sleep(2)
        print "Successfully exported all current VFL records - EXCEL"
        #Copy export to client specific folder
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test028_export_all_excel:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test028_export_all_excel:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test028_export_all_excel:TEST COMPLETED"

    def test_029_export_current_page_excel(self):
        """Test creates .xlsx file which includes all current page of VFL records (10 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test029_export_current_page_excel:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #export current page of VFL records
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label[2]/i").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text("Excel")
        time.sleep(1)
        driver.find_element_by_id("submit_modalExport").click()
        time.sleep(2)
        print "Successfully exported current page of VFL records - EXCEL"
        #Copy export to client specific folder
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test029_export_current_page_excel:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test029_export_current_page_excel:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test029_export_current_page_excel:TEST COMPLETED"

    def test_030_export_selected_rows_excel(self):
        """Test creates .xlsx file which includes only selected VFL records (5 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test030_export_selected_rows_excel:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Manually select top five records
        for x in range(1,6):
            y = str(x)
            driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr["+y+"]/td[1]/input").click()
        print "Selected top 5 VFL records on first page of list view"
        #export selected records only
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label[3]/i").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text("Excel")
        time.sleep(1)
        driver.find_element_by_id("submit_modalExport").click()
        time.sleep(2)
        print "Successfully exported selected VFL records - EXCEL"
        #Copy export to client specific folder
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test030_export_selected_rows_excel:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test030_export_selected_rows_excel:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test030_export_selected_rows_excel:TEST COMPLETED"

    def test_031_export_all_csv(self):
        """Test creates .csv file which includes all current 55 VFL records. After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test031_export_all_csv:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #export all current records
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label[1]/i").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text("CSV")
        time.sleep(1)
        driver.find_element_by_id("submit_modalExport").click()
        time.sleep(2)
        driver.find_element_by_id("bot2-Msg1").click()
        time.sleep(2)
        print "Successfully exported all current VFL records - CSV"
        #Copy export to client specific folder
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test031_export_all_csv:Successfully moved csv file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test031_export_all_csv:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test031_export_all_csv:TEST COMPLETED" 

    def test_032_export_current_page_csv(self):
        """Test creates .csv file which includes all current page of VFL records (10 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test032_export_current_page_csv:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #export current page of VFL records
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label[2]/i").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text("CSV")
        time.sleep(1)
        driver.find_element_by_id("submit_modalExport").click()
        time.sleep(2)
        print "Successfully exported current page of VFL records - CSV"
        #Copy export to client specific folder
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test032_export_current_page_csv:Successfully moved csv file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test032_export_current_page_csv:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test032_export_current_page_csv:TEST COMPLETED"

    def test_033_export_selected_rows_csv(self):
        """Test creates .csv file which includes only selected VFL records (5 in total). After the file is
        downloaded, the move_file() function is used to place the file into its client specific
        folder."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test033_export_selected_rows_csv:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Manually select top five records
        for x in range(1,6):
            y = str(x)
            driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr["+y+"]/td[1]/input").click()
        print "Selected top 5 VFL records on first page of list view"
        #export selected records only
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-export").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='formExport']/div[1]/section[1]/div/label[3]/i").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath("//*[@id='ExportAs']")).select_by_visible_text("CSV")
        time.sleep(1)
        driver.find_element_by_id("submit_modalExport").click()
        time.sleep(2)
        print "Successfully exported selected VFL records - CSV"
        #Copy export to client specific folder
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test033_export_selected_rows_csv:Successfully moved excel file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test033_export_selected_rows_csv:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test033_export_selected_rows_csv:TEST COMPLETED"
    
    def tearDown(self):
        """Test Tear Down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        

class Test_005_VFL_Reports(unittest.TestCase):
    """Set of tests responsible for testing the various VFL reports available to the user."""
    def setUp(self):
        """Setup edited so that its uses a specific firefox profile called 'auto_test_profile'.
        When using this firefox profile the user will not be prompted when downloading specific
        file types, such as .xlsx and .csv. Lines were left in but commented out that control
        the setup and tear down of a temp directory to be used for downloads. This approach might
        be revisited at a later stage."""
        auto_test_profile = webdriver.FirefoxProfile("C:/Users/rhoward.EMEX/AppData/Roaming/Mozilla/Firefox/Profiles/kz6phe2o.auto_test_profile")
        self.driver = webdriver.Firefox(firefox_profile=auto_test_profile)
        self.driver.implicitly_wait(30)
        self.base_url = client_variables.base_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_034_vfl_activity_summary_report_no_subgroups(self):
        """Test generates a VFL Activity Summary Report. The report is in .pdf format but gets openeding
        inside the browser. The test will change tab to the new tab and download the .pdf report for review
        later. NO Subgroups will be contained in this report"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Move to the Reports section
        driver.find_element_by_xpath("//*[@id='left-panel']/nav/ul/li[3]/a/i").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='content']/div[1]/div[1]/h1").text
        try:
            assert elem == 'Reports'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:Failed to access to the Report tab', 'FAILED')
            print 'Assertion Error - Failed to access to the Report tab'
        else:
            function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:Successfully moved to the Report section', 'PASSED')
            print 'Asserted that we have successfully moved to the Report section'
        #Open the VFL Activity Summary Report parameters & Verify that WorkGroup field is mandatory
        driver.find_element_by_xpath("//*[@id='widDtReports']/div/div[2]/div[1]/a").click()
        time.sleep(1)
        print "Opened VFL Activity Summary Report parameters"
        elem = driver.find_element_by_xpath("//*[@class='select required-select2']/input")
        workgroup_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(workgroup_mandatory)
        #Enter a high tiered WorkGroup that has lots of VFL records created during test.
        #Don't select the Include SubGroups checkbox.
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").click()
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(client_variables.wg_default_false)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(Keys.RETURN)
        time.sleep(2)
        #driver.switch_to_window(driver.window_handles[-1])
        #time.sleep(2)
        #driver.find_element_by_xpath("///*[@id='download']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='submit_modalSettings']").click()
        print "Generated and downloaded VFL Activity Summary Report"
        time.sleep(5)
        #Rename and Copy report to client specific folder
        source = client_variables.output_folder
        newname = 'Summary Report No Subgroups.pdf'
        renamefiles = os.listdir(source)
        ext = (".xlsx", ".csv", ".pdf", ".png")
        for renamefile in renamefiles:
            if renamefile.endswith(ext):
                renamefile = source + "/" + renamefile
                print "renaming:", renamefile
                newname = source + "/" + newname
                print "newname:", newname
                os.rename(renamefile, newname)
            elif renamefile.startswith('GetTotalByYearReport'):
                renamefile = source + "/" + renamefile
                print "renaming:", renamefile
                newname = source + "/" + newname
                print "newname:", newname
                os.rename(renamefile, newname)
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:Successfully moved report file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test034_vfl_activity_summary_report_no_subgroups:TEST COMPLETED"

    def test_035_vfl_activity_summary_report_with_subgroups(self):
        """Test generates a VFL Activity Summary Report. The report is in .pdf format but gets openeding
        inside the browser. The test will change tab to the new tab and download the .pdf report for review
        later. Subgroups will be contained in this report"""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Move to the Reports section
        driver.find_element_by_xpath("//*[@id='left-panel']/nav/ul/li[3]/a/i").click()
        time.sleep(1)
        elem = driver.find_element_by_xpath("//*[@id='content']/div[1]/div[1]/h1").text
        try:
            assert elem == 'Reports'
        except AssertionError:
            function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:Failed to access to the Report tab', 'FAILED')
            print 'Assertion Error - Failed to access to the Report tab'
        else:
            function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:Successfully moved to the Report section', 'PASSED')
            print 'Asserted that we have successfully moved to the Report section'
        #Open the VFL Activity Summary Report parameters
        driver.find_element_by_xpath("//*[@id='widDtReports']/div/div[2]/div[1]/a").click()
        time.sleep(1)
        print "Opened VFL Activity Summary Report parameters"
        elem = driver.find_element_by_xpath("//*[@class='select required-select2']/input")
        workgroup_mandatory = elem.get_attribute("aria-required")
        function_module.field_is_mandatory(workgroup_mandatory)
        #Enter a root WorkGroup that has lots of VFL records created during test.
        #Select Include SubGroups checkbox.
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").click()
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(client_variables.root_wg)
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='s2id_autogen2']").send_keys(Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='formSettings']/section[2]/div[2]/label/i").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='submit_modalSettings']").click()
        print "Generated and download VFL Activity Summary Report"
        time.sleep(15)
        #Rename and Copy report to client specific folder
        source = client_variables.output_folder
        newname = 'Summary Report With Subgroups.pdf'
        renamefiles = os.listdir(source)
        ext = (".xlsx", ".csv", ".pdf", ".png")
        for renamefile in renamefiles:
            if renamefile.endswith(ext):
                renamefile = source + "/" + renamefile
                print "renaming:", renamefile
                newname = source + "/" + newname
                print "newname:", newname
                os.rename(renamefile, newname)
            elif renamefile.startswith('GetTotalByYearReport'):
                renamefile = source + "/" + renamefile
                print "renaming:", renamefile
                newname = source + "/" + newname
                print "newname:", newname
                os.rename(renamefile, newname)
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:Successfully moved report file into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test035_vfl_activity_summary_report_with_subgroups:TEST COMPLETED"

    def test_036_vfl_summary_report(self):
        """Test generates a VFL Summary Report. No output file is generated by this report, so only capturing
        a screengrab can be used to ensure the report was correctly generated during testing."""
        driver = self.driver
        driver.get(self.base_url + "/")
        #Login to the application
        driver.find_element_by_name("UserName").clear()
        driver.find_element_by_name("UserName").send_keys(client_variables.username1)
        driver.find_element_by_name("Password").clear()
        driver.find_element_by_name("Password").send_keys(client_variables.pword1)
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:Successfully logged in and started test')
        time.sleep(5)
        print "Logged in successfully"
        #Select the VFL Module
        driver.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-comments").click()
        time.sleep(5)
        print "Moved to VFL Module"
        #Edit first VFL record in list, adding acts with comments, attachments and actions
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[8]/div[2]/div/a[2]/i").click()
        time.sleep(1)
        print "Edited first VFL record on list view page"
        #Move successfully to the next tab
        driver.find_element_by_id("btnNextSubmit").click()
        time.sleep(1)
        print "Moved to Acts Tab"
        #Add a Safe Act of type 1
        driver.find_element_by_xpath("//*[@id='formActs']/div/section[1]/div/label[1]/i").click()
        Select(driver.find_element_by_id("Acts")).select_by_visible_text(client_variables.act_type1)
        driver.find_element_by_id("btnSubmitFormActs").click()
        time.sleep(2)
        print "Added a Safe Act of type1"
        #Add a Conversation & attach an image
        driver.find_element_by_css_selector("i.fa.fa-comment-o.glyphicon-size").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='Comment']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='Comment']").send_keys("Testing adding conversations")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='btnAdd_Files']/input[@type='file']").send_keys("V:\QA\Automation\Automation_Resources\Attachments\Conversation Image\PM5544_with_non-PAL_signals.png")
        time.sleep(5)  
        driver.find_element_by_id("submit_modalConversation").click()
        time.sleep(1)
        print "Added a conversation with image file attached"
        #Add an Action
        driver.find_element_by_css_selector("i.fa.fa-file-text-o.glyphicon-size").click()
        time.sleep(1)
        #Select Due Date
        driver.find_element_by_xpath("//*[@id='DueDate']").send_keys(function_module.today())
        driver.find_element_by_xpath("//*[@id='DueDate']").send_keys(Keys.RETURN)
        time.sleep(2)
        #Select Priority
        Select(driver.find_element_by_xpath("//*[@id='Priority']")).select_by_visible_text("Low")
        time.sleep(2)
        #Add a Description
        driver.find_element_by_xpath("//*[@id='Description']").click()
        driver.find_element_by_xpath("//*[@id='Description']").send_keys("testing automated VFL Corrective Actions")
        time.sleep(1)
        #Select an AssignedTo user
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").click()
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(client_variables.username2)
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='s2id_autogen1']").send_keys(Keys.RETURN)
        time.sleep(1)
        #Save the Action
        driver.find_element_by_xpath("//*[@id='submit_modalAction']").click()
        time.sleep(5)
        print "Added an Action"
        #Select the finish button to return to the Main List View
        driver.find_element_by_link_text("Finish").click()
        print "Successfully saved VFL Record and returned to list view"
        #Assert the Print Report button is disabled by default
        elem = driver.find_element_by_xpath("//*[@id='printVfl']")
        print_disabled = elem.get_attribute("disabled")
        function_module.field_is_read_only(print_disabled)
        time.sleep(1)
        print "Print Report button disabled by default"
        #Select the first VFL record and choose the Print Report button
        driver.find_element_by_xpath("//*[@id='dtVFL']/tbody/tr[1]/td[1]/input").click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='printVfl']").click()
        time.sleep(3)
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:Successfully run Print Report for VFL Record')
        print "Selected VFL Record and selected Print Report button"
        #Take a screengrab of the generated report
        driver.switch_to_window(driver.window_handles[-1])
        time.sleep(2)
        driver.get_screenshot_as_file('V:/QA/Automation/Automation_Resources/Output/summary_report.png')
        time.sleep(2)
        #driver.get_screenshot_as_file(screenshot_string)
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:Successfully took a screenshot of report')
        print "took screenshot and saved to output folder"
        time.sleep(5)
        #Rename and Copy screengrab to client specific folder
        source = client_variables.output_folder
        newname = 'Print Report Screengrab.png'
        renamefiles = os.listdir(source)
        ext = (".xlsx", ".csv", ".pdf", ".png")
        for renamefile in renamefiles:
            if renamefile.endswith(ext):
                renamefile = source + "/" + renamefile
                print "renaming:", renamefile
                newname = source + "/" + newname
                print "newname:", newname
                os.rename(renamefile, newname)
            elif renamefile.startswith('GetTotalByYearReport'):
                renamefile = source + "/" + renamefile
                print "renaming:", renamefile
                newname = source + "/" + newname
                print "newname:", newname
                os.rename(renamefile, newname)
        function_module.move_file()
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:Successfully moved screenshot of report into client specific folder')
        time.sleep(2)
        print "Moved file into client specific folder"
        #Log out of the application
        driver.switch_to_window(driver.window_handles[0])
        time.sleep(2)
        driver.find_element_by_css_selector("i.fa.fa-power-off").click()
        driver.find_element_by_id("bot2-Msg1").click()
        function_module.log_to_file('Test_VFL_Module:test036_vfl_summary_report:TEST COMPLETED', 'PASSED')
        print "Test_VFL_Module:test036_vfl_summary_report:TEST COMPLETED"
    
    def tearDown(self):
        """Test Tear Down method"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
