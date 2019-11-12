import turtle
import random

global move_history

class Board:
    def make_empty_board(sz):
        board = []
        for i in range(sz):
            board.append([" "]*sz)
        return board
    def is_empty(board):
        return board == [[' ']*len(board)]*len(board)
    def is_in(board, y, x):
        return 0 <= y < len(board) and 0 <= x < len(board)
    def is_win(board):
        black = ScoreSystem.col(board,'b')
        white = ScoreSystem.col(board,'w')

        ScoreSystem.total_sum_col(black)
        ScoreSystem.total_sum_col(white)

        if 5 in black and black[5] == 1:
            return 'Black won'
        elif 5 in white and white[5] == 1:
            return 'White won'
        
class Graphic:
    @staticmethod
    def click(x,y):
        global board,colors,win, move_history
        x,y = Graphic.getindexposition(x,y)

        if x == -1 and y == -1 and len(move_history) != 0:
            x, y = move_history[-1]
            del(move_history[-1])
            board[y][x] = " "
            x, y = move_history[-1]
            del(move_history[-1])
            board[y][x] = " "
            return

        if not Board.is_in(board, y, x): return

        if board[y][x] == ' ':
            Graphic.draw_stone(x,y,colors['b'])
            board[y][x]='b'
            move_history.append((x, y))
            game_res = Board.is_win(board)

            if game_res in ["White won", "Black won"]:
                print (game_res)
                win = True
                turtle.exitonclick()
                print("Good Bye")

            ay,ax = AI.best_move(board,'w')
            Graphic.draw_stone(ax,ay,colors['w'])
            board[ay][ax]='w'
            move_history.append((ax, ay))
            game_res = Board.is_win(board)

            if game_res in ["White won", "Black won"]:
                print (game_res)
                win = True
                turtle.exitonclick()
                print("Good Bye")

    @staticmethod
    def getindexposition(x,y):
        intx,inty = int(x),int(y)
        dx,dy = x-intx,y-inty

        if dx > 0.5: x = intx + 1
        elif dx < -0.5: x = intx - 1
        else: x = intx

        if dy > 0.5: y = inty + 1
        elif dx < -0.5: y = inty - 1
        else: y = inty

        return x,y

    @staticmethod
    def draw_stone(x,y,colturtle):
        colturtle.goto(x,y-0.3)
        colturtle.pendown()
        colturtle.begin_fill()
        colturtle.circle(0.3)
        colturtle.end_fill()
        colturtle.penup()

class AI:
    @staticmethod
    def march(board,y,x,dy,dx,length):
        '''
        Find the arthest position in dy,dx in length
        When yf and xf are not on the board, subtract
        '''
        yf = y + length*dy
        xf = x + length*dx

        while not Board.is_in(board,yf,xf):
            yf -= dy
            xf -= dx
        return yf,xf

    @staticmethod
    def best_move(board,col):
        '''
        Return the minmax of each color
        Enter a random position if the board is empty
        Else recur the best move to get 3 and 4 in a row to win
        '''
        if col == 'w':
            anticol = 'b'
        else:
            anticol = 'w'

        movecol = (0,0)
        maxscorecol = '' 
        if Board.is_empty(board):
            movecol = ( int((len(board))*random.random()),int((len(board[0]))*random.random()))
        else:
            moves = AI.possible_moves(board)

            for move in moves:
                y,x = move
                if maxscorecol == '':
                    scorecol= ScoreSystem.stupid_score(board,col,anticol,y,x)
                    maxscorecol = scorecol
                    movecol = move
                else:
                    scorecol= ScoreSystem.stupid_score(board,col,anticol,y,x)
                    if scorecol > maxscorecol:
                        maxscorecol = scorecol
                        movecol = move
        return movecol

    @staticmethod
    def possible_moves(board):  
        '''
        Create a list of coordinates that have 3 stones in a row
        Taken saves the value of player and AI on the baord
        cord saves the uncheck coordinates
        The second loop check for values on the board (can't go)
        '''
        taken = []
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
        cord = {}

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != ' ':
                    taken.append((i,j))

        for direction in directions:
            dy,dx = direction
            for coord in taken:
                y,x = coord
                for length in [1,2,3,4]:
                    move = AI.march(board,y,x,dy,dx,length)
                    if move not in taken and move not in cord:
                        cord[move]=False
        return cord

    @staticmethod
    def row_to_list(board,y,x,dy,dx,yf,xf):
        '''Return list of y,x from yf and xf'''
        row = []
        while y != yf + dy or x !=xf + dx:
            row.append(board[y][x])
            y += dy
            x += dx
        return row

class ScoreSystem:
    @staticmethod
    def row(board,cordi,dy,dx,cordf,col):
        '''Return a list that represent the score of 5 boxes'''

        colscores = []
        y,x = cordi
        yf,xf = cordf
        row = AI.row_to_list(board,y,x,dy,dx,yf,xf)
        for start in range(len(row)-4):
            score = ScoreSystem.score_of_list(row[start:start+5],col)
            colscores.append(score)
        return colscores

    @staticmethod
    def col(board,col):
        '''
        Calculate the score of each direction in column.
        Use in is_win function
        scores is the score in 4 directions
        '''

        f = len(board)
        scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
        for start in range(len(board)):
            scores[(0,1)].extend(ScoreSystem.row(board,(start, 0), 0, 1,(start,f-1), col))
            scores[(1,0)].extend(ScoreSystem.row(board,(0, start), 1, 0,(f-1,start), col))
            scores[(1,1)].extend(ScoreSystem.row(board,(start, 0), 1,1,(f-1,f-1-start), col))
            scores[(-1,1)].extend(ScoreSystem.row(board,(start,0), -1, 1,(0,start), col))

            if start + 1 < len(board):
                scores[(1,1)].extend(ScoreSystem.row(board,(0, start+1), 1, 1,(f-2-start,f-1), col))
                scores[(-1,1)].extend(ScoreSystem.row(board,(f -1 , start + 1), -1,1,(start+1,f-1), col))
        return ScoreSystem.init(scores)

    @staticmethod
    def init(scorecol):
        '''Init score board'''
        sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
        for key in scorecol:
            for score in scorecol[key]:
                if key in sumcol[score]:
                    sumcol[score][key] += 1
                else:
                    sumcol[score][key] = 1
        return sumcol

    @staticmethod
    def score_of_col_one(board,col,y,x):
        '''Return the score of column y,x in 4 directions and only checking for 5 boxes instead of all'''

        scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
        scores[(0,1)].extend(ScoreSystem.row(board,AI.march(board,y,x,0,-1,4), 0, 1,AI.march(board,y,x,0,1,4), col))
        scores[(1,0)].extend(ScoreSystem.row(board,AI.march(board,y,x,-1,0,4), 1, 0,AI.march(board,y,x,1,0,4), col))
        scores[(1,1)].extend(ScoreSystem.row(board,AI.march(board,y,x,-1,-1,4), 1, 1,AI.march(board,y,x,1,1,4), col))
        scores[(-1,1)].extend(ScoreSystem.row(board,AI.march(board,y,x,-1,1,4), 1,-1,AI.march(board,y,x,1,-1,4), col))

        return ScoreSystem.init(scores)

    @staticmethod
    def score_of_list(lis,col):
        blank = lis.count(' ')
        filled = lis.count(col)

        if blank + filled < 5:
            return -1
        elif blank == 5:
            return 0
        else:
            return filled

    @staticmethod
    def TF34score(score3,score4):
        '''Return the guarantee win chance (4 in a row with no cutting off'''

        for key4 in score4:
            if score4[key4] >=1:
                for key3 in score3:
                    if key3 != key4 and score3[key3] >=2:
                        return True
        return False

    @staticmethod
    def stupid_score(board,col,anticol,y,x):
        ''' Move y,x to advantage situation'''

        global colors
        M = 1000
        res,adv, dis = 0, 0, 0

        '''Attack Score'''
        board[y][x]=col
        sumcol = ScoreSystem.score_of_col_one(board,col,y,x)
        a = ScoreSystem.winning_situation(sumcol)
        adv += a * M
        ScoreSystem.total_sum_col(sumcol)
        '''{0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}'''
        adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]

        '''Defend Score'''
        board[y][x]=anticol
        sumanticol = ScoreSystem.score_of_col_one(board,anticol,y,x)
        d = ScoreSystem.winning_situation(sumanticol)
        dis += d * (M-100)
        ScoreSystem.total_sum_col(sumanticol)
        dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

        res = adv + dis
        board[y][x]=' '
        return res

    @staticmethod
    def winning_situation(sumcol):
        '''
        Return winning situation like
        {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
        1-5 save score in ascending order and -1 is the worst situation, need to defend
        '''

        if 1 in sumcol[5].values():
            return 5
        elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
            return 4
        elif ScoreSystem.TF34score(sumcol[3],sumcol[4]):
            return 4
        else:
            score3 = sorted(sumcol[3].values(),reverse = True)
            if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
                return 3
        return 0

    @staticmethod
    def total_sum_col(sumcol):
        '''Total Sum of all directions'''

        for key in sumcol:
            if key == 5:
                sumcol[5] = int(1 in sumcol[5].values())
            else:
                sumcol[key] = sum(sumcol[key].values())

class Main:
    def initialize(size):

        global win,board,screen,colors, move_history

        move_history = []
        win = False
        board = Board.make_empty_board(size)

        screen = turtle.Screen()
        screen.onclick(Graphic.click)
        screen.setup(screen.screensize()[1]*2,screen.screensize()[1]*2)
        screen.setworldcoordinates(-1,size,size,-1)
        screen.bgcolor('khaki')
        screen.tracer(500)

        colors = {'w':turtle.Turtle(),'b':turtle.Turtle(), 'g':turtle.Turtle()}
        colors['w'].color('white')
        colors['b'].color('black')

        for key in colors:
            colors[key].ht()
            colors[key].penup()
            colors[key].speed(0)

        border = turtle.Turtle()
        border.speed(9)
        border.penup()

        side = (size-1)/2

        i=-1
        for start in range(size):
            border.goto(start,side + side *i)
            border.pendown()
            i*=-1
            border.goto(start,side + side *i)
            border.penup()

        i=1
        for start in range(size):
            border.goto(side + side *i,start)
            border.pendown()
            i *= -1
            border.goto(side + side *i,start)
            border.penup()

        border.ht()
        screen.listen()
        screen.mainloop()

if __name__ == '__main__':
    print("--------------WELCOME TO GOMOKU---------------")
    print("---The point of the game is to has 5 stones---")
    print("----In a row in any direction, and prevent----")
    print("----Your opponent from doing so---------------")
    print("-----------------HAVE FUN!!-------------------")
    Main.initialize(15)
