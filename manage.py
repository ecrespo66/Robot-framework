import os
import sys
from getpass import getpass
from pathlib import Path
from iBott import RobotFlow
from robot.robot import Robot

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create_documentation":
            RobotFlow.connect_nodes()
            process_document = f"#Robot\n{Robot.__doc__}"
            process_document = process_document + "\n" + RobotFlow.generate_documentation()
            folder = Path(os.path.dirname(os.path.realpath(__file__))).parent

            with open(os.path.join("robot.md"), 'w') as file:
                file.write(process_document)

        if sys.argv[1] == "--add_credentials":
            username = input("Username: ")
            password = getpass("Password: ")
            orchestrator_url = input("Orchestrator URL: ")
            os.environ["IBOTT_USERNAME"] = username
            os.environ["IBOTT_PASSWORD"] = password
            os.environ["IBOTT_ORCHESTRATOR_URL"] = orchestrator_url
    else:
        raise Exception("No arguments provided")
