import turtle, random, sqlintg, fdbck, pickle, os

def game():
        global f,points,screen,wn,l,inv,t,btst,x,points,sp1,sp2,sp3,sp4
        turtle.TurtleScreen._RUNNING = True
        f=1
        points=0
        
        X=500
        Y=500
        turtle.setup(X,Y)
        screen=turtle.Screen()
        turtle.title("Space Inv")
        wn=screen
        wn.bgcolor('black')
        #line
        l=turtle.Turtle()
        l.penup()
        l.setx(-(X/2))
        l.sety(-(Y/2)+100)
        l.pendown()
        l.pencolor('white')
        l.setx(X/2+1)
        l.hideturtle()

        invim = "rocket.gif"
        bulletim='bullet.gif'
        wn.register_shape(invim)
        wn.register_shape(bulletim)
        #hero
        inv=turtle.Turtle()
        inv.left(90)
        inv.penup()
        inv.sety(-(Y/2)+50)
        inv.shape(invim)
        invx=0
        invy=-(Y/2)+50

        #bullet
        t=turtle.Turtle()
        wn.delay(0)

        t.ht()
        wn.delay(0)
        t.shape(bulletim)
        wn.delay(0)
        t.setheading(90)
        wn.delay(0)
        t.pu()
        t.goto(0,Y/2)
        btst="R"#bulletstate
        def bullet():
                global btst,t
                if btst=='R':
                        btst='F'
                        wn.delay(0)
                        t.goto(inv.pos())
                        wn.delay(0)
                        t.st()
                        
        def chbtst():
                global btst,t
                if t.ycor()>=Y/2:
                        t.ht()
                        btst='R'
                else:
                        btst='F'

        def right():
                if inv.xcor()<=X/2-10:
                        inv.setx(inv.xcor()+5*f)

        def left():
                if inv.xcor()>=-X/2+10:
                        inv.setx(inv.xcor()-5*f)

        wn.listen()
        wn.onkeypress(right,'Right')
        wn.onkeypress(left,'Left')
        wn.onkeypress(bullet,'space')

        #invadoras
        sp1=turtle.Turtle()
        sp2=turtle.Turtle()
        sp3=turtle.Turtle()
        sp4=turtle.Turtle()
        def respwn(turt):
                turt.ht()
                turt.color('white')
                turt.pu()
                spx=random.randint(-X/2+10,X/2-10)
                turt.goto(spx,Y/2)
                turt.setheading(270)
                turt.st()
        respwn(sp1)
        respwn(sp2)
        respwn(sp3)
        respwn(sp4)
        x=1
        def hitreg():
                global points
                global x
                if sp1.distance(t)<20:
                        respwn(sp1)
                        points+=1
                        print("Points:",points)
                if sp2.distance(t)<20:
                        respwn(sp2)
                        points+=1
                        print("Points:",points)
                if sp3.distance(t)<20:
                        respwn(sp3)
                        points+=1
                        print("Points:",points)
                if sp4.distance(t)<20:
                        respwn(sp4)
                        points+=1
                        print("Points:",points)

                for i in (sp1,sp2,sp3,sp4):
                        if i.ycor()<(-(Y/2)+100):
                                x=0

        while True:
                try:
                        t.fd(1)
                        chbtst()
                        sp1.forward(0.1*f)
                        sp2.forward(0.025*f)
                        sp3.forward(0.025*f)
                        sp4.forward(0.025*f)
                        hitreg()
                        f+=points/10**5
                except:
                        print("Thank you for playing. ;-)")
                        print('Don\'t forget to drop a feedback :)')
                        #in def for replay turtle.TurtleScreen._RUNNING = True
                        #del f,screen,wn,l,inv,t,btst,x,sp1,sp2,sp3,sp4
                        break
                finally:
                        if x==0:
                                print("Well played. ;)")
                                print('Don\'t forget to drop a feedback :)')
                                # ^^
                                turtle.bye()
                                break
        sqlopen(points)

def binfilestore(pid, points, k=0, u=None):
        if k == 0:
                pid=str(pid)+'.bin'
                try:
                        f=open(pid,'rb')
                        t=pickle.load(f)
                        t=t+(points,)
                        f.close()
                        f=open(pid,'wb')
                        pickle.dump(t,f)
                        f.close()
                except:
                        f=open(pid,'wb')
                        t=(points,)
                        pickle.dump(t,f)
                        f.close()
        elif k==1:
                pid=str(pid)+'.bin'
                f=open(pid,'rb')
                t=pickle.load(f)
                res = list(t)
                f.close()
                print('Score history of '+u+':', res)
                #[print(abc, end=',') for abc in res]

        elif k==2:
                os.remove(str(pid)+'.bin')

def sqlopen(points):
        con, cursor = sqlintg.create_conn()
        new = sqlintg.check_new(con, cursor, user)
        if not new:
                sqlintg.add_new(con, cursor, user, points)
        elif new[0][-1] < points:
                sqlintg.update(con, cursor, user, points)
        pid = sqlintg.games_played(con, cursor, user)
        binfilestore(pid, points)
        while True:
                print('\nPress 1 to view leaderboards')
                print('Press 2 to submit feedback')
                print('Press 3 to view your score history')
                print('Press 4 to change your username')
                print('Press 5 to delete account')
                print('Press 6 to exit game\n')
                #print('Press 4 to create table(only if you already don\'t have the table)')
                n = input().strip()
                if n == '':
                        print('Enter a valid number(refer to the menu).')
                        pass
                n = int(n)
                if n == 1:
                        sqlintg.retrieve(con, cursor)
                elif n == 5:
                        hij = input('Are you sure you want to delete your account?(y/n):')
                        if hij.upper() == 'Y':
                                sqlintg.deleteacc(con, cursor, pid)
                                binfilestore(pid, points, k=2)
                                print('Account deleted successfully...')
                elif n == 4:
                        newuser= input('Enter new username:')
                        sqlintg.updateusername(con, cursor, newuser, pid)
                        print('Username changed successfully...')
                elif n == 6:
                        quit()
                elif n==3:
                        try:
                                binfilestore(pid, points, 1, user)
                        except Exception:
                                print('Account dosen\'t exist')
                elif n == 2:
                        fdbck.main_screen()
                        print('Thanks for your feedback :)')
                '''elif n == 4:
                        sqlintg.create(con, cursor)'''
        con.close()
                        
def play1():
    global screen
    screen.bye()
    game()

def play(uname):
        global screen
        global user

        user = uname
        turtle.TurtleScreen._RUNNING = True
        screen = turtle.Screen()
        screen.bgcolor('black')
        x,y=750,500
        screen.setup(x, y)
        screen.title("SPACE INVADER")
        txt = turtle.Turtle()
        txt.ht()
        txt.pu()
        txt.color('red')
        txt.goto(0,100)
        txt.write("SPACE INVADERS",False,'center',('courier',50,'normal'))
        txt.goto(0,0)
        txt.color('white')
        txt.write("Gameplay: Use the arrow keys to navigate and space bar to shoot",False,'center',('courier',14,'normal'))
        txt.goto(0,-100)
        txt.color('red')
        txt.write("PRESS SPACE TO PLAY",False,'center',('courier',25,'normal'))
        screen.listen()
        screen.onkeypress(play1, "space")
