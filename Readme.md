# Robot Framework

Robot-framework is an RPA frame written in Python, it is designed for an easy and fast development of RPA automations.
You can connect your developments with the **robot manager console** to use cloud features or execute your process locally.

visit https://ibott.io/Academy/robot-manager to learn more about the robot manager features.

## [Robot folder](robot)
Find the robot files in the **[robot](robot)** directory. 
### [1. robot.py](robot/robot.py)
**Robot class:**

This class is used to design the main structure of the robot.
It contains all the methods to be executed by the robot.
Heritages from Bot class to use predefine features and attributes.

**Example:**

```python
from robot.robot import Bot
    
class Robot(Bot):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)   
        
    def start(self):
        print("I'm the first method")
        
    def second(self):
        print("I'm the second method")
        
    def last(self):
        print("I'm the last method")    

```        

**Arguments:**

Robot class can receive some arguments to establish connection with the robot manager console.
These arguments are sent automatically from the robot manager console to initialize Bot class and establish the connection. 
You can also set the variables in **debug.json** file to use some console features while debugging your code.


1. robotId: The robot's ID.
2. ExecutionId: The execution ID.
3. url: The url of the iBott API.
4. username: The username of iBott account.
5. password: The password of iBott account.
6. orchestrator_parameters: Additional parameters sent from the robot manager console.

**Decorators:**

@RobotFlow is a decorator class that creates the flow of the bot.
It grabs all decorated functions from the Robot class to create the workflow. 

Example:

```python
from robot.robot import Bot
from iBott import RobotFlow
from robot.flow import Nodes


class Robot(Bot):
   def __init__(self):
      super().__init__()

   @RobotFlow(Nodes.StartNode)
   def start(self):
      print("I'm the fitst method")
```

**Arguments:**
To instance Nodes classes and register them in the flow.
1. Nodes: Nodes class that contains the nodes of the flow read more in flow.py .
2. parents: *optional - Defines the ancestors of the current node in the flow.
3. condition: *optional - Defines the condition of the current node for conditional nodes.


**BusinessException & SystemException**

Default exception classes for the robot.
You must define your own process_exception method in file robot/exceptions.py if you want to use them.
1. BusinessException: Exception raised when the robot fails due to a Business error like input errors, data validation etc.
2. SystemException: Exception raised when the robot fails due to a System error like connection errors, etc.

**Arguments:**

1. Robot: Robot class
2. Message: Exception message
3. next_action: method from robot class to be executed after the exception occurs. like retry, restart, skip, etc.


### [2. flow.py](robot/flow.py)   

Here You can create your custom node classes for your workflow.
New node classes must heritage from the base class RobotNode and be registered in the enum class Nodes.

**Run function:**

You can also override function run for default framework nodes.

**Example:**

```python
from iBott.robot_activities.nodes import *
from enum import Enum


class CustomNode(RobotNode):
   def __init__(self, **kwargs):
      super().__init__(**kwargs)

   # Override default run method    
   def run(self, robot, *args):
      print("I'm the run funtion")


# Register custom nodes            
class Nodes(Enum):
   CustomNode = CustomNode

```
### [3. exceptions.py](robot/exceptions.py)  
Here you can define the actions your process must do when exceptions are raised.

**SystemException:**
This class Heritages from *RobotException* and is used to handle exceptions caused by system errors.

**BusinessException:**
This class Heritages from *RobotException* and is used to handle exceptions caused by Business errors.

*RobotException* class has  3 default actions to handle the exception:
1. retry: Retry the current node.
   1. restart: Restart the current node.
   2. go_to_node: Go to a specific node.
   3. skip: Skip the current node.
   4. stop: Stop the current flow.

Example:

```python
from iBott.robot_activities.exceptions import RobotException


class SystemException(RobotException):

   def __init__(self, *args, **kwargs):
      super.__init__(*args, **kwargs)

   def process_exception(self):
      # send log to robot manager console.
      self.robot.Log.business_exception(self.message)
      # Process exception
      if self.next_action == "retry":
         self.retry(3)
      elif self.next_action == "restart":
         self.restart(3)
      elif self.next_action == "go_to_node":
         self.go_to_node("end", 3)
      elif self.next_action == "skip":
         self.skip()
      elif self.next_action == "stop":
         self.stop()
      else:
         raise Exception("Invalid next_action")


class BusinessException(RobotException):
   def __init__(self, *args, **kwargs):
      super.__init__(*args, **kwargs)

   def process_exception(self):
      self.robot.Log.business_exception(self.message)
      self.stop()
```
        
### [3.settings.py](robot/settings.py)  
Here you can define all the constants you are going to use during the process.

````python

"""Email settings"""
EMAIL_ACCOUNT = None
EMAIL_PASSWORD = None
SMTP_HOST = None
SMTP_PORT = None
IMAP_HOST = None
IMAP_PORT = None
````
        

# [iBott Folder](iBott)
Here you can find pre made activities for your rpa developments.

## [Browser activities](iBott/browser_activities)
### [1. Chrome.py](iBott/browser_activities/chrome.py)  
Here you can find ChromeBrowser class. 
This class is used to create a browser object.
It Heritages from the Chrome class and implements some custom methods to make browser automation easier.

#### Arguments:
1. driver_path: path to the driver
2. undetectable: if True, the browser will not be detected by antispam systems.
 
#### Attributes:
1. driver_path: path to the driver
2. undetectable: if True, the browser will not be detected by antispam systems.
3. chrome_version: version of chrome
4. options: options for the browser

#### Custom Methods:
1. open(): open the browser and load defined options.
2. ignore_images(): ignore images in the browser.
3. ignore_popups(): ignore popups in the browser.
4. ignore_notifications(): ignore notifications in the browser.
5. ignore_errors(): ignore errors in the browser.
6. headless(): open the browser in headless mode.
7. save_cookies(): save the cookies of the browser.
8. load_cookies(): load the cookies of the browser.
9. set_proxy(proxy): set a proxy for the browser.
10. set_user_agent(user_agent): set a user agent for the browser.
11. set_profile(path): set a profile for the browser.
12. scrolldown(h): scroll down to % height of the page .
13. scrollup(h): scroll up to % height of the page .
14. scroll_to_element(element): scroll to the element.
15. set_download_folder(folder): set the download folder.
16. element_exists(element): check if the element exists.
17. add_tab(): add a new tab.
18. get_tabs(): get the tabs of the browser.
19. close_tab(): close the current tab.
20. switch_to_tab(tab_number): switch to the tab.
21. wait_for_element(element, timeout): wait for the element to appear.
22. wait_for_element_to_disappear(element, timeout): wait for the element to disappear.
23. wait_for_element_to_be_clickable(element, timeout): wait for the element to be clickable.

### [2. firefox.py](iBott/browser_activities/firefox.py)  
Here you can find FirefoxBrowser class.  This class is used to create a browser object.
It Heritages from the Firefox class and implements some custom methods to make browser automation easier.

### Arguments:
driver_path: path to the driver
undetectable: if True, to hide bot info in the browser.
### Attributes:
1. driver_path: path to the driver
2. undetectable: if True, to hide bot info in the browser.
### Methods:
1. open(): This method opens firefox browser to start the navigation. Set Custom options before using this method.
2. ignore_images(): This method ignores images in the browser. 
3. ignore_popups(): This method ignores popups in the browser. 
4. ignore_notifications(): This method ignores notifications in the browser. 
5. ignore_errors(): This method ignores errors in the browser. 
6. headless(): This method ignores 
7. save_cookies(): This method saves cookies in the browser. 
8. load_cookies(): This method loads cookies in the browser. 
9. set_proxy(): This method sets proxy in the browser. 
10. set_user_agent(): This method sets user agent in the browser. 
11. set_profile(): This method sets profile in the browser. 
12. set_download_folder(): This method sets download folder in the browser. 
13. scrolldown(): This method scrolls down the browser. 
14. scrollup(): This method scrolls up the browser. 
15. scroll_to_element(): This method scrolls to the element in the browser. 
16. element_exists(): This method checks if the element exists in the browser. 
17. add_tab(): This method adds a new tab in the browser. 
18. get_tabs(): This method gets all the tabs in the browser. 
19. switch_tab(): This method switches to the tab in the browser. 
20. wait_for_element(): This method waits for the element in the browser. 
21. wait_for_element_to_disappear(): This method waits for the element to disappear in the browser. 
22. wait_for_element_to_be_clickable(): This method waits for the element to be clickable in the browser. 

### [3. web_elements.py](iBott/browser_activities/web_elements.py) 
Custom WebElement class to add custom methods to WebElement class.
### Methods:
1. double_click() : Double click on the element. 
2. enter(): Enter text in the element. 
3. tab(): Tab on the element. 
4. escape(): Escape on the element. 
5. backspace(): Backspace on the element. 
6. write(text): Write text in the element. 
7. clear(): Clear the element. 
8. get_text(): Get text from the element. 
9. get_link(): Get link from the element. 
10. get_attribute(attribute): Get attribute from the element.


## [email activities](iBott/email_activities)
### [1. mails.py](iBott/email_activities/mails.py) 
Mail class, used to send and read email messages.
Arguments:
1. email: str
2. password: str
3. smtp_server: str
4. smtp_port: int
5. imap_server: str
6. imap_port: int

Attributes:
1. username: username of the mail account 
2. password: password of the mail account 
3. smtp_server: smtp server of the mail account 
4. smtp_port: smtp port of the mail account 
5. imap_server: imap server of the mail account 
6. imap_port: imap port of the mail account

Methods:
1. send(send_to, subject, text=None, html=None, files=None): send mail 
2. fetch(folder, Query) : fetch mail list from mailbox use Query object and return MailMessage list 
3. find more information about Mail and Query objects here: https://pypi.org/project/imap-tools/0.16.1/#id2


## [files_and_folders](iBott/files_and_folders)
### [1. files.py](iBott/files_and_folders/files.py) 
Class to handle files.
Arguments:
1. file_path (str): path to the file

Attributes:
1. file_path (str): path to the file
2. exists (bool): whether the file exists
3. file_name (str): name of the file
4. byte_size (int): size of the file in bytes
5. creation_datetime (datetime): datetime of the file's creation
6. modification_datetime (datetime): datetime of the file's last modification

Methods:
1. rename(new_file_name): renames the file 
2. move(new_location): moves the file to a new location 
3. remove(): removes the file 
4. copy(new_location): copies the file to a new location 
5. wait_for_file_to_exist(timeout=10): waits for the file to exist


### [2. folders.py](iBott/files_and_folders/folders.py) 
Class to handle folders. 
If folder doesn't exist it automatically creates a new one.
Arguments:
1. path (str) -- path to folder to be instanced.

Attributes:
1. path (str) -- path to folder to be instanced.
2. name (str) -- name of folder
    
Methods:
1. rename(new_folder_name) : Rename folder 
2. move(new_location): move folder to new location 
3. remove(allow_root=False, delete_read_only=True) : remove folder and all files and folders inside 
4. empty(allow_root=False): delete all files and folders in folder, receives allow_root as parameter 
5. copy(new_location=None) : Copy folder to new location 
6. subfolder_list(): list of subfolders 
7. file_list(): list of files in folder 
8. download_file(url, name=None): downloads file from url

### [3. images.py](iBott/files_and_folders/images.py) 
Image Class, heritates from File class
Attributes:
1. size {tuple}: size of image
2. format {str}: format of image

Methods:

1. rotate(): rotate image
2. resize(): resize image
3. crop(): crop image
4. mirrorH(): mirror image horizontally
5. mirrorV(): mirror image vertically

### [3. pdfs.py](iBott/files_and_folders/pdfs.py) 
PDF Class Heritates from File Class
Arguments:
1. file_path (str): Path of the file

Attributes:
1. file_path (str): Path of the file
2. pages (int): number of pages in the file
3. info (str): info of the file

Methods:
1. read_pages(page_num, encoding=None): Returns a string with the text in the page
2. append(pdf_document2,merge_path): Appends a pdf document to the current document
3. split(): split pdf into several pdfs.

## [Computer Vision](iBott/computer_vision)
### [1. ocr_activities.py](iBott/computer_vision/ocr_activities.py)
This class is used to perform OCR on a pdf or an image file.
It uses tesseract technology to convert images to text.
Arguments:
1. path (engine): The path to the OCR engine .
    
Methods:
1. set_config(config): Sets the config for the OCR engine. 
2. read_picture(file_path, lang): Reads a picture and returns the text. 
3. read_pdf(file_path, scale, lang): Reads a pdf and returns the text. 
4. to_grayscale(file_path): Converts an image to grayscale. 
5. remove_noise(file_path): Removes noise from an image. 
6. thresholding(file_path): Thresholds an image. 
7. canny(file_path): Performs canny edge detection on an image. 
8. deskew(file_path): Deskews an image. 
9. opening(file_path): Performs an opening on an image. 
10. erode(file_path): Erodes an image. 
11. dilate(file_path): Dilates an image. 
12. opening(file_path): Performs an opening on an image.

### [2. screen_activities.py](iBott/computer_vision/screen_activities.py)
Screen Class finds and interacts with Bitmap elements on the screen.
Attributes:
1. screen_size (tuple): The size of the screen. 
2. mousePosition (tuple): The position of the mouse.

Methods:
1. click(clicks, button) - Perform click action on the screen. 
2. move_mouse_to(pos) - Move mouse to the specified position. 
3. drag_mouse_to(pos) - Drag mouse to the specified position. 
4. find_element(image_path) - Find the specified element on the screen. 
5. write(text) - Write text to the screen. 
6. click_image(image_path) - Click the specified image on the screen. 
7. shoot(image_path) - Take a screenshot of the screen.

## [Offce activities](iBott/office_activities)
### [1. excels.py](iBott/office_activities/excels.py)
Excel Class, receives path of excel file as parameter
If Excel file doesn't exist it will be created automatically
Arguments:
1. path {str} -- path of excel file

Attributes:
1. workbook {openpyxl.workbook.workbook.Workbook} -- workbook of excel file

Methods:
1. open() -- open excel file 
2. save() -- save excel file 
3. add_sheet() -- add new worksheet to current workbook 
4. remove_sheet() -- remove sheet name 
5. rename_sheet() -- rename sheet name 
6. get_sheets() -- get a list of sheets in current workbook 
7. read_cell() -- read cell value. 
8. read_row_col() -- write cell value. 
9. write_cell() -- write cell value. 
10. write_row_col() -- write cell value.


### [2. words.py](iBott/office_activities/words.py)


Class to manage Word files it heritages from File class
Arguments:
1. file_path (str): path to the file

Attributes:
1. document (docx.Document): document object

Methods:
1. open(): open the file 
2. save(path): save the file 
3. add_heading(text, level): add a heading to the document '
4. add_paragraph(text, style): add a paragraph to the document 
5. add_picture(path, size): add a picture to the document 
6. add_table(matrix): add a table to the document 
7. read(): read the file and return the text 
8. convert_to_pdf(path): convert the file to pdf

### [3. powerpoints.py](iBott/office_activities/powerpoints.py)


