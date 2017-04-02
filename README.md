#  Attendance Reminder

## Module Requirements : 

Note: Apply ```sudo``` if required for your system.
You should have some of the linux packages installed which are
- google chrome
- xvfb
- chrome driver

To install chrome driver follow the instructions:
```
  sudo apt-get install libxss1 libappindicator1 libindicator7
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

  sudo dpkg -i google-chrome*.deb
  sudo apt-get install -f
 ```
 Now we need to install ```xvfb``` which allows us to run Chrome headlessly
 ```
  sudo apt-get install xvfb
 ```
 Time to install ChromeDrive and make it executable
 ```
  sudo apt-get install unzip

  wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
  unzip chromedriver_linux64.zip
  chmod +x chromedriver

  sudo mv -f chromedriver /usr/local/share/chromedriver
  sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
  sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
 ```
  Install the required packages by running:
  
  ```python
    pip install -r requirements.txt
  ```
   
This project is useful only for LPU Faculty members. It tells how many sections are left without attendance on that day.
Date is picked from system clock.

### To execute run the below command
  ```python
    python main.py
  ```
