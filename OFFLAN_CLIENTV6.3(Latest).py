import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pymysql
import socket
import time
import re

class soc_Command:
    def __init__(self):
        self.host = '127.0.0.1'
        self.IP=self.host
        self.port = 1234
        self.addr=None
    def send(self,message):
        s = socket.socket()
        s.bind((self.IP, self.port))
        s.listen(1)
        print("Waiting for client...")
        c, addr = s.accept()
        #c.settimeout(20.0)
        print ('Got connection from', addr)
        self.addr=addr
        c.send( bytes(message, 'utf-8'))
        s.close()
        time.sleep(5)
        if ".py" in message:
            time.sleep(10)
            self.recv_file()
        else:
            c=Cloud()    

    def recv(self):
        s1 = socket.socket()
        s1.connect((self.host, self.port))
        data = s1.recv(1024)
        opt = data.decode('utf-8')
        s1.close()
        return opt
    
    def recv_file(self):
        s = socket.socket()
        s.connect((self.host, self.port))
        data = s.recv(1024)
        file = data.decode('utf-8')
        with open(file, 'wb') as f:
            print('file opened')
            while True:
                print('receiving data...')
                data = s.recv(1024)
                print('data=%s', (data))
                print(not data)
                if not data:
                    break
                # write data to a file
                f.write(data)
        f.close()
        tk.messagebox.showinfo("Received", "Requested File Is Received")
        print('Received')
        s.close()

class OFFLAN:
    """
    Init function will setup all basic requirements for the main interface. 
    """
    def __init__(self):
        #Defining the database...
        #self.IP="192.168.10.74"
        self.IP="localhost"
        self.db = pymysql.connect(host=self.IP, port=3306, user="root", passwd="root", db="OFFLAN")
        self.cur = self.db.cursor()
        #Defining the main interface of the program.
        self.root = tk.Tk()
        self.root.geometry('700x500')
        self.root.title("OFFLAN CLIENT")
        self.root.resizable(0, 0)
        self.photo = tk.PhotoImage(file="Tri.png")
        self.background = tk.Label(self.root, image=self.photo)
        self.background.image = self.photo
        self.background.pack()
        #Calling the function main for further action.
        self.main()

    """
    Buffer function will removes all widgets of self.root(Main Interface) except background label(Beach Pic).
    """
    def buffer(self, func):
        #Taking all widgets names and storing it in widget_lst.
        widget_lst = self.root.winfo_children()
        for i in range(1, len(widget_lst)):
            widget_lst[i].destroy()

        #func() will execute the given function from formal parameter.    
        a = func()
                  
        
    def log_In(self):
        def check_Log(name,ps):
            corflag = False
            self.cur.execute("SELECT * from Profile")
            prof_data = self.cur.fetchall()

            for prof in prof_data:
                if prof[1] == name and prof[2] == ps:
                    messagebox.showinfo("Finish", "Logged Successfully!!")
                    corflag = True
                    name = re.sub(" ","_",nm_ent.get())
                    self.db.close()
                    self.root.destroy()
                    pr = PROFILE(name)
                    
                else:
                    continue
            if corflag is not True:
                messagebox.showinfo("Interrupt", "Name or Password may be incorrect!!")
                
        def entry_Click(etnm, status):
            if status == "nm":
                if self.nm_l is True:
                    etnm.config(fg="black")
                    etnm.delete(0, tk.END)
                    self.nm_l = False

            elif status == "ps":
                if self.ps_l is True:
                    etnm.config(fg="black",show="*")
                    etnm.delete(0, tk.END)
                    self.ps_l = False
                
        self.nm_l = True
        self.ps_l = True        
        nm_ent = tk.Entry(self.root, font="Helvetica 15", width=20, fg="grey")
        nm_ent.insert(0, 'Name')
        nm_ent.bind('<FocusIn>',lambda eff: entry_Click(nm_ent, "nm"))
        nm_ent.place(x=220, y=175)

        ps_ent = tk.Entry(self.root, font="Helvetica 15", width=20, fg="grey")
        ps_ent.insert(0, 'Password')
        ps_ent.bind('<FocusIn>',lambda eff: entry_Click(ps_ent, "ps"))
        ps_ent.place(x=220, y=275)

        sub_button=tk.Button(self.root, text="Log In", font=("Arial", 14, "bold"), bg="orange", fg="white", command=lambda: check_Log(nm_ent.get
                                                                                                                                      (), ps_ent.get()))
        sub_button.place(x=285, y=330)

        back_button = tk.Button(self.root, text="Back", font=("Arial", 11, "bold"), width=12, bg="orange", fg="white", command=lambda: self.buffer(self.main))
        back_button.place(x=540, y=90)
        

    def sign_Up(self):
        def check_Up():
            if new_ps_confirm_ent.get() == new_ps_ent.get():
                if new_nm_ent.get() != "Your Name":
                    messagebox.showinfo("Finish","Registered Successfully!!")
                    rowcount = self.cur.execute("select * from Profile")
                    self.cur.execute("INSERT into Profile values(%s,%s,%s)", (rowcount+1, new_nm_ent.get(), new_ps_ent.get()))
                    self.db.commit()
                    self.cur.execute("CREATE table "+re.sub(" ", "_", new_nm_ent.get())+" (fid int primary key,fname varchar(40))")
                    self.buffer(self.main)
                else:
                    messagebox.showinfo("Error","Name is not being written!!")
            else:
                messagebox.showinfo("Error","Passwords are not matching!!")
            
        def entry_Click(etnm, status):
            if status == "nm":
                if self.nm_s is True:
                    etnm.config(fg="black")
                    etnm.delete(0, tk.END)
                    self.nm_s = False

            elif status == "ps":
                if self.ps_s is True:
                    etnm.config(fg="black",show="*")
                    etnm.delete(0, tk.END)
                    self.ps_s = False

            elif status == "cps":
                if self.cps_s is True:
                    etnm.config(fg="black",show="*")
                    etnm.delete(0, tk.END)
                    self.cps_s = False

        self.nm_s = True
        self.ps_s = True
        self.cps_s = True        
        new_nm_ent = tk.Entry(self.root, font="Helvetica 15", width=20, fg="grey")
        new_nm_ent.insert(0, 'Your Full Name')
        new_nm_ent.bind('<FocusIn>',lambda eff: entry_Click(new_nm_ent, "nm"))
        new_nm_ent.place(x=220, y=175)

        new_ps_ent = tk.Entry(self.root, font="Helvetica 15", width=20, fg="grey")
        new_ps_ent.insert(0, 'Your Password')
        new_ps_ent.bind('<FocusIn>',lambda eff: entry_Click(new_ps_ent, "ps"))
        new_ps_ent.place(x=220, y=275)

        new_ps_confirm_ent = tk.Entry(self.root, font="Helvetica 15", width=20, fg="grey")
        new_ps_confirm_ent.insert(0, 'Confirm Password')
        new_ps_confirm_ent.bind('<FocusIn>',lambda eff: entry_Click(new_ps_confirm_ent, "cps"))
        new_ps_confirm_ent.place(x=220, y=375)

        sign_button=tk.Button(self.root, text="Sign Up", font=("Arial", 14, "bold"), bg="orange", fg="white", command=check_Up)
        sign_button.place(x=285, y=430)

        back_button = tk.Button(self.root, text="Back", font=("Arial", 11, "bold"), width=12, bg="orange", fg="white", command=lambda: self.buffer(self.main))
        back_button.place(x=540, y=90)
        
    def main(self):

        """ Setting The Main GUI """

        log_in_but = tk.Button(self.root, text="LOGIN ACCOUNT", bg="Orange", font=("Arial", 15, "bold"), fg="White", width=25, command=lambda: self.buffer(self.log_In))
        log_in_but.place(x=200, y=175)

        sign_up_but = tk.Button(self.root, text="CREATE NEW ACCOUNT!", bg="Orange", font=("Arial", 15, "bold"), fg="White", width=25, command=lambda: self.buffer(self.sign_Up))
        sign_up_but.place(x=200, y=275)

        self.root.mainloop()

class Cloud:
    def __init__(self):
        self.sock=soc_Command()
        self.root=tk.Toplevel()
        self.root.configure(bg="orange")
        self.root.resizable(0, 0)
        self.root.geometry("600x600")
        self.Display()
        
    def Display(self,file=None):
        def back():
            self.root.destroy()
            self.sock.send("Back")
        def buffer(file):
            self.root.destroy()
            self.sock.send(file)
            
            
        x_place=50
        y_place=90 
        directory=self.sock.recv().split(',')
        print(directory)
        children = self.root.winfo_children()
        for child in children:
            child.destroy()

        back_btn=tk.Button(self.root,text="Back",font=("Helvetica", 12, "bold"), bg='orange', fg="white",command=back)
        back_btn.place(x=500,y=40)
                
        list_Of_btns=[]
        for i in range(0,len(directory)):
            list_Of_btns.append(tk.Button(self.root,text=directory[i],font=("Helvetica", 12, "bold"), bg='orange', fg="white",command=lambda i=i:buffer(directory[i])))
            list_Of_btns[i].place(x=x_place, y=y_place)
            x_place+=250
            if x_place>300:
                y_place+=50
                x_place=50

class PROFILE:
    
    def __init__(self, name):
        self.current_content=None
        self.name = name
        #self.server_IP="192.168.10.74"
        self.server_IP="localhost"
        self.db = pymysql.connect(host=self.server_IP, port=3306, user="root", passwd="root", db="OFFLAN")
        self.cur = self.db.cursor()
        self.profile = tk.Tk()
        self.profile.title(self.name)
        self.photo = tk.PhotoImage(file="main2.png")
        self.background = tk.Label(self.profile, image=self.photo)
        self.background.image = self.photo
        self.background.pack()
        self.main()
        
    def Restart(self):
            self.profile.update()
            
    def main(self):
        
        def Compose(to_name=""):
            def Send():
                to_send_members = (to_ent.get()).split(";")
                members = self.cur.execute("select pname from profile")
                prof_det = self.cur.fetchall()
                for name in to_send_members:
                    for i in range(0, members):
                        if name == prof_det[i][0]:
                            rowcount = self.cur.execute("select * from Messages")
                            self.cur.execute("insert into Messages values(%s,SYSDATE(),%s,%s,%s,%s,%s)", (rowcount+1,"Y", re.sub("_", " ", self.name), name, subject_ent.get(), content_ent.get("1.0",tk.END)))
                            self.db.commit()
                            break
                        else:
                            to_lbl = tk.Label(self.compose, font=("Helvetica", 8, "bold"), text="Some Name Does Not Exist!", bg=self.bg, fg=self.label_fg)
                            to_lbl.place(x=90, y=60)
                #self.db.close()
                self.Restart()

                self.compose.destroy()
                    
            self.bg='#ffa04d'
            self.label_fg='white'
            self.compose = tk.Toplevel()
            self.compose.geometry("550x600")
            self.compose.resizable(0, 0)
            self.compose.title("Compose")
            self.compose.configure(background=self.bg)

            to_lbl = tk.Label(self.compose, font=("Helvetica", 13, "bold"), text="To:", bg=self.bg, fg=self.label_fg)
            to_lbl.place(x=10, y=30)
            to_ent = tk.Entry(self.compose, font="Helvetica 13", width=48)
            to_ent.place(x=85, y=30)
            to_ent.insert(0,to_name)

            sub_lbl = tk.Label(self.compose, font=("Helvetica", 13, "bold"), text="Subject:", bg=self.bg, fg=self.label_fg)
            sub_lbl.place(x=10, y=130)
            subject_ent = tk.Entry(self.compose, font="Helvetica 13", width=48)
            subject_ent.place(x=85, y=130)

            cont_lbl = tk.Label(self.compose, font=("Helvetica", 13, "bold"), text="Text:", bg=self.bg, fg=self.label_fg)
            cont_lbl.place(x=10, y=230)
            content_ent = tk.Text(self.compose, font="Helvetica 13", width=48,height=15)
            content_ent.place(x=85, y=230)

            send_but = tk.Button(self.compose, text="Send!", font=("Helvetica", 14, "bold"), width=10, bg="orange", fg="white", command=Send)
            send_but.place(x=210, y=550)
            
        def Open():
            def delete():
                res = messagebox.askquestion("Delete","Are you sure you want to delete?\n(WARNING:It will also get deleted from receiver)",parent=self.open)
                if res == "yes":
                    self.cur.execute("UPDATE Messages SET userenabled=%s WHERE mid=%s ",("N",values[0]))
                    self.db.commit()
                    #self.db.close()
                    self.Restart()
                    send_ml()
                    self.open.destroy()
                else:
                    pass
                
            def buff():
                self.open.destroy()
                Compose(values[1])
            self.open = tk.Toplevel()
            self.open.geometry("600x640")
            self.open.configure(bg="orange")
            self.open.resizable(0, 0)
            self.mydict = tree.item(tree.focus())
            values = self.mydict.get("values")
            lbl = tk.Label(self.open, text="Name: ", font=("Arial", 12, "bold"), fg="white", bg="orange")
            lbl.place(x=10, y=10)

            lbl2 = tk.Label(self.open, text="Subject: ", font=("Arial", 12, "bold"), fg="white", bg="orange")
            lbl2.place(x=10, y=100)

            lbl3 = tk.Label(self.open, text="Text: ", font=("Arial", 12, "bold"), fg="white", bg="orange")
            lbl3.place(x=10, y=200)

            lbl4 = tk.Label(self.open, text=values[1], font=("Arial", 12,), bg="white",width=54)
            lbl4.place(x=100, y=10)

            lbl5 = tk.Label(self.open, text=values[2], font=("Arial", 12,), bg="white",width=54)
            lbl5.place(x=100, y=100)

            txt = tk.Text(self.open, font=("Arial", 12,), width=54,height=21)
            txt.place(x=100, y=200)
            
            self.cur.execute("SELECT received,subject,content from Messages WHERE mid=%s",values[0])
            res = self.cur.fetchone()
            txt.insert("1.0",str(res[2]))
            txt.config(state=tk.DISABLED)

            reply_but = tk.Button(self.open, text="Reply", font=("Arial", 12, "bold"), fg="white", bg="orange", command=lambda: buff())
            reply_but.place(x=300, y=600)

            delete_but = tk.Button(self.open, text="Delete", font=("Arial", 12, "bold"), fg="white", bg="orange", command=lambda: delete())
            
            if self.message_status == "received": 
                delete_but.place(x=500, y=600)
            else:
                delete_but.place(x=500, y=150)

        def friend_list():
            def poke_friend():
                to_poke_members = []
                for i in range(0,len(self.friend_list)):
                    if self.friend_tick_box_value[i].get() == 1:
                        to_poke_members.append(self.friend_list[i])
                        
                for name in to_poke_members:
                        #print(name)
                        rowcount = self.cur.execute("select * from Poke")
                        print(rowcount+1)
                        self.cur.execute("insert into Poke values(%s,%s,%s)", (rowcount+1,re.sub("_", " ", self.name), name))
                        self.db.commit()
                #self.db.close()
                self.Restart()
                self.friend.destroy()

            def select_all():
                if self.all_select is True:
                    for obj in self.friend_name_box:
                        obj.select()
                    self.all_select_but.config(text="Unselect All")
                    self.all_select = False
                else:
                    for obj in self.friend_name_box:
                        obj.deselect()
                    self.all_select_but.config(text="Select All")
                    self.all_select = True

            def setup_env():
                self.all_select = True
                self.all_select_but = tk.Button(self.friend, text = "Select All",  
                     width = 10, fg="white", bg="orange", font=("Arial", 12, "bold"),command=select_all)
                self.all_select_but.place(x=20, y=100)
                
                self.cur.execute("select fname from "+self.name)
                result = self.cur.fetchall()
                self.friend_list = []
                self.friend_name_box = []
                for friend_det in result:
                    self.friend_list.append(friend_det[0])
                self.friend_tick_box_value=[]
                a=50
                b=150
                i=0
                for name in self.friend_list:
                    self.friend_tick_box_value.append(tk.IntVar())
                    self.friend_name_box.append(tk.Checkbutton(self.friend, text = name, 
                     variable=self.friend_tick_box_value[i], 
                     width = 15, fg="white", bg="orange", font=("Arial", 12, "bold")))
                    self.friend_name_box[i].config(selectcolor="orange")
                    if a>550:
                        b+=100
                        a=50
                    self.friend_name_box[len(self.friend_name_box)-1].place(x=a,y=b)
                    a+=200
                    i+=1
            def add_friend(fname):
                self.cur.execute("select pname from Profile")
                result = self.cur.fetchall()
                profile_list = []
                for friend_det in result:
                    profile_list.append(friend_det[0])
                if fname in profile_list:
                    row = self.cur.execute("Select * from "+self.name)
                    self.cur.execute("Insert into "+self.name+" values(%s,%s)",(str(row+1),fname))
                    self.db.commit()
                    self.Restart()
                    messagebox.showinfo("Done", "Added Successfully!", parent=self.friend)
                    for chk_btn_obj in self.friend_name_box:
                        chk_btn_obj.destroy()
                    setup_env()
                    
                else:
                    messagebox.showinfo("Not Found!", "Given Name Is Not Registered!", parent=self.friend)
                    
            self.friend = tk.Toplevel()
            self.friend.geometry("700x700")
            self.friend.configure(bg="orange")
            self.friend.resizable(0, 0)

            setup_env()
                            
            add_friend_entry = tk.Entry(self.friend, width=25, font=("Arial", 12, "bold"))
            add_friend_entry.place(x=150, y=50)

            add_friend_but = tk.Button(self.friend, text="Add em up!!", font=("Arial", 12, "bold"), fg="white", bg="orange", command=lambda: add_friend(add_friend_entry.get()))
            add_friend_but.place(x=400, y=50)

            poke_friend_but = tk.Button(self.friend, text="Poke!!", font=("Arial", 14, "bold"), fg="white", bg="orange", width=10, command=lambda: poke_friend())
            poke_friend_but.place(x=250, y=550)

        def setting_Account():
            def change_Setting(status):
                    if new_ent.get() == newconf_ent.get():
                        self.cur.execute("UPDATE Profile SET "+status+" = %s WHERE pname = %s ",(new_ent.get(),re.sub("_", " ", self.name)))
                        self.set.destroy()
                        messagebox.showinfo("Done", "Successfull changed!!")
                        self.db.commit()
                        #self.db.close()
                        self.Restart()
                    else:
                        messagebox.showinfo("Oh oh!!", "Passwords are not matching!", parent=self.set)  
                        
            def buffer(status):
                setsub_btn.place(x=150, y=450)
                if status == "ps":
                    self.stat = "password"
                    new_lbl.config(text="New Password:")
                    new_lbl.place(x=30, y=110)
                    newconf_lbl.config(text="Confirm Password:")
                    newconf_lbl.place(x=30, y=180)
                    
                    new_ent.place(x=200, y=110)
                    newconf_ent.place(x=200, y=180)

                else:
                    self.stat = "pname"
                    new_lbl.config(text="New Name:")
                    new_lbl.place(x=30, y=310)
                    newconf_lbl.config(text="Confirm Name:")
                    newconf_lbl.place(x=30, y=380)
                    
                    new_ent.place(x=200, y=310)
                    newconf_ent.place(x=200, y=380)
                    
            self.set = tk.Toplevel()
            self.set.geometry("500x500")
            self.set.configure(bg="orange")
            self.set.resizable(0, 0)

            pass_setbtn = tk.Button(self.set, text="Change Password", font=("Arial", 12, "bold"), fg="white", bg="orange", width=20, command=lambda: buffer("ps"))
            pass_setbtn.place(x=140, y=50)

            name_setbtn = tk.Button(self.set, text="Change Name", font=("Arial", 12, "bold"), fg="white", bg="orange", width=20, command=lambda: buffer("nm"))
            name_setbtn.place(x=140, y=250)

            new_ent = tk.Entry(self.set, width=25, font=("Arial", 12, "bold"))
            newconf_ent = tk.Entry(self.set, width=25, font=("Arial", 12, "bold"))

            new_lbl = tk.Label(self.set, font=("Arial", 12, "bold"), fg="white", bg="orange")
            newconf_lbl = tk.Label(self.set, font=("Arial", 12, "bold"), fg="white", bg="orange")
            setsub_btn = tk.Button(self.set,text="Change", font=("Arial", 12, "bold"), fg="white", bg="orange", width=15, command=lambda: change_Setting(self.stat))

        def Refresh(Flag=None):
            self.cur.execute("select sender from Poke where received = %s",re.sub("_", " ", self.name))
            result = self.cur.fetchall()
            for obj in result: 
                messagebox.showinfo("Message!!", obj[0]+" called you!", parent=self.profile)
            self.cur.execute("Delete from Poke where received = %s",re.sub("_", " ", self.name))
            self.db.commit()
            #self.db.close()
            self.Restart()
            if Flag:
                recv_ml()
            #print("Refresh")
            self.profile.after(1000,Refresh)
        def print_Text():
            tree.delete(*tree.get_children())
            sender_rows = self.cur.fetchall()
            for row in reversed(sender_rows):
                st=str(row[3])
                tree.insert("", tk.END, values=(row[0],row[1],row[2],st[:10]))
            
        def recv_ml():
            self.message_status="sender"
            tree.heading('#2', text='From')
            self.cur.execute("SELECT mid,sender,subject,content from Messages WHERE userenabled = %s AND received = %s", ("Y", re.sub("_", " ", self.name)))
            print_Text()
            
        def send_ml():
            self.message_status="received"  
            tree.heading("#2", text="To")
            self.cur.execute("SELECT mid,received,subject,content from Messages WHERE userenabled = %s AND sender = %s", ("Y", re.sub("_", " ", self.name)))
            print_Text()    
            
        def about_Us():
            messagebox.showinfo("About Us","Made  By  Hritik Bhat.")
        def log_Out():
            res = messagebox.askquestion("Logging Out","Are you sure?")
            if res == "yes":
                self.profile.destroy()
                of=OFFLAN()

        def Search():
            if self.message_status == "received":
                st="sender"
                tree.heading('#2', text='To')
            else:
                st="received"
                tree.heading('#2', text='From')
            self.cur.execute("SELECT mid,"+self.message_status+",subject,content from Messages WHERE "+st+"=%s AND userenabled = %s AND "+self.message_status+" REGEXP %s", (re.sub("_", " ", self.name),"Y", "^"+search_ent.get()))
            print_Text()
            

        self.message_status="received"    
        msb = ttk.Scrollbar(self.profile)
        tree = ttk.Treeview(self.profile, column=("column1","column2", "column3", "column4"), show='headings', height=25, yscrollcommand=msb.set)
        tree.heading("#1",text="ID")
        tree.column("column1", stretch=False,minwidth=0,width=0)
        tree.heading("#2", text="From")
        tree.column("column2", stretch=False,minwidth=0, width=125, anchor="center")
        tree.heading("#3", text="Subject")
        tree.column("column3", stretch=False,minwidth=0, width=125, anchor="center")
        tree.heading("#4", text="Content")
        tree.column("column4", stretch=False,minwidth=0, width=750, anchor="center")
        tree.bind('<<TreeviewSelect>>', lambda ef: Open())
        tree.place(x=250, y=150)
        
        msb.place(x=1250, y=151, height=525)
        msb.config(command=tree.yview)
    
        self.profile.update()
        recv_ml()

        search_ent = tk.Entry(self.profile, font="Helvetica 13", width=48)
        search_ent.place(x=500, y=100)

        search_but = tk.Button(self.profile, text="Search!", font=("Helvetica", 8, "bold"), width=10, bg="orange", fg="white", command=Search)
        search_but.place(x=1000, y=100)

        compose_but = tk.Button(self.profile, text="Compose!", font=("Helvetica", 14, "bold"), width=10, bg="orange", fg="white", command=Compose)
        compose_but.place(x=60, y=60)

        refresh_but = tk.Button(self.profile, text="Refresh", font=("Helvetica", 8, "bold"), width=10, bg="orange", fg="white", command=lambda:Refresh(True))
        refresh_but.place(x=1170, y=125)

        tools_frame = tk.Frame(self.profile)
        tools_frame.place(x=36, y=150)
        self.but_width = 17

        sent_but = tk.Button(tools_frame, text='Sent', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white",command=send_ml)
        recv_but = tk.Button(tools_frame, text='Received', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white", command=recv_ml)
        friend_list_but = tk.Button(tools_frame, text='Friend List', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white", command=friend_list)
        cld_but = tk.Button(tools_frame, text='Cloud', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white", command=lambda: Cloud())
        set_but = tk.Button(tools_frame, text='Setting', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white", command=setting_Account)
        us_but = tk.Button(tools_frame, text='About Us', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white",command=about_Us)
        log_out_but = tk.Button(tools_frame, text='Log Out', font=("Helvetica", 14, "bold"), width=self.but_width, bg='orange', fg="white", command=log_Out)
        
        sent_but.pack(side=tk.TOP)
        recv_but.pack(side=tk.TOP)
        friend_list_but.pack(side=tk.TOP)
        cld_but.pack(side=tk.TOP)
        set_but.pack(side=tk.TOP)
        us_but.pack(side=tk.TOP)
        log_out_but.pack(side=tk.TOP)
        self.profile.after(3000, Refresh)
        
        self.profile.mainloop

of = OFFLAN()
        
#of=PROFILE("Hritik")

#of=PROFILE("Dan_Smith")
