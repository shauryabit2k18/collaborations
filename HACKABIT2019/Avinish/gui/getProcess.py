
import subprocess
import re
import requests
import json
import tkinter as tk


class process():
    def __init__(self):
        print(process)
        allowedProcesses = []
        file = open("allowedProcesses.txt", "r")
        for name in file:
            name = re.sub('\n', '', name)
            allowedProcesses.append(name)
        #print(allowedProcesses)

        LARGE_FONT= ("Verdana", 12)
        NORM_FONT = ("Helvetica", 10)
        SMALL_FONT = ("Helvetica", 8)

        # Funtion for providing popup when a process which is not recognised as a productive one is running

        def checkList(vars, List):        
            File = open("allowedProcesses.txt", 'a+')
            for i in range(0, len(List)):
                if vars[i].get():
                    File.write(List[i])
            File.close()

        def on_click(vars, i):
            print(i , vars[i].get())
            if vars[i].get() == True:
                vars[i].set(False)
            else :
                vars[i].set(True)
            
        def popupmsgtoaddexception(msg):
            popup = tk.Tk()
            popup.wm_title("Add Exception")
            label = tk.Label(popup, text="Select/Close to cancel", font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            List = json.loads(msg)
            vars = []
            jj = []
            checkbox = []
            for i in range(0, len(List)):
                print(i , " -> 6666666\n")
                vars.append(tk.BooleanVar())
                checkbox.append("4")
                checkbox[i] = tk.Checkbutton(popup, text=List[i], variable=vars[i], command = lambda index=i: on_click(vars,index))
                checkbox[i].pack()
                vars[i].set(False)        

            B1 = tk.Button(popup, text="Confirm", command = lambda: checkList(vars, List)).pack()
            popup.mainloop()

        def popupmsg(msg):
            popup = tk.Tk()
            popup.wm_title("!")
            label = tk.Label(popup, text=msg, font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Add Exception", command =  lambda: popupmsgtoaddexception(msg))
            B1.pack()
            popup.mainloop()

        # Function for the popup ends and getting the processes starts

        processNameSource = subprocess.Popen(["powershell","gps | ? {$_.mainwindowtitle} | select name | ft -AutoSize"],stdout=subprocess.PIPE)

        processNames = processNameSource.communicate()[0].decode('ascii').strip().split('\r\n')

        for ii in range(0, len(processNames) - 1) :
            processNames[ii] = re.sub(' +', '', processNames[ii])
            
        # removed Column titles : 'Names' from the list
        del processNames[:2]

        processesToCLose = []
        for ii in range(0, len(processNames)-1) :
            runningProcess = processNames[ii]
            result = [allowedProcessName for allowedProcessName in allowedProcesses if(allowedProcessName.lower() in runningProcess.lower() or runningProcess.lower() in allowedProcessName.lower())]
            if not bool(result) :
                processesToCLose.append(runningProcess)

        jsonStringProcessesToClose = json.dumps(processesToCLose, separators=(',', ':'))
        print(jsonStringProcessesToClose)

        popupmsg(jsonStringProcessesToClose)

        print(not bool(processesToCLose))


# if bool(processesToCLose) :
#     requests.post(url = "http://localhost:3001", jsonStringProcessesToClose)
