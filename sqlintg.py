import mysql.connector
from tabulate import tabulate

def retrieve(con, cursor):
    cursor.execute('select * from leaderboards order by highscore desc;')
    data = cursor.fetchall()
    print(tabulate(data, headers=['PlayerID', 'Player', 'Games_played', 'Highscore'], tablefmt='psql'))

def check_new(con, cursor, uname):
    cursor.execute('select * from leaderboards where user=\''+uname+'\';')
    data = cursor.fetchall()

    return data

def games_played(con, cursor, uname):
    cursor.execute('select * from leaderboards where user=\''+uname+'\';')
    data = cursor.fetchall()
    prev_gamesplayed = data[-1][-2]
    cursor.execute('update leaderboards set games_played='+str(prev_gamesplayed+1)+' where user=\''+uname+'\';')
    con.commit()

    return data[-1][0]

def updateusername(con, cursor, newuser, pid):
    cursor.execute('update leaderboards set user=\''+newuser+'\' where playerid='+str(pid)+';')
    con.commit()

def update(con, cursor, uname, points):
    cursor.execute('update leaderboards set highscore='+str(points)+' where user=\''+uname+'\';')
    con.commit()

def deleteacc(con, cursor, pid):
    cursor.execute('delete from leaderboards where playerid='+str(pid)+';')
    con.commit()

def add_new(con, cursor, new_uname, new_score):
    cursor.execute('select * from leaderboards;')
    data = cursor.fetchall()
    try:
        prev_playerid = data[-1][0]
    except Exception:
        prev_playerid = 0
    #print('insert into leaderboards values('+str(prev_playerid+1)+', \''+new_uname+'\', '+str(0)+', '+str(new_score)+');')
    cursor.execute('insert into leaderboards values('+str(prev_playerid+1)+', \''+new_uname+'\', '+str(0)+', '+str(new_score)+');')
    con.commit()

def create(con, cursor):
    cursor.execute('create table leaderboards (playerid int(3) primary key, user char(50), games_played int, highscore int);')
    con.commit()

def create_conn():
    con = mysql.connector.connect(host='localhost', user='root', passwd='password', database='space_invaders')
    cursor = con.cursor()

    return con, cursor
'''con, cursor = create_conn()
create(con, cursor)
con.close()'''
