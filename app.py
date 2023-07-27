from flask import Flask,redirect,request,url_for,render_template,session
import smtplib
import random

s= smtplib.SMTP('smtp.gmail.com',587)
s.starttls()

s.login("obulasaimochi@gmail.com","")
app = Flask(__name__)
import sqlite3
import pymysql.cursors
con = pymysql.connect(host='localhost',
                      user='root',
                      password='',
                      database='sms'
                      )

cursor = con.cursor()
app.secret_key="qwerty"



@app.route('/',methods=['GET','POST'])
def home():

        if("user" in session):
            students=[]
            data=[]
            id=set()
            branch=set()
            subjects=set()
            sql="select distinct id,branch,subject from students,faculty"
            cursor.execute(sql)
            var=cursor.fetchall()
            for i in var:
                students.append(i)
            for i in students:
                id.add(i[0])
                branch.add(i[1])
                subjects.add(i[2])
            std=len(id)
            sbj=len(subjects)
            brn=len(branch)


            return render_template("index.html",std=std,sbj=sbj,brn=brn)
        else:
            return redirect('/login')




@app.route('/login',methods=['POST','GET'])
def signin():
    if "fid" in session:
        return redirect('/')
    else:
        if(request.method=='POST'):
            session.permanent=True
            fid = request.form['fid']
            session['fid'] = fid
            password = request.form['password']
            l1=[]
            fids=[]
            sql="select fid from faculty"
            cursor.execute(sql)
            var1 = cursor.fetchall()
            for i in var1:
                l1.append(i)
            for i in l1:
                for j in i:
                    fids.append(str(j))
            
            if(fid in fids):
                sql = "select password from faculty where fid=(%s)"
                v = [fid]
                cursor.execute(sql,v)
                var = cursor.fetchone()
                password1 = var[0]
                if(password==password1):
                    return render_template('index.html')
                else:
                    msg="incorrect password !"
                    return render_template("login.html",msg=msg)
            else:
                msg="you have no account please create a new account !"
                return render_template("login.html",msg=msg)



    return render_template("login.html")

@app.route('/forgetpassword',methods=['POST','GET'])
def forgetpassword():
    if(request.method=='POST'):
            fid = request.form['fid']
            otp = request.form['otp']
            otp = str(otp)

            list=[1,2,3,4,5,6,7,8,9,0]
            s1=""
            for i in range(4):
                s1+=str(random.choice(list))
            if(len(otp)==0):
                sql = "select email from faculty where fid=(%s)"
                v = [fid]
                cursor.execute(sql,v)
                var = cursor.fetchone()
                email = var[0]
                email=str(email)
                msg = "Your Otp For Verification is {}".format(s1)
                session['otp1'] = s1
                session['email']=email
                s.sendmail("obulasaimochi@gmail.com",email,msg)
                s.quit()
                return render_template("forgetpassword.html",msg="OTP sent to registered email !")
            elif(otp == session['otp1']):
                session.pop('otp1',None)
                session['fid']=fid
                return redirect("/createpassword")
            elif(otp != session['otp1']):
                m="incorrect OTP !"
                return render_template("forgetpassword.html",msg=m)
            else:
                return redirect('/login')


    return render_template("forgetpassword.html")


@app.route('/logout')
def lagout():
    session.pop("fid",None)
    return redirect('/login')


@app.route('/register',methods=['POST','GET'])
def register():
    if(request.method=='POST'):
        fid =  request.form['fid']
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        password = request.form['password']
        email = str(email)
        l1=[]
        emails=[]
        sql="select email from faculty"
        cursor.execute(sql)
        var1 = cursor.fetchall()
        for i in var1:
            l1.append(i)
        for i in l1:
            for j in i:
                emails.append(str(j))
        if(email in emails):
            msg="you have already account please login !"
            return render_template('register.html',msg=msg)
        else:
            sql = "insert into faculty(fid,name,email,password,subject)values(%s,%s,%s,%s,%s)"
            l = [fid,name,email,password,subject]
            cursor.execute(sql,l)
            con.commit()
            session['fid']=fid
            return redirect('/')
    return render_template("register.html")






@app.route('/createpassword',methods=['POST','GET'])
def createpass():
    if(request.method=='POST'):
        password = request.form['password']
        password1 = request.form['password1']
        password=str(password)
        password1=str(password1)
        # try:
        if(password == password1):
            fid = session['fid']
            fid=str(fid)
            sql = "update `faculty` set `password`=(%s) where `fid` =(%s)"
            v=[password,fid]
            cursor.execute(sql,v)
            con.commit()
            session.pop("email",None)
            session.pop("otp1",None)

            return render_template("createpass.html",msg="your password changed successfully please signin !")
        else:
            return render_template("createpass.html",msg="passwords not matched !")
        # except:
        #     return redirect('/forgetpassword')
    return render_template("createpass.html")


#-----------------------------------------------------------------------------------------------------------------



@app.route('/students',methods=['POST','GET'])
def students():
    try:
        if request.method == 'POST':
            sid = request.form['sid']
            sname = request.form['sname']
            semail = request.form['semail']
            sbranch = request.form['sbranch']
            sphone = request.form['sphone']
            sgender = request.form['sgender']
            syear = request.form['syear']
            ssem = request.form['ssem']
            ssection = request.form['ssection']
            list=[]
            sql="select id from students"
            cursor.execute(sql)
            var = cursor.fetchall()
            for i in var:
                list.append(str(i))
            sql = '''insert into students(id,name,email,phone,gender,year,sem,section,branch)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            data = [sid,sname,semail,sphone,sgender,syear,ssem,ssection,sbranch]

            cursor.execute(sql,data)
            con.commit()
            return render_template("students.html",msg="student details inserted successfully")
    except:
        return render_template("students.html",msg="This id already registered")

    return render_template("students.html")

@app.route('/attendance',methods=['POST','GET'])
def attendance():
    if request.method == 'POST':
        sid = request.form['sid']
        percentage = request.form['percentage']
        sql = "update `students` set `attendance`=(%s) where `id` =(%s)"
        v=[percentage,sid]
        cursor.execute(sql,v)
        con.commit()
        return render_template("attendance.html",msg="attendance updated")
    return render_template("attendance.html")




@app.route('/details')
def details():
    details=[]
    sql="select * from students"
    cursor.execute(sql)
    var = cursor.fetchall()
    for i in var:
        details.append(list(i))
    return render_template("details.html",details=details)


@app.route('/edit/<id>',methods=['POST','GET'])
def edit(id):
    list1=[]
    sql="select * from students where `id`=(%s)"
    v=[id]
    cursor.execute(sql,v[0])
    var = cursor.fetchall()
    for i in var:
        list1.append(i)
    list2=[]
    for i in list1:
        for j in i:
            list2.append(j)
    if request.method == 'POST':
        sname = request.form['sname']
        semail = request.form['semail']
        sbranch = request.form['sbranch']
        sphone = request.form['sphone']
        sgender = request.form['sgender']
        syear = request.form['syear']
        ssem = request.form['ssem']
        ssection = request.form['ssection']
        spercentage = request.form['spercentage']
#        list2=["name","email","branch","phone","gender","year","sem","section","percentage"]
        cursor.execute(f"UPDATE `students` SET `name`='{sname}',`email`='{semail}',`branch`='{sbranch}',`gender`='{sgender}',`phone`='{sphone}',`year`='{syear}',`sem`='{ssem}',`attendance`='{spercentage}',`section`='{ssection}' where `id`='{id}'")
        # v="s"+i
        # data=[v,id]
        # cursor.execute(sql,data)
        con.commit()
        list3=[]
        sql1="select * from students where `id`=(%s)"
        v1=[id]
        cursor.execute(sql1,v1[0])
        var1 = cursor.fetchall()
        for i in var1:
            list3.append(i)
        list4=[]
        for i in list3:
            for j in i:
                list4.append(j)
        return render_template("edit.html",msg="details updated",list=list4)
    return render_template("edit.html",list=list2)


@app.route('/delete/<id>',methods=['POST','GET'])
def delete(id):
    list1=[]
    cursor.execute(f"delete from `students` where `id`='{id}'")
    con.commit()
    return redirect('/details')


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=='POST':
        id=request.form['sid']
        cursor.execute(f"select * from `students` where `id`='{id}'")
        var = cursor.fetchall()
        list=[]
        for i in var:
            list.append(i)
        list1=["id","name","email","phone","gender","year","semister","section","branch","attendance"]
        list2=[]
        for i in list:
            for j in i:
                list2.append(j)
        list.clear()
        list=list2
        
        return render_template("search.html",list=list,list1=list1,a=0)
    return render_template("search.html",list=[],list1=[],a=1)



@app.route('/inputtable',methods=['POST','GET'])
def inputtable():
    if request.method=='POST':
        sql1="truncate timetable"
        cursor.execute(sql1)
        a1=request.form['a1']
        a2=request.form['a2']
        a3=request.form['a3']
        a4=request.form['a4']
        a5=request.form['a5']
        a6=request.form['a6']
        b1=request.form['b1']
        b2=request.form['b2']
        b3=request.form['b3']
        b4=request.form['b4']
        b5=request.form['b5']
        b6=request.form['b6']
        c1=request.form['c1']
        c2=request.form['c2']
        c3=request.form['c3']
        c4=request.form['c4']
        c5=request.form['c5']
        c6=request.form['c6']
        d1=request.form['d1']
        d2=request.form['d2']
        d3=request.form['d3']
        d4=request.form['d4']
        d5=request.form['d5']
        d6=request.form['d6']
        e1=request.form['e1']
        e2=request.form['e2']
        e3=request.form['e3']
        e4=request.form['e4']
        e5=request.form['e5']
        e6=request.form['e6']
        f1=request.form['f1']
        f2=request.form['f2']
        f3=request.form['f3']
        f4=request.form['f4']
        f5=request.form['f5']
        f6=request.form['f6']


        a=[a1,a2,a3,a4,a5,a6]
        b=[b1,b2,b3,b4,b5,b6]
        c=[c1,c2,c3,c4,c5,c6]
        d=[d1,d2,d3,d4,d5,d6]
        e=[e1,e2,e3,e4,e5,e6]
        f=[f1,f2,f3,f4,f5,f6]

        data=[a,b,c,d,e,f]

        sql="insert into timetable(monday,tuesday,wednesday,thursday,friday,saturday) values(%s,%s,%s,%s,%s,%s)"   
        for i in data:
            cursor.execute(sql,i)     
        
        con.commit()
        
        return render_template("input_table.html",msg="Time Table Updated Successfully")

    return render_template("input_table.html")


@app.route('/timetable')
def table():
    sample=[]
    sql="select * from timetable"
    cursor.execute(sql)
    var = cursor.fetchall()
    for i in var:
        sample.append(i)
    if len(sample)==0:
        return redirect('/inputtable')
    a=sample[0]
    b=sample[1]
    c=sample[2]
    d=sample[3]
    e=sample[4]
    f=sample[5]
    return render_template("timetable.html",a=a,b=b,c=c,d=d,e=e,f=f)
    



con.commit()



if __name__ == "__main__":
    app.run(debug=True)

























# sql = '''create table `customers`(
# `cid` int(50) NOT NULL AUTO_INCREMENT,
# `username` varchar(255),
# `email` varchar(255),
# `password` varchar(255),
# `cart-items` varchar(20),
# PRIMARY KEY(cid)
# )
# '''