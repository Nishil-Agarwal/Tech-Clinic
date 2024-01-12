#Connecting to mySQL client :---------------------------------------------------------------------------

import pymysql as pm
conobj=pm.connect(
    host='localhost',
    user='root',
    passwd='Nishil12#'
    )
mycur=conobj.cursor()

#Pre-Requisites :---------------------------------------------------------------------------------------

try:
    #Creating the 3 data tables within the project database
    mycur.execute("create database if not exists Cs_project;")
    mycur.execute("use Cs_project;")
    mycur.execute("create table if not exists patients(Patient_ID varchar(100) UNIQUE,Patient varchar(255), Age varchar(200), Gender varchar(100), Last_Visit varchar(255), Address varchar(255));")
    mycur.execute("create table if not exists problems(Patient_ID varchar(100) UNIQUE,Symptoms varchar(255),Prescription varchar(255), Allergy varchar(255));")
    mycur.execute("create table if not exists collections(Date varchar(255), Collection int(11));")
    conobj.commit()
except Exception as e:
    print(e)
    
#SQL Functions :----------------------------------------------------------------------------------------

def curdate():
    #Fetches current date of laptop
    mycur.execute('select curdate()')
    return str(mycur.fetchall()[0][0])
    #double [0][0] required as fetchall returns a tuple containing a tuple which in turn stores date in tuple format (^~^)

def register(name,id,age, gender, address, allergies, symptoms, prescription, fee):
    #To register a new patient into the database using phone number as key/id
    date=curdate()
    sql1="insert into patients values(%s,%s,%s,%s,%s,%s)"
    sql2="insert into problems values(%s,%s,%s,%s)"
    sql3="insert into collections values(%s,%s)"
    patients=(id,name,age,gender,date,address)
    problems=(id,symptoms,prescription,allergies)
    if fee=="":fee=0
    collections=(date,int(fee))
    mycur.execute(sql1,patients)
    mycur.execute(sql2,problems)
    mycur.execute(sql3,collections)
    conobj.commit()

def update_dat(name,id,age, gender, address, allergies, symptoms, prescription, fee):
    #To update selected patient details in the database using phone number as key/id
    date=curdate()
    d={"patient":name,"age":age,"gender":gender,"address":address,"allergy":allergies,"symptoms":symptoms,"prescription":prescription,"collection":fee,"last_visit":date}
    for i in d:
        if d[i]!="":                  #To not replace existing entries by blanks
            try:
                x=(d[i],id)
                st="update patients set "+i+"=%s where patient_id=%s;" #To prevent error if field not exist int his specific table
                mycur.execute(st,x)
                conobj.commit()
            except:
                try:
                    x=(d[i],id)
                    st="update problems set "+i+"=%s where patient_id=%s;"
                    mycur.execute(st,x)
                    conobj.commit()
                except:
                    pass
    if fee=="":       #handling empty fee field
        fee=0
    x=(date,int(fee))
    st="insert into collections values(%s,%s)"
    mycur.execute(st,x)
    conobj.commit()

def records_id(id):
    #Searching for record details by id/phone number of patient
    x=(id,id)
    st="select patient,patients.Patient_id,age,gender,address,allergy,symptoms,prescription from patients,problems where patients.Patient_ID=%s and problems.Patient_ID=%s"
    #Ensuring that ID same = enough for all details
    mycur.execute(st,x)
    l=list(mycur.fetchall())
    return l

def records_name(name):
    #Searching for record details by name of patient
    st="select patient,patients.Patient_id,age,gender,address,allergy,symptoms,prescription from patients,problems where patients.Patient like '%{}%' and problems.Patient_id=patients.patient_id order by Last_visit".format(name)
    #Used name match condition
    mycur.execute(st)
    l=list(mycur.fetchall())
    return l

def records_symptoms(symptom):
    #Searching for record details by matching symptoms
    st="select patient,patients.Patient_id,age,gender,address,allergy,symptoms,prescription from patients,problems where problems.symptoms like '%{}%' and problems.Patient_ID=patients.patient_id order by Last_visit".format(symptom)
    #Used like operator to search for specific symptom in a sea of symptoms for a specific person
    #Had touse format else %%s% not work due to % sign confusion
    mycur.execute(st)
    l=list(mycur.fetchall())
    return l

def visit7():
    #returns lists of details of all patients who have visited in last 7 days
    mycur.execute("select curdate() - interval 7 day;")         #'- Interval x day' is command to get the date of day x number of days before a given date
    date=mycur.fetchall()[0][0]
    st="select patient,patients.Patient_id,age,gender,address,allergy,symptoms,prescription from patients,problems where patients.last_visit>=%s and problems.Patient_ID=patients.patient_id order by Last_visit"
    #Using last visit within specified range of date to get only recent visitors
    mycur.execute(st,date)
    l=list(mycur.fetchall())
    return l

def money(start,stop):
    #Returns money earned in specified duration

    ################Enter money only in YYYY-MM-DD#####################

    x=(start,stop)
    st='select sum(Collection) from collections where date between %s and %s'
    #Collection was stored as int data type hence can directly add
    mycur.execute(st,x)
    l=mycur.fetchall()[0][0]
    #Double [0][0] required as fetchall returns tuple even if only a single element!
    #This sum came attached with details like decimal data type etc.(In form of a tuple). So had to extract it
    return l

def database_dat():
    #Returns list of detaisl of all patients in the database
    st="select patient,patients.Patient_id,age,gender,address,allergy,symptoms,prescription from patients,problems where problems.Patient_ID=patients.patient_id order by Last_visit"
    #Id same =sufficient condition to extract data
    mycur.execute(st)
    l=list(mycur.fetchall())
    return l
        
def age_dat(start,stop):
    #Tells number of patients in specified age group who visited in the last 30 days
    x=(start,stop)
    st='select * from patients where Age>=%s and Age<%s and last_visit>=(select curdate() - interval 30 day);'
    #Using interval command to fetch data of only last 30 days
    #select * or some specific field doesn't matter as we just have to count the number of entries satisfying the condition.
    mycur.execute(st,x)
    n=mycur.rowcount
    return n

#Getting started :---------------------------------------------------------------------------------------
from tkinter import *
import math
ini=Tk()
ini.geometry("260x140")
ini.title("User Verification")
ini.resizable(0,0)
backg=PhotoImage(file=r"C:\Users\nishi\Vs_Code_Projects\IIITD\Resources\Previous_Sems\SEM_1\IP\Assignments\Assignment3_Bonus_2022334_Nishil_Agarwal\Background.png")
bg=Label(ini, image = backg)        #Attaching image as label at pixel position 0,0
bg.place(x=0,y=0)


#Password Verification :---------------------------------------------------------------------------------
b=""
def go():# we cant close it else will stop working
    global b
    b=a.get()
    ini.destroy()
a=StringVar(ini)
label1=Label(ini,text="Password :",font=("Calibri 15 bold"),bg="#DBF3FA")
ent=Entry(ini, textvariable=a)
b1=Button(ini,text="SUBMIT", height=1, width=10 ,bg="#A44801", borderwidth=4,command=go,font="Calibri 15 bold")
label1.place(x=70,y=20)
ent.place(x=60,y=50)
b1.place(x=65,y=85)
ini.mainloop()       #Starting at password screen
if b=="abcd":
    #On submit button click, pervious window gets destroyed and new one creation on correct password:-
    root=Tk()
    root.geometry("950x660")
    root.title("CS Project 2021-2022")
    backg=PhotoImage(file=r"C:\Users\nishi\Vs_Code_Projects\IIITD\Resources\Previous_Sems\SEM_1\IP\Assignments\Assignment3_Bonus_2022334_Nishil_Agarwal\Background.png")
    bg=Label(root, image = backg)
    bg.place(x=0,y=0)


#Functions Tkinter :-------------------------------------------------------------------------------------

    def create():
        #Gui button code to register a patient on click and if all the details have been filled properly
        global pname,id,age,gender,address,allergies,symptoms,notes,fee
        def back():
            top.destroy()
            top.update()
        b=True                                     #Name and symptoms can't be empty
        if pname.get()=="" or symptoms.get()=="":
            b=False
        elif id.get()=="":                         #ID can't be blank
            a=False
        else:
            try:
                register(pname.get(),id.get(),age.get(),gender.get(),address.get(),allergies.get(),symptoms.get(),notes.get(),fee.get())
                #Code to add details to table, and add up the fee to according currdate-fee table
                pass
            except Exception as e:
                a=False               #Repeated id not allowed, in case same patient, update pateint instead
                print(e)
            else:
                a=True
        
     #Code for user confirmation :-
        top=Toplevel()         #To create dialogue box
        top.geometry("210x100")
        top.title("Confirmation")
        top.resizable(0,0)
        global backg
        bg=Label(top, image=backg)    
        bg.place(x=0,y=0)
        if b==False:       #Empty symptom/name error
            label=Label(top,text="Name/symptoms empty!",font=("Calibri 15 bold"),bg="#DBF3FA")
        elif a==True:
            label=Label(top,text="SUCCESS",font=("Calibri 15 bold"),bg="#DBF3FA")
        #Code to make entries fields empty after task is done for next patient
            ent1.delete(0,END),ent2.delete(0,END),ent3.delete(0,END),ent4.delete(0,END),ent5.delete(0,END),ent6.delete(0,END),ent7.delete(0,END),ent8.delete(0,END),ent10.delete(0,END)
            ent1.insert(0,""),ent2.insert(0,""),ent3.insert(0,""),ent4.insert(0,""),ent5.insert(0,""),ent6.insert(0,""),ent7.insert(0,""),ent8.insert(0,""),ent10.insert(0,"")

        else:        #Incorrect id/missing id error
            label=Label(top,text="Check ID",font=("Calibri 15 bold"),bg="#DBF3FA")
        #Back button code which is common to popup of all 3 cases
        b1=Button(top,text="Close",command=back,bg="#A44801",font=("Calibri 15 bold"))
        if b==False:
            label.place(x=0,y=10)
        else:
            label.place(x=65,y=10)
        b1.place(x=75,y=50)
    def update():
        #Gui button code to update a patient detials on click using id
        global pname,id,age,gender,address,allergies,symptoms,notes,fee
        details=[pname.get(),id.get(),age.get(),gender.get(),address.get(),allergies.get(),symptoms.get(),notes.get(),fee.get()]
        def back():
            top.destroy()
            top.update()
        
        b=True                 #Id must be entered and not empty
        if details[1]=="":
            b=False
        
        try:
            update_dat(pname.get(),id.get(),age.get(),gender.get(),address.get(),allergies.get(),symptoms.get(),notes.get(),fee.get())
            #Code to search according to id(unchangeable) and replace all details which are not ""
        except Exception as e:
            a=False
            print(e)
        else:
            a=True

     #Code for confirmation :-
        top=Toplevel()
        top.geometry("200x100")
        top.title("Confirmation")
        top.resizable(0,0)
        global backg
        bg=Label(top, image=backg)    
        bg.place(x=0,y=0)
        if a==True and b==True:
            label=Label(top,text="SUCCESS",font=("Calibri 15 bold"),bg="#DBF3FA")
         #Code to make entries empty -
            ent1.delete(0,END),ent2.delete(0,END),ent3.delete(0,END),ent4.delete(0,END),ent5.delete(0,END),ent6.delete(0,END),ent7.delete(0,END),ent8.delete(0,END),ent10.delete(0,END)
            ent1.insert(0,""),ent2.insert(0,""),ent3.insert(0,""),ent4.insert(0,""),ent5.insert(0,""),ent6.insert(0,""),ent7.insert(0,""),ent8.insert(0,""),ent10.insert(0,"")

        else:       #Incorrect id/missing id error
            label=Label(top,text="Check ID",font=("Calibri 15 bold"),bg="#DBF3FA")
        b1=Button(top,text="Close",command=back,bg="#A44801",font=("Calibri 15 bold"))
        label.place(x=65,y=10)
        b1.place(x=75,y=50)
    def search_pg():
        #Code for search window accroding to various options
        top=Toplevel()
        top.geometry("950x650")
        top.title("CS Project 2021-2022")
        top.resizable(0,0)
        global backg                        #Image must be assigned globally else python has no means to store it
        bg=Label(top, image=backg)    
        bg.place(x=0,y=0)
        #Functions :-
        def back():
            top.destroy()
            top.update()
        def sid():
            #Function to search for patient through id provided and display records found in a table form
            top=Toplevel()
            top.geometry("1254x670")
            top.title("CS Project 2021-2022")
            top.resizable(0,0)
            global backg
            bg=Label(top, image=backg)    
            bg.place(x=0,y=0)
            frame=Frame(top)
            frame.place(x=0,y=0)
            
            data=records_id(value.get())
            #Recieve list of relevant data
            
            #Display Code :-
            start=0
            stop=6              #Showing only 6 records at a time to simulate scrolling/different pages
            def show():
                global backg
                bag=Label(frame, image=backg)
                bag.place(x=0,y=0)
                headers=["Patient name","ID","Age","Gender","Address","Allergies","Symptoms","Prescription"]
                for i in range(len(headers)):
                    if i==7:       #Specifically making prescription field larger in size to accomodate large amounts of text
                        label=Label(frame, text=headers[i], width=35, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                    else:
                        label=Label(frame, text=headers[i], width=12, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                active_data=data[start:stop]      #6 records only
                for i in range(len(active_data)): 
                    for j in range(len(data[i])):
                        if j==7:
                            label = Label(frame, text=data[start+i][j], width=35,height=math.ceil(len(data[start+i][j])/35), fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=325) 
                            label.grid(row=i+2, column=j) 
                        else:
                            label = Label(frame, text=data[start+i][j],height= math.ceil(len(data[start+i][j])/12),width=12, fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=115) 
                            label.grid(row=i+2, column=j) 
            def nex():
                #Button code to show only 6 records at a time and show next 6 only on clicking of button
                nonlocal stop,start
                start+=6
                stop+=6
                #Erase screen's data :-
                for widget in frame.winfo_children():   #Lists all widgets on current level window
                    widget.destroy()
                show()
            but=Button(top,text="Next 6 records", height=1, width=15,bg="#A44801", borderwidth=3,command=nex,font="Calibri 13 bold")
            show()
            but.place(x=20,y=600) 
        def sname():
            #Function to search for patient through name provided and display records found in a table form
            top=Toplevel()
            top.geometry("1254x670")
            top.title("CS Project 2021-2022")
            top.resizable(0,0)
            global backg
            bg=Label(top, image=backg)    
            bg.place(x=0,y=0)
            frame=Frame(top)
            frame.place(x=0,y=0)    

            data=records_name(value.get())
            #Recieve list of relevant data
            
            #Display Code :-
            start=0
            stop=6
            def show():
                global backg
                bag=Label(frame, image=backg)
                bag.place(x=0,y=0)
                headers=["Patient name","ID","Age","Gender","Address","Allergies","Symptoms","Prescription"]
                for i in range(len(headers)):
                    if i==7:
                        label=Label(frame, text=headers[i], width=35, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                    else:
                        label=Label(frame, text=headers[i], width=12, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                active_data=data[start:stop]
                for i in range(len(active_data)): 
                    for j in range(len(data[i])):
                        if j==7:
                            label = Label(frame, text=data[start+i][j], width=35,height=math.ceil(len(data[start+i][j])/35), fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=325) 
                            label.grid(row=i+2, column=j) 
                        else:
                            label = Label(frame, text=data[start+i][j],height= math.ceil(len(data[start+i][j])/12),width=12, fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=115) 
                            label.grid(row=i+2, column=j) 
            def nex():
                nonlocal stop,start
                start+=6
                stop+=6
                #Erase screen's data :-
                for widget in frame.winfo_children():
                    widget.destroy()
                show()
            but=Button(top,text="Next 6 records", height=1, width=15,bg="#A44801", borderwidth=3,command=nex,font="Calibri 13 bold")
            show()
            but.place(x=20,y=600)
        def ssymptom():
            #Searching for entries as per symptoms matched
            top=Toplevel()
            top.geometry("1254x670")
            top.title("CS Project 2021-2022")
            top.resizable(0,0)
            global backg
            bg=Label(top, image=backg)    
            bg.place(x=0,y=0)
            frame=Frame(top)
            frame.place(x=0,y=0)    

            data=records_symptoms(value.get())
            #Recieve list of relevant data
            
            #Display Code :-
            start=0
            stop=6
            def show():
                global backg
                bag=Label(frame, image=backg)
                bag.place(x=0,y=0)
                headers=["Patient name","ID","Age","Gender","Address","Allergies","Symptoms","Prescription"]
                for i in range(len(headers)):
                    if i==7:
                        label=Label(frame, text=headers[i], width=35, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                    else:
                        label=Label(frame, text=headers[i], width=12, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                active_data=data[start:stop]
                for i in range(len(active_data)): 
                    for j in range(len(data[i])):
                        if j==7:
                            label = Label(frame, text=data[start+i][j], width=35,height=math.ceil(len(data[start+i][j])/35), fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=325) 
                            label.grid(row=i+2, column=j) 
                        else:
                            label = Label(frame, text=data[start+i][j],height= math.ceil(len(data[start+i][j])/12),width=12, fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=115) 
                            label.grid(row=i+2, column=j) 
            def nex():
                nonlocal stop,start
                start+=6
                stop+=6
                #Erase screen's data :-
                for widget in frame.winfo_children():
                    widget.destroy()
                show()
            but=Button(top,text="Next 6 records", height=1, width=15,bg="#A44801", borderwidth=3,command=nex,font="Calibri 13 bold")
            show()
            but.place(x=20,y=600)
     #Master Window for search options :-
        #Elements :-
        a=StringVar(top)
        label1=Label(top, text="TECH CLINIC", bg="#DBF3FA",fg="purple", font=("Bahnschrift 72 underline"))
        label2=Label(top, text="SEARCH OPTIONS", bg="white",fg="black", font=("Bahnschrift 30 underline bold"))
        label15=Label(top, text="Value :",bg="light grey",fg="Black", font=("Bahnschrift 20 bold"))
        value=StringVar(top)
        ent15=Entry(top,textvariable=value)
        b1=Button(top,text="Search by ID", height=2, width=20 ,bg="#A44801", borderwidth=4,command=sid,font=("Calibri 18 bold"))
        b2=Button(top,text="Search by Name", height=2, width=20 ,bg="#A44801", borderwidth=4,command=sname,font=("Calibri 18 bold"))
        b3=Button(top,text="Search by Symptom", height=2, width=20 ,bg="#A44801", borderwidth=4,command=ssymptom,font=("Calibri 18 bold"))
        b4=Button(top,text="Back", height=2, width=8 ,bg="#A44801", borderwidth=4,command=back,font=("Calibri 14 bold"))
        #Placing :-
        label1.place(x=200, y=0)
        label2.place(x=305, y=150)
        label15.place(x=325,y=550)
        ent15.place(x=420,y=555,height=30,width=300)
        b1.place(x=325,y=225)
        b2.place(x=325,y=325)
        b3.place(x=325,y=425)
        b4.place(x=830,y=555)     
    def reports_pg():
        #Code for reports window with all its various options
        top=Toplevel()
        top.geometry("950x650")
        top.title("CS Project 2021-2022")
        top.resizable(0,0)
        global backg
        bg=Label(top, image=backg)    
        bg.place(x=0,y=0)
        #Functions :-
        def back():
            top.destroy()
            top.update()
        def visits():
            #To display records of all patients who have visited in last 7 days
            top=Toplevel()
            top.geometry("1254x670")
            top.title("CS Project 2021-2022")
            top.resizable(0,0)
            global backg
            bg=Label(top, image=backg)    
            bg.place(x=0,y=0)
            frame=Frame(top)
            frame.place(x=0,y=0)    

            data=visit7()
            #Recieve list of relevant data
            
            #Display Code :-
            start=0
            stop=6
            def show():
                global backg
                bag=Label(frame, image=backg)
                bag.place(x=0,y=0)
                headers=["Patient name","ID","Age","Gender","Address","Allergies","Symptoms","Prescription"]
                for i in range(len(headers)):
                    if i==7:
                        label=Label(frame, text=headers[i], width=35, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                    else:
                        label=Label(frame, text=headers[i], width=12, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                        label.grid(row=1,column=i)
                active_data=data[start:stop]
                for i in range(len(active_data)): 
                    for j in range(len(data[i])):
                        if j==7:
                            label = Label(frame, text=data[start+i][j], width=35,height=math.ceil(len(data[start+i][j])/35), fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=325) 
                            label.grid(row=i+2, column=j) 
                        else:
                            label = Label(frame, text=data[start+i][j],height= math.ceil(len(data[start+i][j])/12),width=12, fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=115) 
                            label.grid(row=i+2, column=j) 
            def nex():
                nonlocal stop,start
                start+=6
                stop+=6
                #Erase screen's data :-
                for widget in frame.winfo_children():
                    widget.destroy()
                show()
            but=Button(top,text="Next 6 records", height=1, width=15,bg="#A44801", borderwidth=3,command=nex,font="Calibri 13 bold")
            show()
            but.place(x=20,y=600) 
        def earn():
            #To open popup window which tells total earnings in a specific duration
            top=Toplevel()
            def back():
                top.destroy()
                top.update()
            top.geometry("280x180")
            top.title("CS Project 2021-2022")
            top.resizable(0,0)
            global backg
            bg=Label(top, image=backg)    
            bg.place(x=0,y=0)
            #Display Code :-
            start=StringVar(top)
            stop=StringVar(top)
            label1=Label(top,text="From:",font=("Calibri 15 bold"),bg="#DBF3FA")
            label2=Label(top,text="To :",font=("Calibri 15 bold"),bg="#DBF3FA")
            fent=Entry(top, textvariable=start)
            tent=Entry(top, textvariable=stop)

            def submit():
                To,From=fent.get(),tent.get()
                data=str(money(To,From))#Code to get list of all relevant data's sum
                label3=Label(top,text=("Collected fee :"+data),font=("Calibri 15 bold"),bg="#DBF3FA")
                label3.place(x=35,y=85)

            b0=Button(top,text="Submit",command=submit,bg="#A44801",font=("Calibri 15 bold"))
            b1=Button(top,text="Close",command=back,bg="#A44801",font=("Calibri 15 bold"))
            label1.place(x=10,y=10)
            label2.place(x=10,y=45)
            fent.place(x=70,y=10, height=28)
            tent.place(x=70,y=45, height=28)
            b0.place(x=200,y=17)
            b1.place(x=115,y=135)
        def insight():
            #To open pop-up display showing how many patients from which age group have visited
            top=Toplevel()
            top.geometry("255x155")
            top.title("CS Project 2021-2022")
            top.resizable(0,0)
            global backg
            bg=Label(top, image=backg)    
            bg.place(x=0,y=0)
            #Display Code :-
            headers=["Age group","Frequency"]
            for i in range(len(headers)):
                label=Label(top, text=headers[i], width=12, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                label.grid(row=1,column=i)
            headers2=["0-10","10-30","30-60","60+"]
            for i in range(len(headers2)):
                label=Label(top, text=headers2[i], width=12, fg='black',font="Calibri 14",borderwidth=3,relief="solid") 
                label.grid(row=i+2,column=0)
            val1=age_dat('0','10')#Frequency of visit in current month of age grp 0-10
            val2=age_dat('10','30')#Frequency of visit in current month of age grp 10-30
            val3=age_dat('30','60')#Frequency of visit in current month of age grp 30-60
            val4=age_dat('60','200')#Frequency of visit in current month of age grp 60+
            values=[val1,val2,val3,val4]
            for i in range(len(values)):
                label=Label(top, text=values[i], width=12, fg='black',font="Calibri 14",borderwidth=1,relief="solid") 
                label.grid(row=i+2,column=1)
     #Master Window for report options :-
        #Elements :-
        label1=Label(top, text="TECH CLINIC", bg="#DBF3FA",fg="purple", font=("Bahnschrift 72 underline"))
        label2=Label(top, text="REPORTS OPTIONS", bg="white",fg="black", font=("Bahnschrift 30 underline bold"))
        b1=Button(top,text="Recent Patient Visits", height=2, width=25 ,bg="#A44801", borderwidth=4,command=visits,font=("Calibri 16 bold"))
        b2=Button(top,text="Earnings in Specific Duration", height=2, width=25 ,bg="#A44801", borderwidth=4,command=earn,font=("Calibri 16 bold"))
        b3=Button(top,text="Patient's age group insight", height=2, width=25 ,bg="#A44801", borderwidth=4,command=insight,font=("Calibri 16 bold"))
        b4=Button(top,text="Back", height=2, width=8 ,bg="#A44801", borderwidth=4,command=back,font=("Calibri 14 bold"))
        #Placing :-
        label1.place(x=200, y=0)
        label2.place(x=305, y=150)
        b1.place(x=325,y=225)
        b2.place(x=325,y=325)
        b3.place(x=325,y=425)
        b4.place(x=830,y=555)
    def database():
        #To display all records of database 6 at a time in table
        top=Toplevel()
        top.geometry("1254x670")
        top.title("CS Project 2021-2022")
        global backg
        bg=Label(top, image=backg)    
        bg.place(x=0,y=0)
        frame=Frame(top)
        frame.place(x=0,y=0)    

        data=database_dat()
        #Recieve list of relevant data
        
        #Display Code :-
        start=0
        stop=6
        def show():
            global backg
            bag=Label(frame, image=backg)
            bag.place(x=0,y=0)
            headers=["Patient name","ID","Age","Gender","Address","Allergies","Symptoms","Prescription"]
            for i in range(len(headers)):
                if i==7:
                    label=Label(frame, text=headers[i], width=35, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                    label.grid(row=1,column=i)
                else:
                    label=Label(frame, text=headers[i], width=12, fg='black',font="Calibri 14 bold",borderwidth=3,relief="solid") 
                    label.grid(row=1,column=i)
            active_data=data[start:stop]
            for i in range(len(active_data)): 
                for j in range(len(data[i])):
                    if j==7:
                        label = Label(frame, text=data[start+i][j], width=35,height=math.ceil(len(data[start+i][j])/35), fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=325) 
                        label.grid(row=i+2, column=j) 
                    else:
                        label = Label(frame, text=data[start+i][j],height= math.ceil(len(data[start+i][j])/12),width=12, fg='black',font="Calibri 14",borderwidth=1,relief="solid",wraplength=115) 
                        label.grid(row=i+2, column=j) 
        def nex():
            nonlocal stop,start
            start+=6
            stop+=6
            #Erase screen's data :-
            for widget in frame.winfo_children():
                widget.destroy()
            show()
        but=Button(top,text="Next 6 records", height=1, width=15,bg="#A44801", borderwidth=3,command=nex,font="Calibri 13 bold")
        show()
        but.place(x=20,y=600)
    def end():
        root.quit()

#Coding elements Home Page :------------------------------------------------------------------------------
    # Variables :-
    pname=StringVar(root)
    id=StringVar(root)
    age=StringVar(root)
    gender=StringVar(root)
    address=StringVar(root)
    allergies=StringVar(root)
    symptoms=StringVar(root)
    notes=StringVar(root)
    fee=StringVar(root)

    # Display elements :-
    label=Label(root, text="TECH CLINIC", bg="#DBF3FA",fg="purple", font=("Bahnschrift 72 underline"))
    label1=Label(root, text="Patient Name :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label2=Label(root, text="Ph. number/ID :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label3=Label(root, text="Age :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label4=Label(root, text="Gender :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label5=Label(root, text="Address :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label6=Label(root, text="Allergies :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label7=Label(root, text="Symptoms :",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label8=Label(root, text="Prescriptions :\nand notes",bg="light grey",fg="Black", font=("Calibri 15 bold"))
    label10=Label(root, text="Fee :",bg="light grey",fg="Black", font=("Calibri 15 bold"))

    # Input fields :-
    ent1=Entry(root, textvariable=pname)
    ent2=Entry(root, textvariable=id)
    ent3=Entry(root, textvariable=age)
    ent4=Entry(root, textvariable=gender)
    ent5=Entry(root, textvariable=address)
    ent6=Entry(root, textvariable=allergies)
    ent7=Entry(root, textvariable=symptoms)
    ent8=Entry(root, textvariable=notes)
    ent10=Entry(root, textvariable=fee)

    # Buttons :-
    b1=Button(root,text="Create New Patient", height=2, width=25,bg="#A44801", borderwidth=4,command=create,font="Calibri 15 bold")
    b2=Button(root,text="Update Patient", height=2, width=25,bg="#A44801", borderwidth=4,command=update,font="Calibri 15 bold")
    b3=Button(root,text="Search Patient", height=2, width=25,bg="#A44801", borderwidth=4,command=search_pg,font="Calibri 15 bold")
    b4=Button(root,text="Generate Reports", height=2, width=25,bg="#A44801", borderwidth=4,command=reports_pg,font="Calibri 15 bold")
    b5=Button(root,text="Display database", height=2, width=15 ,bg="#A44801", borderwidth=4,command=database,font="Calibri 15 bold")
    b6=Button(root,text="EXIT", height=2, width=10 ,bg="#A44801", borderwidth=4,command=end,font="Calibri 15 bold")


#Placing elements :---------------------------------------------------------------------------------------
    # Display elements :-
    label.place(x=225, y=0)
    label1.place(x=30, y=170)
    label2.place(x=30, y=220)
    label3.place(x=30, y=270)
    label4.place(x=30, y=320)
    label5.place(x=30, y=370)
    label6.place(x=30, y=420)
    label7.place(x=30, y=470)
    label8.place(x=30, y=520)#570
    label10.place(x=30, y=600)

    # Input fields :-
    ent1.place(x=180, y=170, height=28, width = 450)
    ent2.place(x=180, y=220, height=28, width = 450)
    ent3.place(x=180, y=270, height=28, width = 450)
    ent4.place(x=180, y=320, height=28, width = 450)
    ent5.place(x=180, y=370, height=28, width = 450)
    ent6.place(x=180, y=420, height=28, width = 450)
    ent7.place(x=180, y=470, height=28, width = 450)
    ent8.place(x=180, y=520, height=50, width = 450)
    ent10.place(x=180, y=600, height=28, width = 450)

    # Buttons :-
    b1.place(x=660, y=150)
    b2.place(x=660, y=230)
    b3.place(x=660, y=310)
    b4.place(x=660, y=390)
    b5.place(x=760, y=500)
    b6.place(x=810, y=580)


#Closure:------------------------------------------------------------------------------------------------
    root.resizable(0,0)
    root.mainloop()