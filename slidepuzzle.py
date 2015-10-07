#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      maleonv
#
# Created:     02/10/2015
# Copyright:   (c) maleonv 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame, sys, random
from pygame.locals import *

#constants
BOARDWIDTH = 4
BOARDHEIGHT = 4
TITLESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BLACK         = (  0,   0,   0)
WHITE         = (255, 255, 255)
BRIGHTBLUE    = (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN         = (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int ((WINDOWWIDTH - (TITLESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) /2)
YMARGIN = int ((WINDOWHEIGHT - (TITLESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) /2)

UP = 'up'
DOWN = 'down'
LEFT  = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, \
    SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # srote the option buttons and their rectangles in OPTIONS
    RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, \
     WINDOWHEIGHT - 90)
    NEW_SURF, NEW_RECT = makeText ('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, \
    WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, \
    WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board at the start
    allMoves = [] # list of moves made from the solved configuration

    while True:
        slideTo = None # the direction a tile should slide
        msg = '' # contains the message to show in the uppser left corner.

        if mainBoard == SOLVEDBOARD:
            msg = 'Solved'
        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves) # clicked reset button
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80) # clicked new game
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) #clicked solve
                        allMoves = []
                else:
                    #check if the clicked tile was next to the blank spot
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN
            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWNN):
                    slideTo = DOWN
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide' \
            , 8) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_SCAPE:
            terminate()
        pygame.event.post(event) # put the other KEYUP event objets back

def getStartingBoard():
    # return a board data structure with tiles in the solved state.
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH  - 1
    board[BOARDWIDTH - 1][BOARDHEIGHT -1] = None
    return board

def getBlankPosition(board):
    # return the x an y of board coordinates of the blank space
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return(x, y)

def makeMove(board, move):
    # does not check if move is valid
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1] \
        , board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1] \
        , board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx  + 1][blanky] \
        , board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky] \
        , board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or (move == DOWN and blanky != 0) \
          or (move == LEFT and blankx != len(board) - 1) or (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are qualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TITLESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TITLESIZE) + (tileY - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # from x & y pixel coords, get the x & board coords
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TITLESIZE, TITLESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def drawTile (tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coords tilex and tiley, optionally a fea
    # pixels over(determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF,TILECOLOR, (left + adjx, top + adjy, TITLESIZE, TITLESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int (TITLESIZE / 2) + adjx, top + int(TITLESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
    # create the surface and rect objects for some text
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TITLESIZE
    height = BOARDHEIGHT * TITLESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height \
    +11), 4)
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

def slideAnimation(board, direction, message, animationSpeed):
    # this function does not check if move is valid

    blankx, blankY = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blankY + 1
    elif direction == DOWN:
        movex = blankx
        movey = blankY - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blankY
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blankY

    #prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the base surface
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TITLESIZE, TITLESIZE))
    #
    for i in range(0, TITLESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)
        #
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides):
    # from a starting configuration, make numSlides number of moves (and animate them)
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle..', int(TITLESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)

def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()
    #
    for move in revAllMoves:
        if move == UP:
            oppoisteMove = DOWN
        elif move == DOWN:
            oppoisteMove = UP
        elif move == RIGHT:
            oppoisteMove = LEFT
        elif move == LEFT:
            oppoisteMove = RIGHT
        slideAnimation(board, oppoisteMove, '', int(TITLESIZE / 2))
        makeMove(board, oppoisteMove)

if __name__ == '__main__':
    main()
