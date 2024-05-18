from tkinter import *
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('bank.db', isolation_level=None)

def logIn():

    def login_action():
        user = nameEntry.get()
        password = passEntry.get()

        res = conn.execute(
            f'''SELECT username, password FROM users WHERE username = "{user}" AND password = "{password}";''')
        results = res.fetchall()

        if (len(results) != 0):
            frame.destroy()
            mainFrame()


        else:
            messagebox.showerror(title="Log In Error", message="The Username or Password is incorect")

        passEntry.delete(0, END)

    frame = Tk()
    frame.geometry("300x150")
    frame.title("Log In")

    name_label = Label(frame, text="Username:")
    name_label.place(x=10, y=20)
    pass_label = Label(frame, text="Password:")
    pass_label.place(x=10, y=60)

    nameEntry = Entry(frame, font=("Arial", 10))
    nameEntry.place(x=72, y=20)
    passEntry = Entry(frame, font=("Arial", 10))
    passEntry.place(x=70, y=60)

    enterButton = Button(frame, text="Log In", command=login_action)
    enterButton.place(x=130, y=100)

    frame.mainloop()

def addUser():

    def add():
        user = nameEntry.get()
        password = passEntry.get()
        try:
            conn.execute(f'''INSERT INTO users (username, password) VALUES('{user}','{password}');''')
            messagebox.showinfo(title="Add Successful", message="User Added")
            frame.destroy()
        except sqlite3.Error as err:
            messagebox.showerror(title="Add Error", message="The Username and Password already exists")

    frame = Tk()
    frame.geometry("300x150")
    frame.title("Add New User")

    name_label = Label(frame, text="Username:")
    name_label.place(x=10, y=20)
    pass_label = Label(frame, text="Password:")
    pass_label.place(x=10, y=60)

    nameEntry = Entry(frame, font=("Arial", 10))
    nameEntry.place(x=72, y=20)
    passEntry = Entry(frame, font=("Arial", 10))
    passEntry.place(x=70, y=60)

    enterButton = Button(frame, text="Add User", command=add)
    enterButton.place(x=130, y=100)

    frame.mainloop()

constraint = ""
def mainFrame():
    global constraint

    def search():
        global constraint
        constraint = searchEntry.get()
        show()

    items = []
    def show():
        result = conn.execute('''SELECT * FROM accounts;''').fetchall()
        for item in items:
            item.destroy()
        items.clear()
        if constraint != "":
            temp = []
            for i in range(0, len(result)):
                if str(constraint) in str(result[i][0]):
                    temp.append(result[i])
            result = temp


        for i in range(1, len(result) + 1):
            num, name, id, balance, active = result[i-1]

            noLabel = Label(frame, text=str(i))
            noLabel.place(x=20, y=170 + (i-1)*40)
            items.append(noLabel)
            numberLabel = Label(frame, text=str(num))
            numberLabel.place(x=100, y=170 + (i-1)*40)
            items.append(numberLabel)
            nameLabel = Label(frame, text=name)
            nameLabel.place(x=280, y=170 + (i-1)*40)
            items.append(nameLabel)
            idLabel = Label(frame, text=str(id))
            idLabel.place(x=450, y=170 + (i-1)*40)
            items.append(idLabel)
            balanceLabel = Label(frame, text=str(balance))
            balanceLabel.place(x=620, y=170 + (i-1)*40)
            items.append(balanceLabel)
            statusLabel = Label(frame, text="Active" if active == 1 else "Not-Active")
            statusLabel.place(x=730, y=170 + (i-1)*40)
            items.append(statusLabel)

    def delete():
        num = numEntry.get()
        result = conn.execute(f'''SELECT * FROM accounts WHERE number = {num};''').fetchall()
        if len(result) == 0:
            messagebox.showerror(title="Delete Error", message="The Username is invalid")
        else:
            conn.execute(f'''DELETE FROM accounts WHERE number = {num};''')
            messagebox.showinfo(title="Delete Account", message="The Account was deleted successfuly")
        numEntry.delete(0, END)
        show()

    def exchangeDep():
        num = numEntry.get()
        result = conn.execute(f'''SELECT * FROM accounts WHERE number = {num};''').fetchall()
        numEntry.delete(0, END)
        if len(result) == 0:
            messagebox.showerror(title="Delete Error", message="The Username is invalid")
        else:
            exchange_frame(num, True)

        show()

    def exchangeWth():
        num = numEntry.get()
        result = conn.execute(f'''SELECT * FROM accounts WHERE number = {num};''').fetchall()
        numEntry.delete(0, END)
        if len(result) == 0:
            messagebox.showerror(title="Delete Error", message="The Username is invalid")
        else:
            exchange_frame(num, False)

        show()

    def edit():
        num = numEntry.get()
        result = conn.execute(f'''SELECT * FROM accounts WHERE number = {num};''').fetchall()
        numEntry.delete(0, END)
        if len(result) == 0:
            messagebox.showerror(title="Delete Error", message="The Username is invalid")
        else:
            edit_frame(num)

        show()

    def addAcc():
        addAccountFrame()
        show()



    frame = Tk()
    frame.geometry("1000x700+200+80")
    frame.title("Account Manager")

    searchEntry = Entry(frame, font=("Arial", 15), width=15)
    searchEntry.place(x = 20, y = 20)
    searchButton = Button(frame, text="Search", font=("Arial", 10), command=search)
    searchButton.place(x=200, y=18)

    addUserButton = Button(frame, text="Add New User", font=("Arial", 10), padx=50, command=addUser)
    addUserButton.place(x=800, y=18)
    addAccButton = Button(frame, text="Add New Account", font=("Arial", 10), padx=40, command=addAcc)
    addAccButton.place(x=800, y=50)

    refreshButton = Button(frame, text="Refresh", font=("Arial", 10), command=show)
    refreshButton.place(x = 200, y = 50)

    numEntry = Entry(frame, font=("Arial", 12), width=15)
    numEntry.place(x = 450, y = 15)
    deleteButton = Button(frame, text="Delete", font=("Arial", 10), command=delete)
    deleteButton.place(x = 400, y = 40)
    editButton = Button(frame, text="Edit", font=("Arial", 10), command=edit)
    editButton.place(x=460, y=40)
    depoButton = Button(frame, text="Deposit", font=("Arial", 10), command=exchangeDep)
    depoButton.place(x=505, y=40)
    withdrawButton = Button(frame, text="Withdraw", font=("Arial", 10), command=exchangeWth)
    withdrawButton.place(x=570, y=40)

    noLabel = Label(frame, text="No.", fg="red", bg="#c0c1c4")
    noLabel.place(x = 20, y = 140)
    numberLabel = Label(frame, text="Account Number", fg="red", bg="#c0c1c4")
    numberLabel.place(x=100, y=140)
    nameLabel = Label(frame, text="Account Owner", fg="red", bg="#c0c1c4")
    nameLabel.place(x=280, y=140)
    idLabel = Label(frame, text="Owner National Id", fg="red", bg="#c0c1c4")
    idLabel.place(x=450, y=140)
    balanceLabel = Label(frame, text="Balance", fg="red", bg="#c0c1c4")
    balanceLabel.place(x=620, y=140)
    statusLabel = Label(frame, text="Status", fg="red", bg="#c0c1c4")
    statusLabel.place(x=730, y=140)

    show()

    frame.mainloop()

def exchange_frame(id, depo = True):
    frame = Tk()
    frame.geometry("250x150")
    frame.title("Exchange Money")

    numEntry = Entry(frame, font=("Arial", 12), width=15)
    numEntry.place(x=50, y=45)

    result = conn.execute(f'''SELECT * FROM accounts WHERE number = {id};''').fetchall()
    money = result[0][3]
    def dep():
        temp = money + float(numEntry.get())
        conn.execute(f'''UPDATE accounts SET balance = {temp} WHERE number = {id}''')
        frame.destroy()
    def wth():
        temp = money - float(numEntry.get())
        if temp < 0:
            messagebox.showerror(title="Exchange error", message="the Balance is not enough")
        else:
            conn.execute(f'''UPDATE accounts SET balance = {temp} WHERE number = {id}''')
            frame.destroy()

    if depo:
        button = Button(frame, text="Deposit", command=dep)
    else:
        button = Button(frame, text="WithDraw", command=wth)
    button.place(x = 100, y = 100)
    frame.mainloop()

def edit_frame(nid):
    frame = Tk()
    frame.geometry("750x150")
    frame.title("Edit Account")

    def editAccount():
        new_name = nameEntry.get()
        new_id = idEntry.get()
        new_balance = balanceEntry.get()
        new_status = 1 if statusCheck.get() == "y" else 0
        conn.execute(f'''UPDATE accounts SET holder = "{new_name}", holder_id = {new_id}, balance = {new_balance}, active = {new_status} WHERE number = {nid}''')
        frame.destroy()

    result = conn.execute(f'''SELECT * FROM accounts WHERE number = {nid};''').fetchall()
    num = result[0][0]
    name = result[0][1]
    id = result[0][2]
    balance = result[0][3]
    status = bool(result[0][4])

    numberLabel = Label(frame, text="Account Number", fg="red", bg="#c0c1c4")
    numberLabel.place(x=20, y=20)
    numberEntry = Label(frame, text=str(num), font=("Arial", 12))
    numberEntry.place(x = 50, y = 60)

    nameLabel = Label(frame, text="Account Owner", fg="red", bg="#c0c1c4")
    nameLabel.place(x=180, y=20)
    nameEntry = Entry(frame, font=("Arial", 12), width=12)
    nameEntry.insert(0, name)
    nameEntry.place(x=180, y=60)

    idLabel = Label(frame, text="Owner National Id", fg="red", bg="#c0c1c4")
    idLabel.place(x=340, y=20)
    idEntry = Entry(frame, font=("Arial", 12), width=12)
    idEntry.insert(0, id)
    idEntry.place(x=340, y=60)

    balanceLabel = Label(frame, text="Balance", fg="red", bg="#c0c1c4")
    balanceLabel.place(x=500, y=20)
    balanceEntry = Entry(frame, font=("Arial", 14), width=13)
    balanceEntry.insert(0, balance)
    balanceEntry.place(x=500, y=60)

    statusLabel = Label(frame, text="Active?(y/n)", fg="red", bg="#c0c1c4")
    statusLabel.place(x=670, y=20)
    statusCheck = Entry(frame, font=("Arial", 14), width=5)
    statusCheck.insert(0, "y")
    statusCheck.place(x = 675, y = 60)

    editButton = Button(frame, text="Edit", command=editAccount)
    editButton.place(x = 350, y = 100)

    frame.mainloop()

def addAccountFrame():
    frame = Tk()
    frame.geometry("750x150")
    frame.title("Add Account")

    def addAccount():
        new_num = numberEntry.get()
        new_name = nameEntry.get()
        new_id = idEntry.get()
        new_balance = balanceEntry.get()
        new_status = 1 if statusCheck.get() == "y" else 0
        conn.execute(f'''INSERT INTO accounts VALUES ({new_num},"{new_name}",{new_id},{new_balance},{new_status});''')
        frame.destroy()

    numberLabel = Label(frame, text="Account Number", fg="red", bg="#c0c1c4")
    numberLabel.place(x=20, y=20)
    numberEntry = Entry(frame, font=("Arial", 12), width=12)
    numberEntry.place(x=50, y=60)

    nameLabel = Label(frame, text="Account Owner", fg="red", bg="#c0c1c4")
    nameLabel.place(x=180, y=20)
    nameEntry = Entry(frame, font=("Arial", 12), width=12)
    nameEntry.place(x=180, y=60)

    idLabel = Label(frame, text="Owner National Id", fg="red", bg="#c0c1c4")
    idLabel.place(x=340, y=20)
    idEntry = Entry(frame, font=("Arial", 12), width=12)
    idEntry.place(x=340, y=60)

    balanceLabel = Label(frame, text="Balance", fg="red", bg="#c0c1c4")
    balanceLabel.place(x=500, y=20)
    balanceEntry = Entry(frame, font=("Arial", 14), width=13)
    balanceEntry.place(x=500, y=60)

    statusLabel = Label(frame, text="Active?(y/n)", fg="red", bg="#c0c1c4")
    statusLabel.place(x=670, y=20)
    statusCheck = Entry(frame, font=("Arial", 14), width=5)
    statusCheck.place(x=675, y=60)

    addButton = Button(frame, text="Add Account", command=addAccount)
    addButton.place(x=350, y=100)

    frame.mainloop()

logIn()