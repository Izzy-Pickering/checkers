
import random
import math
import turtle

# Set global variable
SIZE = 7

def main():
    b = generateBoard()
    print(solution(b))

    # Open the turtle window
    window = turtle.Screen()
    showBoard(b)
    window.exitonclick()

def solution(B):  
    # Set variable for the result
    results = []

    # Set the initial node
    startNode = Node()
    startNode.parentBoard = []    
    startNode.childBoard = B

    # Find the 'O'
    for line in B:
        if 'O' in line:
           startNode.oRow = B.index(line)
           startNode.oCol = B[startNode.oRow].index('O') 
    
    # Set the search object and add the start state
    search = StackSearch()
    search.reserve.append(startNode)

    # Examine the game
    while True:
        if len(search.reserve) == 0:
            break
        
        # Take the last node in the reserve
        examinedNode = search.reserve[-1]
        search.check(examinedNode)

        # Get next positions to look at
        a = examinedNode.oRow-1
        b1 = examinedNode.oCol-1
        b2 = examinedNode.oCol+1
        c = examinedNode.oRow-2
        d1 = examinedNode.oCol-2
        d2 = examinedNode.oCol+2

        # Check there is room to move up
        if c < 0:
            pass

        # Look top-right to see if I can move there
        try: 
            if examinedNode.childBoard[a][b1] == 'X' and examinedNode.childBoard[c][d1] == '.':
                createNewNode('R', c, d1, examinedNode.childBoard, search)
        except IndexError:
            pass

        # Look top-left to see if I can move there
        try:
            if examinedNode.childBoard[a][b2] == 'X' and examinedNode.childBoard[c][d2] == '.':  
                createNewNode('L', c, d2, examinedNode.childBoard, search)
        except IndexError:
            pass
        
        # Delete this node from the list
        search.delete(examinedNode) 


    # If you can't move anymore, traceback to beginning to assess how many points you have
    for node in search.checked:
        result = 0
        while True:
            if node.childBoard == B:
                results.append(result)
                break
            else:
                # Look for the parent node in the checked list
                for n in search.checked:
                    if n.childBoard == node.parentBoard:
                        node = n
                        break
                result+=1
    return max(results)   

def createNewNode(direction, x, y, parent, search):
    # Set up the new node
    newNode = Node()
    
    newNode.oRow = x
    newNode.oCol = y
    newNode.parentBoard = parent

    # Check the value is in the board
    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        return

    # Update the board
    for i in range (SIZE):
        newNode.childBoard.append('')
        for j in range (SIZE):
            if i == x and j == y:
                newNode.childBoard[i] += 'O'
            elif i == x + 1 and ((direction == 'R' and j == y + 1) or (direction == 'L' and j == y - 1)):
                    newNode.childBoard[i] += '.'
            elif i == x + 2 and ((direction == 'R' and j == y + 2) or (direction == 'L' and j == y - 2)):
                    newNode.childBoard[i] += '.'
            else:
                newNode.childBoard[i] += newNode.parentBoard[i][j]

    # Add the new node to the list to review
    search.add(newNode)

def generateBoard():
    board = []
    for i in range(SIZE):
        board.append('')
        for j in range(SIZE):
            # Add the bottom row
            if i == SIZE - 1:
                if j == math.floor(SIZE / 2):
                    board[i] += 'O'
                else:
                    board[i] += '.'
            else: 
                r = random.choices([0,1,3])
                if r[0] == 0:
                    board[i] += 'X'
                else:
                    board[i] += '.'
        print(board[i])
    return board

def showBoard(board):
    # Based on explination here: https://www.geeksforgeeks.org/draw-square-and-rectangle-in-turtle-python/
    t = turtle.Turtle()

    # Define the screen criteria
    screen = turtle.Screen()
    x = -screen.window_width()/2
    y = screen.window_height()/2
    
    # Set the size of the squares
    s = 100

    # Set the speed
    t.speed(0)

    # Go to the top of the screen
    topScreen(t, x, y)

    # Draw the grid 
    for i in range (SIZE):
        if i % 2 == 0:
            r = 'even'
        else:
            r = 'odd'

        for j in range (SIZE):
            t.color('black')
            if j != 0:
                t.forward(s)
            # Set the alternating colour filling for the grid
            if j % 2 == 0 and r == 'even':
                t.begin_fill()
            elif j % 2 != 0 and r =='odd':
                t.begin_fill()
            
            # Draw a square
            for _ in range(4):
                t.forward(s)
                t.left(90)
            t.end_fill()

        # Got back to the beginning of the row
        if i != SIZE - 1:
            startRow(t, s)

    # Fill the grid
    # Go to the top of the grid
    topScreen(t, x, y)
    t.forward(s/2)
    # Determine what should be in that cell
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 'X':
                t.color('#a10000')
                t.begin_fill()
                t.circle(50)
                t.end_fill()
            elif board[i][j] == 'O':
                t.color('#006939')
                t.begin_fill()
                t.circle(50)
                t.end_fill()
            if j != SIZE - 1:
                t.penup()
                t.forward(s)
                t.pendown()
        # Go back to the beginning of the row    
        if i != SIZE - 1:
            startRow(t, s)

def topScreen(t, x, y):
    # Move the turtle
    t.penup()
    t.goto(x, y) 
    t.pendown()

def startRow(t, s):
    t.penup()
    t.backward(s*(SIZE-1))
    t.right(90)
    t.forward(s)
    t.left(90)
    t.pendown()


# Define needed classes
class Node():
    def __init__(self):
        self.oRow = 0
        self.oCol = 0
        self.parentBoard = []
        self.childBoard = []

class StackSearch():
    def __init__(self):
        self.reserve = []
        self.checked = []

    def add(self, node):
        self.reserve.append(node)

    def check(self, node):
        self.checked.append(node)

    def delete(self, node):
        if len(self.reserve) == 0:
            raise Exception ("Finished")
        else:
            self.reserve.remove(node)

main()