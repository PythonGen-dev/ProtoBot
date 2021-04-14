import psycopg2
import os
DATABASE_URL = os.environ['DATABASE_URL']
def opendatabase():
   con = psycopg2.connect(DATABASE_URL, sslmode='require')
   return con

def createtable(tablename, firstname, secondname, secondnametype = "TEXT", firstnametype = "TEXT"):
   con = opendatabase()
   cur = con.cursor()
   cur.execute("CREATE TABLE "+str(tablename)+" ("+str(firstname)+" "+str(firstnametype)+" NOT NULL, "+str(secondname)+" "+str(secondnametype)+");")
   con.commit()  
   con.close()

def inserttotable(tablename, firstname, firstnamevalue, secondname, secondnamevalue):
   con = opendatabase()
   cur = con.cursor()
   cur.execute("INSERT INTO "+str(tablename)+" ("+str(firstname)+","+str(secondname)+") VALUES ("+str(firstnamevalue)+", '"+str(secondnamevalue)+"')")
   con.commit()  
   con.close() 

def updaterow(tablename, firstname, firstnamevalue, secondname, secondnamevalue):
   con = opendatabase()
   cur = con.cursor()
   cur.execute("UPDATE "+str(tablename)+" set "+str(secondname)+" = "+secondnamevalue+" where "+firstname+" = "+str(firstnamevalue))  
   con.commit()  
   con.close()

def getrow(tablename, firstname, secondname, rowid):
   con = opendatabase()
   cur = con.cursor() 
   cur.execute("SELECT "+str(firstname)+", "+str(secondname)+"  from "+str(tablename))
   rows = cur.fetchall()
   data = None
   for I in rows:
      if I[0] == str(rowid):
         data = I
   if data == None: return("0")
   return(data)

def upsert(tablename, firstname, secondname, firstnamevalue, secondnamevalue):
   getdata = str(getrow(tablename=tablename, firstname=firstname, secondname = secondname, rowid=secondnamevalue))
   if getdata == "0":
      inserttotable(tablename, firstname, firstnamevalue, secondname, secondnamevalue)
   else:
      updaterow(tablename, firstname, firstnamevalue, secondname, secondnamevalue)
