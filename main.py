from faculty_class import Faculty
import getpass


if __name__ == "__main__":
    username = raw_input("Username : ")
    password = getpass.getpass()
    faculty = Faculty(username, password)
    faculty.first_time_login()
    faculty.download_attendance_report()
