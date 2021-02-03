import requests
from iBot import Robot

robotId='ZM75IV7V0BRH'
url = 'http://localhost:8000'
ip ='localhost'
port = '8001'
username ='enriquecrespodebenito'
password = 'Mariquinah3'
ExecutionId = '443622Y3YMTETDDJ5SCW48OB9T7Y0VKI'

robot = Robot(robotId, ExecutionId, url, ip, port, username, password)

#robot.createQueue("Pollastre")
Queue = robot.findQueueById('AHSHSJJAKKSKS')
robot.Log.info("Info")
robot.Log.systemException("System Exception")
robot.Log.businessException("Business Exception")
robot.Log.log("Log")