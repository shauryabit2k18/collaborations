import tkinter as tk
from tkinter import *
import tkinter.messagebox as tm
import json 
import requests
import multiprocessing
from threading import Thread
import sys
import gaze_dnn
import time
import receive
import getProcess
from PIL import *
from PIL import ImageTk as itk

back = '#454647'
titleBack = '#343b80'
startClick = 0

logInToken = ""
r =tk.Tk()
contentFrame = Frame(r, bg=back)



def popupmsg(): 
    background = 'plot1.jpg'
    img = Image.open('plot1.jpg')
    img.show()

class eyeDetails :
	def __init__(self):
		global contentFrame
		contentFrame.destroy()
		contentFrame = Frame(r, bg=back)
		title = Label(contentFrame, text = "Eye Details")
		title.pack(side = TOP)
		contentFrame.pack(side = TOP, fill=BOTH, expand=True)
		contentFrame.tkraise()


class history :
	def __init__(self) :
		global contentFrame
		contentFrame.destroy()
		contentFrame = Frame(r, bg=back)
		title = Label(contentFrame, text = "History")
		title.pack(side = TOP)
		contentFrame.pack(side = TOP,fill=BOTH,expand=True)

class plot:
	def __init__(self) :
		global contentFrame
		contentFrame.destroy()
		contentFrame = Frame(r, bg=back)
		img = PhotoImage(Image.open("True1.gif"))
		panel = Label(contentFrame, image = img)
		panel.pack(side = "TOP", fill = "both", expand = "yes")


class dashboard:
    def __init__(self):
        self.bottomFrame = Frame(r,bg=back,padx=20,pady=30)
        self.onOFFButton = Button(self.bottomFrame,text='Start',width=20,height=2,bg=titleBack,fg='white',font=(None,11,'bold'),border=0,command=self.onOFF)
        self.onOFFButton.pack(side=RIGHT)
        self.bottomFrame.pack(side=BOTTOM,fill=X)
        r.title('Destello')
        r.configure(background=back)
        r.geometry("800x600")

        titleFrame = Frame(r,bg=titleBack)
        titleFrame.pack(side=TOP, fill=X,ipady=2)

        title = Label(titleFrame,text="Destello",bg=titleBack,fg="white",font=('Woodcut', 18,'italic'))
        title.pack(fill=X)

        topdown = Frame(r,height=10)
        eyeHealthButton = Button(topdown, text = 'Eye Health',width=20,height=2,bg="green",relief=SUNKEN,fg='white',font=(None,11,'bold'),border=0, command=popupmsg) # add command to execute
        eyeHealthButton.pack(side=LEFT, padx = 8, pady = 10, fill=X)

        # seperator = Label(topdown, text = ' History ',width=20,height=2,bg="green",relief=SUNKEN,fg='white',font=(None,11,'bold'),border=0)
        # seperator.pack(side = LEFT, padx = 8, pady = 10)

        # historyOptions = StringVar(r)
        # historyOptions.set("Select")


        # historyDropdown = OptionMenu(topdown, historyOptions, "Past 24 hrs", "Past 30 days ")
        # historyDropdown.pack(side = LEFT, padx = 8, pady = 10)
        # addExceptionAppButton = Button(topdown, text = "Add exception app")
        # addExceptionAppButton.pack(side=LEFT, padx = 8, pady = 3)

        # logoutButton = Button(topdown, text = "Logout")
        # logoutButton.pack(side=LEFT, padx = 8, pady = 3, fill=X)

        topdown.pack(side=TOP, fill=X)

        
        # def on_field_change(self,*args):
        #     print("value changed to " + historyOptions.get())
        #     history()
        # historyOptions.trace('w', on_field_change)
        contentm = Frame(r,bg=back)
        wel = Label(contentm,text="Welcome to Destello",bg=back,fg='white',font=(None, 30),pady=100)
        desc = Label(contentm,text="We will take care of your study",bg=back,fg='#1600a6',font=(None, 18),pady=10)
        wel.pack()
        desc.pack()
        contentm.pack(side=TOP,fill=BOTH,expand=True)
        r.mainloop()

    def onOFF(self):
        global startClick 
        startClick+=1
        if(startClick%2==1):
            self.start()
        else:
            self.stop()

    def start(self):
        self.onOFFButton.configure(text='Stop')
        self.t2 = gaze_dnn.track()
        self.t1 = receive.alert()
        # try:
        self.t1.start()
        self.t2.start()
        getProcess.process()
        #     while True: time.sleep(100)
        # except (KeyboardInterrupt, SystemExit):
        #     print('\n! Received keyboard interrupt, quitting threads.\n')
            
    def stop(self):
        self.onOFFButton.configure(text='Start')
        self.t2.stop()
        self.t1.stop()

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        master.geometry("400x200")
        self.label_email = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_email.grid(row=0, sticky=E,pady=(70,0))
        self.label_password.grid(row=1, sticky=E,pady=(10,0))
        self.entry_email.grid(row=0, column=1,pady=(70,0))
        self.entry_password.grid(row=1, column=1,pady=(10,0))

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(column=0,pady=(30,0))
        
        self.signbtn = Button(self, text="Signup", command=self._signup_open)
        self.signbtn.grid(row=2,column=1,pady=(30,0))

        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        email = self.entry_email.get()
        password = self.entry_password.get()

        # print(email, password)

        url = "http://localhost:3001/users/login"
        # dic = '{"email":"'+email+'", "password":"'+password+'"}'
        dic = '{"email":"avnishmay@gmail.com", "password":"test1234"}'

        data = json.loads(dic)
        print(data)
        res = requests.post(url = url , json = data) 
        print(res.text)
        resJSON = json.loads(res.text) 
        print(resJSON)
        if resJSON == {}:
            tm.showerror("Login error", "Incorrect email")
        else:
            saveToken(resJSON['token'])
            self.destroy()
            dash = dashboard()
        # if email == "john" and password == "password":
        #     tm.showinfo("Login info", "Welcome John")
        # else:
        #     tm.showerror("Login error", "Incorrect email")

    def _signup_open(self):
        self.destroy()
        SignupFrame(r)


class SignupFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        master.geometry("400x250")
        self.label_name = Label(self, text="Name")
        self.label_email = Label(self, text="Email")
        self.label_password = Label(self, text="Password")

        self.entry_name = Entry(self)
        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_name.grid(row=0, sticky=E,pady=(70,0))
        self.label_email.grid(row=1, sticky=E,pady=(10,0))
        self.label_password.grid(row=2, sticky=E,pady=(10,0))
        self.entry_name.grid(row=0, column=1,pady=(70,0))
        self.entry_email.grid(row=1, column=1,pady=(10,0))
        self.entry_password.grid(row=2, column=1,pady=(10,0))

        self.signbtn = Button(self, text="Signup", command=self._signup_btn_clicked)
        self.signbtn.grid(columnspan=2,pady=(30,0))
        self.loginbtn = Button(self, text="Login", command=self._login_open)
        self.loginbtn.grid(row=3,column=2,pady=(30,0))

        self.pack()

    def _signup_btn_clicked(self):
        # print("Clicked")
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # print(email, password)

        url = "http://localhost:3001/users"
        # dic = '{"name":"'+name+'","email":"'+email+'", "password":"'+password+'"}'
        dic = '{"name":"Avinish Kumar", "email":"avnish31may@gmail.com", "password":"test1234"}'

        data = json.loads(dic)
        # print(data)
        res = requests.post(url = url , json = data) 
        
        resJSON = json.loads(res.text) 
        # print(resJSON)
        if resJSON['errmsg'] :
            tm.showerror("Login error", "Incorrect email")
        else:
            saveToken(resJSON['token'])
            self.destroy()
            dash = dashboard()
        # if email == "john" and password == "password":
        #     tm.showinfo("Login info", "Welcome John")
        # else:
        #     tm.showerror("Login error", "Incorrect email")

    def _login_open(self):
        
        self.destroy()
        lf = LoginFrame(r)

def saveToken(str):
	#TODO: enter relative path of file
	file = open("token.txt", "w+")
	file.write(str)
	file.close()

class log():
    def __init__(self):
        sf = SignupFrame(r)
        r.mainloop()

with open('token.txt', 'r') as file:
    logInToken = file.read().replace('\n', '')

if len(logInToken):
	print("Hello")
	dash = dashboard()
else:
	print("NO")
	log()