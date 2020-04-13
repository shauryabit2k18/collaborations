from tkinter import *
import tkinter.messagebox as tm
import requests
import json

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
        self.logbtn.grid(columnspan=2,pady=(30,0))

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
        
        resJSON = json.loads(res.text) 
        if resJSON == {}:
            tm.showerror("Login error", "Incorrect email")
        else:
            print(resJSON['token']) 
        # if email == "john" and password == "password":
        #     tm.showinfo("Login info", "Welcome John")
        # else:
        #     tm.showerror("Login error", "Incorrect email")


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
        print(data)
        res = requests.post(url = url , json = data) 
        
        resJSON = json.loads(res.text) 
        if resJSON == {}:
            tm.showerror("Signup error", "Incorrect data")
        else:
            print(resJSON['token'])
        # if email == "john" and password == "password":
        #     tm.showinfo("Login info", "Welcome John")
        # else:
        #     tm.showerror("Login error", "Incorrect email")

    def _login_open(self):
        
        self.destroy
        lf = LoginFrame(root)
    

root = Tk()
sf = SignupFrame(root)
root.mainloop()
# Sorry for not going over every single line what is happening there. I leave it to you to figure out. Its good exercise. 