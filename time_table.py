from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import os,time
from shutil import copyfile
import getpass

def download_time_table(username, password, term_id):
    driver = webdriver.Chrome()
    driver.get('https://ums.lpu.in/lpuums')
    TextBox1 = driver.find_element_by_id('TextBox1')
    TextBox1.send_keys(username, Keys.TAB)
    TextBox2 = driver.find_element_by_id('TextBox2')
    TextBox2.send_keys(password)

    submit_button = driver.find_element_by_id('iBtnLogin')
    submit_button.click()
    driver.get('https://ums.lpu.in/LpuUms/Reports/frmMyTimeTable.aspx')
    select = Select(driver.find_element_by_xpath('//*[@id="DropDownList1"]'))
    
    for option in select.options:
        try:
            option_value = option.text  #.encode('utf-8')
            if option_value == term_id.decode("utf-8"):
                option.click()
        except:
            pass
     
    try:
        if sys.platform == 'linux2':
            os.chdir('/home/mama/Desktop/FacultyUms')
        else: os.chdir("C:\\Users\\Program Files")
    except:
        pass
    
    time.sleep(4) 
    # Download Excel file of time table 
    driver.execute_script("$find('ReportViewer1').exportReport('EXCEL');")
    time.sleep(4)
    
    # copy the time table at C: drive
    destination = ''
    src = ''
    """if os.path.isdir("C:\\Users\\Program Files"):
        destination = "C:\\Users\\Program Files" + "rptTimeTableFaculty.xls"

    else:
        destination = "C:\\Users\\Downloads" + "rptTimeTableFaculty.xls"

    if os.path.isdir("C:\\Users\\"+ user +"\\Downloads":
        #destination = os.getcwd() + "\\rptTimeTable.xls"
        # src = "C:\\Users\\" + user + "\\Downloads\\rptTimeTable.xls"
    """
    user = getpass.getuser()
    dest = 'C:\\Program Files\\Class Reminder\\rptTimeTableFaculty.xls'
    src = 'C:\\Users\\'+user+'\\rptTimeTableFaculty.xls'
    #destination = "/home/mama/Desktop/FacultyUms/rptTimeTableFaculty.xls"
    #src = "/home/mama/Downloads/rptTimeTableFaculty.xls"
        
        # src = "~/home/mama/Downloads/rptTimeTable.xls"
    copyfile(src, destination)
    #os.remove('/home/mama/Downloads/rptTimeTableFaculty.xls')

    #file_name = 'rptTimeTableFaculty.xls'
    #src = os.path.abspath('Downloads/'+file_name)
    #shutil.copyfile(src, os.getcwd())
    #os.rename('rptTimeTableFaculty.xls','Time Table.xls')

#download_time_table(16915,'Kh@123','16172')
