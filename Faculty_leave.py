import sqlite3
import tkinter 
from tkinter import *
from easygui import *
from tkinter.font import Font
from tkinter import ttk
import PIL
import PIL.Image as p
from PIL import Image,ImageTk
from tkinter import messagebox
import smtplib
from email.message import EmailMessage
from validate_email_address import validate_email
import random
from datetime import *

conn=sqlite3.connect('Faculty.db')
cursor=conn.cursor()
cursor.execute("Create TABLE IF NOT EXISTS BALANCE(Faculty_Id varchar2,Casual_Leave int,Medical_Leave int,Loss_of_pay int,maternity_leave int,CCL int)")
cursor.execute("CREATE TABLE IF NOT EXISTS FACULTY(Faculty_Id varchar2,Name varchar2,Gender varchar(1),Subject varchar2,Password varchar2,contact_no varchar2,email_id varchar2,sections_teaching varchar2,security_code varchar2)")
cursor.execute("Create TABLE IF NOT EXISTS STATUS(Leave_Id int,Faculty_Id varchar2,Leave varchar2,Date1 varchar2,Date2 varchar2,Days int,status varchar2,workid varchar2,work_facid varchar2,status_workload varchar2)")
cursor.execute("Create TABLE IF NOT EXISTS Revoke(Leave_Id int,Faculty_Id varchar2,Leave varchar2,Date1 varchar2,Date2 varchar2,status varchar2,Request_date date )")
cursor.execute("Create TABLE IF NOT EXISTS ADMIN(Username varchar2,Password varchar2,Security_code varchar2,email varchar2,passcode varchar2)")
cursor.execute("Create Table IF NOT EXISTS Month(Faculty_Id varchar2,first int,second int,third int,fourth int,fifth int,sixth int,seventh int,eighth int,ninth int,tenth int,eleventh int,twelvth int)")
cursor.execute("Create Table IF NOT EXISTS Month1(Faculty_Id varchar2,first int,second int,third int,fourth int,fifth int,sixth int,seventh int,eighth int,ninth int,tenth int,eleventh int,twelvth int)")
cursor.execute("CREATE TABLE IF NOT EXISTS WORKASSIGN(Work_Id int,assigned_by varchar2,Faculty_Id varchar2,Message varchar2,startdate varchar2,enddate varchar2)")
def adminvalidation():
    message='Admin Login'
    text='Enter login Id and password '
    filed_names=['Username','Password']
    fields=multpasswordbox(message,text,filed_names)
    cursor.execute("SELECT * FROM ADMIN")
    for row_1 in cursor.execute("SELECT * FROM ADMIN"):
        Id=row_1[0]
        password=row_1[1]
    if fields[0]==Id and fields[1]==password:
        messagebox.showinfo('Admin login','log in successfully')
        adminmain_window()
    else:
        messagebox.showerror('Admin login','Invalid ID or Password')
        
def Faculty_registration():
    message="Faculty Registration"
    text='Enter following details'
    field_names=["Faculty_ID","Name","Gender","contact_no","email id","Subject teaching","Sections teaching","Security code","Password"]
    fields=multpasswordbox(message,text,field_names)
    while True:
        faculmsg=""
        for i in range(len(fields)):
            if fields[i]=="":
                faculmsg=faculmsg+('"%s" is a required filed\n\n'%field_names[i])
        if faculmsg=="":
            break
        fields=multpasswordbox(faculmsg,message,field_names,fields)
        
    while True:

        if len(fields[2])>1:
            fields=multpasswordbox("In Gender only M or F is accepted",message,field_names,fields)
        elif fields[2].upper()!="M" and fields[2].upper()!="F":
            fields=multpasswordbox("In Gender only M or F is accepted",message,field_names,fields)
        elif len(fields[3])<10 or len(fields[3])>10:
            fields=multpasswordbox("Invalid Mobile no",message,field_names,fields)
        elif (fields[3],) in cursor.execute("SELECT contact_no From FACULTY"):
            fields=multpasswordbox("Mobile no already in use by others",message,field_names,fields)
        elif (fields[4],) in cursor.execute("SELECT email_id from FACULTY") or (fields[4],) in cursor.execute('SELECT email from ADMIN'):
            fields=multpasswordbox("Email ID already in use by others",message,field_names,fields)
        elif (fields[7],) in cursor.execute("SELECT security_code From FACULTY") or (fields[7],) in cursor.execute("SELECT Security_code From ADMIN"):
            fields=multpasswordbox("The Security Code is weak or Invalid",message,field_names,fields)
        elif (fields[0],) in cursor.execute("SELECT Faculty_Id From FACULTY"):
            fields=multpasswordbox("The Faculty Id is already in use by others",message,field_names,fields)
        else:
            cursor.execute("INSERT INTO FACULTY(Faculty_Id,Name,Gender,contact_no,email_id,Subject,sections_teaching,security_code,Password) VALUES(?,?,?,?,?,?,?,?,?)",(fields[0],fields[1],(fields[2]).upper(),fields[3],fields[4],fields[5],fields[6],fields[7],fields[8]))
            cursor.execute("INSERT INTO BALANCE(Faculty_Id,Casual_Leave,Medical_Leave,Loss_of_pay,maternity_leave,CCL) VALUES(?,?,?,?,?,?)",(fields[0],24,31,0,55,0))
            cursor.execute("INSERT INTO Month(Faculty_Id,first,second,third,fourth,fifth,sixth,seventh,eighth,ninth,tenth,eleventh,twelvth) Values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(fields[0],0,0,0,0,0,0,0,0,0,0,0,0))
            cursor.execute("INSERT INTO Month1(Faculty_Id,first,second,third,fourth,fifth,sixth,seventh,eighth,ninth,tenth,eleventh,twelvth) Values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(fields[0],0,0,0,0,0,0,0,0,0,0,0,0))
            conn.commit()
            subject_f=fields[1]+','+'\n\n\nYour details are successfully registered with us.' 
            mail_sender(fields[4],"Faculty Registration",subject_f)
            messagebox.showinfo('Faculty Registration','Details Registered successfully')
            break
    
def Faculty_login():
    FaculWindow=Toplevel()
    FaculWindow.wm_attributes("-fullscreen",1)
    back_img=Label(FaculWindow,image=img2)
    back_img.place(x=0,y=0,relwidth=1, relheight=1)
    all_Faculty=Button(FaculWindow,text="Faculty Information",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Faculty_Info,pady=3)
    all_Faculty["font"]=Btnfont
    last_leave=Button(FaculWindow,text="Last Leave Status",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=last_leavewindow,pady=3)
    last_leave["font"]=Btnfont
    All_leave=Button(FaculWindow,text="All Leave Status",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=all_leave_status,pady=3)
    All_leave["font"]=Btnfont
    submit_leave=Button(FaculWindow,text="Submit Leave",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=work_assign,pady=3)
    submit_leave["font"]=Btnfont
    Balance_leave=Button(FaculWindow,text="Leave Balance",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=balance_left,pady=3)
    Balance_leave["font"]=Btnfont
    work_leave=Button(FaculWindow,text="Work Adjustment",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=work_left,pady=3)
    work_leave["font"]=Btnfont
    Revoke_leave=Button(FaculWindow,text="Revoke Leave",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Revoke_apply,pady=3)
    Revoke_leave["font"]=Btnfont
    Edit_Details=Button(FaculWindow,text="Edit Details",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=edit_Faculty,pady=3)
    Edit_Details["font"]=Btnfont
    Exit_leave=Button(FaculWindow,text="Exit",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=FaculWindow.destroy,pady=3)
    Exit_leave["font"]=Btnfont
    print(cursor.fetchall())
    all_Faculty.place(relx=0.5,rely=0.11,anchor=CENTER)
    last_leave.place(relx = 0.5, rely = 0.207, anchor = CENTER)
    work_leave.place(relx = 0.5, rely = 0.304, anchor = CENTER)
    All_leave.place(relx = 0.5, rely = 0.402, anchor = CENTER)
    Balance_leave.place(relx = 0.5, rely = 0.499, anchor = CENTER)
    Revoke_leave.place(relx = 0.5, rely = 0.596, anchor = CENTER)
    submit_leave.place(relx = 0.5, rely = 0.693,anchor=CENTER)
    Edit_Details.place(relx = 0.5, rely = 0.791,anchor=CENTER)
    Exit_leave.place(relx = 0.5, rely = 0.888,anchor=CENTER)
    
def Faculty_Success():
    global matches
    matches=False
    message="Faculty login"
    Title="Enter Faculty_Id and password"
    Fields21=["Faculty_Id","Password"]
    Fields_S=multpasswordbox(message,Title,Fields21)
    for row in cursor.execute("SELECT * FROM FACULTY WHERE Faculty_Id=?",[Fields_S[0]]):
        global login
        login=Fields_S[0]
        if Fields_S[0]==row[0] and Fields_S[1]==row[4]:
            matches=True
            messagebox.showinfo("Faculty Login","Log in successfully")
            Faculty_login()
    while True:
        if Fields_S==["",""] or (Fields_S[0]=="" or Fields_S[1]==""):
            Title1="Please Fill all Details"
            Fields_S=multpasswordbox(Title1,message,Fields21,Fields_S)
            for row in cursor.execute("SELECT * FROM FACULTY WHERE Faculty_Id=?",[Fields_S[0]]):
                if Fields_S[0]==row[0] and Fields_S[1]==row[4]:
                    matches=True
                    messagebox.showinfo("Faculty Login","Log in successfully")
                    Faculty_login()
        elif matches==False:
            messagebox.showerror("Faculty Login","Incorrrect Id or Password")
            break
        else:
            break
    print(cursor.fetchall())

def monthretrieve(m,I_D):
    if m==1:
        for i in cursor.execute("SELECT first FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==2:
        for i in cursor.execute("SELECT second FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==3:
        for i in cursor.execute("SELECT third FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==4:
        for i in cursor.execute("SELECT fourth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==5:
        for i in cursor.execute("SELECT fifth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==6:
        for i in cursor.execute("SELECT sixth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==7:
        for i in cursor.execute("SELECT seventh FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==8:
        for i in cursor.execute("SELECT eighth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==9:
        for i in cursor.execute("SELECT ninth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==10:
        for i in cursor.execute("SELECT tenth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==11:
        for i in cursor.execute("SELECT eleventh FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==12:
        for i in cursor.execute("SELECT twelvth FROM Month where Faculty_Id =?",[I_D]):
            days_g=i[0]
    return days_g

def monthretrieve1(m,I_D):
    if m==1:
        for i in cursor.execute("SELECT first FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==2:
        for i in cursor.execute("SELECT second FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==3:
        for i in cursor.execute("SELECT third FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==4:
        for i in cursor.execute("SELECT fourth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==5:
        for i in cursor.execute("SELECT fifth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==6:
        for i in cursor.execute("SELECT sixth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==7:
        for i in cursor.execute("SELECT seventh FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==8:
        for i in cursor.execute("SELECT eighth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==9:
        for i in cursor.execute("SELECT ninth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==10:
        for i in cursor.execute("SELECT tenth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==11:
        for i in cursor.execute("SELECT eleventh FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    elif m==12:
        for i in cursor.execute("SELECT twelvth FROM Month1 where Faculty_Id =?",[I_D]):
            days_g=i[0]
    return days_g

def work_assign():
    choices_list=list()
    for i in cursor.execute("SELECT Faculty_Id FROM FACULTY where Faculty_Id !=?",[login]):
        choices_list.append(i[0])
    workID=random.randint(1, 1000)
    message="Select the Faculty Id"
    Title="Assign Work Load"
    if choices_list==[]:
        assign_updated
    elif len(choices_list)==1:
        choice_box=choices_list[0]
        while True:
            message="Enter the work message"
            Title='Work assign'
            field_names=['Work Message']
            fields=multenterbox(message,Title,field_names)
            if fields[0]=="":
                fields=multenterbox("Message Should'nt be Empty",Title,field_names)
            else:
                apply(workID,choice_box)
                for i in cursor.execute('SELECT * FROM STATUS where workid=?',[workID]):
                    date1=i[3]
                    date2=i[4]
                for j in cursor.execute('SELECT workid from status'):
                    last_upw=j[0]
                start_datew=datetime(int(date1[-4:]),int(date1[3:5]),int(date1[0:2]))
                end_datew=datetime(int(date2[-4:]),int(date2[3:5]),int(date2[0:2]))
                Date_check=[]
                for x in cursor.execute('SELECT * FROM STATUS'):
                    if x[7]!=last_upw:
                        if x[8]==choice_box:
                            if x[9]!='Work adjustment Declined' and x[9]!='Work adjustment Revoked':
                                print(x)
                                k=datetime(int(x[3][-4:]),int(x[3][3:5]),int(x[3][0:2]))
                                d=datetime(int(x[4][-4:]),int(x[4][3:5]),int(x[4][0:2]))
                                Date_check.append(k)
                                Date_check.append(d)
                if len(Date_check)==0:
                    cursor.execute('INSERT INTO WORKASSIGN Values(?,?,?,?,?,?)',(workID,login,choice_box,fields[0],date1,date2))
                    conn.commit()
                    for e in cursor.execute('SELECT email_id from FACULTY where Faculty_Id=?',[choice_box]):
                        email1=e[0]
                    for n in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[login]):
                        name_a=n[0]
                    for date_e in cursor.execute('SELECT startdate,enddate from WORKASSIGN where work_Id=?',[workID]):
                        Date1e=date_e[0]
                        Date2e=date_e[1]
                    subject34=f'Work adjustment request from'+f' {name_a}'
                    body='\n\n\nThere is a '+subject34+' with work id '+str(workID)+' in dates '+'from '+Date1e+' to '+Date2e+' pending for your approval.'+'\n\n Login in to the Faculty leave Management System to approve or decline it.'
                    mail_sender(email1,subject34,body)
                    succeed_leave()
                else:
                    cond_date=any(datewqs>=start_datew and datewqs<=end_datew for datewqs in Date_check)
                    if cond_date==True:
                        workASSG_updated()
                        cursor.execute('DELETE FROM STATUS where workid=:r',{"r":workID})
                        conn.commit()
                        break
                    else:
                        cursor.execute('INSERT INTO WORKASSIGN Values(?,?,?,?,?,?)',(workID,login,choice_box,fields[0],date1,date2))
                        conn.commit()
                        for e in cursor.execute('SELECT email_id from FACULTY where Faculty_Id=?',[choice_box]):
                            email1=e[0]
                        for n in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[login]):
                            name_a=n[0]
                        for date_e in cursor.execute('SELECT startdate,enddate from WORKASSIGN where work_Id=?',[workID]):
                            Date1e=date_e[0]
                            Date2e=date_e[1]
                        subject34=f'Work adjustment request from'+f' {name_a}'
                        body='\n\n\nThere is a '+subject34+' with work id '+str(workID)+' in dates '+'from '+Date1e+' to '+Date2e+' pending for your approval.'+'\n\n Login in to the Faculty leave Management System to approve or decline it.'
                        mail_sender(email1,subject34,body)
                        succeed_leave()   
                        break
    else:
        choice_box=choicebox(message,Title,choices_list)
        if choice_box==None:
            choice_status()
        else:
            while True:
                message="Enter the work message"
                Title='Work assign'
                field_names=['Work Message']
                fields=multenterbox(message,Title,field_names)
                if fields[0]=="":
                    fields=multenterbox("Message Should'nt be Empty",Title,field_names)
                else:
                    apply(workID,choice_box)
                    for j in cursor.execute('SELECT workid from status'):
                        last_upw=j[0]
                    for i in cursor.execute('SELECT * FROM STATUS where workid=?',[workID]):
                        date1=i[3]
                        date2=i[4]
                    start_datew=datetime(int(date1[-4:]),int(date1[3:5]),int(date1[0:2]))
                    end_datew=datetime(int(date2[-4:]),int(date2[3:5]),int(date2[0:2]))
                    Date_check=[]
                    for x in cursor.execute('SELECT * FROM STATUS'):
                        if x[7]!=last_upw:
                            if x[8]==choice_box:
                                if x[9]!='Work adjustment Declined' and x[9]!='Work adjustment Revoked':
                                    print(x)
                                    k=datetime(int(x[3][-4:]),int(x[3][3:5]),int(x[3][0:2]))
                                    d=datetime(int(x[4][-4:]),int(x[4][3:5]),int(x[4][0:2]))
                                    Date_check.append(k)
                                    Date_check.append(d)
                    if len(Date_check)==0:
                        cursor.execute('INSERT INTO WORKASSIGN Values(?,?,?,?,?,?)',(workID,login,choice_box,fields[0],date1,date2))
                        conn.commit()
                        for e in cursor.execute('SELECT email_id from FACULTY where Faculty_Id=?',[choice_box]):
                            email1=e[0]
                        for n in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[login]):
                            name_a=n[0]
                        for date_e in cursor.execute('SELECT startdate,enddate from WORKASSIGN where work_Id=?',[workID]):
                            Date1e=date_e[0]
                            Date2e=date_e[1]
                        subject34=f'Work adjustment request from'+f' {name_a}'
                        body='\n\n\nThere is a '+subject34+' with work id '+str(workID)+' in dates '+'from '+Date1e+' to '+Date2e+' pending for your approval.'+'\n\n Login in to the Faculty leave Management System to approve or decline it.'
                        mail_sender(email1,subject34,body)
                        succeed_leave()
                        break
                    else:
                        cond_date=any(datewqs>=start_datew and datewqs<=end_datew for datewqs in Date_check)
                        if cond_date==True:
                            workASSG_updated()
                            cursor.execute('DELETE FROM STATUS where workid=:r',{"r":workID})
                            conn.commit()
                            break
                        else:
                            cursor.execute('INSERT INTO WORKASSIGN Values(?,?,?,?,?,?)',(workID,login,choice_box,fields[0],date1,date2))
                            conn.commit()
                            for e in cursor.execute('SELECT email_id from FACULTY where Faculty_Id=?',[choice_box]):
                                email1=e[0]
                            for n in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[login]):
                                name_a=n[0]
                            for date_e in cursor.execute('SELECT startdate,enddate from WORKASSIGN where work_Id=?',[workID]):
                                Date1e=date_e[0]
                                Date2e=date_e[1]
                            subject34='Work adjustment request from'+f' {name_a}'
                            body='\n\n\nThere is a '+subject34+' with work id '+str(workID)+' in dates '+'from '+Date1e+' to '+Date2e+' pending for your approval.'+'\n\n Login in to the Faculty leave Management System to approve or decline it.'
                            mail_sender(email1,subject34,body)
                            succeed_leave()
                            break


def  work_left(): 
    message="Select the operation"
    choices_list=["Accept","Decline","View"]
    Title="Work load Accept/Decline/View"
    choice_box=choicebox(message,Title,choices_list)
    if choice_box==None:
        choice_status()
    elif choice_box=="View":
        for i in cursor.execute("SELECT count(*) FROM WORKASSIGN where Faculty_Id=?",[login]):
            g=i[0]
        if g==0:
            casual_updatedawfddw()
        else:
            rootff=Toplevel()
            rootff.geometry('653x300')
            lst=[]
            for i in cursor.execute("SELECT Work_Id,assigned_by varchar2,Message,startdate,enddate varchar2 From WORKASSIGN where Faculty_Id=?",[login]):
                lst.append(i)
            table=ttk.Treeview(rootff,show='headings',height=300)
            style_table=ttk.Style()
            style_table.theme_use('clam')
            table["columns"]=("Work_Id","assigned_by","Message","startdate","enddate","status_workload",)
            table.column("Work_Id",width=50,minwidth=50,anchor=CENTER)
            table.column("assigned_by",width=75,minwidth=50,anchor=CENTER)
            table.column("Message",width=245,minwidth=65,anchor=CENTER)
            table.column("startdate",width=65,minwidth=65,anchor=CENTER)
            table.column("enddate",width=65,minwidth=65,anchor=CENTER)
            table.column("status_workload",width=153,minwidth=70,anchor=CENTER)
            #Heading
            table.heading("Work_Id",text="Work.Id",anchor=CENTER)
            table.heading("assigned_by",text="Assigned by",anchor=CENTER)
            table.heading("Message",text="Message",anchor=CENTER)
            table.heading("startdate",text="Start date",anchor=CENTER)
            table.heading("enddate",text="End date",anchor=CENTER)
            table.heading("status_workload",text="Work adjustment",anchor=CENTER)
            k=0
            while k<g:
                for i in cursor.execute("SELECT status_workload from STATUS where workid=?",[lst[k][0]]):
                    table.insert("",k,text="",values=(lst[k][0],lst[k][1],lst[k][2],lst[k][3],lst[k][4],i[0]))
                k=k+1
            table.pack()
    else:
        message="Enter work Id"
        Title="Workload Accept/Decline"
        field_names=['Work Id']
        fields=multenterbox(message,Title,field_names)
        while True:
            statuswid=None
            for i in cursor.execute("SELECT status_workload from STATUS where workid=?",[fields[0]]):
                statuswid=i[0]
            if fields[0]=="":
                fields=multenterbox("Invalid Work Id",Title,field_names)
            elif (fields[0],) in cursor.execute('select Work_Id from WORKASSIGN where Faculty_Id=?',[login]):
                fields=multenterbox("This Work Id doesn't belongs to you or Invalid WorkID",Title,field_names,fields)
            elif statuswid==None:
                fields=multenterbox("This Work Id doesn't exist",Title,field_names,fields)
            elif statuswid=="Work adjustment Accepted" or statuswid=="Work adjustment Declined":
                fields=multenterbox("This Work Id is already Accepted/Declined",Title,field_names,fields)
            else:
                if choice_box=="Accept":
                    cursor.execute("UPDATE STATUS SET status_workload=? where workid=?",("Work adjustment Accepted",fields[0]))
                    conn.commit()
                    for f in cursor.execute('SELECT Faculty_Id,assigned_by from WORKASSIGN where Work_Id=?',[fields[0]]):
                        facid=f[0]
                        facass=f[1]
                    for e in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[facid]):
                        name=e[0]
                    for n in cursor.execute('SELECT Name,email_id from FACULTY where Faculty_Id=?',[facass]):
                        name2=n[0]
                        email1=n[1]
                    for w in cursor.execute('SELECT Leave_Id from STATUS where workid=?',[fields[0]]):
                        wid=w[0]
                    for r in cursor.execute('SELECT email from ADMIN'):
                        eid=r[0]
                    print(eid)
                    subject="Work adjustment approved!"
                    body=f'{name2},\n\n\nYour work adjustment request with the work id {fields[0]} is approved by {name}'
                    mail_sender(email1,subject,body)
                    subject2=f'Leave request from {name2} with leave request id {wid}'
                    body2='\n\n\nThere is a '+subject2+', pending for your approval.\n\n Approve or decline by logging into the Faculty Leave Management System'
                    mail_sender(eid,subject2,body2)                  
                    work_accepted()
                    break
                else:
                    cursor.execute("UPDATE STATUS SET status_workload=? where workid=?",("Work adjustment Declined",fields[0]))
                    conn.commit()
                    for f in cursor.execute('SELECT Faculty_Id,assigned_by from WORKASSIGN where Work_Id=?',[fields[0]]):
                        facid=f[0]
                        facass=f[1]
                    for e in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[facid]):
                        name=e[0]
                    for n in cursor.execute('SELECT Name,email_id from FACULTY where Faculty_Id=?',[facass]):
                        name2=n[0]
                        email1=n[1]
                    subject="Work adjustment declined!"
                    body=f'{name2},\n\n\nYour work adjustment request with the work id {fields[0]} is declined by {name}'
                    mail_sender(email1,subject,body)
                    work_declined()
                    break
                        
def returnmonthsdays(start_date,end_date):
    day=int(start_date[0:2])
    month=int(start_date[3:5])
    year=int(start_date[-4:])
    day1=int(end_date[0:2])
    month1=int(end_date[3:5])
    year1=int(end_date[-4:])
    if ((year%4)==0 and (year%100)!=0)or (year%400)==0:
        leap={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        m1=leap[month]
        start_date2=date(year,month,m1)
    else:
        non_leap={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        m1=non_leap[month]
        start_date2=date(year,month,m1)
    start_dateN=date(year,month,day)
    end_dateN=date(year1,month1,day1)
    return month,(start_date2-start_dateN).days+1,month1,(end_dateN-start_date2).days

def casual_updated():
    root012=Toplevel()
    root012.geometry("440x85")
    msg23=Label(root012,text="Sick leaves cannot be more than 3 in a Month",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def casual_updated4():
    root012=Toplevel()
    root012.geometry("250x85")
    msg23=Label(root012,text="No CCLs are left to use",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def casual_updated4345():
    root012=Toplevel()
    root012.geometry("290x95")
    msg23=Label(root012,text="Casual leaves quota is over\n exceeds the limit",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def casual_updated4345M():
    root012=Toplevel()
    root012.geometry("295x95")
    msg23=Label(root012,text="Medical leaves quota is over or\n exceeds the limit ",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def casual_updatedaww():
    root012=Toplevel()
    root012.geometry("265x85")
    msg23=Label(root012,text="Work messages are empty",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def casual_updatedawfddw():
    root012=Toplevel()
    root012.geometry("265x85")
    msg23=Label(root012,text="No Work Assigned!",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def casual_updatedawwdf():
    root012=Toplevel()
    root012.geometry("250x85")
    msg23=Label(root012,text="All messages are cleared",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def Leave_record():
    root012=Toplevel()
    root012.geometry("250x85")
    msg23=Label(root012,text="No leave record found",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def revoke_record():
    root012=Toplevel()
    root012.geometry("250x85")
    msg23=Label(root012,text="No revoke request found",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def Leave_record2():
    root012=Toplevel()
    root012.geometry("490x95")
    msg23=Label(root012,text="No leave record found with work Adjustment Approval",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def medical_updated():
    root012=Toplevel()
    root012.geometry("480x90")
    msg23=Label(root012,text="Medical leaves cannot be more than 15 in a Month",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def assign_updated():
    root012=Toplevel()
    root012.geometry("480x90")
    msg23=Label(root012,text="No faculty registered or\nyou may have clciked Delete All",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def workASSG_updated():
    root012=Toplevel()
    root012.geometry("880x90")
    msg23=Label(root012,text="The given faculty Id for work load adjustment has already taken work adjustment or\n Some other work adjustment approval is pending from the given Faculty in your date range ",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def succeed_leave():
    root6=Toplevel()
    root6.geometry("170x80")
    msg=Label(root6,text="Leave Submitted",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root6,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg="white",justify=CENTER,command=root6.destroy)
    ok_btn.pack()
    
def succeed_l():
    root6=Toplevel()
    root6.geometry("170x80")
    msg=Label(root6,text="Request sent",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root6,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg="white",justify=CENTER,command=root6.destroy)
    ok_btn.pack()

def succeed_23():
    root6=Toplevel()
    root6.geometry("170x80")
    msg=Label(root6,text="Message sent!",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root6,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg="white",justify=CENTER,command=root6.destroy)
    ok_btn.pack()
    
def validate1(email):
    Exists = validate_email(email, verify=True)
    return Exists

def all_leave_status():
    for i in cursor.execute("SELECT COUNT(*) FROM STATUS where Faculty_Id=?",[login]):
        g=i[0]
    if g==0:
        Leave_record()
    else:
        all_facleave=Toplevel()
        all_facleave.title('All Leave Status')
        all_facleave.geometry("650x300")
        table=ttk.Treeview(all_facleave,show='headings',height=300)
        style_table=ttk.Style()
        style_table.theme_use('clam')
        table["columns"]=("Leave_Id","Leave","Date1","Date2","Days","work_facid","status_workload","status")
        table.column("Leave_Id",width=55,minwidth=50,anchor=CENTER)
        table.column("Leave",width=100,minwidth=65,anchor=CENTER)
        table.column("Date1",width=65,minwidth=65,anchor=CENTER)
        table.column("Date2",width=65,minwidth=65,anchor=CENTER)
        table.column("Days",width=40,minwidth=40,anchor=CENTER)
        table.column("work_facid",width=50,minwidth=50,anchor=CENTER)
        table.column("status_workload",width=155,minwidth=70,anchor=CENTER)
        table.column("status",width=120,minwidth=65,anchor=CENTER)
        #Heading
        table.heading("Leave_Id",text="Leave.Id",anchor=CENTER)
        table.heading("Leave",text="Leave",anchor=CENTER)
        table.heading("Date1",text="From",anchor=CENTER)
        table.heading("Date2",text="To",anchor=CENTER)
        table.heading("Days",text="Days",anchor=CENTER)
        table.heading("work_facid",text="Work.Id",anchor=CENTER)
        table.heading("status_workload",text="work adjustment",anchor=CENTER)
        table.heading("status",text="Admin approval",anchor=CENTER)
        i=0
        for row in cursor.execute("SELECT Leave_Id,Leave,Date1,Date2,Days,work_facid,status_workload,status from STATUS where Faculty_Id=?",[login]):
            table.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            i=i+1
        table.pack()

def mail_sender(email_to,subject,body):
    try:
        cursor.execute('SELECT EMAIL FROM ADMIN')
        email=cursor.fetchone()[0]
        cursor.execute('SELECT PASSCODE FROM ADMIN')
        passcode=cursor.fetchone()[0]
        Email_Address=email
        Email_Password=passcode
        msg=EmailMessage()
        msg['Subject']=subject
        msg['From']=Email_Address
        msg['To']=email_to
        msg.set_content(body)
        smtp1=smtplib.SMTP_SSL('smtp.gmail.com',465)
        smtp1.login(Email_Address,Email_Password)
        smtp1.send_message(msg)
        smtp1.quit()
    except Exception:
        mv_email_updated()
    
def updatedadminemid():
    Title='Update email address'
    Message='Enter new email id'
    fields_names=['Email Id:','Passcode']
    fields=multenterbox(Message,Title,fields_names)
    while True:
        if fields[0]=="":
            fields=multenterbox("Emaild should not be empty",Title,fields_names)
        elif fields[1]=="":
            fields=multenterbox("Passcode should not be empty",Title,fields_names)
        else:
            if (fields[0],) in cursor.execute('SELECT email_id from FACULTY'):
                fields=multenterbox("Email id already in use by faculty",Title,fields_names,fields)
            else:
                cursor.execute('UPDATE ADMIN SET email=?,passcode=?',[fields[0],fields[1]])
                conn.commit()
                email_updatedadmin()
                break
def status_cleared():
    root7=Toplevel()
    root7.geometry("175x80")
    msg=Label(root7,text="All Status Cleared",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root7,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg="white",justify=CENTER,command=root7.destroy)
    ok_btn.pack()
                
def choice_status():
    root7=Toplevel()
    root7.geometry("200x80")
    msg=Label(root7,text="Choice not selected!",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root7,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg="white",justify=CENTER,command=root7.destroy)
    ok_btn.pack()
    
def status_updated():
    root0=Toplevel()
    root0.geometry("165x80")
    msg=Label(root0,text="Status Updated",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()
    
def email_updatedadmin():
    root0=Toplevel()
    root0.geometry("175x80")
    msg=Label(root0,text="Email Id Updated",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()
    
def status_updatedAVAN():
    root0=Toplevel()
    root0.geometry("175x80")
    msg=Label(root0,text="Message Deleted!",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()

def status_stop():
    root0=Toplevel()
    root0.geometry("230x80")
    msg=Label(root0,text="Status Already Updated",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()

def statusfac_stop():
    root0=Toplevel()
    root0.geometry("230x80")
    msg=Label(root0,text="No Faculty Registered!",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()
    
def work_accepted():
    root0=Toplevel()
    root0.geometry("255x80")
    msg=Label(root0,text="Work Adjustment Accepted",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()
    
def work_declined():
    root0=Toplevel()
    root0.geometry("255x80")
    msg=Label(root0,text="Work Adjustment Declined",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()
    
def Faculty_Info():
    Faculty_Info=Toplevel()
    facul=[]
    for row in cursor.execute('SELECT Faculty_Id,Name,Gender,contact_no,email_id,Subject,sections_teaching,security_code From FACULTY where Faculty_ID=?',[login]):
        facul=row
    label1=Label(Faculty_Info,text="Faculty Id :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label2=Label(Faculty_Info,text=facul[0],fg="blue",font=('calibre',16),justify=LEFT)
    label3=Label(Faculty_Info,text="Name :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label4=Label(Faculty_Info,text=facul[1],fg="blue",font=('calibre',16),justify=LEFT)
    label5=Label(Faculty_Info,text="Gender :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label6=Label(Faculty_Info,text=facul[2],fg="blue",font=('calibre',16),justify=LEFT)
    label7=Label(Faculty_Info,text="contact no :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label8=Label(Faculty_Info,text=facul[3],fg="blue",font=('calibre',16),justify=LEFT)
    label9=Label(Faculty_Info,text="Email Id:",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label10=Label(Faculty_Info,text=facul[4],fg="blue",font=('calibre',16),justify=LEFT)
    label11=Label(Faculty_Info,text="Subject Teaching :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label12=Label(Faculty_Info,text=facul[5],fg="blue",font=('calibre',16),justify=LEFT)
    label13=Label(Faculty_Info,text="Sections Teaching :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label14=Label(Faculty_Info,text=facul[6],fg="blue",font=('calibre',16),justify=LEFT)
    label15=Label(Faculty_Info,text="Security Code :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
    label16=Label(Faculty_Info,text=facul[7],fg="red",font=('calibre',16),justify=LEFT)
    label1.grid(row=0,column=0)
    label2.grid(row=0,column=1)
    label3.grid(row=1,column=0)
    label4.grid(row=1,column=1)
    label5.grid(row=2,column=0)
    label6.grid(row=2,column=1)
    label7.grid(row=3,column=0)
    label8.grid(row=3,column=1)
    label9.grid(row=4,column=0)
    label10.grid(row=4,column=1)
    label11.grid(row=5,column=0)
    label12.grid(row=5,column=1)
    label13.grid(row=6,column=0)
    label14.grid(row=6,column=1)
    label15.grid(row=7,column=0)
    label16.grid(row=7,column=1)
    
def edit_Faculty():
    lst=[]
    for row in cursor.execute("select Faculty_Id,Name,Gender,contact_no,email_id,Subject,sections_teaching,security_code,Password from Faculty where Faculty_Id=?",[login]):
        lst.append(row[0])
        lst.append(row[1])
        lst.append(row[2])
        lst.append(row[3])
        lst.append(row[4])
        lst.append(row[5])
        lst.append(row[6])
        lst.append(row[7])
        lst.append(row[8])
    for row in cursor.execute("SELECT security_code from FACULTY where Faculty_Id=?",[login]):
        e1=row[0]
    for row in cursor.execute("SELECT contact_no from FACULTY where Faculty_Id=?",[login]):
        e2=row[0]
    for row in cursor.execute("SELECT email_id from FACULTY where Faculty_Id=?",[login]):
        e3=row[0]
    message="Edit Your Details"
    Title="Update Your required Fields"
    editfields=["Faculty_ID","Name","Gender","contact_no","Email Id","Subject teaching","Sections teaching","Security code","Password"]
    fields1=multpasswordbox(Title,message,editfields,lst)
    while True:
        faculmsg=""
        for i in range(len(fields1)):
            if fields1[i]=="":
                faculmsg=faculmsg+('"%s" is a required filed\n\n'%editfields[i])
        if faculmsg=="":
            break
        fields1=multpasswordbox(faculmsg,message,editfields,fields1)
    while True:
        d=validate1(fields1[4])
        if fields1[2].upper()!="M" and fields1[2].upper()!="F":
            fields1=multpasswordbox("Only M or F accepted in Gender",message,editfields,fields1)
        elif (fields1[0],) in cursor.execute("SELECT Faculty_Id From FACULTY where NOT Faculty_Id=?",[login]):
            fields1=multpasswordbox("The Faculty ID is already in use\nuse other ID",message,editfields,fields1)
        elif len(fields1[3])<10 or len(fields1[3])>10:
            fields1=multpasswordbox("Invalid mobile no provided",message,editfields,fields1)
        elif (fields1[3],) in cursor.execute("Select contact_no from FACULTY where NOT contact_no=:r1",{'r1':e2}):
            fields1=multpasswordbox("Mobile no is already in use by others",message,editfields,fields1)
        elif (fields1[4],) in cursor.execute("Select email_id from FACULTY where NOT email_id=:r1",{'r1':e3}) or (fields1[4],) in cursor.execute('SELECT email from ADMIN'):
            fields1=multpasswordbox("Email ID is already in use by others",message,editfields,fields1)
        elif d==None or d==False:
            fields1=multpasswordbox("Please provide a valid email id or\ncheck internet connection",message,editfields,fields1)
        elif (fields1[7],) in cursor.execute("Select security_code from FACULTY where NOT security_code=:r1",{'r1':e1}) or (fields1[7],) in cursor.execute("Select Security_code from ADMIN"):
            fields1=multpasswordbox("The Security code is weak\nInvalid-use other code",message,editfields,fields1)
        else:     
            cursor.execute('update FACULTY set Faculty_Id=?,Name=?,Gender=?,contact_no=?,email_id=?,Subject=?,sections_teaching=?,security_code=?,Password=? where Faculty_Id=?',((fields1[0]),(fields1[1]),(fields1[2]).upper(),(fields1[3]),(fields1[4]),(fields1[5]),(fields1[6]),(fields1[7]),(fields1[8]),login))
            cursor.execute('UPDATE BALANCE SET Faculty_Id=? where Faculty_Id=?',((fields1[0]),login))
            cursor.execute('UPDATE STATUS SET Faculty_Id=? where Faculty_Id=?',((fields1[0]),login))
            cursor.execute('UPDATE Revoke SET Faculty_Id=? where Faculty_Id=?',((fields1[0]),login))
            cursor.execute("UPDATE Month SET Faculty_Id=? where Faculty_Id=?",((fields1[0]),login))
            cursor.execute("UPDATE Month1 SET Faculty_Id=? where Faculty_Id=?",((fields1[0]),login))
            cursor.execute("UPDATE WORKASSIGN SET Faculty_Id=? where Faculty_Id=?",((fields1[0]),login))
            conn.commit()
            messagebox.showinfo("Edit Details","Details Updated\n Log in again")
            break

def apply(workID,choice_box):
    message="Fill the following details"
    message1='Day is out of range for month or Month is out of range\n Invalid Date format'    
    Title="Leave Apply"
    fields=[]
    fields_names=['Faculty Id','From','To','days']
    List_default=[login,"dd/mm/yyyy","dd/mm/yyyy","No of Days"]
    fields=multenterbox(message,Title,fields_names,List_default)
    while True:
        if fields is None:
            break
        err_msg=""
        for i in range(len(fields)):
            if fields[i]=="":
                err_msg=err_msg+("'%s' is a required field\n\n"%fields_names[i])
        if err_msg=="":
            break
        fields=multenterbox(err_msg,Title,fields_names,fields)
    while True:
        if (fields[0],) not in cursor.execute("SELECT Faculty_Id From Faculty"):
            fields=multenterbox("Invalid Id",Title,fields_names,fields)
        if len(fields[1])!=10 or len(fields[2])!=10:
            fields=multenterbox("Invalid Date Format\nPlease enter date in dd/mm/yyyy format",Title,fields_names,fields)
        elif fields[1]=="dd/mm/yyyy" or fields[2]=="dd/mm/yyyy":
            fields=multenterbox("Invalid Date Format\nPlease enter exact date",Title,fields_names,fields)              
        elif len(fields[3])==0:
            fields=multenterbox("Days should not be empty",Title,fields_names,fields)
        elif len(fields[3])>=3:
            fields=multenterbox("Invalid input for Days\nonly two digits are allowed",Title,fields_names,fields)
        elif ((fields[1][0] not in "0123456789") or (fields[1][1] not in "0123456789")) or ((fields[1][3] not in "0123456789") or (fields[1][4] not in "0123456789")) or ((fields[1][6] not in "0123456789") or (fields[1][7] not in "0123456789")) or ((fields[1][8] not in "0123456789") or (fields[1][9] not in "0123456789")) or ((fields[1][2] not in "/") or (fields[1][5] not in "/")):
            fields=multenterbox("Invalid Date Format\nPlease enter date in dd/mm/yyyy format",Title,fields_names,fields)
        elif ((fields[2][0] not in "0123456789") or (fields[2][1] not in "0123456789")) or ((fields[2][3] not in "0123456789") or (fields[2][4] not in "0123456789")) or ((fields[2][6] not in "0123456789") or (fields[2][7] not in "0123456789")) or ((fields[2][8] not in "0123456789") or (fields[2][9] not in "0123456789")) or ((fields[2][2] not in "/") or (fields[2][5] not in "/")):
            fields=multenterbox("Invalid Date Format\nPlease enter date in dd/mm/yyyy format",Title,fields_names,fields)
        elif len(fields[3])==1:
            if fields[3] not in "0123456789":
                fields=multenterbox("Invalid input for Days\nonly integers are allowed in Days",Title,fields_names,fields)
            elif fields[3]=="0":
                fields=multenterbox("Invalid input for Days\nDays should not be 0",Title,fields_names,fields)
            else:
                day=int(fields[1][0:2])
                month=int(fields[1][3:5])
                year=int(fields[1][-4:])
                day1=int(fields[2][0:2])
                month1=int(fields[2][3:5])
                year1=int(fields[2][-4:])
                today=date.today()
                try:
                    start_date=date(year,month,day)
                except ValueError:
                    start_date=None
                try:
                    end_date=date(year1,month1,day1)
                except ValueError:
                    end_date=None
                while True:
                    if start_date==None or end_date==None:
                        fields=multenterbox(message1,Title,fields_names,fields)
                        if len(fields[3])==0:
                            message1="Days should not be empty"
                        elif len(fields[3])>=3:
                            message1="Invalid input for Days-only two digits are allowed\n or Days is out of range for month or month is out of range"
                        elif len(fields[1])!=10 or len(fields[2])!=10:
                            message1="Invalid Date Format-Please enter date in dd/mm/yyyy format\n or Days is out of range for month or month is out of range"
                        elif ((fields[1][0] not in "0123456789") or (fields[1][1] not in "0123456789")) or ((fields[1][3] not in "0123456789") or (fields[1][4] not in "0123456789")) or ((fields[1][6] not in "0123456789") or (fields[1][7] not in "0123456789")) or ((fields[1][8] not in "0123456789") or (fields[1][9] not in "0123456789")) or ((fields[1][2] not in "/") or (fields[1][5] not in "/")):
                            message1="Invalid Date Format-Please enter date in dd/mm/yyyy format\n or Days is out of range for month or month is out of range"
                        elif ((fields[2][0] not in "0123456789") or (fields[2][1] not in "0123456789")) or ((fields[2][3] not in "0123456789") or (fields[2][4] not in "0123456789")) or ((fields[2][6] not in "0123456789") or (fields[2][7] not in "0123456789")) or ((fields[2][8] not in "0123456789") or (fields[2][9] not in "0123456789")) or ((fields[2][2] not in "/") or (fields[2][5] not in "/")):
                            message1="Invalid Date Format-Please enter date in dd/mm/yyyy format\n or Days is out of range for month or month is out of range"
                        elif len(fields[3])==1:
                            if fields[3] not in "0123456789":
                                message1="Invalid input for Days-only integers are allowed in Days\n or Days is out of range for month or month is out of range"
                            elif fields[3]=="0":
                                message1="Invalid input for Days-Days should not be 0\n or Days is out of range for month or month is out of range"
                            else:
                                day=int(fields[1][0:2])
                                month=int(fields[1][3:5])
                                year=int(fields[1][-4:])
                                day1=int(fields[2][0:2])
                                month1=int(fields[2][3:5])
                                year1=int(fields[2][-4:])
                                today=date.today()
                                try:
                                    start_date=date(year,month,day)
                                except ValueError:
                                    start_date=None
                                try:
                                    end_date=date(year1,month1,day1)
                                except ValueError:
                                    end_date=None 
                        elif len(fields[3])==2:
                            if fields[3][0] not in "0123456789" or fields[3][1] not in "0123456789":
                                message1="Invalid input for Days-only integers are allowed in Days\n or Days is out of range for month or month is out of range"
                            elif fields[3]=="00":
                                message1="Invalid input for Days-Days should not be 0\n or Days is out of range for month or month is out of range"
                            else:
                                day=int(fields[1][0:2])
                                month=int(fields[1][3:5])
                                year=int(fields[1][-4:])
                                day1=int(fields[2][0:2])
                                month1=int(fields[2][3:5])
                                year1=int(fields[2][-4:])
                                today=date.today()
                                try:
                                    start_date=date(year,month,day)
                                except ValueError:
                                    start_date=None
                                try:
                                    end_date=date(year1,month1,day1)
                                except ValueError:
                                    end_date=None
                    else:
                        break
                diff1=(start_date-today).days
                diff2=(end_date-today).days
                diff3=(end_date-start_date).days
                if diff1>=0 and (diff2>=0 and diff3>=0):
                    if diff3+1==fields[3]:
                        break
                    else:
                        fields[3]=diff3+1
                        break
                else:
                    fields=multenterbox("Invalid Date\nDate should not be any previous date\nor start date is far than end date",Title,fields_names,fields)
                
        elif len(fields[3])==2:
            if fields[3][0] not in "0123456789" or fields[3][1] not in "0123456789":
                fields=multenterbox("Invalid input for Days\nonly integers are allowed in Days",Title,fields_names,fields)
            elif fields[3]=="00":
                fields=multenterbox("Invalid input for Days\nDays should not be 0",Title,fields_names,fields)
            else:
                day=int(fields[1][0:2])
                month=int(fields[1][3:5])
                year=int(fields[1][-4:])
                day1=int(fields[2][0:2])
                month1=int(fields[2][3:5])
                year1=int(fields[2][-4:])
                today=date.today()
                try:
                    start_date=date(year,month,day)
                except ValueError:
                    start_date=None
                try:
                    end_date=date(year1,month1,day1)
                except ValueError:
                    end_date=None
                while True:
                    if start_date==None or end_date==None:
                        fields=multenterbox(message1,Title,fields_names,fields)
                        if len(fields[3])==0:
                            message1="Days should not be empty\n or Days is out of range for month or month is out of range"
                        elif len(fields[3])>=3:
                            message1="Invalid input for Days-only two digits are allowed\n or Days is out of range for month or month is out of range"
                        elif len(fields[1])!=10 or len(fields[2])!=10:
                            message1="Invalid Date Format\nPlease enter date in dd/mm/yyyy format\n or Days is out of range for month or month is out of range"
                        elif ((fields[1][0] not in "0123456789") or (fields[1][1] not in "0123456789")) or ((fields[1][3] not in "0123456789") or (fields[1][4] not in "0123456789")) or ((fields[1][6] not in "0123456789") or (fields[1][7] not in "0123456789")) or ((fields[1][8] not in "0123456789") or (fields[1][9] not in "0123456789")) or ((fields[1][2] not in "/") or (fields[1][5] not in "/")):
                            message1="Invalid Date Format\nPlease enter date in dd/mm/yyyy format\n or Days is out of range for month or month is out of range"
                        elif ((fields[2][0] not in "0123456789") or (fields[2][1] not in "0123456789")) or ((fields[2][3] not in "0123456789") or (fields[2][4] not in "0123456789")) or ((fields[2][6] not in "0123456789") or (fields[2][7] not in "0123456789")) or ((fields[2][8] not in "0123456789") or (fields[2][9] not in "0123456789")) or ((fields[2][2] not in "/") or (fields[2][5] not in "/")):
                            message1="Invalid Date Format\nPlease enter date in dd/mm/yyyy format\n or Days is out of range for month or month is out of range"
                        elif len(fields[3])==1:
                            print('case1 of 1')
                            if fields[3] not in "0123456789":
                                message1="Invalid input for Days-only integers are allowed in Days\n or Days is out of range for month or month is out of range"
                            elif fields[3]=="0":
                                message1="Invalid input for Days-Days should not be 0\n or Days is out of range for month or month is out of range"
                            else:
                                day=int(fields[1][0:2])
                                month=int(fields[1][3:5])
                                year=int(fields[1][-4:])
                                day1=int(fields[2][0:2])
                                month1=int(fields[2][3:5])
                                year1=int(fields[2][-4:])
                                today=date.today()
                                try:
                                    start_date=date(year,month,day)
                                except ValueError:
                                    start_date=None
                                try:
                                    end_date=date(year1,month1,day1)
                                except ValueError:
                                    end_date=None 
                        elif len(fields[3])==2:
                            if fields[3][0] not in "0123456789" or fields[3][1] not in "0123456789":
                                message1="Invalid input for Days-only integers are allowed in Days\n or Days is out of range for month or month is out of range"
                            elif fields[3]=="00":
                                message1="Invalid input for Days-Days should not be 0\n or Days is out of range for month or month is out of range"
                            else:
                                day=int(fields[1][0:2])
                                month=int(fields[1][3:5])
                                year=int(fields[1][-4:])
                                day1=int(fields[2][0:2])
                                month1=int(fields[2][3:5])
                                year1=int(fields[2][-4:])
                                today=date.today()
                                try:
                                    start_date=date(year,month,day)
                                except ValueError:
                                    start_date=None
                                try:
                                    end_date=date(year1,month1,day1)
                                except ValueError:
                                    end_date=None
                    else:
                        break
                diff1=(start_date-today).days
                diff2=(end_date-today).days
                diff3=(end_date-start_date).days
                if diff1>=0 and (diff2>=0 and diff3>=0):
                    if diff3+1==fields[3]:
                        break
                    else:
                        fields[3]=diff3+1
                        break
                else:
                    fields=multenterbox("Invalid Date\nDate should not be any previous date\nor start date is far than end date",Title,fields_names,fields)  
                    
    while True:
        if (fields[0],) in cursor.execute("SELECT Faculty_Id From Faculty"):
            for i in cursor.execute("SELECT Gender From Faculty where Faculty_Id=?",[login]):
                gender=i[0]
            if gender=='M':
                message='Select Type of leave'
                Title='Type of leave'
                choices=["Casual leave", "Medical leave", "Loss of pay","CCL"]
                leaveid = random.randint(1, 10000)
                choice_apply=choicebox(message,Title,choices)
                if choice_apply==None:
                    choice_status()
                    break
                elif choice_apply=="Casual leave":
                    for i in cursor.execute("SELECT Casual_Leave from BALANCE where Faculty_Id=?",[login]):
                        balancec=i[0]
                    if (balancec-int(fields[3]))<0:
                        casual_updated4345()
                        break
                    today=date.today().strftime("%d/%m/%Y")
                    month=int(today[3:5])
                    s=monthretrieve(month,fields[0])
                    if month==month1:
                        d=fields[3]
                    if month!=month1:
                        if int(fields[1][3:5])==int(fields[2][3:5]):
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=fields[3]
                        else:
                            g=returnmonthsdays(fields[1],fields[2])
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=g[1]
                            d1=g[3]
                            if s+d1>3:
                               casual_updated()
                               break
                    if s+d>3:
                        casual_updated()
                        break
                    else:
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(10000, 20000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                elif choice_apply=="Medical leave":
                    for i in cursor.execute("SELECT Medical_Leave from BALANCE where Faculty_Id=?",[login]):
                        balancecm=i[0]
                    if (balancecm-int(fields[3]))<0:
                        casual_updated4345M()
                        break
                    today=date.today().strftime("%d/%m/%Y")
                    month=int(today[3:5])
                    s=monthretrieve1(month,fields[0])
                    if month==month1:
                        d=fields[3]
                    if month!=month1:
                        if int(fields[1][3:5])==int(fields[2][3:5]):
                            d=fields[3]
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                        else:
                            g=returnmonthsdays(fields[1],fields[2])
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=g[1]
                            d1=g[3]
                            if s+d1>15:
                               medical_updated()
                    if s+d>15:
                        medical_updated()
                        break
                    else:
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(1, 10000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                elif choice_apply=="CCL":
                    message="Select choice"
                    Title="Compensated Casual Leave"
                    choice_updates=["ADD CCL","USE CCL"]
                    choice_apply1=choicebox(message,Title,choice_updates)
                    for row6 in cursor.execute("SELECT CCL From BALANCE where Faculty_Id=:r1",{"r1":fields[0]}):
                        balance5=row6[0]
                    if choice_apply1==None:
                        choice_status()
                        break
                    elif choice_apply1=="ADD CCL":
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(10000, 20000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply1,fields[1],fields[2],fields[3],"Request to add CCL","NA","NA","Work adjustment Accepted"))
                            conn.commit()
                            succeed_l()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply1,fields[1],fields[2],fields[3],"Request to add CCL","NA","NA","Work adjustment Accepted"))
                            conn.commit()
                            succeed_l()
                            break
                    else:
                        if (balance5-int(fields[3]))<0:
                            casual_updated4()
                            break
                        else:
                            if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                                leaveid2=random.randint(10000, 20000)
                                cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply1,fields[1],fields[2],fields[3],"Request to use CCL",workID,choice_box,"Work adjustment Pending"))
                                conn.commit()
                                break
                            else:
                                cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply1,fields[1],fields[2],fields[3],"Request to use CCL",workID,choice_box,"Work adjustment Pending"))
                                conn.commit()
                                break
                else:
                    cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                    conn.commit()
                    break
            else:
                message='Select Type of leave'
                Title='Type of leave'
                choices=["Casual leave", "Medical leave", "Loss of pay","Maternity leave","CCL"]
                leaveid = random.randint(1, 1000)
                month=int(fields[1][3:5])
                month1=int(fields[2][3:5])
                choice_apply=choicebox(message,Title,choices)
                for row6 in cursor.execute("SELECT CCL From BALANCE where Faculty_Id=:r1",{"r1":fields[0]}):
                    balance5=row6[0]
                if choice_apply==None:
                    choice_status()
                    break
                elif choice_apply=="Casual leave":
                    for i in cursor.execute("SELECT Casual_Leave from BALANCE where Faculty_Id=?",[login]):
                        balancec=i[0]
                    if (balancec-int(fields[3]))<0:
                        casual_updated4345()
                        break
                    today=date.today().strftime("%d/%m/%Y")
                    month=int(today[3:5])
                    s=monthretrieve(month,fields[0])
                    if month==month1:
                        d=fields[3]
                    if month!=month1:
                        if int(fields[1][3:5])==int(fields[2][3:5]):
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=fields[3]
                        else:
                            g=returnmonthsdays(fields[1],fields[2])
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=g[1]
                            d1=g[3]
                            if s+d1>3:
                               casual_updated() 
                               
                    if s+d>3:
                        casual_updated()
                        break
                    else:
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(10000, 20000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                elif choice_apply=="Medical leave":
                    for i in cursor.execute("SELECT Medical_Leave from BALANCE where Faculty_Id=?",[login]):
                        balancecm=i[0]
                    if (balancecm-int(fields[3]))<0:
                        casual_updated4345M()
                        break
                    today=date.today().strftime("%d/%m/%Y")
                    month=int(today[3:5])
                    s=monthretrieve1(month,fields[0])
                    if month==month1:
                        d=fields[3]
                    if month!=month1:
                        if int(fields[1][3:5])==int(fields[2][3:5]):
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=fields[3]
                        else:
                            g=returnmonthsdays(fields[1],fields[2])
                            month=int(fields[1][3:5])
                            s=monthretrieve(month,fields[0])
                            d=g[1]
                            d1=g[3]
                            if s+d1>15:
                               medical_updated()
                    if s+d>15:
                        medical_updated()
                        break
                    else:
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(10000, 20000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                elif choice_apply=="CCL":
                    message="Select choice"
                    Title="Compensated Casual Leave"
                    choice_updates=["ADD CCL","USE CCL"]
                    choice_apply1=choicebox(message,Title,choice_updates)
                    if choice_apply1==None:
                        choice_status()
                        break
                    elif choice_apply1=="ADD CCL":
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(10000, 20000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply1,fields[1],fields[2],fields[3],"Request to add CCL","NA","NA","Work adjustment Accepted"))
                            conn.commit()
                            succeed_l()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply1,fields[1],fields[2],fields[3],"Request to add CCL","NA","NA","Work adjustment Accepted"))
                            conn.commit()
                            succeed_l()
                            break
                    else:
                        if (balance5-int(fields[3]))<0:
                            casual_updated4()
                            break
                        if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                            leaveid2=random.randint(10000, 20000)
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply1,fields[1],fields[2],fields[3],"Request to use CCL",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                        else:
                            cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply1,fields[1],fields[2],fields[3],"Request to use CCL",workID,choice_box,"Work adjustment Pending"))
                            conn.commit()
                            break
                
                else:
                    if (leaveid,) in cursor.execute("SELECT Leave_Id from STATUS"):
                        leaveid2=random.randint(10000, 20000)
                        cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid2,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                        conn.commit()
                        break
                    else:
                        cursor.execute('INSERT INTO STATUS(Faculty_Id,Leave_Id,Leave,Date1,Date2,Days,status,workid,work_facid,status_workload) VALUES(?,?,?,?,?,?,?,?,?,?)',(fields[0],leaveid,choice_apply,fields[1],fields[2],fields[3],"Pending",workID,choice_box,"Work adjustment Pending"))
                        conn.commit()
                        break
                        
        else:
            fields=multenterbox("Invalid Id",Title,fields_names,fields)

def Revoke_Approve():
    message="Enter Revoke request Id"
    Title="Approve Revoke"
    input_list=["Revoke request Id"]
    App_revoke=multenterbox(message,Title,input_list)
    while True:
        if (int(App_revoke[0]),) in cursor.execute("SELECT Leave_Id FROM Revoke"):
            for statusm in cursor.execute("SELECT status from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                status=statusm[0]
            if status=="Approved" or status=="Denied":
                status_stop()
                break
            else:
                for i in cursor.execute('SELECT workid from STATUS where Leave_Id=:r1',{"r1":int(App_revoke[0])}):
                    workIDr=i[0]
                for row in cursor.execute("SELECT Faculty_Id from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                    Id1=row[0]
                for row2 in cursor.execute("SELECT Casual_Leave From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                    balance1=row2[0]
                for row3 in cursor.execute("SELECT Medical_Leave From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                    balance2=row3[0]
                for row4 in cursor.execute("SELECT maternity_leave From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                    balance3=row4[0]
                for row5 in cursor.execute("SELECT Loss_of_pay From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                    balance4=row5[0]
                for row6 in cursor.execute("SELECT CCL From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                    balance5=row6[0]
                for i in cursor.execute("SELECT workid from STATUS where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                    workIdr=i[0]
                for d in cursor.execute('SELECT Name,email_id from FACULTY where Faculty_Id=?',[Id1]):
                    n=d[0]
                    eid=d[1]
                message="Select Approve/Deny"
                title="Approve/Deny Revoke Id"
                input_list=["Approved","Denied"]
                CHOICE_R=choicebox(message,title,input_list)
                if CHOICE_R=="None":
                    choice_status()
                    break
                if CHOICE_R=="Denied":
                    cursor.execute("UPDATE Revoke SET status=? where Leave_Id=?",(CHOICE_R,(int(App_revoke[0]))))
                    conn.commit()
                    subject=f'Revoke leave request with id {App_revoke[0]} is Declined'
                    body=f'{n},\n\n\n Your {subject}'
                    mail_sender(eid,subject,body)
                    status_updated()
                    break
                cursor.execute("UPDATE Revoke SET status=? where Leave_Id=?",(CHOICE_R,(int(App_revoke[0]))))
                conn.commit()
                subject=f'Revoke leave request with id {App_revoke[0]} is approved'
                body=f'{n},\n\n\n Your {subject}'
                mail_sender(eid,subject,body)
                for row in cursor.execute("SELECT Date1 from Revoke WHERE Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                    day=row[0]
                for row in cursor.execute("SELECT Date2 from Revoke WHERE Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                    day1=row[0]
                dd=int(day[0:2])
                mm=int(day[3:5])
                yy=int(day[-4:])
                dd1=int(day1[0:2])
                mm1=int(day1[3:5])
                yy1=int(day1[-4:])
                today=date.today()
                start_date=date(yy,mm,dd)
                End_date=date(yy1,mm1,dd1)
                diff=(End_date-today).days
                diff1=(start_date-today).days
                diffe=(End_date-start_date).days
                if diff1==0:
                    print('case11')
                    for Lea1 in cursor.execute("SELECT Leave from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                        type0=Lea1[0]
                    if type0=="Casual leave":
                        cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+diffe+1),Id1))
                        for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            ava=start[0]
                            de1=int(ava[8:])
                            m1=int(ava[5:7])
                            ye1=int(ava[0:4])
                        for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            esw=end[0]
                            de2=int(esw[0:2])
                            m2=int(esw[3:5])
                            ye2=int(esw[-4:])
                            s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                        for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                            bg=i
                        dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                        if m1==m2:
                            if m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                            elif m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                            elif m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                            elif m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                            elif m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                            elif m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                            elif m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                            elif m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                            elif m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                            elif m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                            elif m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                            elif m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                        else:
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            start_dc=ava
                            end_dc=s
                            f=returnmonthsdays(start_dc,end_dc)
                            start_m1=f[0]
                            start_daysre=f[1]
                            end_m1=f[2]
                            end_daysre=f[3]
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            if start_m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                            elif start_m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                            elif start_m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                            elif start_m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                            elif start_m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                            elif start_m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                            elif start_m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                            elif start_m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                            elif start_m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                            elif start_m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                            elif start_m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                            elif start_m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                            if end_m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                            elif end_m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                            elif end_m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                            elif end_m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                            elif end_m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                            elif end_m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                            elif end_m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                            elif end_m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                            elif end_m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                            elif end_m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                            elif end_m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                            elif end_m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                    elif type0=="Loss of pay":
                        cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+diffe+1),Id1))
                    elif type0=="USE CCL":
                        cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+diffe+1),Id1))
                    elif type0=="Medical leave":
                        cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+diffe+1),Id1))
                        for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            ava=start[0]
                            de1=int(ava[8:])
                            m1=int(ava[5:7])
                            ye1=int(ava[0:4])
                        for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            esw=end[0]
                            de2=int(esw[0:2])
                            m2=int(esw[3:5])
                            ye2=int(esw[-4:])
                            s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                        for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                            bg=i
                        dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                        if m1==m2:
                            if m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                            elif m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                            elif m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                            elif m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                            elif m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                            elif m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                            elif m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                            elif m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                            elif m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                            elif m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                            elif m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                            elif m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                        else:
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            start_dc=ava
                            end_dc=s
                            f=returnmonthsdays1(start_dc,end_dc)
                            start_m1=f[0]
                            start_daysre=f[1]
                            end_m1=f[2]
                            end_daysre=f[3]
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            if start_m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                            elif start_m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                            elif start_m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                            elif start_m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                            elif start_m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                            elif start_m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                            elif start_m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                            elif start_m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                            elif start_m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                            elif start_m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                            elif start_m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                            elif start_m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                            if end_m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                            elif end_m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                            elif end_m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                            elif end_m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                            elif end_m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                            elif end_m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                            elif end_m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                            elif end_m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                            elif end_m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                            elif end_m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                            elif end_m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                            elif end_m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                    elif type0=="Maternity leave": 
                        cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+diffe+1),Id1))
                    cursor.execute("UPDATE STATUS set status='Leave Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                    cursor.execute("UPDATE STATUS set status_workload='Work adjustment Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                    cursor.execute('DELETE FROM WORKASSIGN where Work_Id=:r1',{"r1":workIdr})
                    conn.commit()
                    status_updated()
                    break
                elif diff==0:
                    print('case12')
                    for Lea1 in cursor.execute("SELECT Leave from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                        type0=Lea1[0]
                    if type0=="Casual leave":
                        cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+1),Id1))
                        for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            ava=start[0]
                            de1=int(ava[8:])
                            m1=int(ava[5:7])
                            ye1=int(ava[0:4])
                        for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            esw=end[0]
                            de2=int(esw[0:2])
                            m2=int(esw[3:5])
                            ye2=int(esw[-4:])
                            s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                        for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                            bg=i
                        dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                        if m1==m2:
                            if m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                            elif m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                            elif m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                            elif m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                            elif m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                            elif m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                            elif m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                            elif m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                            elif m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                            elif m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                            elif m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                            elif m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                        else:
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            start_dc=ava
                            end_dc=s
                            f=returnmonthsdays(start_dc,end_dc)
                            start_m1=f[0]
                            start_daysre=f[1]
                            end_m1=f[2]
                            end_daysre=f[3]
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            if start_m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                            elif start_m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                            elif start_m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                            elif start_m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                            elif start_m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                            elif start_m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                            elif start_m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                            elif start_m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                            elif start_m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                            elif start_m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                            elif start_m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                            elif start_m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                            if end_m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                            elif end_m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                            elif end_m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                            elif end_m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                            elif end_m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                            elif end_m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                            elif end_m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                            elif end_m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                            elif end_m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                            elif end_m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                            elif end_m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                            elif end_m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                    elif type0=="Loss of pay":
                        cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+1),Id1))
                    elif type0=="USE CCL":
                        cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+1),Id1))
                    elif type0=="Medical leave":
                        cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+1),Id1))
                        conn.commit()
                        for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            ava=start[0]
                            de1=int(ava[8:])
                            m1=int(ava[5:7])
                            ye1=int(ava[0:4])
                        for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            esw=end[0]
                            de2=int(esw[0:2])
                            m2=int(esw[3:5])
                            ye2=int(esw[-4:])
                            s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                        for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                            bg=i
                        dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                        if m1==m2:
                            if m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                            elif m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                            elif m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                            elif m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                            elif m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                            elif m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                            elif m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                            elif m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                            elif m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                            elif m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                            elif m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                            elif m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                        else:
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            start_dc=ava
                            end_dc=s
                            f=returnmonthsdays1(start_dc,end_dc)
                            start_m1=f[0]
                            start_daysre=f[1]
                            end_m1=f[2]
                            end_daysre=f[3]
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            if start_m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                            elif start_m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                            elif start_m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                            elif start_m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                            elif start_m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                            elif start_m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                            elif start_m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                            elif start_m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                            elif start_m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                            elif start_m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                            elif start_m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                            elif start_m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                            if end_m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                            elif end_m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                            elif end_m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                            elif end_m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                            elif end_m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                            elif end_m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                            elif end_m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                            elif end_m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                            elif end_m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                            elif end_m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                            elif end_m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                            elif end_m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                    elif type0=="Maternity leave":
                        cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+1),Id1))
                    cursor.execute("UPDATE STATUS set status='Leave partially Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                    cursor.execute("UPDATE STATUS set status_workload='Work adjustment Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                    conn.commit()
                    status_updated()
                    break
               
                elif diff>0:
                    print('case13')
                    for Lea1 in cursor.execute("SELECT Leave from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                        type0=Lea1[0]
                        choices=["Casual leave", "Medical leave", "Loss of pay","Maternity leave"]
                    if type0=="Casual leave":
                        cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+diff+1),Id1))
                        for start in cursor.execute("SELECT Request_date FROM Revoke where  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            ava=start[0]
                            de1=int(ava[8:])
                            m1=int(ava[5:7])
                            ye1=int(ava[0:4])
                        for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            esw=end[0]
                            de2=int(esw[0:2])
                            m2=int(esw[3:5])
                            ye2=int(esw[-4:])
                            s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                        for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                            bg=i
                        dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                        if m1==m2:
                            if m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                            elif m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                            elif m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                            elif m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                            elif m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                            elif m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                            elif m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                            elif m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                            elif m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                            elif m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                            elif m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                            elif m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            conn.commit()
                        else:
                            for start in cursor.execute("SELECT Request_date FROM Revoke where  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                me2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            start_dc=ava
                            end_dc=s
                            f=returnmonthsdays(start_dc,end_dc)
                            start_m1=f[0]
                            start_daysre=f[1]
                            end_m1=f[2]
                            end_daysre=f[3]
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            if start_m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                            elif start_m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                            elif start_m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                            elif start_m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                            elif start_m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                            elif start_m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                            elif start_m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                            elif start_m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                            elif start_m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                            elif start_m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                            elif start_m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                            elif start_m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                            if end_m1==1:
                                cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                            elif end_m1==2:
                                cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                            elif end_m1==3:
                                cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                            elif end_m1==4:
                                cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                            elif end_m1==5:
                                cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                            elif end_m1==6:
                                cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                            elif end_m1==7:
                                cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                            elif end_m1==8:
                                cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                            elif end_m1==9:
                                cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                            elif end_m1==10:
                                cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                            elif end_m1==11:
                                cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                            elif end_m1==12:
                                cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                    elif type0=="Loss of pay":
                        cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+diff+1),Id1))
                    elif type0=="USE CCL":
                        cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+diff+1),Id1))
                    elif type0=="Medical leave":
                        cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+diff+1),Id1))
                        for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            ava=start[0]
                            de1=int(ava[8:])
                            m1=int(ava[5:7])
                            ye1=int(ava[0:4])
                        for end in cursor.execute("SELECT Date2 FROM Revoke where  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            esw=end[0]
                            de2=int(esw[0:2])
                            m2=int(esw[3:5])
                            ye2=int(esw[-4:])
                            s=str(de2)+"/"+str(me2)+"/"+str(ye2)
                        for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                            bg=i
                        dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                        if m1==m2:
                            if m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                            elif m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                            elif m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                            elif m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                            elif m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                            elif m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                            elif m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                            elif m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                            elif m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                            elif m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                            elif m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                            elif m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                        else:
                            for start in cursor.execute("SELECT Request_date FROM Revoke  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where  Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            start_dc=ava
                            end_dc=s
                            f=returnmonthsdays1(start_dc,end_dc)
                            start_m1=f[0]
                            start_daysre=f[1]
                            end_m1=f[2]
                            end_daysre=f[3]
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            if start_m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                            elif start_m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                            elif start_m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                            elif start_m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                            elif start_m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                            elif start_m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                            elif start_m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                            elif start_m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                            elif start_m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                            elif start_m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                            elif start_m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                            elif start_m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                            if end_m1==1:
                                cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                            elif end_m1==2:
                                cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                            elif end_m1==3:
                                cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                            elif end_m1==4:
                                cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                            elif end_m1==5:
                                cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                            elif end_m1==6:
                                cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                            elif end_m1==7:
                                cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                            elif end_m1==8:
                                cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                            elif end_m1==9:
                                cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                            elif end_m1==10:
                                cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                            elif end_m1==11:
                                cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                            elif end_m1==12:
                                cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                    elif type0=="Maternity leave":
                        cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+diff+1),Id1))
                    cursor.execute("UPDATE STATUS set status='Leave partially Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                    cursor.execute("UPDATE STATUS set status_workload='Work adjustment Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                    conn.commit()
                    status_updated()
                    break
                else:
                    for AVAN in cursor.execute("SELECT Request_date FROM Revoke"):
                        g=AVAN[0]
                    yyy=int(g[0:4])
                    dd=int(g[5:7])
                    mm=int(g[8:])
                    print(yyy)
                    print(dd)
                    print(mm)
                    f=date(yyy,dd,mm)
                    diff=(End_date-f).days
                    diff1=(start_date-f).days
                    diffe=(End_date-start_date).days
                    if diff1==0:
                        print('case21')
                        for Lea1 in cursor.execute("SELECT Leave from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            type0=Lea1[0]
                        if type0=="Casual leave":
                            cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+diffe+1),Id1))
                            conn.commit()
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(me2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cusror.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    ava=start[0]
                                    de1=int(ava[8:])
                                    m1=int(ava[5:7])
                                    ye1=int(ava[0:4])
                                for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                    s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=s
                                f=returnmonthsdays(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif type0=="Loss of pay":
                            cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+diffe+1),Id1))
                        elif type0=="USE CCL":
                            cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+diffe+1),Id1))
                        elif type0=="Medical leave":
                            cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+diffe+1),Id1))
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cusror.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    ava=start[0]
                                    de1=int(ava[8:])
                                    m1=int(ava[5:7])
                                    ye1=int(ava[0:4])
                                for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                    s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=s
                                f=returnmonthsdays1(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif type0=="Maternity leave": 
                            cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+diffe+1),Id1))
                        cursor.execute("UPDATE STATUS set status='Leave Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                        cursor.execute("UPDATE STATUS set status_workload='Work adjustment Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                        cursor.execute('DELETE FROM WORKASSIGN where Work_Id=:r1',{"r1":workIdr})
                        conn.commit()
                        status_updated()
                        break
                    elif diff==0:
                        print('case22')
                        for Lea1 in cursor.execute("SELECT Leave from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            type0=Lea1[0]
                        if type0=="Casual leave":
                            cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+1),Id1))
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    ava=start[0]
                                    de1=int(ava[8:])
                                    m1=int(ava[5:7])
                                    ye1=int(ava[0:4])
                                for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                    s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=s
                                f=returnmonthsdays(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif type0=="Loss of pay":
                            cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+1),Id1))
                        elif type0=="USE CCL":
                            cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+1),Id1))
                        elif type0=="Medical leave":
                            cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+1),Id1))
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    ava=start[0]
                                    de1=int(ava[8:])
                                    m1=int(ava[5:7])
                                    ye1=int(ava[0:4])
                                for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                    s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=s
                                f=returnmonthsdays1(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif type0=="Maternity leave":
                            cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+1),Id1))
                        cursor.execute("UPDATE STATUS set status='Leave partially Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                        cursor.execute("UPDATE STATUS set status_workload='Work adjustment Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                        conn.commit()
                        status_updated()
                        break
                    elif diff>0:
                        print('case23')
                        for Lea1 in cursor.execute("SELECT Leave from Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                            type0=Lea1[0]
                            choices=["Casual leave", "Medical leave", "Loss of pay","Maternity leave"]
                        if type0=="Casual leave":
                            cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+diff+1),Id1))
                            conn.commit()
                            for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cursor.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    ava=start[0]
                                    de1=int(ava[8:])
                                    m1=int(ava[5:7])
                                    ye1=int(ava[0:4])
                                for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                    s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=s
                                f=returnmonthsdays(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif type0=="Loss of pay":
                            cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+diff+1),Id1))
                        elif type0=="USE CCL":
                            cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+diff+1),Id1))
                        elif type0=="Medical leave":
                            cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+diff+1),Id1))
                            for start in cusror.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                ava=start[0]
                                de1=int(ava[8:])
                                m1=int(ava[5:7])
                                ye1=int(ava[0:4])
                            for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                                s=str(de2)+"/"+str(m2)+"/"+str(ye2)
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cursror.execute("SELECT Request_date FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    ava=start[0]
                                    de1=int(ava[8:])
                                    m1=int(ava[5:7])
                                    ye1=int(ava[0:4])
                                for end in cursor.execute("SELECT Date2 FROM Revoke where Leave_Id=:r1",{"r1":int(App_revoke[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                    s=str(de2)+"/"+str(me2)+"/"+str(ye2)
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=s
                                f=returnmonthsdays1(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif type0=="Maternity leave":
                            cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+diff+1),Id1))
                        cursor.execute("UPDATE STATUS set status='Leave partially Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                        cursor.execute("UPDATE STATUS set status_workload='Work adjustment Revoked' where Leave_Id=:r1",{"r1":int(App_revoke[0])})
                        conn.commit()
                        status_updated()
                        break
        else:
            App_revoke=multenterbox("Invalid Revoke request id",Title,input_list,App_revoke)

def Revoke_ALLstatus():
    for k in cursor.execute('SELECT count(*) from Revoke'):
        l=k[0]
    if l==0:
        revoke_record()
    else:
        Revoke_Full_status=Toplevel()
        Revoke_Full_status.title('Revoke leave status')
        Revoke_Full_status.geometry("620x300")
        table=ttk.Treeview(Revoke_Full_status,show='headings',height=300)
        style_table=ttk.Style()
        style_table.theme_use('clam')
        table["columns"]=("Leave_Id","Faculty_Id","Leave","Date1","Date2","Request_date","status")
        table.column("Leave_Id",width=65,minwidth=50,anchor=CENTER)
        table.column("Faculty_Id",width=70,minwidth=50,anchor=CENTER)
        table.column("Leave",width=110,minwidth=65,anchor=CENTER)
        table.column("Date1",width=65,minwidth=65,anchor=CENTER)
        table.column("Date2",width=65,minwidth=65,anchor=CENTER)
        table.column("Request_date",width=105,minwidth=65,anchor=CENTER)
        table.column("status",width=140,minwidth=65,anchor=CENTER)
        #Heading
        table.heading("Leave_Id",text="Leave.Id",anchor=CENTER)
        table.heading("Faculty_Id",text="Faculty.Id",anchor=CENTER)       
        table.heading("Leave",text="Leave",anchor=CENTER)
        table.heading("Date1",text="From",anchor=CENTER)
        table.heading("Date2",text="To",anchor=CENTER)
        table.heading("Request_date",text="Requested date",anchor=CENTER)
        table.heading("status",text="Admin approval",anchor=CENTER)
        i=0
        for j in cursor.execute('SELECT Leave_Id,Faculty_Id,Leave,Date1,Date2,Request_date,status From Revoke'):
            table.insert("",i,text="",values=(j[0],j[1],j[2],j[3],j[4],j[5],j[6]))
            i=i+1
        table.pack()

def REVOKE_HOME():
    REVOKE_HOMEPAGE=Toplevel()
    REVOKE_HOMEPAGE.wm_attributes('-fullscreen', '1')
    Bg_img=Label(REVOKE_HOMEPAGE,image=img3)
    Bg_img.place(x=0,y=0,relwidth=1,relheight=1)
    Revokestatus=Button(REVOKE_HOMEPAGE,text="Revoke request status",bd=13,relief=GROOVE,fg='white',bg='navy',command=Revoke_ALLstatus,pady=3)
    Revokestatus["font"]=Btnfont
    ALLleavebutn=Button(REVOKE_HOMEPAGE,text="All leave request status",bd=13,relief=GROOVE,fg='white',bg='navy',command=Leave_list,pady=3)
    ALLleavebutn["font"]=Btnfont
    Revokebutn=Button(REVOKE_HOMEPAGE,text="Approve Revoke",bd=13,relief=GROOVE,fg='white',bg='navy',command=Revoke_Approve,pady=3)
    Revokebutn["font"]=Btnfont
    Leavebutn=Button(REVOKE_HOMEPAGE,text="Approve Leave ",bd=13,relief=GROOVE,fg='white',bg='navy',command=leave_approval,pady=3)
    Leavebutn["font"]=Btnfont
    Leaveb=Button(REVOKE_HOMEPAGE,text="Exit",bd=13,relief=GROOVE,fg='white',bg='navy',command=REVOKE_HOMEPAGE.destroy,pady=3)
    Leaveb["font"]=Btnfont
    ALLleavebutn.place(relx=0.5,rely=0.31,anchor=CENTER)
    Revokestatus.place(relx=0.5,rely=0.410,anchor=CENTER)
    Revokebutn.place(relx=0.5,rely=0.508,anchor=CENTER)
    Leavebutn.place(relx=0.5,rely=0.606,anchor=CENTER)
    Leaveb.place(relx=0.5,rely=0.704,anchor=CENTER)


def revoke_stop1():
    root01=Toplevel()
    root01.geometry("170x80")
    msg1=Label(root01,text="Invalid Leave Id",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg1.pack()
    ok_btn1=Button(root01,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root01.destroy)
    ok_btn1.pack()


def Revoke_stop1():
    root02=Toplevel()
    root02.geometry("260x80")
    msg2=Label(root02,text="Already applied for Revoke",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg2.pack()
    ok_btn2=Button(root02,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root02.destroy)
    ok_btn2.pack()

def Revoke_stop1rty():
    root02=Toplevel()
    root02.geometry("250x80")
    msg2=Label(root02,text="Leave already revoked",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg2.pack()
    ok_btn2=Button(root02,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root02.destroy)
    ok_btn2.pack()
    
def Revoke_Permit():
    root_1=Toplevel()
    root_1.geometry("280x80")
    msg_1=Label(root_1,text="Cannot revoke Denied Leave!",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg_1.pack()
    ok_btn_1=Button(root_1,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root_1.destroy)
    ok_btn_1.pack()
    
def Revoke_Date():
    root_1=Toplevel()
    root_1.geometry("270x100")
    msg_1=Label(root_1,text="The Leave is expired\nNo days left to revoke!",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg_1.pack()
    ok_btn_1=Button(root_1,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root_1.destroy)
    ok_btn_1.pack()
    
def Revoke_Pending():
    root_2=Toplevel()
    root_2.geometry("255x80")
    msg_2=Label(root_2,text="The Leave is Revoked",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg_2.pack()
    ok_btn_2=Button(root_2,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root_2.destroy)
    ok_btn_2.pack()
    
def Revoke_Pendingd():
    root_2=Toplevel()
    root_2.geometry("255x80")
    msg_2=Label(root_2,text="Invalid leave type",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg_2.pack()
    ok_btn_2=Button(root_2,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root_2.destroy)
    ok_btn_2.pack()
    
def Revoke_Submitted1():
    root012=Toplevel()
    root012.geometry("260x80")
    msg23=Label(root012,text="Revoke Request Submitted",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def Revoke_Exit():
    global login1
    login1=-1
    RevokeWindow1.destroy()

def Revoke_All_status():
    for k in cursor.execute('SELECT count(*) from Revoke where Faculty_Id=?',[login]):
        l=k[0]
    if l==0:
        revoke_record()
    else:
        Revoke_Full_status=Toplevel()
        Revoke_Full_status.title('Revoke leave status')
        Revoke_Full_status.geometry("550x300")
        table=ttk.Treeview(Revoke_Full_status,show='headings',height=300)
        style_table=ttk.Style()
        style_table.theme_use('clam')
        table["columns"]=("Leave_Id","Leave","Date1","Date2","Request_date","status")
        table.column("Leave_Id",width=65,minwidth=50,anchor=CENTER)
        table.column("Leave",width=110,minwidth=65,anchor=CENTER)
        table.column("Date1",width=65,minwidth=65,anchor=CENTER)
        table.column("Date2",width=65,minwidth=65,anchor=CENTER)
        table.column("Request_date",width=105,minwidth=65,anchor=CENTER)
        table.column("status",width=140,minwidth=65,anchor=CENTER)
        #Heading
        table.heading("Leave_Id",text="Leave.Id",anchor=CENTER)
        table.heading("Leave",text="Leave",anchor=CENTER)
        table.heading("Date1",text="From",anchor=CENTER)
        table.heading("Date2",text="To",anchor=CENTER)
        table.heading("Request_date",text="Requested date",anchor=CENTER)
        table.heading("status",text="Admin approval",anchor=CENTER)
        i=0
        for j in cursor.execute('SELECT Leave_Id,Leave,Date1,Date2,Request_date,status From Revoke where Faculty_Id=?',[login]):
            table.insert("",i,text="",values=(j[0],j[1],j[2],j[3],j[4],j[5]))
            i=i+1
        table.pack()
    
def Revoke_apply():
    global RevokeWindow1
    RevokeWindow1=Toplevel()
    RevokeWindow1.wm_attributes("-fullscreen",1)
    back_img=Label(RevokeWindow1,image=img3)
    back_img.place(x=0,y=0,relwidth=1,relheight=1)
    Revoke_leave1=Button(RevokeWindow1,text="Revoke Leave",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Revoke_apply_Home,pady=3)
    Revoke_leave1["font"]=Btnfont
    Revoke_status1=Button(RevokeWindow1,text="Revoke Leave Status",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Revoke_All_status,pady=3)
    Revoke_status1["font"]=Btnfont
    Revoke_Exit1=Button(RevokeWindow1,text="Exit",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Revoke_Exit,pady=3)
    Revoke_Exit1["font"]=Btnfont
    Revoke_status1.place(relx=0.5,rely=0.36,anchor=CENTER)
    Revoke_leave1.place(relx=0.5,rely=0.458,anchor=CENTER)
    Revoke_Exit1.place(relx=0.5,rely=0.555,anchor=CENTER)
    
    
def Revoke_apply_Home():
    message1="Enter Leave_Id to Get it Revoked"
    Title1="Revoke Leave"
    field_names1=["Leave_Id"]
    fields31=multenterbox(message1,Title1,field_names1)
    while True:
        if fields31[0]=="":
            fields31=multenterbox("Fill all details",Title1,field_names1)
        else:
            break
    while True:
        if (int(fields31[0]),) in cursor.execute("Select Leave_Id from STATUS WHERE Faculty_Id=?",([login])):
            if (int(fields31[0]),) in cursor.execute("Select Leave_Id from Revoke WHERE Faculty_Id=?",([login])):
                for i in cursor.execute("SELECT status from STATUS where Leave_Id=?",[int(fields31[0])]):
                    k=i[0]
                if k=="Leave Revoked":
                    Revoke_stop1rty()
                    break
        if (int(fields31[0]),) in cursor.execute("Select Leave_Id from STATUS WHERE Faculty_Id=?",([login])):
            if (int(fields31[0]),) in cursor.execute("Select Leave_Id from Revoke WHERE Faculty_Id=?",([login])):
                Revoke_stop1()
                break
            else:
                for row in cursor.execute("SELECT status from STATUS WHERE Leave_Id=:r1",{"r1":int(fields31[0])}):
                    statusm=row[0]
                for row in cursor.execute("SELECT Leave,Date1,Date2 from STATUS WHERE Leave_Id=:r1",{"r1":int(fields31[0])}):
                    Leave_type=row[0]
                    Date1_c=row[1]
                    Date2_c=row[2]
                if Leave_type=="ADD CCL":
                    Revoke_Pendingd()
                    break
                if statusm=="Approved":
                    for row in cursor.execute("SELECT Date1 from STATUS WHERE Leave_Id=:r1",{"r1":int(fields31[0])}):
                        day1=row[0]
                    for row in cursor.execute("SELECT Date2 from STATUS WHERE Leave_Id=:r1",{"r1":int(fields31[0])}):
                        day2=row[0]
                    for row in cursor.execute("SELECT Faculty_Id from STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                        Id1=row[0]
                    for row2 in cursor.execute("SELECT Casual_Leave From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                        balance1=row2[0]
                    for row3 in cursor.execute("SELECT Medical_Leave From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                        balance2=row3[0]
                    for row4 in cursor.execute("SELECT maternity_leave From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                        balance3=row4[0]
                    for row5 in cursor.execute("SELECT Loss_of_pay From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                        balance4=row5[0]
                    for row6 in cursor.execute("SELECT Loss_of_pay From BALANCE where Faculty_Id=:r1",{"r1":Id1}):
                        balance5=row5[0]
                    dd=int(day1[0:2])
                    mm=int(day1[3:5])
                    yy=int(day1[-4:])
                    dd1=int(day2[0:2])
                    mm1=int(day2[3:5])
                    yy1=int(day2[-4:])
                    today=date.today()
                    start_date_r=date(yy,mm,dd)
                    end_date_r=date(yy1,mm1,dd1)
                    diff=(start_date_r-today).days
                    if diff>0:
                        diffr=(end_date_r-start_date_r).days
                        if Leave_type=="Casual leave":
                            cursor.execute("UPDATE balance set Casual_Leave=? where Faculty_Id=?",((balance1+diffr+1),(Id1)))
                            for start in cursor.execute("SELECT Date1 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                ava=start[0]
                                de1=int(ava[0:2])
                                m1=int(ava[3:5])
                                ye1=int(ava[-4:])
                            for end in cursor.execute("SELECT Date2 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cursor.execute("SELECT Date1 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                    ava=start[0]
                                    de1=int(ava[0:2])
                                    m1=int(ava[3:5])
                                    ye1=int(ava[-4:])
                                for end in cursor.execute("SELECT Date2 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=esw
                                f=returnmonthsdays(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif Leave_type=="Loss of pay":
                            cursor.execute("UPDATE balance set Loss_of_pay=? where Faculty_Id=?",((balance4+diffr+1),Id1))
                        elif Leave_type=="USE CCL":
                            cursor.execute("UPDATE balance set CCL=? where Faculty_Id=?",((balance5+diffr+1),Id1))
                        elif Leave_type=="Medical leave":
                            cursor.execute("UPDATE balance set Medical_Leave=? where Faculty_Id=?",((balance2+diffr+1),Id1))
                            for start in cursor.execute("SELECT Date1 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                ava=start[0]
                                de1=int(ava[0:2])
                                m1=int(ava[3:5])
                                ye1=int(ava[-4:])
                            for end in cursor.execute("SELECT Date2 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                esw=end[0]
                                de2=int(esw[0:2])
                                m2=int(esw[3:5])
                                ye2=int(esw[-4:])
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                bg=i
                            dse=(date(ye2,m2,de2)-date(ye1,m1,de1)).days+1
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-dse,Id1))
                                elif m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-dse,Id1))
                                elif m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-dse,Id1))
                                elif m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-dse,Id1))
                                elif m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-dse,Id1))
                                elif m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-dse,Id1))
                                elif m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-dse,Id1))
                                elif m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-dse,Id1))
                                elif m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-dse,Id1))
                                elif m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-dse,Id1))
                                elif m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-dse,Id1))
                                elif m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-dse,Id1))
                            else:
                                for start in cursor.execute("SELECT Date1 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                    ava=start[0]
                                    de1=int(ava[0:2])
                                    m1=int(ava[3:5])
                                    ye1=int(ava[-4:])
                                for end in cursor.execute("SELECT Date2 FROM STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                                    esw=end[0]
                                    de2=int(esw[0:2])
                                    m2=int(esw[3:5])
                                    ye2=int(esw[-4:])
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                start_dc=ava
                                end_dc=esw
                                f=returnmonthsdays1(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Id1}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-start_daysre,Id1))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-start_daysre,Id1))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-start_daysre,Id1))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-start_daysre,Id1))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-start_daysre,Id1))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-start_daysre,Id1))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-start_daysre,Id1))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-start_daysre,Id1))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-start_daysre,Id1))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-start_daysre,Id1))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-start_daysre,Id1))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-start_daysre,Id1))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]-end_daysre,Id1))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]-end_daysre,Id1))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]-end_daysre,Id1))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]-end_daysre,Id1))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]-end_daysre,Id1))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]-end_daysre,Id1))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]-end_daysre,Id1))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]-end_daysre,Id1))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]-end_daysre,Id1))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]-end_daysre,Id1))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]-end_daysre,Id1))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]-end_daysre,Id1))
                        elif Leave_type=="Maternity leave":
                            cursor.execute("UPDATE balance set maternity_leave=? where Faculty_Id=?",((balance3+diffr+1),Id1))
                        cursor.execute("UPDATE STATUS set status='Leave Revoked' WHERE Leave_Id=:r1",{"r1":int(fields31[0])})
                        for i in cursor.execute("SELECT workid from STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                            k=i[0]
                        cursor.execute("DELETE FROM WORKASSIGN where Work_Id=:r2",{"r2":k})   
                        conn.commit()
                        Revoke_Pending()
                        break
                    elif (end_date_r-today).days<0:
                        Revoke_Date()
                        break
                    else:
                        cursor.execute('INSERT INTO Revoke (Leave_Id,Faculty_Id,Leave,Date1,Date2,status,Request_date) Values(?,?,?,?,?,?,?)',(int(fields31[0]),login,Leave_type,Date1_c,Date2_c,"Pending",today))
                        conn.commit()
                        for i in cursor.execute('SELECT Name from FACULTY where Faculty_Id=?',[login]):
                            n=i[0]
                        for e in cursor.execute('SELECT email from ADMIN'):
                            eid=e[0]
                        subject=f'Revoke leave request from {n} with Id {fields31[0]}'
                        body2=f'\n\n\nThere is a {subject}, is pending for your approval.\n\nApprove or Decline it by logging into the faculty leave management system'
                        mail_sender(eid,subject,body2)
                        Revoke_Submitted1()
                        break
                elif statusm=="Denied":
                    Revoke_Permit()
                    break
                elif statusm=="Pending":
                    for i in cursor.execute("SELECT workid from STATUS where Leave_Id=:r1",{"r1":int(fields31[0])}):
                        k=i[0]
                    cursor.execute("DELETE FROM WORKASSIGN where Work_Id=:r2",{"r2":k})
                    cursor.execute("DELETE FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields31[0])})
                    conn.commit()
                    Revoke_Pending()
                    break
        else:
            revoke_stop1()
            break
            
def Forget_Home():
    global Forget_Home
    Forget_Home=Toplevel()
    Forget_Home.wm_attributes('-fullscreen', '1')
    bg_Forget=Label(Forget_Home,image=img2)
    bg_Forget.place(x=0,y=0,relwidth=1,relheight=1)
    Admin_Button1=Button(Forget_Home,text="Faculty",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Faculty_Forget_pass,pady=3)
    Admin_Button1["font"]=Btnfont
    Faculty_Button1=Button(Forget_Home,text="Admin",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Admin_Forget,pady=3)
    Faculty_Button1["font"]=Btnfont
    Exit_Button1=Button(Forget_Home,text="Exit",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Forget_Home.destroy,pady=3)
    Exit_Button1["font"]=Btnfont
    Admin_Button1.place(relx=0.5,rely=0.458,anchor=CENTER)
    Faculty_Button1.place(relx=0.5,rely=0.557,anchor=CENTER)
    Exit_Button1.place(relx=0.5,rely=0.654,anchor=CENTER)

def username_updated():
    root0=Toplevel()
    root0.geometry("185x80")
    msg=Label(root0,text="Username Updated",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()

def Password_updated():
    root0=Toplevel()
    root0.geometry("185x80")
    msg=Label(root0,text="Password Updated",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg.pack()
    ok_btn=Button(root0,text="Ok",font=('calibre',12, 'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root0.destroy)
    ok_btn.pack()

def Both_updated():
    root012=Toplevel()
    root012.geometry("335x80")
    msg23=Label(root012,text="Username and Password Updated!",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()

def sec_email_updated():
    root012=Toplevel()
    root012.geometry("335x80")
    msg23=Label(root012,text="Security code is sent to the mail id!",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def mv_email_updated():
    root012=Toplevel()
    root012.geometry("350x87")
    msg23=Label(root012,text="Email notification failed!\nCheck your internert\n Or you may have provided wrong email address ",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def sec_email_updated22():
    root012=Toplevel()
    root012.geometry("330x80")
    msg23=Label(root012,text="Check your internet connection!",fg="red",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
    
def Security_code_updated():
    root012=Toplevel()
    root012.geometry("260x80")
    msg23=Label(root012,text="Security Code updated!",fg="green",font=('calibre',15, 'bold'),justify=CENTER)
    msg23.pack()
    ok_btn23=Button(root012,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=root012.destroy)
    ok_btn23.pack()
 
def Admin_Forget():
    Title="Select the required field to modify"
    message="Forget Username or Password"
    choices1=["Username","Password","Both","Security code"]
    Admin_choice=choicebox(Title,message,choices1)
    if Admin_choice=="Username":
        message="Enter Admin Security Code To Proceed Further"
        Title='Forget Username'
        input_list1=["Security Code"]
        Security_admin=multpasswordbox(message,Title,input_list1)
        while True:
            for security in cursor.execute("SELECT Security_code FROM ADMIN"):
                check=security[0]
            if Security_admin[0]==check:
                message="Enter New Username"
                Title="Forget Username"
                input_list=["Username"]
                Username_admin=multenterbox(message,Title,input_list)
                while True:
                    if Username_admin==[""]:
                        Username_admin=multenterbox("Please fill all details",Title,input_list)
                    elif (Username_admin[0],) in cursor.execute('SELECT Faculty_Id from Faculty'):
                        Username_admin=multenterbox("This Id is already in use by Faculty",Title,input_list,Username_admin)
                    else:
                        cursor.execute("UPDATE ADMIN SET Username=:r1",{"r1":Username_admin[0]})
                        conn.commit()
                        username_updated()
                        break
                break
            else:
                Security_admin=multpasswordbox("Invalid Security code",Title,input_list1)
                
    elif Admin_choice=="Password":
        message="Enter Admin Security Code To Proceed Further"
        Title='Forget Password'
        input_list2=["Security Code"]
        Security_admin2=multpasswordbox(message,Title,input_list2)
        while True:
            for security in cursor.execute("SELECT Security_code FROM ADMIN"):
                check=security[0]
            if Security_admin2[0]==check:
                message1="Enter New Password"
                Title1="Forget Password"
                input_list1=["Password"]
                Password_admin=multpasswordbox(message1,Title1,input_list1)
                while True:
                    if Password_admin==['']:
                        Password_admin=multpasswordbox("Please fill all details",Title1,input_list1)
                    else: 
                        cursor.execute("UPDATE ADMIN SET Password=:r1",{"r1":Password_admin[0]})
                        conn.commit()
                        Password_updated()
                        break
                break
            else:
                Security_admin2=multpasswordbox("Invalid Security code",Title,input_list2)
                
    elif Admin_choice=="Both":
        message="Enter Admin Security Code To Proceed Further"
        Title3='Forget Username and Password'
        input_list4=["Security Code"]
        Security_admin3=multpasswordbox(message,Title,input_list4)
        while True:
            for security in cursor.execute("SELECT Security_code FROM ADMIN"):
                check=security[0]
            if Security_admin3[0]==check:
                message="Enter New Username and Password"
                Title='Forget Username and Password'
                input_list3=["Username","Password"]
                Both_admin=multpasswordbox(message,Title,input_list3)
                while True:
                    if Both_admin==["",""] or (Both_admin[0]=='' or Both_admin[1]==''):
                        Both_admin=multpasswordbox("Please fill all details",Title,input_list3,Both_admin)
                    elif (Both_admin[0],) in cursor.execute('Select Faculty_Id from Faculty'):
                        Both_admin=multpasswordbox("This ID is already in use by Faculty",Title,input_list3,Both_admin)
                    else:
                        cursor.execute("UPDATE ADMIN SET Username=:r1",{"r1":Both_admin[0]})
                        cursor.execute("UPDATE ADMIN SET Password=:r1",{"r1":Both_admin[0]})
                        conn.commit()
                        Both_updated()
                        break
                break
            else:
                Security_admin3=multpasswordbox("Invalid Security code",Title3,input_list4)

    elif Admin_choice=="Security code":
        for row in cursor.execute("SELECT email,Security_code From ADMIN"):
            email_s=row[0]
            ss_code=row[1]
        mail_sender(email_s,'Forget security code',f'\n\nYour security code is {ss_code}')
        sec_email_updated()
        
def Faculty_Forget_pass():
    message="Select the required field"
    Title="Forget Username or Password"
    choiceFaculty=["Username","Password","Security code"]
    choice_of_Faculty=choicebox(message,Title,choiceFaculty)
    if choice_of_Faculty=="Username":
        message="Enter your security code to proceed further"
        Title="Forget Username"
        F_list=["Security Code"]
        Faculty_UsernameF=multpasswordbox(message,Title,F_list)
        while True:
            if (Faculty_UsernameF[0],) in cursor.execute("SELECT Security_code From FACULTY"):
                for row in cursor.execute("SELECT Faculty_Id From FACULTY where Security_code=:r1",{"r1":Faculty_UsernameF[0]}):
                    Id=row[0]
                str1="Your Id is: "+Id
                Display=Toplevel()
                Display.geometry("335x80")
                text_bar=Label(Display,text=str1,fg="green",font=('calibre',15, 'bold'),justify=CENTER)
                ok_button=Button(Display,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=Display.destroy)
                text_bar.pack()
                ok_button.pack()
                break
            else:
                Faculty_UsernameF=multpasswordbox("Invalid Security Code",Title,F_list)
    elif choice_of_Faculty=="Password":
        message="Enter The details to proceed further"
        Title="Forget Password"
        F_list1=["Faculty Id","Security Code"]
        Faculty_UsernameF2=multpasswordbox(message,Title,F_list1)
        while True:
            if Faculty_UsernameF2==["",""] or (Faculty_UsernameF2[0]==[''] or Faculty_UsernameF2[1]==['']):
                Faculty_UsernameF2=multpasswordbox("Please fill all required details",Title,F_list1)
            else:
                for i in cursor.execute("SELECT Security_code FROM FACULTY where Faculty_Id=:r1",{"r1":Faculty_UsernameF2[0]}):
                    row=i[0]
                if (Faculty_UsernameF2[0],) in cursor.execute("SELECT Faculty_Id FROM FACULTY") and Faculty_UsernameF2[1]==row:
                    for row in cursor.execute("SELECT Password FROM FACULTY where Faculty_Id=:r1",{"r1":Faculty_UsernameF2[0]}):
                        sec_FACULTY=row[0]
                    str1="Your Password is: "+sec_FACULTY
                    Display=Toplevel()
                    Display.geometry("335x80")
                    text_bar=Label(Display,text=str1,fg="green",font=('calibre',15, 'bold'),justify=CENTER)
                    ok_button=Button(Display,text="Ok",font=('calibre',12,'bold','underline'),bg="blue",fg='white',justify=CENTER,command=Display.destroy)
                    text_bar.pack()
                    ok_button.pack()
                    break
                else:
                    Faculty_UsernameF2=multpasswordbox("Invalid Username or Security Code",Title,F_list1,Faculty_UsernameF2)
    elif choice_of_Faculty=="Security code":
        message="Enter Faculty ID"
        Title="Forget Security code"
        F_list1=["Faculty Id"]
        Faculty_Security=multenterbox(message,Title,F_list1)
        while True:
            if Faculty_Security==['']:
                Faculty_Security=multenterbox("Please fill all required details",Title,F_list)
            elif (Faculty_Security[0],) not in cursor.execute("SELECT Faculty_Id from FACULTY"):
                Faculty_Security=multenterbox("Invalid Id",Title,F_list1,)
            else:
                for i in cursor.execute('SELECT email_id,security_code from FACULTY where Faculty_Id=?',[Faculty_Security[0]]):
                    email=i[0]
                    security=i[1]
                mail_sender(email,'Forget security code',f'\n\nYour security code is {security}')
                sec_email_updated()
                break

def leave_approval():
    message="Enter Leave_Id"
    Title="Leave Approval"
    field_names=['Leave_Id']
    fields3=multenterbox(message,Title,field_names)
    while True:
        if fields3 == None:
            break
        err_msg1=""
        for i in range(len(fields3)):
            if fields3[i]=="":
                err_msg1=err_msg1+("'%s'is a required field"%field_names[i])
        if err_msg1=="":
            break
        fields3=multenterbox(err_msg1,Title,field_names)
    while True:
        if (int(fields3[0]),) in cursor.execute("SELECT Leave_Id FROM STATUS"):
            for row in cursor.execute("Select status From STATUS where Leave_Id=:r1",{"r1":int(fields3[0])}):
                re_check=row[0]
            if re_check=="Approved" or re_check=="Denied":
                status_stop()
                break
            else:
                message="Approve/deny"
                Title="Leave Approval"
                choices=["Approved","Denied"]
                choice5=choicebox(message,Title,choices)
                if choice5==None:
                    choice_status()
                    break
                for i in cursor.execute("SELECT status FROM STATUS where Leave_Id=:r3",{'r3':int(fields3[0])}):
                    g=i[0]
                for h in cursor.execute("SELECT Faculty_Id from STATUS where Leave_Id=:r3",{'r3':int(fields3[0])}):
                    fac=h[0]
                for j in cursor.execute("SELECT Name,email_id from FACULTY where Faculty_Id=?",[fac]):
                    nme=j[0]
                    email=j[1]
                cursor.execute("UPDATE STATUS SET status=? where Leave_Id=?",(choice5,(int(fields3[0]))))
                conn.commit()
                if choice5=="Denied":
                    cursor.execute("UPDATE STATUS SET status_workload=? where Leave_Id=?",('Work adjustment Revoked',(int(fields3[0]))))
                    conn.commit()
                subject=f'Leave request with id {fields3[0]} is {choice5}'
                body=f'{nme},\n\n\n Your {subject}'
                mail_sender(email,subject,body)
                status_updated()
                if choice5=="Approved":
                    cursor.execute("SELECT Leave FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields3[0])})
                    row=cursor.fetchall()
                    col=row
                    print(col)
                    for row in cursor.execute("SELECT Faculty_Id From STATUS where Leave_Id=:r1",{'r1':int(fields3[0])}):
                        Fac_Id=row[0]
                    for row1 in cursor.execute("SELECT Days FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields3[0])}):
                        Faculty_days=row1[0]
                    for row2 in cursor.execute("SELECT Casual_Leave From BALANCE where Faculty_Id=:r1",{"r1":Fac_Id}):
                        balance1=row2[0]
                    for month in cursor.execute("SELECT Date1 FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields3[0])}):
                        start_dc=month[0]
                        m1=int(month[0][3:5])
                    for month2 in cursor.execute("SELECT Date2 FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields3[0])}):
                        end_dc=month2[0]
                        m2=int(month2[0][3:5])
                    for month in cursor.execute("SELECT Date1 FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields3[0])}):
                        start_a=month[0]
                    for month2 in cursor.execute("SELECT Date2 FROM STATUS WHERE Leave_Id=:r1",{"r1":int(fields3[0])}):
                        end_a=month2[0]
                    for row3 in cursor.execute("SELECT Medical_Leave From BALANCE where Faculty_Id=:r1",{"r1":Fac_Id}):
                        balance2=row3[0]
                    for row4 in cursor.execute("SELECT maternity_leave From BALANCE where Faculty_Id=:r1",{"r1":Fac_Id}):
                        balance3=row4[0]
                    for row5 in cursor.execute("SELECT Loss_of_pay From BALANCE where Faculty_Id=:r1",{"r1":Fac_Id}):
                        balance4=row5[0]
                    for row6 in cursor.execute("SELECT CCL From BALANCE where Faculty_Id=:r1",{"r1":Fac_Id}):
                        balance5=row6[0]
                    if (col[0]==('Casual leave',)):
                        if (balance1-Faculty_days)<0:
                            cursor.execute("UPDATE STATUS SET status='Leave Exceeded in Casual leave quota,you can take loss of pay leave if required' where Leave_Id=:r3",{'r3':int(fields3[0])})              
                        else:
                            cursor.execute("UPDATE BALANCE SET Casual_Leave=? where Faculty_Id=?",((balance1-Faculty_days),(Fac_Id)))
                            for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Fac_Id}):
                                bg=i
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]+Faculty_days,Fac_Id))
                                elif m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]+Faculty_days,Fac_Id))
                                elif m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]+Faculty_days,Fac_Id))
                                elif m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]+Faculty_days,Fac_Id))
                                elif m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]+Faculty_days,Fac_Id))
                                elif m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]+Faculty_days,Fac_Id))
                                elif m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]+Faculty_days,Fac_Id))
                                elif m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]+Faculty_days,Fac_Id))
                                elif m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]+Faculty_days,Fac_Id))
                                elif m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]+Faculty_days,Fac_Id))
                                elif m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]+Faculty_days,Fac_Id))
                                elif m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]+Faculty_days,Fac_Id))
                            else:
                                f=returnmonthsdays(start_dc,end_dc)
                                start_m1=f[0]
                                print(start_m1)
                                start_daysre=f[1]
                                print(start_daysre)
                                end_m1=f[2]
                                print(end_m1)
                                end_daysre=f[3]
                                print(end_daysre)
                                for i in cursor.execute("SELECT * FROM  Month where Faculty_Id=:r1",{"r1":Fac_Id}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]+start_daysre,Fac_Id))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]+start_daysre,Fac_Id))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]+start_daysre,Fac_Id))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]+start_daysre,Fac_Id))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]+start_daysre,Fac_Id))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]+start_daysre,Fac_Id))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]+start_daysre,Fac_Id))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]+start_daysre,Fac_Id))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]+start_daysre,Fac_Id))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]+start_daysre,Fac_Id))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]+start_daysre,Fac_Id))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]+start_daysre,Fac_Id))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month set first=? where Faculty_Id=?",(bg[1]+end_daysre,Fac_Id))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month set second=? where Faculty_Id=?",(bg[2]+end_daysre,Fac_Id))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month set third=? where Faculty_Id=?",(bg[3]+end_daysre,Fac_Id))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month set fourth=? where Faculty_Id=?",(bg[4]+end_daysre,Fac_Id))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month set fifth=? where Faculty_Id=?",(bg[5]+end_daysre,Fac_Id))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month set sixth=? where Faculty_Id=?",(bg[6]+end_daysre,Fac_Id))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month set seventh=? where Faculty_Id=?",(bg[7]+end_daysre,Fac_Id))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month set eighth=? where Faculty_Id=?",(bg[8]+end_daysre,Fac_Id))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month set ninth=? where Faculty_Id=?",(bg[9]+end_daysre,Fac_Id))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month set tenth=? where Faculty_Id=?",(bg[10]+end_daysre,Fac_Id))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month set eleventh=? where Faculty_Id=?",(bg[11]+end_daysre,Fac_Id))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month set twelvth=? where Faculty_Id=?",(bg[12]+end_daysre,Fac_Id))
                    if (col[0]==('Medical leave',)):
                        if (balance2-Faculty_days)<0:
                            cursor.execute("UPDATE STATUS SET status='Leave Exceeded in Medical leave quota,you can take loss of pay leave if required' where Leave_Id=:r3",{'r3':int(fields3[0])})              
                        else:
                            cursor.execute("UPDATE BALANCE SET Medical_Leave=? where Faculty_Id=?",((balance2-Faculty_days),(Fac_Id)))
                            for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Fac_Id}):
                                bg=i
                            if m1==m2:
                                if m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]+Faculty_days,Fac_Id))
                                elif m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]+Faculty_days,Fac_Id))
                                elif m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]+Faculty_days,Fac_Id))
                                elif m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]+Faculty_days,Fac_Id))
                                elif m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]+Faculty_days,Fac_Id))
                                elif m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]+Faculty_days,Fac_Id))
                                elif m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]+Faculty_days,Fac_Id))
                                elif m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]+Faculty_days,Fac_Id))
                                elif m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]+Faculty_days,Fac_Id))
                                elif m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]+Faculty_days,Fac_Id))
                                elif m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]+Faculty_days,Fac_Id))
                                elif m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]+Faculty_days,Fac_Id))
                            else:
                                f=returnmonthsdays(start_dc,end_dc)
                                start_m1=f[0]
                                start_daysre=f[1]
                                end_m1=f[2]
                                end_daysre=f[3]
                                for i in cursor.execute("SELECT * FROM  Month1 where Faculty_Id=:r1",{"r1":Fac_Id}):
                                    bg=i
                                if start_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]+start_daysre,Fac_Id))
                                elif start_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]+start_daysre,Fac_Id))
                                elif start_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]+start_daysre,Fac_Id))
                                elif start_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]+start_daysre,Fac_Id))
                                elif start_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]+start_daysre,Fac_Id))
                                elif start_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]+start_daysre,Fac_Id))
                                elif start_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]+start_daysre,Fac_Id))
                                elif start_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]+start_daysre,Fac_Id))
                                elif start_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]+start_daysre,Fac_Id))
                                elif start_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]+start_daysre,Fac_Id))
                                elif start_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]+start_daysre,Fac_Id))
                                elif start_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]+start_daysre,Fac_Id))
                                if end_m1==1:
                                    cursor.execute("UPDATE Month1 set first=? where Faculty_Id=?",(bg[1]+end_daysre,Fac_Id))
                                elif end_m1==2:
                                    cursor.execute("UPDATE Month1 set second=? where Faculty_Id=?",(bg[2]+end_daysre,Fac_Id))
                                elif end_m1==3:
                                    cursor.execute("UPDATE Month1 set third=? where Faculty_Id=?",(bg[3]+end_daysre,Fac_Id))
                                elif end_m1==4:
                                    cursor.execute("UPDATE Month1 set fourth=? where Faculty_Id=?",(bg[4]+end_daysre,Fac_Id))
                                elif end_m1==5:
                                    cursor.execute("UPDATE Month1 set fifth=? where Faculty_Id=?",(bg[5]+end_daysre,Fac_Id))
                                elif end_m1==6:
                                    cursor.execute("UPDATE Month1 set sixth=? where Faculty_Id=?",(bg[6]+end_daysre,Fac_Id))
                                elif end_m1==7:
                                    cursor.execute("UPDATE Month1 set seventh=? where Faculty_Id=?",(bg[7]+end_daysre,Fac_Id))
                                elif end_m1==8:
                                    cursor.execute("UPDATE Month1 set eighth=? where Faculty_Id=?",(bg[8]+end_daysre,Fac_Id))
                                elif end_m1==9:
                                    cursor.execute("UPDATE Month1 set ninth=? where Faculty_Id=?",(bg[9]+end_daysre,Fac_Id))
                                elif end_m1==10:
                                    cursor.execute("UPDATE Month1 set tenth=? where Faculty_Id=?",(bg[10]+end_daysre,Fac_Id))
                                elif end_m1==11:
                                    cursor.execute("UPDATE Month1 set eleventh=? where Faculty_Id=?",(bg[11]+end_daysre,Fac_Id))
                                elif end_m1==12:
                                    cursor.execute("UPDATE Month1 set twelvth=? where Faculty_Id=?",(bg[12]+end_daysre,Fac_Id))
                    if (col[0]==('Maternity leave',)):
                        if (balance3-Faculty_days)<0:
                            cursor.execute("UPDATE STATUS SET status='Leave Exceeded in Maternity leave quota,you can take loss of pay leave  if required' where Leave_Id=:r3",{'r3':int(fields3[0])})              
                        else:
                            cursor.execute("UPDATE BALANCE SET maternity_leave=? where Faculty_Id=?",((balance3-Faculty_days),(Fac_Id)))
                    if (col[0]==('Loss of pay',)):
                        cursor.execute("UPDATE BALANCE SET Loss_of_pay=? where Faculty_Id=?",((balance4-Faculty_days),(Fac_Id)))
                    if col[0]==("USE CCL",):
                        if (balance5-Faculty_days)<0:
                            cursor.execute("UPDATE STATUS SET status='No CCLS are left to use' where Leave_Id=:r3",{'r3':int(fields3[0])})
                        else:
                            cursor.execute("UPDATE BALANCE SET CCL=? where Faculty_Id=?",((balance5-Faculty_days),(Fac_Id)))
                    if col[0]==('ADD CCL',):
                        cursor.execute("UPDATE BALANCE SET CCL=? where Faculty_Id=?",((balance5+Faculty_days),(Fac_Id)))
                    conn.commit()
                break
        else:
            fields3=multenterbox("Invalid Leave id",Title,field_names,fields3)
            
def Leave_list():
    for i in cursor.execute("Select count(*) from Status"):
        g=i[0]
    if g==0:
        Leave_record()
    else:
        leave_Status=Toplevel()
        leave_Status.title("All leave Status")
        leave_Status.geometry("890x350")
        table=ttk.Treeview(leave_Status,show='headings',height=350)
        style_table=ttk.Style()
        style_table.theme_use('clam')
        table["columns"]=("Leave_Id",'Faculty_Id',"Leave","Date1","Date2","Days","workid","work_facid","status_workload","status")
        table.column("Leave_Id",width=60,minwidth=50,anchor=CENTER)
        table.column("Faculty_Id",width=60,minwidth=50,anchor=CENTER)
        table.column("Leave",width=100,minwidth=65,anchor=CENTER)
        table.column("Date1",width=65,minwidth=65,anchor=CENTER)
        table.column("Date2",width=65,minwidth=65,anchor=CENTER)
        table.column("Days",width=40,minwidth=40,anchor=CENTER)
        table.column("workid",width=55,minwidth=50,anchor=CENTER)
        table.column("work_facid",width=80,minwidth=50,anchor=CENTER)
        table.column("status_workload",width=160,minwidth=70,anchor=CENTER)
        table.column("status",width=205,minwidth=65,anchor=CENTER)
        #Heading
        table.heading("Leave_Id",text="Leave.Id",anchor=CENTER)
        table.heading("Faculty_Id",text="Faculty.Id",anchor=CENTER)
        table.heading("Leave",text="Leave",anchor=CENTER)
        table.heading("Date1",text="From",anchor=CENTER)
        table.heading("Date2",text="To",anchor=CENTER)
        table.heading("Days",text="Days",anchor=CENTER)
        table.heading("workid",text="Work.Id",anchor=CENTER)
        table.heading("work_facid",text="Assigned to",anchor=CENTER)
        table.heading("status_workload",text="work adjustment",anchor=CENTER)
        table.heading("status",text="Admin approval",anchor=CENTER)
        j=0
        for i in cursor.execute("SELECT * From Status where status_workload!=?",['Work adjustment Pending']):
            table.insert('',j,text="",values=(i[0],i[1],i[2],i[3],i[4],i[5],i[7],i[8],i[9],i[6]))
            j=j+1
        table.pack()

def balance_left():
    balance_left1=Toplevel()
    global balanceleft1
    for Giga in cursor.execute("SELECT * from BALANCE where Faculty_Id=?",[login]):
        balanceleft2=Giga
    for row_1 in cursor.execute("Select Gender from FACULTY where Faculty_Id=?",[login]):
        gender_b=row_1[0]
    if gender_b=="F":
        Casual=str(balanceleft2[1])+"/24"
        Medical=str(balanceleft2[2])+"/31"
        Maternity=str(balanceleft2[4])+"/55"
        Loss_of_pay=str(balanceleft2[3])
        CCLs=str(balanceleft2[5])
        label1=Label(balance_left1,text="Faculty Id :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label2=Label(balance_left1,text=balanceleft2[0],fg="blue",font=('calibre',16),justify=LEFT)
        label3=Label(balance_left1,text="Casual Leave :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label4=Label(balance_left1,text=Casual,fg="blue",font=('calibre',16),justify=LEFT)
        label5=Label(balance_left1,text="Medical Leave :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label6=Label(balance_left1,text=Medical,fg="blue",font=('calibre',16),justify=LEFT)
        label7=Label(balance_left1,text="Maternity Leave :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label8=Label(balance_left1,text=Maternity,fg="blue",font=('calibre',16),justify=LEFT)
        label9=Label(balance_left1,text="Loss of pay :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label10=Label(balance_left1,text=Loss_of_pay,fg="red",font=('calibre',16),justify=LEFT)
        label11=Label(balance_left1,text="CCLs :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label12=Label(balance_left1,text= CCLs,fg="green",font=('calibre',16),justify=LEFT)
        label1.grid(row=0,column=0)
        label2.grid(row=0,column=1)
        label3.grid(row=1,column=0)
        label4.grid(row=1,column=1)
        label5.grid(row=2,column=0)
        label6.grid(row=2,column=1)
        label7.grid(row=3,column=0)
        label8.grid(row=3,column=1)
        label9.grid(row=4,column=0)
        label10.grid(row=4,column=1)
        label9.grid(row=5,column=0)
        label10.grid(row=5,column=1)
        label11.grid(row=6,column=0)
        label12.grid(row=6,column=1)

        
    elif gender_b=="M":
        Casual1=str(balanceleft2[1])+"/24"
        Medical1=str(balanceleft2[2])+"/31"
        Loss_of_pay1=str(balanceleft2[3])
        CCLs=str(balanceleft2[5])
        label1=Label(balance_left1,text="Faculty Id :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label2=Label(balance_left1,text=balanceleft2[0],fg="blue",font=('calibre',16),justify=LEFT)
        label3=Label(balance_left1,text="Casual Leave :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label4=Label(balance_left1,text=Casual1,fg="blue",font=('calibre',16),justify=LEFT)
        label5=Label(balance_left1,text="Medical Leave :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label6=Label(balance_left1,text=Medical1,fg="blue",font=('calibre',16),justify=LEFT)
        label7=Label(balance_left1,text="Loss of pay :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label8=Label(balance_left1,text=Loss_of_pay1,fg="red",font=('calibre',16),justify=LEFT)
        label9=Label(balance_left1,text="CCLs :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label10=Label(balance_left1,text= CCLs,fg="green",font=('calibre',16),justify=LEFT)
        label1.grid(row=0,column=0)
        label2.grid(row=0,column=1)
        label3.grid(row=1,column=0)
        label4.grid(row=1,column=1)
        label5.grid(row=2,column=0)
        label6.grid(row=2,column=1)
        label7.grid(row=3,column=0)
        label8.grid(row=3,column=1)
        label9.grid(row=4,column=0)
        label10.grid(row=4,column=1)
    
def last_leavewindow():
    global leave1
    leave1=[]
    for i in cursor.execute("SELECT * from STATUS where Faculty_Id=?",[login]):
        leave1=i
    for i in cursor.execute("SELECT count(*) from STATUS where Faculty_Id=?",[login]):
        g=i[0]
    if g==0:
        Leave_record()
    elif leave1[9]=="Work adjustment Declined" or leave1[9]=="Work adjustment Accepted" or leave1[9]=="Work adjustment Pending":
        LastLeaveWindow=Toplevel()
        label1=Label(LastLeaveWindow,text="Faculty Id =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label2=Label(LastLeaveWindow,text=leave1[1],fg="blue",font=('calibre',16),justify=LEFT)
        label3=Label(LastLeaveWindow,text="Type=",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label4=Label(LastLeaveWindow,text=leave1[2],fg="blue",font=('calibre',16),justify=LEFT)
        label5=Label(LastLeaveWindow,text="Start_Date =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label6=Label(LastLeaveWindow,text=leave1[3],fg="blue",font=('calibre',16),justify=LEFT)
        label7=Label(LastLeaveWindow,text="End_Date =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label8=Label(LastLeaveWindow,text=leave1[4],fg="blue",font=('calibre',16),justify=LEFT)
        label9=Label(LastLeaveWindow,text="Status :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label10=Label(LastLeaveWindow,text=leave1[9],fg="red",font=('calibre',16),justify=LEFT)
        label11=Label(LastLeaveWindow,text="Leave Id =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label12=Label(LastLeaveWindow,text=leave1[0],fg="blue",font=('calibre',16),justify=LEFT)
        label11.grid(row=0,column=0)
        label12.grid(row=0,column=1)
        label1.grid(row=1,column=0)
        label2.grid(row=1,column=1)
        label3.grid(row=2,column=0)
        label4.grid(row=2,column=1)
        label5.grid(row=3,column=0)
        label6.grid(row=3,column=1)
        label7.grid(row=4,column=0)
        label8.grid(row=4,column=1)
        label9.grid(row=5,column=0)
        label10.grid(row=5,column=1)
    else:
        LastLeaveWindow=Toplevel()
        label1=Label(LastLeaveWindow,text="Faculty Id =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label2=Label(LastLeaveWindow,text=leave1[1],fg="blue",font=('calibre',16),justify=LEFT)
        label3=Label(LastLeaveWindow,text="Type=",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label4=Label(LastLeaveWindow,text=leave1[2],fg="blue",font=('calibre',16),justify=LEFT)
        label5=Label(LastLeaveWindow,text="Start_Date =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label6=Label(LastLeaveWindow,text=leave1[3],fg="blue",font=('calibre',16),justify=LEFT)
        label7=Label(LastLeaveWindow,text="End_Date =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label8=Label(LastLeaveWindow,text=leave1[4],fg="blue",font=('calibre',16),justify=LEFT)
        label9=Label(LastLeaveWindow,text="Status :",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label10=Label(LastLeaveWindow,text=leave1[6],fg="red",font=('calibre',16),justify=LEFT)
        label11=Label(LastLeaveWindow,text="Leave Id =",fg="blue",font=('calibre',16, 'bold'),justify=LEFT)
        label12=Label(LastLeaveWindow,text=leave1[0],fg="blue",font=('calibre',16),justify=LEFT)
        label11.grid(row=0,column=0)
        label12.grid(row=0,column=1)
        label1.grid(row=1,column=0)
        label2.grid(row=1,column=1)
        label3.grid(row=2,column=0)
        label4.grid(row=2,column=1)
        label5.grid(row=3,column=0)
        label6.grid(row=3,column=1)
        label7.grid(row=4,column=0)
        label8.grid(row=4,column=1)
        label9.grid(row=5,column=0)
        label10.grid(row=5,column=1)
    

def adminmain_window():  
    LoginWindow = Toplevel()
    LoginWindow.wm_attributes('-fullscreen',1)
    Background_img=Label(LoginWindow,image=img2)
    Background_img.place(x=0,y=0,relwidth=1, relheight=1)
    all_Employ=Button(LoginWindow,text="All Faculty Info",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=all_Faculty_info,pady=3)
    all_Employ["font"]=Btnfont
    DeleteFaculty=Button(LoginWindow,text="Delete Faculty",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=delete_Faculty,pady=3)
    DeleteFaculty["font"]=Btnfont
    all_Employ.place(relx = 0.5, rely = 0.23, anchor = CENTER)
    DeleteFaculty.place(relx = 0.5, rely = 0.328, anchor = CENTER)
    Aproove_Deny=Button(LoginWindow,text="Update my\nEmail id",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=updatedadminemid,pady=3)
    Aproove_Deny["font"]=Btnfont
    Aproove_Deny.place(relx = 0.5, rely = 0.445, anchor = CENTER)
    Aproove_list=Button(LoginWindow,text="Aproove\nLeave",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=REVOKE_HOME,pady=3)
    Aproove_list["font"]=Btnfont
    Aproove_list.place(relx = 0.5, rely = 0.580, anchor = CENTER)
    Clear_status=Button(LoginWindow,text="Clear\nStatus",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=clear_status,pady=3)
    Clear_status["font"]=Btnfont
    Clear_status.place(relx = 0.5, rely = 0.715, anchor = CENTER)
    Exit=Button(LoginWindow,text="Exit",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=LoginWindow.destroy,pady=3)
    Exit["font"]=Btnfont
    Exit.place(relx = 0.5, rely = 0.832, anchor = CENTER)
    
def all_Faculty_info():
    for i in cursor.execute("SELECT count(*) from Faculty"):
        k=i[0]
    if k==0:
        statusfac_stop()
    else:
        FacInfo=Toplevel()
        FacInfo.title('All Faculty Info')
        FacInfo.geometry('810x350')
        table=ttk.Treeview(FacInfo,show='headings',height=350)
        style_table=ttk.Style()
        style_table.theme_use('clam')
        table["columns"]=('Faculty_Id',"Name","Subject","sections_teaching","contact_no","email_id")
        table.column("Faculty_Id",width=60,minwidth=50,anchor=CENTER)
        table.column("Name",width=160,minwidth=65,anchor=CENTER)
        table.column("Subject",width=160,minwidth=65,anchor=CENTER)
        table.column("sections_teaching",width=140,minwidth=65,anchor=CENTER)
        table.column("contact_no",width=90,minwidth=50,anchor=CENTER)
        table.column("email_id",width=200,minwidth=50,anchor=CENTER)
        #Heading
        table.heading("Faculty_Id",text="Faculty.Id",anchor=CENTER)
        table.heading("Name",text="Name",anchor=CENTER)
        table.heading("Subject",text="Subjects teaching",anchor=CENTER)
        table.heading("sections_teaching",text="Sections teaching",anchor=CENTER)
        table.heading("contact_no",text="Contact.no",anchor=CENTER)
        table.heading("email_id",text="Email Id",anchor=CENTER)
        i=0
        for row in cursor.execute("Select Faculty_Id,Name,Subject,sections_teaching,contact_no,email_id from Faculty "):
            table.insert("",i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]))
            i=i+1
        table.pack()
              
def clear_status():
    cursor.execute("DELETE FROM STATUS")
    cursor.execute("DELETE FROM Revoke")
    cursor.execute("DELETE FROM WORKASSIGN")
    cursor.execute("UPDATE BALANCE SET Casual_Leave=?,Medical_Leave=?,Loss_of_pay=?,maternity_leave=?,CCL=?",(24,31,0,55,0))
    cursor.execute("UPDATE Month SET first=?,second=?,third=?,fourth=?,fifth=?,sixth=?,seventh=?,eighth=?,ninth=?,tenth=?,eleventh=?,twelvth=?",(0,0,0,0,0,0,0,0,0,0,0,0))
    cursor.execute("UPDATE Month1 SET first=?,second=?,third=?,fourth=?,fifth=?,sixth=?,seventh=?,eighth=?,ninth=?,tenth=?,eleventh=?,twelvth=?",(0,0,0,0,0,0,0,0,0,0,0,0))
    conn.commit()
    status_cleared()
        
def delete_Faculty():
    delete_Faculty=Toplevel()
    delete_Faculty.wm_attributes('-fullscreen',1)
    Background_lb=Label(delete_Faculty,image=img3)
    Background_lb.place(x=0,y=0,relwidth=1, relheight=1)
    all_Employ=Button(delete_Faculty,text="All Faculty Info",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=all_Faculty_info,pady=3)
    all_Employ["font"]=Btnfont
    Deletebutn=Button(delete_Faculty,text="Delete By ID",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=delete_option,pady=3)
    Deletebutn["font"]=Btnfont
    all_Delete=Button(delete_Faculty,text="Delete All",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=Delete_All,pady=3)
    all_Delete["font"]=Btnfont
    Exit=Button(delete_Faculty,text="Exit",bd=13,relief=GROOVE,fg='white',bg='navy',font=("Callibri",36,"bold"),command=delete_Faculty.destroy,pady=3)
    Exit["font"]=Btnfont
    all_Employ.place(relx=0.5,rely=0.36,anchor=CENTER)
    Deletebutn.place(relx=0.5,rely=0.458,anchor=CENTER)
    all_Delete.place(relx=0.5,rely=0.555,anchor=CENTER)
    Exit.place(relx=0.5,rely=0.654,anchor=CENTER)
    
def Delete_All():
    cursor.execute("DELETE FROM FACULTY")
    cursor.execute("DELETE FROM STATUS")
    cursor.execute("DELETE FROM REVOKE")
    cursor.execute("DELETE FROM BALANCE")
    cursor.execute("DELETE FROM Month") 
    cursor.execute("DELETE FROM Month1")
    cursor.execute("DELETE FROM WORKASSIGN")
    conn.commit()
    messagebox.showinfo("Delete ALL","All Data cleared")
def delete_option():
    global rot
    rot=Toplevel()
    rot.geometry("390x170")
    global ID_int
    ID_int=StringVar()
    msg=Label(rot,text="Enter ID to Delete Faculty",font=('calibre',20, 'bold'))
    name_vid=Label(rot,text = 'ID', font=('calibre',16 ))
    Id=Entry(rot,textvariable=ID_int, font=('calibre',16))
    submit_btn=Button(rot,text="Submit",font=('calibre',16,"bold","underline"),relief=GROOVE,fg="white",bg="Navy blue",command=submit)
    msg.pack()
    name_vid.pack(side=LEFT)
    Id.pack(side=LEFT)
    submit_btn.pack(side=LEFT)

def delete_option1():
    global rot
    rot=Toplevel()
    rot.geometry("390x170")
    global ID_int
    ID_int=StringVar()
    msg=Label(rot,text="Invalid Leave ID",font=('calibre',20, 'bold'))
    name_vid=Label(rot,text ='ID', font=('calibre',16 ))
    Id=Entry(rot,textvariable=ID_int, font=('calibre',16))
    submit_btn=Button(rot,text="Submit",font=('calibre',16,"bold","underline"),relief=GROOVE,fg="white",bg="Navy blue",command=submit)
    msg.pack()
    name_vid.pack(side=LEFT)
    Id.pack(side=LEFT)
    submit_btn.pack(side=LEFT)
    
    
def submit():
    rot.destroy()
    exist=False
    ID1=ID_int.get()
    for row in cursor.execute('Select * from FACULTY where Faculty_Id=:record',{"record":ID1}):
        exist=True
    if exist==True:
        for row in cursor.execute('Select Name from FACULTY where Faculty_Id=:record',{"record":ID1}):
            d=''.join(row)
            d=d+" deleted successfully"
        for row in cursor.execute('Select * from FACULTY where Faculty_Id=:record',{"record":ID1}):
            cursor.execute('DELETE FROM FACULTY where Faculty_Id=:record',{"record":ID1})
            cursor.execute('DELETE FROM BALANCE where Faculty_Id=:record',{"record":ID1})
            cursor.execute('DELETE FROM STATUS where Faculty_Id=:record',{"record":ID1})
            cursor.execute('DELETE FROM Revoke where Faculty_Id=:record',{"record":ID1})
            cursor.execute('DELETE FROM Month where Faculty_Id=:record',{"record":ID1})
            cursor.execute('DELETE FROM Month1 where Faculty_Id=:record',{"record":ID1})
            cursor.execute('DELETE FROM WORKASSIGN where Faculty_Id=:record',{"record":ID1})
            conn.commit()
        root6=Toplevel()
        root6.geometry("400x80")
        msg=Label(root6,text=d,fg="green",font=('calibre',16, 'bold'),justify=CENTER)
        msg.pack()
        ok_btn=Button(root6,text="Ok",font=('calibre',12, 'bold','underline'),justify=CENTER,bg="blue",fg='white',command=root6.destroy)
        ok_btn.pack()
    else:
        rot.destroy()
        delete_option1()
    
root=Tk()
root.title("Leave Management System")
root.wm_attributes('-fullscreen', '1')
root.iconbitmap(default='leavelogo.ico')
Btnfont=Font(family="Callibry(body)",size=20)
path1="jkk.png"
path2="bg2.png"
path3="hh.jpg"
img = ImageTk.PhotoImage(p.open(path1))
img2 = ImageTk.PhotoImage(p.open(path2))
img3 = ImageTk.PhotoImage(p.open(path3))
label1=Label(image=img)
label1.place(x=0,y=0)
label2=Label(text="Faculty Leave Management System",borderwidth=13,relief=SUNKEN,fg='white',bg='navy',font=('Callibri',36,"bold"),pady=3)
label2.pack(pady=240)
Adminbutn=Button(text="Admin Login",bd=13,relief=SUNKEN,fg='white',bg='navy',command=adminvalidation,pady=2)
Adminbutn["font"]=Btnfont
Facultybutn=Button(text="Faculty\nRigistration",bd=13,relief=SUNKEN,fg='white',bg='navy',command=Faculty_registration,pady=2)
Facultybutn["font"]=Btnfont
Faculty_forget=Button(text="Forget\nPassword",bd=13,relief=SUNKEN,fg='white',bg='navy',command=Forget_Home,pady=2)
Faculty_forget["font"]=Btnfont
Facultyreg=Button(text="Faculty\nLogin",bd=13,relief=SUNKEN,fg='white',bg='navy',command=Faculty_Success,pady=2)
Facultyreg["font"]=Btnfont
Exit=Button(text="Exit",bd=13,relief=SUNKEN,fg='white',bg='navy',command=root.destroy,pady=2)
Exit["font"]=Btnfont
Adminbutn.place(relx = 0.5, rely = 0.43, anchor = CENTER)
Facultybutn.place(relx = 0.5, rely = 0.55, anchor = CENTER)
Faculty_forget.place(relx = 0.5, rely = 0.69, anchor = CENTER)
Facultyreg.place(relx = 0.5, rely = 0.83, anchor = CENTER)
Exit.place(relx = 0.5, rely = 0.95, anchor = CENTER)
root.geometry('150x150')
root.mainloop()



        
    
