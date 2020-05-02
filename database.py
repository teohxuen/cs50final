from cs50 import SQL

# create database by opening it
open(f"fitness.db", "w").close()
db = SQL("sqlite:///fitness.db")

#create the tables
db.execute("CREATE TABLE 'users' (\
	'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	'name'	TEXT NOT NULL,\
	'birthday'	datetime NOT NULL,\
	'pushup'	INTEGER NOT NULL,\
	'situp'	INTEGER NOT NULL,\
	'run'	datetime NOT NULL,\
	'hash'	TEXT NOT NULL)")

db.execute('CREATE TABLE "ippt" (\
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	"userid"	INTEGER NOT NULL,\
	"date"	datetime,\
	"pushup"	INTEGER NOT NULL,\
	"situp"	INTEGER NOT NULL,\
	"run"	datetime NOT NULL,\
	"score" TEXT,\
	"notes"	TEXT,\
	FOREIGN KEY("userid") REFERENCES "users"("id"))')

db.execute('CREATE TABLE "history" (\
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	"exerciseid"	INTEGER NOT NULL,\
	"userid"	INTEGER NOT NULL,\
	"count"	REAL NOT NULL,\
	"notes"	TEXT,\
	"time"	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,\
	FOREIGN KEY("exerciseid") REFERENCES "exercises"("id"),\
	FOREIGN KEY("userid") REFERENCES "users"("id"))')

db.execute('CREATE TABLE "exercises" (\
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
	"name"	TEXT NOT NULL,\
	"desc"	TEXT,\
	"userid"	INTEGER NOT NULL,\
	"target"	REAL,\
	"date"	datetime,\
	FOREIGN KEY("userid") REFERENCES "users"("id"))')