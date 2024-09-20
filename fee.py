import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import messagebox

class fee():
    def __init__(self,root):
        self.root = root
        self.root.title("Fee Management")
        self.width = self.root.winfo_screenwidth()
        self.height =self.root.winfo_screenheight()

        self.root.geometry(f"{self.width}x{self.height}+0+0")
        label = tk.Label(self.root,text="Fee Management System",fg="light green",bg="gray",bd=4,relief="groove", font=("Arial",50,"bold"))
        label.pack(side="top",fill="x")

        self.mainFrame = tk.Frame(self.root,bg="sky blue", bd=4,relief="ridge")
        self.mainFrame.place(x=80, y=100,width=self.width/3, height=self.height-180)

        rnlbl = tk.Label(self.mainFrame, text="RollNo:", bg="sky blue", font=("Arial",15))
        rnlbl.grid(row=0, column=0, padx=10, pady=30)
        self.rnIn = tk.Entry(self.mainFrame,font=("Arial",20),width=18,bd=2)
        self.rnIn.grid(row=0,column=1, padx=10,pady=30)

        feelbl = tk.Label(self.mainFrame, text="Enter Fee:", bg="sky blue", font=("Arial",15))
        feelbl.grid(row=1,column=0,padx=10,pady=30)
        self.feeIn = tk.Entry(self.mainFrame,font=("Arial",20),width=18,bd=2)
        self.feeIn.grid(row=1,column=1,padx=10,pady=30)

        submitBtn = tk.Button(self.mainFrame,text="Submit",command=self.submit, bd=2, bg="light gray", font=("Arial",15),width=20)
        submitBtn.grid(row=2,column=0,padx=40, pady=100,columnspan=2)

        detailBtn = tk.Button(self.mainFrame,text="Fee Detail",command=self.showAll,bd=2,bg="light gray",font=("Arial",15),width=20)
        detailBtn.grid(row=3,column=0,padx=40,pady=20,columnspan=2)

        # fee detail frame

        self.feeFrame = tk.Frame(self.root, bg="light green", bd=4, relief="ridge")
        self.feeFrame.place(width=self.width/2, height= self.height-180, x=self.width/3+150,y=100)
        feelabel= tk.Label(self.feeFrame,text="Fee Details", bg="light green", font=("Arial",30,"bold"))
        feelabel.pack(side="top")
        self.feeInfo()

    def feeInfo(self):
        tabFrame = tk.Frame(self.feeFrame,bg="light gray",bd=3,relief="sunken")
        tabFrame.place(width=self.width/2-40,height=self.height-240,x=20,y=50)

        x_scrl = tk.Scrollbar(tabFrame,orient="horizontal")
        x_scrl.pack(side="bottom",fill="x")

        y_scrl = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrl.pack(side="right",fill="y")

        self.table = ttk.Treeview(tabFrame,columns=("rollno","name","total","paid","remaining"), xscrollcommand=x_scrl.set, yscrollcommand=y_scrl.set)

        x_scrl.config(command=self.table.xview)
        y_scrl.config(command=self.table.yview)

        self.table.heading("rollno", text="Roll_No")
        self.table.heading("name", text="Name")
        self.table.heading("total", text="Total_Fee")
        self.table.heading("paid", text="Paid_Fee")
        self.table.heading("remaining", text="Pending_Fee")
        self.table["show"] = "headings"

        self.table.column("rollno", width=150)
        self.table.column("name", width=150)
        self.table.column("total", width=150)
        self.table.column("paid", width=150)
        self.table.column("remaining", width=150)

        self.table.pack(fill="both", expand=1)

    def submit(self):
        rn = int(self.rnIn.get())  
        getFee = int(self.feeIn.get())
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
            cur = con.cursor()
            query = f"select name,paid_fee,remaining from fee where rollNo={rn}"
            cur.execute(query)
            row = cur.fetchone()

            pend = row[2] - getFee
            paid = row[1] + getFee

            query2= f"update fee set paid_fee={paid}, remaining={pend} where rollNo={rn}"
            cur.execute(query2)
            con.commit()
            
            tk.messagebox.showinfo("Success",f"Fee submitted for {row[0]}")
            query3= f"select * from fee where rollNo={rn}"
            cur.execute(query3)
            data = cur.fetchone()
            self.feeInfo()
            self.table.delete(*self.table.get_children())
            
            self.table.insert('',tk.END,values=data)
            cur.close()
            con.close()

        except Exception as e:
            tk.messagebox.showerror("Error",f"Database Error:{e}")

    def showAll(self):
        try:
            con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
            cur = con.cursor()
            cur.execute("select * from fee")
            data = cur.fetchall()

            self.feeInfo()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END,values=i)

        except Exception as ex:
            tk.messagebox.showerror("Error",f"Error: {ex}")


root =tk.Tk()
obj = fee(root)
root.mainloop()