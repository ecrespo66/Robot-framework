# Robot Framework

Robot-framework is an RPA frame written in Python, it is designed for an easy and fast development of RPA automations.
You can connect your developments with the **robot manager console** to use cloud features or execute your process locally.

visit https://ibott.io/Academy/robot-manager to learn more about the robot manager features.

## Robot Files
Find the robot files in the **robot** directory.
### 1. robot.py
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
        print("I'm the fitst method")
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


### 2. flow.py

Here You can create your custom node classes for your workflow.
New node classes must heritage from the base class RobotNode and be registered in the enum class Nodes.

**Run function:**

You can also override function run for default framework nodes.

**Example:**

```python
from iBott.robot_activities.nodes import *
from enum import Enum


class CustomNode(RobotNode):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        
    #Override default run method    
    def run(self, robot, *args):
        print("I'm the run funtion")
        
#Register custom nodes            
class Nodes(Enum):
    CustomNode = CustomNode

```
### 3. exceptions.py
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
    
    def _init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def process_exception(self):
       #send log to robot manager console.
       self.robot.Log.business_exception(self.message)
       #Process exception
       if self.next_action == "retry":
          self.retry(3)
       elif self.next_action == "restart":
          self.restart(3)
       elif self.next_action == "go_to_node":
          self.go_to_node("end",3)
       elif self.next_action == "skip":
          self.skip()
       elif self.next_action == "stop":
          self.stop()
       else:
          raise Exception("Invalid next_action")
       
       
class BusinessException(Exception):
   def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
   def process_exception(self):
     self.robot.Log.business_exception(self.message)
     self.stop()
```
       
          
### 3.settings.py
Here you can define all the constants you are going to use during the process.

````python
import os
from pathlib import Path

"""Folders to store Chrome Driver DON'T CHANGE"""
ROBOT_FOLDER = Path(os.path.dirname(os.path.realpath(__file__))).parent
CHROMEDRIVER_PATH = os.path.join(ROBOT_FOLDER, "Driver")

"""Email General settings"""
EMAIL_ACCOUNT = None
EMAIL_PASSWORD = None
````
        













