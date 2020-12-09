# start includeing librarys that we need for work
import time
import main

def read_datas_every_S():
    while True:
        main.getalldatas()
        time.sleep(1)