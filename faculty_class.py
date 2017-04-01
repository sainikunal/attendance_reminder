from selenium import webdriver
from pyvirtualdisplay import Display
from mechanize import Browser
from bs4 import BeautifulSoup
import os, sys, time, getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time_table import download_time_table
from section import get_sections

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
    print 'UMS is not responding or Internet Connection interrupted'
    sys.exit()

class Faculty:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def first_time_login(self):
           
        try:
            br.select_form(name='form1')
            br['TextBox1'] = self._username
            br['TextBox2'] = self._password
        except :
            print "UMS is not working"
            sys.exit()

        content = br.submit()
        title_after_login = 'Lovely Professional University :: University Management System (UMS)'
        if br.title() == title_after_login:
            
            self.get_current_term_id()
            return
        else: 
            print 'Invalid details'

    def class_scheduled_held(self):
        pass

    # never used in this project
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

    # never used in this project
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

        
    def download_attendance_report(self):
	    """
            prints all sections whose attendance is not marked on that day
            This method finds class on that day, from time table, if no class exists then simply exit,
            if more than one class exists then go to UMS, login with faculty ID, go to attendance report page, 
            and fetch the report of current day, parse html, compare fetched sections with time table,
            It doesn't tells makeup/adjustment classes.
        """
        option = webdriver.ChromeOptions()
    	option.add_argument('load.strategy=unstable')
    
    	driver = webdriver.Chrome(chrome_options = option)

    	driver.get('https://ums.lpu.in/lpuums')
    	script = "document.getElementById('TextBox1').value = '%d';\
                document.getElementById('TextBox2').value= '%s';"\
                % (int(self._username),self._password) 
    
        try:
            submit_button = WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.ID, 'iBtnLogin'))
                    )
        except :
            print "UMS is taking too long to respond"
            driver.close()
            sys.exit()
    	driver.execute_script(script) 
        submit_button.click()
        title_after_login = 'Lovely Professional University :: University Management System (UMS)'
	try:
	    if driver.title != title_after_login:
	        print '{:>2}'.format('[*] Login with valid Details.')
	        driver.close()
        	sys.exit()
	except:
	    print 'Incorrect Details'
            driver.close()
	    sys.exit()

        driver.get('https://ums.lpu.in/lpuums/Reports/frmClassesPlannedVsActual.aspx')
        date_picker = driver.find_element_by_id('TabContainer1_ReportView_RadDatePicker1_dateInput')
        today = time.localtime(time.time())
        day = today.tm_mday
        month = today.tm_mon
        year = today.tm_year
        day_of_week = today.tm_wday
        date = '%s/%s/%s' %(month,day,year)
        date_picker.send_keys(date)
        button = driver.find_element_by_id('TabContainer1_ReportView_btnShow')
        button.click()

        week_days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday',
                    4:'Friday', 5:'Saturday', 6:'Sunday'}
        section_list = get_sections()
        class_that_day = section_list[week_days[day_of_week]]
        # ['K1506', K1526', ... ]

        total_class = len(class_that_day)
        
        # store all sections found in webpage and compare with time table
        # display those which do not match
        section_marked = []
        section_left = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        
        scheduled = int(soup.find('span',id='TabContainer1_ReportView_gvPlannedVSSchedule_ctl02_Label13').text.encode('utf-8'))
        
        held = int(soup.find('span',id='TabContainer1_ReportView_gvPlannedVSSchedule_ctl02_Label14').text.encode('utf-8'))


        if total_class  > 0:

            # get section names from source of page
            # starting from 2 because of span id in web page
            iterate = max(held,scheduled,total_class)

            for i in range(2, iterate+2):
                            
                try:
                    # span which contains section id
                    section_span = 'TabContainer1_ReportView_gvPlannedVSSchedule_ctl02_gvScheduleDetails_ctl0' + str(i) + '_Label1'
                    
                    # Attendance marked time 
                    marked_time = 'TabContainer1_ReportView_gvPlannedVSSchedule_ctl02_gvScheduleDetails_ctl0' + str(i) + '_LblAttendanceTime'
                    
                    section_span = soup.find('span', id=section_span).text.encode('utf-8')
                    marked_time = soup.find('span', id=marked_time).text.encode('utf-8')
                    
                    section_marked.append(section_span)
                    
                except:
                    pass
                    
            for i in range(len(class_that_day)):
                if class_that_day[i] not in section_marked:
                    section_left.append(class_that_day[i])
            
            print "Section without Attendace : %s" % section_left
        else:
            print "You don't have any class on %s" % week_days[day_of_week]
        driver.close()
        


