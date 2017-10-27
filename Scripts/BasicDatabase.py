import psycopg2
import json
import os

def PollDatabaseJustState(state):
	conn = psycopg2.connect( host=os.environ['HostName'], user=os.environ['UserName'], password=os.environ['password'], dbname=os.environ['DataBase'])
	cur = conn.cursor()
	cur.execute("SELECT * FROM politicians WHERE state='%s'" %(state))
	result = cur.fetchall()
	for pol in result:
		print("Name: " + pol[1])
		print("Party: " +pol[2])
		print("Chamber: " + pol[3])
		print("Twitter: "+pol[6])
		print("--------------------")
	conn.commit()

def PollDatabaseStateandChamber(state, chamber):
	conn = psycopg2.connect( host=os.environ['HostName'], user=os.environ['UserName'], password=os.environ['password'], dbname=os.environ['DataBase'])
	cur = conn.cursor()
	cur.execute("SELECT * FROM politicians WHERE state='%s' and chamber='%s'" %(state, chamber))
	result = cur.fetchall()
	for pol in result:
		print("Name: " + pol[1])
		print("Party: " +pol[2])
		print("Chamber: " + pol[3])
		print("Twitter: "+pol[6])
		print("--------------------")
	conn.commit()


if __name__ == "__main__":
	#PollDatabaseJustState('CO')
	PollDatabaseStateandChamber('NJ', 'Senate')


