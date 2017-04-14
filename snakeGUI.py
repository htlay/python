#!/usr/bin/python

import MySQLdb
import random
from Tkinter import *
from tkFont import Font

class Game:

    # constructor
    def __init__(self):

        # set up TKinter
        self.root = Tk()

        # set up main windows
        self.frame1 = None
        self.w = None

        # set up score windows
        self.frame2 = None
        
        # variables to hold the score
        self.scoreC = None
        self.score = 0

        # horizontal
        self.hor = True
        
        # direction for how the snake will move
        self.upid = self.downid = self.rightid = self.leftid = 0
        
        # snake head
        self.head = -1
        
        # snake speed
        self.time = 700

        # set up database
        self.DB_HOST = "localhost"
        self.DB_USER = "cs408_user"
        self.DB_PW = "cs408"
        self.DB_DB = "game"

    # start page
    def home(self):

        # frame1 create main windows size
        self.frame1 = Frame(self.root, width=750, height=350,bg="black")
        
        # set up windows
        self.root.wm_minsize(width=750, height=666)
        self.root.title("Snake")
        
        # set background color
        self.root.configure(bg="black")
        
        # draw windows
        self.frame1.pack_propagate(0)
        self.frame1.update()

        # start button so player can start the game
        start = Button(self.frame1, text="start", highlightbackground="black", command=lambda: self.callgame(100))

        # score button
        showScore = Button(self.frame1, text="Show Score", highlightbackground="black", command=lambda: self.showScore())

        # display start button
        start.grid(row=0, columnspan=2)

        # display score button
        showScore.grid(row=1, columnspan=2)

        # set up header and display header
        self.H=Label(self.root, text="CS 408\nJimmy Cheng, Hung Lay, Samantha Wu", bg="black", fg="white", pady=10)
        self.H.pack()

        # draw main window
        self.frame1.pack(expand=True)

        # keep windows open
        self.root.mainloop()

    # function to call to start the game 
    def callgame(self, time):
        # speed
        self.time = time

        # start game
        self.game()


    # functions: calldown, callup, callright, callleft, player will use up, down, left, and right arrow keys
    # to play the game.

    # down arrow
    def calldown(self, key):
        if self.hor:
            self.w.after_cancel(self.leftid)
            self.w.after_cancel(self.rightid)
            self.down(0)

    # up arrow
    def callup(self, key):
        if self.hor:
            self.w.after_cancel(self.leftid)
            self.w.after_cancel(self.rightid)
            self.up(0)

    # right arrow
    def callright(self, key):
        if not self.hor:
            self.w.after_cancel(self.upid)
            self.w.after_cancel(self.downid)
            self.right(0)

    # left arrow
    def callleft(self, key):
        if not self.hor:
            self.w.after_cancel(self.upid)
            self.w.after_cancel(self.downid)
            self.left(0)

    # game
    def game(self):

        # initial score
        self.score = 0

        # window's size
        self.w = Canvas(self.root, width=750, height=500, relief="flat", highlightbackground="white", highlightthickness=10)

        # close start window
        self.frame1.destroy()

        # draw game window
        self.w.configure(background="black")
        self.w.pack(side="left")

        # creates the initial location of the snake
        self.w.create_line(300, 250, 350, 250, width=10, fill="white")

        # define a variable to show the score of player
        self.scoreC = Label(self.root, text="Score\n" + str(self.score), bg="black", fg="white")
        self.scoreC.pack(side="bottom")

        # arrow keys
        self.root.bind("<Up>", self.callup)
        self.root.bind("<Down>", self.calldown)
        self.root.bind("<Right>", self.callright)
        self.root.bind("<Left>", self.callleft)

        # generate food
        self.createFood()

        # initial movement
        self.right(0)

    def arrow(self, direction, i):

        # coordinates
        crd = self.w.coords(1)
        if len(crd) > 0:
            if crd[0] == crd[2]:
                if crd[1] > crd[3]:
                    # print("inside if1")
                    crd[1] -= 10
                if crd[1] < crd[3]:
                    # print("inside if2")
                    crd[1] += 10
            else:
                if crd[0] > crd[2]:
                    crd[0] -= 10
                if crd[0] < crd[2]:
                    crd[0] += 10

            # change crd depending on y or x movement
            if direction == 'down':
                crd[-1] += 10
            elif direction == 'up':
                crd[-1] -= 10
            elif direction == 'right':
                crd[-2] += 10
            elif direction == 'left':
                crd[-2] -= 10

            if i == 0:
                crd.append(crd[-2])
                crd.append(crd[-2])

                if direction == 'down':
                    crd[-3] -= 10
                elif direction == 'up':
                    crd[-3] += 10
                elif direction == 'right':
                    crd[-4] -= 10
                elif direction == 'left':
                    crd[-4] += 10
            
            if crd[0] == crd[2] and crd[1] == crd[3]:
                crd = crd[2:]
            self.w.coords(1, *crd)
            self.w.delete(self.head)

            # draws snake head
            if direction == 'down':
                self.head = self.w.create_line(crd[-2], crd[-1], crd[-2], crd[-1] + 5, width=10, fill="white")
            elif direction == 'up':
                self.head = self.w.create_line(crd[-2], crd[-1], crd[-2], crd[-1] + 5, width=10, fill="white")
            elif direction == 'right':
                self.head = self.w.create_line(crd[-2], crd[-1], crd[-2] + 5, crd[-1], width=10, fill="white")
            elif direction == 'left':
                self.head = self.w.create_line(crd[-2], crd[-1], crd[-2] - 5, crd[-1], width=10, fill="white")

            # check if game ends
            end = self.end()

            # check if food is eaten
            self.checkEaten()

            i += 1

            if direction == 'down' or direction == 'up':
                self.hor = False
            else:
                self.hor = True

            # if game continues
            if not end:

                # set directon
                if direction == 'down':
                    self.downid = self.w.after(self.time, self.down, i)
                elif direction == 'up':
                    self.upid = self.w.after(self.time, self.up, i)
                elif direction == 'right':
                    self.rightid = self.w.after(self.time, self.right, i)
                elif direction == 'left':
                    self.leftid = self.w.after(self.time, self.left, i)

            # else game ends
            else:
                # delete stuff
                self.w.delete(1)
                self.w.delete(self.head)
                self.w.delete(self.food)
                self.restart = Button(self.root, highlightbackground="black", text="Restart", command=lambda: self.callhome())
                self.restart.pack(side="bottom")

    # down arrow
    def down(self, i):
        self.arrow('down', i)

    # up arrow
    def up(self, i):
        self.arrow('up', i)

    # right arrow
    def right(self, i):
        self.arrow('right', i)

    # left arrow
    def left(self, i):
        self.arrow('left', i)

    def createFood(self):

        crd = self.w.coords(1)
        ext = []
        for i in crd:
            ext.append(i)
            for j in range(-50, 50):
                ext.append(i + j)

        # random location to create the food 
        randx = random.randrange(20, 730)
        randy = random.randrange(20, 480)

        # check that the food is located in the game window
        while randx not in ext and randy not in ext:
            randx = random.randrange(20, 730)
            randy = random.randrange(20, 480)

        # draw food
        self.food = self.w.create_line(randx, randy, randx + 12, randy, width=10, fill="white")

    def checkEaten(self):

        # snake's head coordinates
        headcoords = self.w.coords(self.head)

        # food coordinates
        foodcoords = self.w.coords(self.food)

        # flag for if food is eaten
        flag = False

        # check if head touches the food
        if int(headcoords[-4]) in range(int(foodcoords[-4]) - 7, int(foodcoords[-2]) + 7
            ) and int(headcoords[-3]) in range(int(foodcoords[-1]) - 10, int(foodcoords[-1] + 10)):

            # set to true
            flag = True

        # if food is eaten
        if flag:

            # size of snake increases
            self.grow()

            # add ten to score
            self.score += 10

            # redraw score
            self.scoreC.configure(text="Score\n" + str(self.score), bg="black", fg="white")

            # delete eaten food
            self.w.delete(self.food)

            # increase speed
            if not self.time == 30:
                self.time = self.time - 10

            # create new food
            self.createFood()

    # increase the size of snake
    def grow(self):

        # get window coordinates
        crd = self.w.coords(1)

        if crd[0] != crd[2]:  # horizontal condition
            if crd[0] < crd[2]:
                crd[0] -= 20
            else:
                crd[0] += 20
            self.w.coords(1, *crd)
        else:
            if crd[3] < crd[1]:
                crd[1] += 20
            else:
                crd[1] -= 20
            self.w.coords(1, *crd)

    # end the game if the head of snake hits the border or itself
    def end(self):

        # get window coordinates
        crd = self.w.coords(1)

        # get head coordinates
        head = self.w.coords(self.head)
        a = 0

        # check if snake hit itself
        while a < len(crd) - 2:
            if crd[a] == crd[a + 2]:
                if (head[0] == crd[a] and crd[a + 1] < head[1] < crd[a + 3]) or (
                        head[0] == crd[a]  and crd[a + 1] > head[1] > crd[a + 3]):
                    return True
            else:
                if (head[1] == crd[a + 1] and crd[a] < head[0] < crd[a + 2]) or (head[1] == crd[a + 1] and crd[a] > head[0] > crd[a + 2]):
                    return True
            a += 2

        # check if snake hits borders
        if (head[0] == 0 and 0 < head[1] < 500) or (head[1] == 0 and 0 < head[0] < 750) or (
            head[1] == 510 and 0 < head[0] < 750) or (head[0] == 760 and 0 < head[1] < 500):

            return True

        # snake is still alive
        return False

    def callhome(self):

        # close game window, close restart button, close header, close score
        self.w.destroy()
        self.restart.destroy()
        self.H.destroy()
        self.scoreC.destroy()

        # ask for name
        self.input = Label(self.root, text="Name (3 CHAR ONLY)", bg = "black", fg = "white", padx = 10)
        self.input.pack(side = LEFT)

        # create input box
        self.entry = Entry(self.root)
        self.entry.pack(side = LEFT)

        # submit button
        self.submit = Button(self.root, text="submit", highlightbackground="black", command=lambda: self.store(self.entry.get().strip()))
        self.submit.pack(side = LEFT)

    def store(self, name):

        # close input prompt, close input box, close submit button
        self.input.destroy()
        self.entry.destroy()
        self.submit.destroy()

        # store name in database
        DB(name, self.score)

        # call start screen
        self.home()

    # display Score
    def showScore(self):
        
        # close start window
        self.frame1.destroy()

        # set up score window
        self.frame2 = Frame(self.root, width=750, height=350, bg="black")

        # display Scores
        self.displayScore()

        # draw back button
        self.back = Button(self.frame2, text="Back", highlightbackground="black", command=lambda: self.backToStart())
        self.back.pack(side="bottom")

        # draw reset button
        self.resetScore = Button(self.frame2, text="Reset", highlightbackground="black", command=lambda: self.reset())
        self.resetScore.pack(side="bottom")

        # draw score window
        self.frame2.pack(expand=True)

    # reset database
    def reset(self):

        # Open databse connection
        self.db = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PW, self.DB_DB)

        # prepare cursor object
        self.cursor = self.db.cursor()

        # delete table
        self.cursor.execute("DROP TABLE IF EXISTS score")

        # add empty table
        sql = "CREATE TABLE score (rank int, name VARCHAR(3), score int, id int NOT NULL AUTO_INCREMENT PRIMARY KEY)"
        self.cursor.execute(sql)

        # commit to database
        self.db.commit()

        # disconnect from server
        self.db.close()

        # close score window
        self.frame2.destroy()

        # close header
        self.H.destroy()

        # call start window
        self.home()

    # back button
    def backToStart(self):

        # close score window
        self.frame2.destroy()

        # close header
        self.H.destroy()

        # call start window
        self.home()

    def displayScore(self):

        # Open databse connection
        self.db = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PW, self.DB_DB)

        # prepare cursor object
        self.cursor = self.db.cursor()

        # get ranks
        sql = "SELECT rank FROM score"
        self.cursor.execute(sql)
        rank = self.cursor.fetchall()
        
        # convert rank to list
        rankList = []
        for i in rank:
            rankList.append(i[0])

        # sort ranks
        rankList = sorted(rankList)

        # display scores by rank
        if not rankList:

            # no values in database
            label = Label(self.frame2, text="No Scores Available", bg="black", fg="white") 
            label.pack()

        else:

            fonts = Font(family='Courier New', size = 16)

            # create database header
            header = Label(self.frame2, text="%-10s%-10s%-10s\n" % ("RANK", "NAME", "SCORE"), font = fonts, bg="black", fg="white")
            header.pack()

            # rotate through list of scores
            for i in range(0, len(rankList)):

                # display only top ten scores
                if i < 10:

                    # get name from database
                    sql = "SELECT name FROM score WHERE rank = '%d'" % (i + 1)
                    self.cursor.execute(sql)
                    name = self.cursor.fetchall()
                    # get score from database
                    sql = "SELECT score FROM score WHERE rank = '%d'" % (i + 1)
                    self.cursor.execute(sql)
                    score = self.cursor.fetchall()

                    # display rank, name, and score
                    display = Label(self.frame2, text="%-10d%-10s%-10d" % (i + 1, name[0][0], score[0][0]), font = fonts, bg="black",fg="white")
                    display.pack()

                else:
                    break
 

        # close database
        self.db.close()

# set up database
class DB:

    def __init__(self, name, score):

        # set up values
        self.DB_HOST = "localhost"
        self.DB_USER = "cs408_user"
        self.DB_PW = "cs408"
        self.DB_DB = "game"

        # Open databse connection
        self.db = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PW, self.DB_DB)

        # prepare cursor object
        self.cursor = self.db.cursor()

        # store score
        self.name = name.upper()
        self.score = score
        self.addScore()

        # commit to database
        self.db.commit()

        # disconnect from server
        self.db.close()

    def sort(self):

        # get ids
        sql = "SELECT id FROM score"
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()

        # convert to values
        idList = []
        for i in ids:
            idList.append(i[0])

        # get scores
        sql = "SELECT score FROM score"
        self.cursor.execute(sql)
        score = self.cursor.fetchall()

        # convert to values
        scoreList = []
        for i in score:
            scoreList.append(i[0])

        # map score to id
        rankingScore = zip(idList, scoreList)

        # sort rankingScore in ascending order
        ranking = sorted(rankingScore, key=lambda rankingScore: rankingScore[1])

        reverse = len(rankingScore) - 1

        for i in range(0, len(ranking)):

            # set ranks of score
            sql = "UPDATE score SET rank = '%d' WHERE id = '%d'" % (i + 1, ranking[reverse][0])
            self.cursor.execute(sql)

            reverse -= 1;

        # commit to database
        self.db.commit()

    def addScore(self):

        # store new score
        sql = "INSERT INTO score (rank, name, score) VALUES (0, '%s', '%d')" % (self.name, self.score)
        self.cursor.execute(sql)

        # sort database
        self.sort()

# start game
g = Game()
g.home()