from selenium import webdriver
from pyvirtualdisplay import Display
from mechanize import Browser
from bs4 import BeautifulSoup
import os, sys, time, getpass
from time_table import download_time_table

UMS_LOGIN_URL = 'https://ums.lpu.in/lpuums'
ASSIGNMENT_UPLOAD_URL = 'https://ums.lpu.in/LpuUms/frmAssignmentUpload.aspx'
PLATFORM = sys.platform
USER = getpass.getuser()
DEFAULT_PATH = "C:\\Program Files\\"

try:
    list_file = os.listdir(DEFAULT_PATH)
    if 'Class Reminder' in list_file:
        pass
    else:
        os.mkdir("C:\\Program Files\\Class Reminder")
        DEFAULT_PATH = "C:\\Program Files\\Class Reminder"
except:
    pass

LINUX_PATH = "/home/mama/Desktop/FacultyUms/"

br = Browser()
br.set_handle_robots(False)
try:
    br.open('https://ums.lpu.in/lpuums')
except:
    print 'Error in Opening url'

class Faculty:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def first_time_login(self):
           
        try:
            br.select_form(name='form1')
            br['TextBox1'] = self._username
            br['TextBox2'] = self._password
        except BrowserStateError as e:
            print "UMS is not working"
            sys.exit()

        content = br.submit()
        title_after_login = 'Lovely Professional University :: University Management System (UMS)'
        if br.title() == title_after_login:
            
            self.get_current_term_id()
            return True
        else: return False

    def class_scheduled_held(self):
        pass

    def update_time_table_file(self):
        """
            Get the last modified time from file and convert it into month.
            To compare with current month.
            If there is differnce of 2 months then call download_time_table()
        """
        
        last_modified = os.path.getmtime(DEFAULT_PATH + 'term_id')
        today = time.localtime(time.time()).tm_mon
        term_id = ''
        with open(DEFAULT_PATH + "term_id", "r") as f:
            term_id = int(f.readline())

        if (last_modified+2) % 12 != today:
            return
        else:
            download_time_table(self._usename, self._password, term_id)

    def update_term_id_file(self):
        """ 
            Get the last modified time from file and convert it into month.
            To compare with current month.
        """
        
        last_modified = time.localtime(os.path.getmtime('term')).tm_mon

        today = time.localtime(time.time()).tm_mon

        # if last_modified is less than 60 days then update it
        if (last_modified+2) % 12 != today:
            return
        else:
            self.get_current_term_id()


    def get_current_term_id(self):
        """ 
            Get current term id and download time table
            open a time table file and check if term_id exists in that 
            file then read and return that id
        """

        file_list = os.listdir(LINUX_PATH)
        if 'term_id' in file_list and 'rptTimeTableFaculty.xls' in file_list:
            print "Returning from get_current_term_id()"
            return
        

        try:
            content = br.open(ASSIGNMENT_UPLOAD_URL)
        except:
            pass
        
        soup = BeautifulSoup(content, 'html.parser')
        term_id = soup.find('span', id='ctl00_ContentPlaceHolder1_gvAssignment_ctl02_Label4').get_text()
        
        with open(DEFAULT_PATH + "term_id","w") as f:
            f.write(term_id)
            download_time_table(self._username, self._password, str(int(term_id)%100000))
            
        
        # return term_id

#if __name__ == "__main__":
#    faculty = Faculty('16915', 'Kh@123')
#    faculty.first_time_login()
