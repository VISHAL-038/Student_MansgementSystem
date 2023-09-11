import os
import mysql.connector
import time
from datetime import datetime
from tabulate import tabulate

def display_menu():
    clr_scrn()
    print("1. Add Student Information.")
    print("2. Search Student")
    print("3. Delete Student Record.")
    print("4. Update Student Record.")
    print("5. View all Records.")
    print("6. promote to next class.")
    print("7. Quit")
    menu_choice= int(input("Enter Your Choice: "))
    if menu_choice==1:
        add_record()
    elif menu_choice==2:
        search_record()
    elif menu_choice==3:
        del_record()
    elif menu_choice==4:
        update_record()
    elif menu_choice==5:
        view_record()
    elif menu_choice==6:
        promote_student()
    elif menu_choice==7:
        clr_scrn()
        exit()
    else:
        print("invalid choice")
        display_menu()
        

def continue_menu():
    input("Press Enter to Continue to main menu.")
    display_menu()
        

def clr_scrn():
    os.system('cls' if os.name=='nt' else 'clear')
    print("*****Welcome to Student Management System*****")
    print("****SELECT THE OPTION AS PER REQUIREMENT*****")

def db_connect():
    global db
    global dbcsr
    db = mysql.connector.connect(host="localhost",charset='latin1', user="root", password="mysql", database="school")
    dbcsr = db.cursor()

def add_record():
    clr_scrn()
    print("+++++Enter Student Information+++++")
    name = input("Enter Student Name:")
    sclass = input("Enter class(1-12):")
    while(int(sclass) not in range(1,13)):
        print("Invalid Class Entered. Kindly Enter correct Class(1-12)")
        sclass = input("Enter class(1-12):")
    else:
        father_name = input("Enter Father Name:")
        mother_name = input("Enter Mother Name:")
        phone_no = input("Enter Phone_no:")
        address = input("Enter Address:")
        email_id = input("Enter Email_id:")
        reg_time = str(time.time())
        qry = "INSERT INTO student_management (id,Name,class,father_name,mather_name,phone_no,address,email_id,reg_date) VALUES(NULL,'"+name+"','"+sclass+"','"+father_name+"','"+mother_name+"','"+phone_no+"','"+address+"','"+email_id+"','"+reg_time+"')"
        db_connect()
        dbcsr.execute(qry)
        db.commit()
        print("+++++Students details saved successfully+++++")
        print("Registration Number is: ",dbcsr.lastrowid)
        continue_menu()


def search_record():
    clr_scrn()
    print("+++++Student  Search+++++")
    qry = "SELECT * FROM student_management"
    db_connect()
    dbcsr.execute(qry)
    dbcsr.fetchall()
    if(dbcsr.rowcount > 0):
        name = input("enter the name to be search;")
        rollno = input("enter roll no;")
        qry="SELECT * FROM student_management WHERE name='"+name+"' AND id='"+rollno+"'"
        dbcsr.execute(qry)
        data = dbcsr.fetchone()
        if(dbcsr.rowcount > 0):
            print("Student Details are")
            print("Registration Number: ",data[0])
            print("Name: ",data[1])
            if(int(data[2]) <=12):
                print("Class: ",data[2])
            else:
                print("Class: School Completed")
            print("Father's Name: ",data[3])
            print("Mother's Name: ",data[4])
            print("Phone No: ",data[5])
            print("Address: ",data[6])
            print("Email Id: ",data[7])
            print("Registration Date: ",datetime.utcfromtimestamp(float(data[8])).strftime('%d-%m-%Y %H:%M:%S'))
            continue_menu()
        else:
            print("Student Not found.")
            continue_menu()
    else:
        print("No record in the database. Add student reecords first")
        continue_menu()
        
    
def del_record():
    clr_scrn()
    print("+++++Delete Student Record+++++")
    qry = "SELECT * FROM student_management"
    db_connect()
    dbcsr.execute(qry)
    dbcsr.fetchall()
    if(dbcsr.rowcount > 0):
        name = input("enter the name to be delete;")
        rollno = input("enter roll number;")
        qry="DELETE FROM student_management WHERE name='"+name+"' AND id='"+rollno+"'"
        dbcsr.execute(qry)
        db.commit()
        if(dbcsr.rowcount == 1):
            print("Record deleted")
        else:
            print("Unable to delete")
        continue_menu()
    else:
        print("No record in the database. Add student reecords first")
        continue_menu()
        

def update_record():
    clr_scrn()
    print("+++++Insert Student Record+++++")
    qry = "SELECT * FROM student_management"
    db_connect()
    dbcsr.execute(qry)
    dbcsr.fetchall()
    if(dbcsr.rowcount > 0):
        name = input("enter the name to be UPDATE;")
        rollno = input("enter roll number;")
        qry="SELECT * FROM student_management WHERE name='"+name+"' AND id='"+rollno+"'"
        dbcsr.execute(qry)
        data = dbcsr.fetchone()
        if(dbcsr.rowcount > 0):
            print("1. Name")
            print("2. Class")
            print("3. Father's Name")
            print("4. Mother's Name")
            print("5. Phone Number")
            print("6. Address")
            print("7. Email")
            choice = int(input("Enter Field to Update: "))
            field = ""
            value = ""
            update = 0
            if choice == 1:
                value = input("Enter Name: ")
                field = "Name"
                update = 1
            elif choice == 2:
                value = input("Enter class: ")
                field = "class"
                update = 1
            elif choice == 3:
                value = input("Enter Father's name: ")
                field = "father_name"
                update = 1
            elif choice == 4:
                value = input("Enter Mother's name: ")
                field = "mother_name"
                update = 1
            elif choice == 5:
                value = input("Enter Phone Number: ")
                field = "phone_no"
                update = 1
            elif choice == 6:
                value = input("Enter address: ")
                field = "address"
                update = 1
            elif choice == 7:
                value = input("Enter Email: ")
                field = "email_id"
                update = 1
            else:
                print("Invalid choice Entered")
                update_record()
            if(update == 1):
                qry = "UPDATE student_management SET "+field+" = '"+value+"' WHERE name='"+name+"' AND id='"+rollno+"'"
                dbcsr.execute(qry)
                db.commit()
                if(dbcsr.rowcount == 1):
                    print("Record Updated")
                else:
                    print("Unable to Update")
            continue_menu()
        else:
            print("Student Not found.")
            continue_menu()
    else:
        print("No record in the database. Add student reecords first")
       

def view_record():
    clr_scrn()
    print("+++++View Student Records+++++")
    print("NOTE: Class 13 means Schooling Completed.")
    qry = "SELECT * FROM student_management"
    print(175*"-")
    #print("Roll No \t Name \t Father Name \t Mother Name \t Mobile \t Address \t Email ID \t Reg Date \t Result")
    #print(175*"-")
    db_connect()
    dbcsr.execute(qry)
    data = dbcsr.fetchall()
    data2 = []
    for i in data:
        i = list(i)
        i[8] = datetime.utcfromtimestamp(float(i[8])).strftime('%d-%m-%Y %H:%M:%S')
        data2.append(i)
    if(dbcsr.rowcount > 0):
        print(tabulate(data2,headers=["Roll No","Name","Class","Father Name","Mother Name","Mobile","Address","Email","Registration Date","Result"]))
#        for x in data:
#            print(x[0],'\t',x[1],'\t',x[2],'\t',x[3],'\t',x[4],'\t',x[5],'\t',x[6],'\t',x[7],'\t',x[8])
#            print(175*"-")
    else:
        print("No record in the database. Add student reecords first")
    continue_menu()

def promote_student():
    clr_scrn()
    print("+++++Promote Student++++")
    qry="SELECT * FROM student_management"
    db_connect()
    dbcsr.execute(qry)
    dbcsr.fetchall()
    if (dbcsr.rowcount > 0):
        roll = input('Enter Student Roll Number to promote; ')
        qry="SELECT * FROM student_management WHERE id ='"+roll+"'"
        dbcsr.execute(qry)
        data = dbcsr.fetchone()
        if (dbcsr.rowcount > 0):
            sclass = data[2]
            uclass = int(sclass)+1
            qry = "UPDATE student_management SET class='"+str(uclass)+"', result='pass' WHERE id='"+roll+"'"
            dbcsr.execute(qry)
            db.commit()
            if(dbcsr.rowcount == 1):
                if(sclass < 12):
                    print("Student Promoted to class ",uclass)
                else:
                    print("Schooling completed")
            else:
                print("Unable to Promote")
        else:
            print("Student Not Found")
        continue_menu()
    else:
        print("No record in the database. Add student reecords first")
    continue_menu()
display_menu()
