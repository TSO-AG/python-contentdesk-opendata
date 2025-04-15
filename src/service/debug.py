import json
from datetime import datetime
import logging
import os

# DEBUG
def loadToDebug(products, fileName):
    # get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    #print("Current date & time : ", current_datetime)
    
    # convert datetime obj to string
    str_current_datetime = str(current_datetime)
    
    # Check if folder exists
    if not os.path.exists("../../docs/debug/"+str_current_datetime+"/"):
        os.makedirs("../../docs/debug/"+str_current_datetime+"/")
    
    with open("../../docs/debug//"+str_current_datetime+"/"+fileName+".json", "w") as file:
        file.write(json.dumps(products))