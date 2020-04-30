from cs50 import SQL

# create database by opening it
open(f"fitness.db", "w").close()
db = SQL("sqlite:///fitness.db")

#create the tables
db.execute("CREATE TABLE 'user' (\
	'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	'name'	TEXT NOT NULL,\
	'birthday'	datetime NOT NULL,\
	'pushup'	INTEGER NOT NULL,\
	'situp'	BLOB NOT NULL,\
	'run'	datetime NOT NULL,\
	'username'	TEXT,\
	'hash'	TEXT)")

db.execute('CREATE TABLE "ippt" (\
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	"userid"	INTEGER NOT NULL,\
	"date"	datetime NOT NULL,\
	"pushup"	INTEGER NOT NULL,\
	"situp"	INTEGER NOT NULL,\
	"run"	datetime NOT NULL,\
	"notes"	TEXT,\
	FOREIGN KEY("userid") REFERENCES "user"("id"))')

db.execute('CREATE TABLE "history" (\
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	"exerciseid"	INTEGER NOT NULL,\
	"userid"	INTEGER NOT NULL,\
	"count"	REAL NOT NULL,\
	"notes"	TEXT,\
	"time"	datetime NOT NULL,\
	FOREIGN KEY("exerciseid") REFERENCES "exercises"("id"),\
	FOREIGN KEY("userid") REFERENCES "user"("id"))')

db.execute('CREATE TABLE "exercises" (\
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	"name"	TEXT NOT NULL,\
	"desc"	TEXT,\
	"userid"	INTEGER NOT NULL,\
	"target"	REAL NOT NULL,\
	"date"	datetime NOT NULL,\
	"favourite"	BLOB NOT NULL,\
	FOREIGN KEY("userid") REFERENCES "user"("id"))')