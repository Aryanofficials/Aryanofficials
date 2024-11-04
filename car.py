import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
class car():
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        title = tk.Label(self.root, text="Car Rental Management",fg="white",bd=4,relief="solid", bg=self.clr(250,10,20), font=("Arial",50,"bold"))
        title.pack(side="top", fill="x")
        # option Frame
        optFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(50,220,20))
        optFrame.place(width=self.width/3, height=self.height-180, x=50,y=100)
        addBtn = tk.Button(optFrame,command=self.addFun, text="Add Car",bg="light gray", width=20, font=("Arial",20,"bold"),bd=2, relief="raised")
        addBtn.grid(row=0,column=0, padx=30, pady=40)
        resBtn = tk.Button(optFrame,command=self.resFun, text="Reserve Car",bg="light gray", width=20, font=("Arial",20,"bold"),bd=2, relief="raised")
        resBtn.grid(row=1, column=0, padx=30, pady=40)
        retBtn = tk.Button(optFrame,command=self.retFun, text="Return Car",bg="light gray", width=20, font=("Arial",20,"bold"),bd=2, relief="raised")
        retBtn.grid(row=2, column=0, padx=30, pady=40)
        clBtn = tk.Button(optFrame,command=self.closeFun, text="Close System",bg="light gray", width=20, font=("Arial",20,"bold"),bd=2, relief="raised")
        clBtn.grid(row=3, column=0, padx=30, pady=40)
        # detail Frame
        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", background=self.clr(50,20,250))
        self.detFrame.place(width=self.width/2+50, height=self.height-180, x=self.width/3+100, y=100)
        lbl = tk.Label(self.detFrame, text="Available Cars", bg="light green", bd=3, relief="ridge",font=("Arial",30,"bold"))
        lbl.pack(side="top",fill="x")
        self.tabFun()
        self.showFun()
    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken")
        tabFrame.place(width=self.width/2+10, height=self.height-280, x=17,y=70)
        x_scrol= tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")
        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")
        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set, columns=("reg","comp","rent","avail"))
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        self.table.heading("reg", text="Registration_No")
        self.table.heading("comp", text="Company")
        self.table.heading("rent", text="Rent")
        self.table.heading("avail", text="Availabilty")
        self.table["show"] = "headings"
        self.table.column("reg", width=120)
        self.table.column("comp", width=150)
        self.table.column("rent", width=120)
        self.table.column("avail", width=100)
        self.table.pack(fill="both",expand=1)
    def closeFun(self):
        self.root.destroy()
    def addFun(self):
        self.insFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150,150,150))
        self.insFrame.place(width=self.width/3, height=self.height-180, x=self.width/3+60, y=100)
        regLbl = tk.Label(self.insFrame, text="Reg_NO:", bg=self.clr(150,150,150), font=("Arial",15,"bold"))
        regLbl.grid(row=0, column=0, padx=20, pady=30)
        self.regIn = tk.Entry(self.insFrame, bd=2, width=20, font=("Arial",15))
        self.regIn.grid(row=0,column=1, padx=10,pady=30)
        compLbl = tk.Label(self.insFrame, text="Company:", bg=self.clr(150,150,150), font=("Arial",15,"bold"))
        compLbl.grid(row=1, column=0, padx=20, pady=30)
        self.compIn = tk.Entry(self.insFrame, bd=2, width=20, font=("Arial",15))
        self.compIn.grid(row=1,column=1, padx=10, pady=30)
        rentLbl =tk.Label(self.insFrame, text="Rent:", bg=self.clr(150,150,150), font=("Arial",15,"bold"))
        rentLbl.grid(row=2, column=0, padx=20, pady=30)
        self.rentIn = tk.Entry(self.insFrame, bd=2, width=20, font=("Arial",15))
        self.rentIn.grid(row=2, column=1, padx=10, pady=30)
        availLbl = tk.Label(self.insFrame, text="Availablity:", bg=self.clr(150,150,150), font=("Arial",15,"bold"))
        availLbl.grid(row=3, column=0, padx=20, pady=30)
        self.availIn= tk.Entry(self.insFrame, bd=2, width=20, font=("Arial",15))
        self.availIn.grid(row=3, column=1, padx=10, pady=30)
        okBtn = tk.Button(self.insFrame,command=self.insertFun, text="Add Car", width=20, font=("Arial",20,"bold"),bd=2, relief="raised")
        okBtn.grid(row=4, column=0, padx=30, pady=40,columnspan=2)
    def insertFun(self):
        reg = self.regIn.get()
        comp = self.compIn.get()
        rent =self.rentIn.get()
        avail = self.availIn.get()
        if reg and comp and rent and avail:
            reg_int = int(reg)
            rent_int = int(rent)
            try:
                self.dbFun()
                self.cur.execute("insert into cars(regNo,company,rent,avail) values(%s,%s,%s,%s)",(reg_int,comp,rent_int,avail))
                self.con.commit()
                tk.messagebox.showinfo("Success","Car is added Successfuly!")
                self.cur.execute("select * from cars where regNo=%s",reg_int)
                row = self.cur.fetchone()
        
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END, values=row)
                self.insFrame.destroy()
                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")
        else:
            tk.messagebox.showerror("Error","Fill All Input Fields!")
    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="Harshit@123", database="car")
        self.cur = self.con.cursor()
    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def showFun(self):
        try:
            self.dbFun()
            self.cur.execute("select * from cars where avail='Yes'")
            data = self.cur.fetchall()
            self.tabFun()
            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END,values=i)
            self.con.close()
        except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")
    
    def resFun(self):
        self.resFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(190,190,190))
        self.resFrame.place(width=self.width/3, height=self.height-400, x=self.width/3+60, y=100)
        lbl1 = tk.Label(self.resFrame, text="Reg_No:", bg=self.clr(190,190,190), font=("Arial",15,"bold"))
        lbl1.grid(row=0,column=0, padx=20, pady=30)
        self.val1 = tk.Entry(self.resFrame, width=20, bd=2, font=("Arial",15))
        self.val1.grid(row=0, column=1, padx=10, pady=30)
        lbl2 = tk.Label(self.resFrame, text="Total_Days:", bg=self.clr(190,190,190), font=("Arial",15,"bold"))
        lbl2.grid(row=1,column=0, padx=20, pady=30)
        self.val2 = tk.Entry(self.resFrame, width=20, bd=2, font=("Arial",15))
        self.val2.grid(row=1, column=1,padx=10, pady=30)
        resBtn = tk.Button(self.resFrame,command=self.resCar, text="Reserve", width=20,bd=2, relief="raised",font=("Arial",20,"bold"))
        resBtn.grid(row=2, column=0, padx=30, pady=40, columnspan=2)
    def resCar(self):
        reg = int(self.val1.get())
        days = int(self.val2.get())
        try:
            self.dbFun()
            self.cur.execute("select rent, avail,company from cars where regNo=%s",reg)
            row = self.cur.fetchone()
            if row:
                if row[1] == "Yes":
                    upd= "No"
                    bill = row[0] * days
                    self.cur.execute("update cars set avail=%s where regNo=%s",(upd,reg))
                    self.con.commit()
                    line = f"Total Rent: {bill} for {days} days for Car: {row[2]}"
                    tk.messagebox.showinfo("Success",line)
                    
                    self.resFrame.destroy()
                    self.showFun()
                else:
                    tk.messagebox.showerror("Error",f"Car with regNo:{reg} is already Reserved!")
            else:
                tk.messagebox.showerror("Error",f"No car exists with regNo:{reg}")
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}")
        
    def retFun(self):
        self.retFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(190,190,190))
        self.retFrame.place(width=self.width/3, height=self.height-460, x=self.width/3+60, y=100)
        lbl1 = tk.Label(self.retFrame, text="Reg_No:", bg=self.clr(190,190,190), font=("Arial",15,"bold"))
        lbl1.grid(row=0,column=0, padx=20, pady=30)
        self.val1 = tk.Entry(self.retFrame, width=20, bd=2, font=("Arial",15))
        self.val1.grid(row=0, column=1, padx=10, pady=30)
        retBtn = tk.Button(self.retFrame,command=self.retCar, text="Return", width=20,bd=2, relief="raised",font=("Arial",20,"bold"))
        retBtn.grid(row=2, column=0, padx=30, pady=40, columnspan=2)
    def retCar(self):
        reg = int(self.val1.get())
        try:
            self.dbFun()
            upd = "Yes"
            self.cur.execute("update cars set avail=%s where regNo=%s",(upd,reg))
            self.con.commit()
            self.showFun()
            tk.messagebox.showinfo("Success",f"Car with RegNo:{reg} is Returned!")
            
            self.retFrame.destroy()
            
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error: {e}")
        
root = tk.Tk()
obj = car(root)
root.mainloop()