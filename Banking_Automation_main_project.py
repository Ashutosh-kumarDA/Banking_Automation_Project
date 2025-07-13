from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog    #import the class of root window,label(that is used to disply anythig on root window) where we made this project.
from tkinter.ttk import Combobox      #combobox component is present in ttk module of tkinter package,this conbobox is used to make the dropdown list here.
import os,shutil
import time               #to add time 
from PIL import Image,ImageTk   #to import image module from pillow library to add the impage on root window from program.
import random           #import the random package for the random generating capcha.     
import Bank_auto_project_sqlite
import sqlite3
import Bank_email


def generate_captcha():   #function for generating captcha
    captcha=[]
    for i in range(2):
        c=chr(random.randint(65,90))
        captcha.append(c)
        b=chr(random.randint(97,122))
        captcha.append(b) 
        n=random.randint(0,9)  
        captcha.append(str(n))
    random.shuffle(captcha)
    captcha=' '.join(captcha)
    return captcha

def refresh(event):                #function to refresh the captcha.
    captcha=generate_captcha()
    captcha_lbl.configure(text=captcha)


root=Tk()                 #make the object of the root window.
root.state("zoomed")      #give the maximize size to the root window.
root.configure(bg='powder blue')     #to apply the background color.
root.title('ABC Bank')               #to give the title over window.
root.resizable(width=False,height=False)    #to remove the tendency of resizing the window by which it do not make effect on the content of the window. 

title_lbl=Label(root,text="Banking Automation",bg='powder blue',font=('Arial',50,'bold','underline'))     #Adding title on the window and also size fixing and adding font.
title_lbl.pack()              #pack() is used to display the content at top center of the root window.

today_lbl=Label(root,text=time.strftime("%A,%d-%B-%Y"),bg='powder blue',font=('arial',15),fg='blue')
today_lbl.pack(pady=10)

img=Image.open("images/logo.png").resize((250,150))    #import the image in the program using image.open methode
img_bitmap=ImageTk.PhotoImage(img,master=root)       #here jpg img is conveted into bitmap formate because root is only supports bitmap formate in thr case of image
logo_lbl=Label(root,image=img_bitmap)           #display the logo on the root window.
logo_lbl.place(relx=0,rely=0)                   #here the loc of this logo that is place top left corner of the window  

img1=Image.open("images/Bank_logo.jpg").resize((250,150))
img1_bitmap=ImageTk.PhotoImage(img1,master=root)
logo1_lbl=Label(root,image=img1_bitmap)
logo1_lbl.place(relx=.84,rely=0)

footer_lbl=Label(root,text="Developed by:Ashutosh_Kumar",bg='powder blue',fg='blue',font=('Arial',15,'bold')) 
footer_lbl.pack(side='bottom',pady=10)
def main_screen():        #adding frame as a main screen with giving it a proper color,fond size and the position of the screen.
    def forgot():
        frm.destroy()
        forgot_screen()
    
    def login():
        uacn=acn_entry.get()        #get() is used to fetch the data form the entry methode
        upass=pass_entry.get()
        ucap=inputcap_entry.get()
        utype=user_combo.get()
        actual_cap=captcha_lbl.cget('text')   #cget() is used to fetch the data from the label methode
        actual_cap=actual_cap.replace(' ','')   #through this we convert the captcha with spaces to captcha without spaces 
        if utype=="Admin":
            
            if(uacn=='0' and upass=='admin'):
                if(ucap==actual_cap):
                    frm.destroy()     #if we don't call destroy() then here 2 screens is formed then for a single we have to call destroy()
                    admin_screen()
                else:
                    messagebox.showerror('Login','Invalid Captcha')
            else:
                messagebox.showerror('Login','Invalid ACN/PASS/TYPE')   
        elif utype=="User":
            if(ucap==actual_cap):
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=? and accounts_pass=?'
                curobj.execute(query,(uacn,upass))

                tup=curobj.fetchone() 
                conobj.close()
                if tup==None:
                    messagebox.showerror("User Login","Invalid ACN/PASS")
                else:
                    frm.destroy()
                    user_screen(uacn)                                    #if we don't call destroy() then here many screens are overlap then for a single we have to call destroy() for previous frame                                       #if we don't call destroy() then here 2 screens is formed then for a single we have to call destroy()
                    
            else:
                messagebox.showerror('Login','Invalid Captcha')
            
        else:
            messagebox.showerror("Login","Kindly Select valid User type")
            

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=0.18,relwidth=1,relheight=.77)
    
    user_lbl=Label(frm,text="User Type",bg='pink',font=('arial',20,'bold'))
    user_lbl.place(relx=.38,rely=.1)

    user_combo=Combobox(frm,values=['Admin','User','---Select---'],font=(20),state='readonly')
    user_combo.current(2)
    user_combo.place(relx=.5,rely=.1)
    
    acn_lbl=Label(frm,text="ACN",bg='pink',font=('arial',20,'bold'))
    acn_lbl.place(relx=.38,rely=.21)
    
    acn_entry=Entry(frm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
    acn_entry.place(relx=.5,rely=.2)
    acn_entry.focus()

    pass_lbl=Label(frm,text="PASS",bg='pink',font=('arial',20,'bold'))
    pass_lbl.place(relx=.38,rely=.31)

    pass_entry=Entry(frm,font=('Arial',20),bd=5,show='*')    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
    pass_entry.place(relx=.5,rely=.3)
    
    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),bg='white',font=('arial',20))
    captcha_lbl.place(relx=.5,rely=.4)
    
    #refresh_btn=Button(frm,text="refresh",bg="yellow",fg="black",command=refresh)  #adding button to refresh the captcha
    #refresh_btn.place(relx=.6,rely=.41)

    refresh_img=Image.open("images/refreshlogo_1.png").resize((30,30))
    refresh_img_bitmap=ImageTk.PhotoImage(refresh_img,master=root)
    refresh_logo=Label(frm,image=refresh_img_bitmap,bg="pink")
    refresh_logo.image=refresh_img_bitmap
    refresh_logo.place(relx=.61,rely=.40)
    refresh_logo.bind("<Button>",refresh)

    inputcap_lbl=Label(frm,text="CAPTCHA",bg='pink',font=('arial',20,'bold'))
    inputcap_lbl.place(relx=.38,rely=.5)
    
    inputcap_entry=Entry(frm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password captcha.It is a basic component easily found in tkinter. 
    inputcap_entry.place(relx=.5,rely=.5)
    
    login_btn=Button(frm,text="login",bg="powder blue",font=('arial',16,'bold'),bd=5,command=login)  #adding button to login.
    login_btn.place(relx=.5,rely=.6)
    
    reset_btn=Button(frm,text="reset",bg="red",font=('arial',16,'bold'),bd=5)  #adding button to reset data.
    reset_btn.place(relx=.6,rely=.6)

    forgotpass_btn=Button(frm,text="forgot pasword",bg="white",fg='blue',font=('arial',13),bd=5,command=forgot)  #adding button to forgot password.
    forgotpass_btn.place(relx=.71,rely=.31)

def admin_screen():       #here is the admin screen where admin perfon their tasks.
    def open_acn():       #this fun is made for the add acn screen by the admin.
        def open_acn_db():
            uname=name_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
            ugender=gender_combo.get()
            ubal=0.0
            uopendate=time.strftime("%A,%d-%B-%Y")
            upass=generate_captcha().replace(' ','')

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()

            query='insert into accounts values(null,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,ugender,uopendate,ubal))
            conobj.commit()
            conobj.close()
            #messagebox.showinfo('Open Account','Account Opened Successfully')
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            
            query="select max(accounts_acno) from accounts"
            curobj.execute(query)

            uacno=curobj.fetchone()[0]
            conobj.close()
            
            try:
                Bank_email.send_mail_for_openacn(uemail,uacno,uname,upass,uopendate)
                msg=f'Account opened with ACN {uacno} and mail sent to {uemail},kindly check spam also.'
                messagebox.showinfo('Open Account',msg)
            except Exception as msg:
                messagebox.showerror("Open Account",msg)

        def reset():
            name_entry.delete(0,"end")
            email_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            gender_combo.current(2)
            name_entry.focus()

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relheight=.6,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is Open Account Screen",bg='white',fg='purple',font=('arial',18))
        title_lbl.pack()

        name_lbl=Label(ifrm,text="Name",bg='white',font=('arial',20,'bold'))
        name_lbl.place(relx=.1,rely=.1)
    
        name_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        name_entry.place(relx=.1,rely=.2)
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",bg='white',font=('arial',20,'bold'))
        email_lbl.place(relx=.1,rely=.35)

        email_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        email_entry.place(relx=.1,rely=.45)

        mob_lbl=Label(ifrm,text="Mob",bg='white',font=('arial',20,'bold'))
        mob_lbl.place(relx=.55,rely=.1)

        mob_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        mob_entry.place(relx=.55,rely=.2)
        
        gender_lbl=Label(ifrm,text="Gender",bg='white',font=('arial',20,'bold'))
        gender_lbl.place(relx=.55,rely=.35)

        gender_combo=Combobox(ifrm,values=['Male','Female','Other','---Select---'],font=('arial',20),state='readonly')
        gender_combo.current(3)
        gender_combo.place(relx=.55,rely=.45)

        open_btn=Button(ifrm,text="Open Account",bg="powder blue",font=('arial',20,'bold'),bd=5,command=open_acn_db)  #adding button to open account.
        open_btn.place(relx=.5,rely=.7)
    
        reset_btn=Button(ifrm,command=reset,text="Reset",bg="powder blue",font=('arial',20,'bold'),bd=5)  #adding button to reset data.
        reset_btn.place(relx=.75,rely=.7)



    def delete_acn():    #this fun is made for the delete acn screen by the admin. 
        def send_otp():
            uacn=acn_entry.get()
            
            #authentication acn,email
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn))

            tup=curobj.fetchone() 
            conobj.close()
            if tup==None:
                messagebox.showerror("Delete Account","Record not found")
            else:
                otp=str(random.randint(1000,9999))
                Bank_email.send_otp(tup[3],tup[1],otp)
                messagebox.showinfo('Delete Account','otp send to given/registered mail id')

                otp_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password captcha.It is a basic component easily found in tkinter. 
                otp_entry.place(relx=.43,rely=.6)
                def verify():
                    uotp=otp_entry.get()
                    if otp==uotp:
                        resp=messagebox.askyesno("Delete Account",f"Do you want to delete this account.")
                        if not resp:
                            frm.destroy()
                            admin_screen()
                            return
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query='delete from accounts where accounts_acno=?'
                        curobj.execute(query,(uacn))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo('Delete Account','Account Deleted')
                        frm.destroy()
                        admin_screen()
                    else:
                        messagebox.showerror("Delete Account","Incorrect OTP")

                verify_btn=Button(frm,command=verify,text="Verify",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
                verify_btn.place(relx=.65,rely=.6)  
            
        
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relheight=.6,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is Delete Account Screen",bg='white',fg='purple',font=('arial',18))
        title_lbl.pack()

        acn_lbl=Label(ifrm,text="ACN",bg='white',font=('arial',20,'bold'))
        acn_lbl.place(relx=.33,rely=.21)
    
        acn_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        acn_entry.place(relx=.43,rely=.2)
        acn_entry.focus

        otp_btn=Button(ifrm,command=send_otp,text="Send OTP",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
        otp_btn.place(relx=.48,rely=.4)
        

    def view_acn():      #this fun is made for the view acn screen by the admin.
        def view_detail():
            uacn=acn_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))

            tup=curobj.fetchone() 
            conobj.close()
            if tup==None:
                messagebox.showerror("Delete Account","Record not found")
            else:
                details=f'''User Name={tup[1]}
Aval bal={tup[7]}
ACN Open Date={tup[6]}
Email={tup[3]}
Mob={tup[4]}
'''         
                messagebox.showinfo('Veiw Account',details)

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.2,relheight=.6,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is View Account Screen",bg='white',fg='purple',font=('arial',18))
        title_lbl.pack()

        acn_lbl=Label(ifrm,text="ACN",bg='white',font=('arial',20,'bold'))
        acn_lbl.place(relx=.33,rely=.21)
    
        acn_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        acn_entry.place(relx=.43,rely=.2)
        acn_entry.focus

        view_btn=Button(ifrm,command=view_detail,text="View ACN",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
        view_btn.place(relx=.48,rely=.4)
     
    def logout():
        resp=messagebox.askyesno('Admin_Screen','Do you want to Logout.')   #this msgbox is display a msg on the screen wants the final confirmation about logout. 
        if resp:
            frm.destroy()
            main_screen()

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=0.18,relwidth=1,relheight=.77)
    
    wel_lbl=Label(frm,text="Welcome Admin",bg='pink',fg='green',font=('arial',20,'bold'))
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",bg="powder blue",font=('arial',20,'bold'),command=logout)  #adding button to logout the admin screen.
    logout_btn.place(relx=.9,rely=0) 

    openacn_btn=Button(frm,text="Open Account",bg="green",fg='white',font=('arial',20),bd=5,command=open_acn)  #adding button to add acn by admin.
    openacn_btn.place(relx=.2,rely=0)     

    deleteacn_btn=Button(frm,text="Delete Account",bg="red",fg='white',font=('arial',20),bd=5,command=delete_acn)  #adding button to delete acn by admin.
    deleteacn_btn.place(relx=.4,rely=0)
     
    viewacn_btn=Button(frm,text="View Account",bg="yellow",font=('arial',20),fg='black',bd=5,command=view_acn)  #adding button to reset data.
    viewacn_btn.place(relx=.6,rely=0)

def forgot_screen():
    def back():
        frm.destroy
        main_screen()
    
    def send_otp():
        uacn=acn_entry.get()
        uemail=email_entry.get()
        ucaptcha=inputcap_entry.get()
        if ucaptcha!=forgot_captcha.replace(' ',''):
                messagebox.showerror('forgot password','Invalid captcha')
                return
        #authentication acn,email
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        curobj.execute(query,(uacn,uemail))

        tup=curobj.fetchone() 
        conobj.close()
        if tup==None:
            messagebox.showerror("Forgot Password","Record not found")
        else:
            otp=str(random.randint(1000,9999))
            Bank_email.send_otp(uemail,tup[1],otp)
            messagebox.showinfo('Forgot Password','otp send to given/registered mail id')

            otp_entry=Entry(frm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password captcha.It is a basic component easily found in tkinter. 
            otp_entry.place(relx=.5,rely=.7)
            def verify():
                uotp=otp_entry.get()
                if otp==uotp:
                    messagebox.showinfo("Forgot Password",f"Your Pass={tup[2]}")
                else:
                    messagebox.showerror("Forgot Password","Incorrect OTP")

            verify_btn=Button(frm,command=verify,text="Verify",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
            verify_btn.place(relx=.72,rely=.7)  
            

    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=0.18,relwidth=1,relheight=.77)

    back_btn=Button(frm,text="back",bg="powder blue",font=('arial',20,'bold'),bd=5,command=back)  #adding button to reset data.
    back_btn.place(relx=0,rely=0)

    acn_lbl=Label(frm,text="ACN",bg='pink',font=('arial',20,'bold'))
    acn_lbl.place(relx=.38,rely=.21)
    
    acn_entry=Entry(frm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
    acn_entry.place(relx=.5,rely=.2)
    acn_entry.focus

    email_lbl=Label(frm,text="Email",bg='pink',font=('arial',20,'bold'))
    email_lbl.place(relx=.38,rely=.31)
    
    email_entry=Entry(frm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
    email_entry.place(relx=.5,rely=.3)

    global captcha_lbl
    forgot_captcha=generate_captcha()
    captcha_lbl=Label(frm,text=forgot_captcha,bg='white',font=('arial',20))
    captcha_lbl.place(relx=.5,rely=.4)
    
    #refresh_btn=Button(frm,text="refresh",bg="yellow",fg="black",command=refresh)  #adding button to refresh the captcha
    #refresh_btn.place(relx=.6,rely=.41)

    refresh_img=Image.open("images/refreshlogo_1.png").resize((30,30))
    refresh_img_bitmap=ImageTk.PhotoImage(refresh_img,master=root)
    refresh_logo=Label(frm,image=refresh_img_bitmap,bg="pink")
    refresh_logo.image=refresh_img_bitmap
    refresh_logo.place(relx=.61,rely=.40)
    refresh_logo.bind("<Button>",refresh)

    inputcap_lbl=Label(frm,text="Captcha",bg='pink',font=('arial',20,'bold'))
    inputcap_lbl.place(relx=.38,rely=.5)
    
    inputcap_entry=Entry(frm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password captcha.It is a basic component easily found in tkinter. 
    inputcap_entry.place(relx=.5,rely=.5)
    
    otp_btn=Button(frm,command=send_otp,text="Send OTP",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
    otp_btn.place(relx=.5,rely=.6)
    
    reset_btn=Button(frm,text="reset",bg="red",font=('arial',16,'bold'),bd=5)  #adding button to reset data.
    reset_btn.place(relx=.6,rely=.6)

def user_screen(uacn=None):
    def logout():
        resp=messagebox.askyesno('User_Screen','Do you want to Logout?')   #this msgbox is display a msg on the screen wants the final confirmation about logout. 
        if resp:
            frm.destroy()
            main_screen()
     
    def detail_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.16,relheight=.7,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is check detail Screen",bg='white',fg='purple',font=('arial',18,"underline"))
        title_lbl.pack()
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        details=f'''Account No.  =  {tup[0]}
Opening date  =  {tup[6]}
Available Bal  =  {tup[7]}
Email Id  =  {tup[3]}
Mob No.  =  {tup[4]}
        
'''
        details_lbl=Label(ifrm,text=details,bg='white',font=('arial',20,'bold'))
        details_lbl.place(relx=.15,rely=.26)
    def update_screen():
        def update_db():
            uname=name_entry.get()
            upass=pass_entry.get()
            uemail=email_entry.get()
            umob=mob_entry.get()
        
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
              
            query='update accounts set accounts_name=?,accounts_pass=?,accounts_email=?,accounts_mob=? where accounts_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Detail","Profile Updated")
              
            user_screen(uacn)
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.16,relheight=.7,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is Update Screen",bg='white',fg='purple',font=('arial',18,"underline"))
        title_lbl.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select * from accounts where accounts_acno=?',(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        name_lbl=Label(ifrm,text="Name",bg='white',font=('arial',20,'bold'))
        name_lbl.place(relx=.1,rely=.1)
    
        name_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        name_entry.place(relx=.1,rely=.2)
        name_entry.insert(0,tup[1])
        name_entry.focus()

        email_lbl=Label(ifrm,text="Email",bg='white',font=('arial',20,'bold'))
        email_lbl.place(relx=.1,rely=.35)

        email_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        email_entry.place(relx=.1,rely=.45)
        email_entry.insert(0,tup[3])

        mob_lbl=Label(ifrm,text="Mob",bg='white',font=('arial',20,'bold'))
        mob_lbl.place(relx=.55,rely=.1)

        mob_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        mob_entry.place(relx=.55,rely=.2)
        mob_entry.insert(0,tup[4])
        
        pass_lbl=Label(ifrm,text="Pass",bg='white',font=('arial',20,'bold'))
        pass_lbl.place(relx=.55,rely=.35)

        pass_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        pass_entry.place(relx=.55,rely=.45)
        pass_entry.insert(0,tup[2])

        update_btn=Button(ifrm,text="Update",bg="powder blue",font=('arial',20,'bold'),bd=5,command=update_db)  #adding button to open account.
        update_btn.place(relx=.5,rely=.7)


    def withdraw_screen():
        def withdraw():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()
             
            if ubal>uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()
             
                t=str(time.time())
                utxnid='txn'+t[:t.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query= 'insert into stmts values(?,?,?,?,?,?)'
                curobj.execute(query,(uacn,uamt,"DB.",time.strftime("%d-%m-%Y %r"),ubal-uamt,utxnid))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Deposit",f'{uamt} Amount Withdraw')
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Withdraw",f'Insufficient Bal {ubal}')

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.16,relheight=.7,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is withdraw Screen",bg='white',fg='purple',font=('arial',18,"underline"))
        title_lbl.pack()

        amt_lbl=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        amt_lbl.place(relx=.33,rely=.21)
    
        amt_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        amt_entry.place(relx=.45,rely=.2)
        amt_entry.focus

        dep_btn=Button(ifrm,command=withdraw,text="Withdraw",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
        dep_btn.place(relx=.48,rely=.4)

    
    def deposit_screen():
        def deposit():
            uamt=float(amt_entry.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()
             
            t=str(time.time())
            utxnid='txn'+t[:t.index('.')]
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query= 'insert into stmts values(?,?,?,?,?,?)'
            curobj.execute(query,(uacn,uamt,"CR.",time.strftime("%d-%m-%Y %r"),ubal,utxnid))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f'{uamt} Amount Deposited')
            frm.destroy()
            user_screen(uacn)

        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.16,relheight=.7,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is deposit Screen",bg='white',fg='purple',font=('arial',18,"underline"))
        title_lbl.pack()
         

        amt_lbl=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        amt_lbl.place(relx=.33,rely=.21)
    
        amt_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        amt_entry.place(relx=.45,rely=.2)
        amt_entry.focus

        dep_btn=Button(ifrm,command=deposit,text="Deposit",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
        dep_btn.place(relx=.48,rely=.4)

    
    def transfer_screen():
        
        def transfer():
            toacn=to_entry.get()
            uamt=float(amt_entry.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            curobj.execute(query,(toacn,))
            to_tup=curobj.fetchone()
            conobj.close()
            
            if to_tup==None:
                messagebox.showerror("Transfer",'To ACN does not exist')
                return
             
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select accounts_bal from accounts where accounts_acno=?'
            curobj.execute(query,(uacn,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query_deduct='update accounts set accounts_bal=accounts_bal-? where accounts_acno=?'
                query_credit='update accounts set accounts_bal=accounts_bal+? where accounts_acno=?'
                curobj.execute(query_deduct,(uamt,uacn))
                curobj.execute(query_credit,(uamt,toacn))
                conobj.commit()
                conobj.close()
             
                t=str(time.time())
                utxnid1='txn_db'+t[:t.index('.')]
                utxnid2='txn_cr'+t[:t.index('.')]
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1= 'insert into stmts values(?,?,?,?,?,?)'
                query2= 'insert into stmts values(?,?,?,?,?,?)'
                
                curobj.execute(query1,(uacn,uamt,"DB.",time.strftime("%d-%m-%Y %r"),ubal-uamt,utxnid1))
                curobj.execute(query2,(uacn,uamt,"CR.",time.strftime("%d-%m-%Y %r"),ubal+uamt,utxnid2))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f'{uamt} Amount Transferred.')
                frm.destroy()
                user_screen(uacn)
            else:
                messagebox.showerror("Transfer",f'Insufficient Bal {ubal}')


        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.16,relheight=.7,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is Transfer Screen",bg='white',fg='purple',font=('arial',18,"underline"))
        title_lbl.pack()

        to_lbl=Label(ifrm,text="TO ACN",bg='white',font=('arial',20,'bold'))
        to_lbl.place(relx=.33,rely=.21)
    
        to_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        to_entry.place(relx=.45,rely=.21)
        to_entry.focus

        amt_lbl=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        amt_lbl.place(relx=.33,rely=.4)
    
        amt_entry=Entry(ifrm,font=('Arial',20),bd=5)    #Entry component is used to allow the entry in whatever like acn no.,password.It is a basic component easily found in tkinter. 
        amt_entry.place(relx=.45,rely=.4)
        amt_entry.focus

        tr_btn=Button(ifrm,command=transfer,text="Transfer",bg="powder blue",font=('arial',16,'bold'),bd=5)  #adding button to login.
        tr_btn.place(relx=.55,rely=.6)


    def history_screen():
        ifrm=Frame(frm,highlightthickness=2,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.16,relheight=.7,relwidth=.7)
          
        title_lbl=Label(ifrm,text="This is Transaction history Screen",bg='white',fg='purple',font=('arial',18,"underline"))
        title_lbl.pack()
        
        from tktable import Table
        table_header=("Txn ID", "Amount","Txn type", "Updated Bal", "Date")
        mytable= Table(ifrm, table_header,col_width=150, headings_bold=True)
        mytable.pack(pady=10)
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select stmts_txnid,stmts_amt,stmts_type,stmts_update_bal,stmts_date from stmts where stmts_acn=?'
        curobj.execute(query,(uacn,))
        for tup in curobj:
            mytable.insert_row(tup)
        conobj.close()
    
    def getdetail():
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=?'
        curobj.execute(query,(uacn,))
        tup=curobj.fetchone() 
        conobj.close()
        return tup  
    
    def update_picture():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'images/{uacn}.png')

        img=Image.open(f'images/{uacn}.png').resize((190,135))    #import the image in the program using image.open methode
        img_bitmap=ImageTk.PhotoImage(img,master=root)       #here jpg img is conveted into bitmap formate because root is only supports bitmap formate in thr case of image
        profile_img_lbl.image=img_bitmap
        profile_img_lbl.configure(image=img_bitmap)
     
    frm=Frame(root)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=0.18,relwidth=1,relheight=.77)
    
    wel_lbl=Label(frm,text=f"Welcome,{getdetail()[1]}",bg='pink',fg='green',font=('arial',20,'bold'))
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,text="logout",bg="powder blue",font=('arial',20,'bold'),command=logout)  #adding button to logout the user screen.
    logout_btn.place(relx=.92,rely=0) 
    
    if os.path.exists(f'images/{uacn}.png'):
        path=f"images/{uacn}.png"
    else:
        path="images/default_user.webp"
    
    img=Image.open(path).resize((190,135))    #import the image in the program using image.open methode
    img_bitmap=ImageTk.PhotoImage(img,master=root)       #here jpg img is conveted into bitmap formate because root is only supports bitmap formate in thr case of image
    profile_img_lbl=Label(frm,image=img_bitmap,bg="pink")           #display the logo on the root window.
    profile_img_lbl.image=img_bitmap
    profile_img_lbl.place(relx=.002,rely=.06) 
    
    updatepic_btn=Button(frm,command=update_picture,text="Update Picture",width=12,bd=5,bg="yellow",font=('arial',17,'bold'))  #adding button to check detail the user screen.
    updatepic_btn.place(relx=.005,rely=0.3)

    check_btn=Button(frm,text="Check Details",width=12,bd=5,bg="yellow",font=('arial',17,'bold'),command=detail_screen)  #adding button to check detail the user screen.
    check_btn.place(relx=.005,rely=0.4)

    deposit_btn=Button(frm,text="Deposit",width=12,bd=5,bg="green",font=('arial',17,'bold'),fg='white',command=deposit_screen)  
    deposit_btn.place(relx=.005,rely=0.5)

    withdraw_btn=Button(frm,text="Withdraw",width=12,bd=5,bg="red",font=('arial',17,'bold'),fg='white',command=withdraw_screen)  
    withdraw_btn.place(relx=.005,rely=0.6)
    
    update_btn=Button(frm,text="Update",width=12,bd=5,bg="powder blue",font=('arial',17,'bold'),command=update_screen)  
    update_btn.place(relx=.005,rely=0.7)

    transfer_btn=Button(frm,text="Transfer",width=12,bd=5,bg="red",font=('arial',17,'bold'),fg='white',command=transfer_screen)  
    transfer_btn.place(relx=.005,rely=0.8)

    history_btn=Button(frm,text="History",width=12,bd=5,bg="powder blue",font=('arial',17,'bold'),command=history_screen)  
    history_btn.place(relx=.005,rely=0.9)

main_screen()             #calling the main screen function i.e. main frame where mainly operations are performing.  
root.mainloop()           #root window is visible by this methode 

