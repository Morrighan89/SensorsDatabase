import sqlite3
conn=sqlite3.connect('tempDB.db')
curs=conn.cursor()

maxTemp = 27.6

print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM sensorsData"):
    print (row)

print ("\nDatabase entries for a specific humidity value:\n")
for row in curs.execute("SELECT * FROM sensorsData WHERE humidity='29'"):
    print (row)
    
print ("\nDatabase entries where the temperature is above 30oC:\n")
for row in curs.execute("SELECT * FROM sensorsData WHERE temperature>30.0"):
    print (row)
    
print ("\nDatabase entries where the temperature is above x:\n")
for row in curs.execute("SELECT * FROM sensorsData WHERE temperature>(?)", (maxTemp,)):
    print (row)

print ("\nDatabase entries where the temperature is above x:\n")
for row in curs.execute("SELECT * FROM sensorsData ORDER BY  tdata desc, ttime asc"):
    print (row)


