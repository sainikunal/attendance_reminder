from xlrd import open_workbook

def get_sections():
    """
        Return a dictionary with Days as keys and no. of sections
        to teach(on that day) as a list 
    """

    # src = 'C:\\Users\\Program Files\\rptTimeTableFaculty.xls'

    src = '/home/mama/Desktop/FacultyUms/rptTimeTableFaculty.xls'
    book = open_workbook(src, on_demand=True)
    sheet = book.sheet_by_name('rptTimeTableFaculty')
    rows = [8,9,10,11,12,13,14,15]

    #  [Mon,Tue,Wed,Thu,Fri,Sat,Sun]
    cols = [3,6,9,11,13,14,18]
    days = {3:'Monday', 6:'Tuesday', 9:'Wednesday', 
        11:'Thursday', 13:'Friday', 14:'Saturday',
        18:'Sunday'}

    week_days = ['Monday','Tuesday','Wednesday','Thursday','Friday',
            'Saturday','Sunday']

    section_on_day = {}
    for column in cols:
        c = sheet.col(column)
        desk = []
        for j in range(len(c)):
            if c[j].value == '' or c[j].value == ' ':
                continue
            else:
                if c[j].value in week_days:
                    continue
                    
                # Fetch only section name
                val = c[j].value.split('/')[0].split(':')[1].encode('utf-8')
                desk.append(val)
    
        section_on_day[days[column]] = desk
    return section_on_day

