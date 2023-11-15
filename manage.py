import os
import sys
from pathlib import Path
from robot_manager.flow import RobotFlow
from robot.robot import Robot

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--doc":
            RobotFlow.connect_nodes()
            process_document = f"#Robot\n{Robot.__doc__}"
            process_document = process_document + "\n" + RobotFlow.generate_documentation()
            folder = Path(os.path.dirname(os.path.realpath(__file__))).parent
            with open(os.path.join("Pdd.md"), 'w') as file:
                file.write(process_document)
                file.close()
    else:
        raise Exception("No arguments provided")
