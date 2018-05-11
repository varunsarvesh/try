import psycopg2
from sqlalchemy.engine import create_engine
# conn = psycopg2.connect(database='sign', user='postgres')
# cur=conn.cursor()
#
# cur.execute('CREATE TABLE signup (name TEXT, pass TEXT, phone TEXT)')
#
# cur.close()

def dbconnect():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/sign')
    connection = engine.connect()
    msg = "Connection is being made"
    return connection


def dbclose(connection):
    connection.close()
    return

connection = dbconnect()
#query = "CREATE TABLE users(username varchar(128),password varchar(128),email varchar(128))"
v='un'
a='sun'
r='fun'
q1="INSERT INTO users VALUES(%s,%s,%s)"
#connection.execute(q1,(v,a,r))
q2="SELECT * FROM users"
ans=connection.execute(q2)
for i in ans:
    print(i['username'],i['password'])
