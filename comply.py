from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir_scrapli.tasks import send_command
import os
from colorama import Fore, Style
import threading

LOCK = threading.Lock()

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

with open('reader.txt', 'r') as f:
    filelines = f.readlines()

clear_command = "clear"
os.system(clear_command)
def runner(task):
    mylist=[]
    output = task.run(task=send_command, command= "show run")
    for cmd in filelines:
        if not cmd in output.result:
            mylist.append(cmd)
    if not mylist:
        john = "blah-de-blah"
    else:
        LOCK.acquire()
        print(Fore.GREEN + "*" * 80)
        print(Fore.RED + f"ALERT: {task.host} is not compliant!")
        print(Fore.YELLOW + "The following commands are missing:")
        try:
            for items in mylist:
                print(items)
        finally:
            LOCK.release()


results = nr.run(task=runner)

print_title("COMPLETED COMPLIANCE TEST")
