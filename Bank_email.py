import gmail
email='xxxxxxxxx@gmail.com'   #mention your gmail id
app_pass='xxxxxxxx'           #mention app password of same gmail account
def send_mail_for_openacn(to_mail,uname,uacno,upass,udate):    

    con=gmail.GMail(email,app_pass)
    sub='Account Opened with ABC bank.'

    body=f"""Dear {uname},
        Your account has been opened Successfully with ABC Bank and details are
        ACN={uacno}
        Pass={upass}
        Open date={udate}

        Kindly change your password when you login first time.
        Thanks
        ABC Bank 
        Noida
        """
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    con.send(msg)
    
def send_otp(to_mail,uname,uotp):
    con=gmail.GMail(email,app_pass)
    sub='OTP for password recovery.'
    body=f"""Dear {uname},
        Your OTP to get password = {uotp}
        Kindly verify this otp to application.
        Thanks
        ABC Bank 
        Noida
        """
    
    msg=gmail.Message(to=to_mail,subject=sub,text=body)
    
    con.send(msg)