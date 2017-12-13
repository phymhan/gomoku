import pygame
import sys
import random
import time
import re
import Skype4Py as sky
from pygame.locals import *
import chessAI
import skywindAI

pygame.init()

PLTYP = 'human'

DEPTH = 3

play_music = False
play_sound = True

T_MAX = 60
T_MIN = 0.5

PLAYER1 = 1
PLAYER2 = 2

CHECK_CONNECT = 'Connection Test'
CHECK_MOVE = 'Moved'
CHECK_OK = 'Ok'
CHECK_RECV = 'Received'
CHECK_PLYR = 'Confirm'
CHECK_QUIT = 'QUIT'
CHECK_CONTINUE = 'Continue'

white = (255,255,255)
black = (0,0,0)
red = (175,0,0)
green = (0,120,0)
lightgreen = (0,175,0)
bg = (32,32,32,255)

fp = './sources/' # 'c:/Users/Ligong/Desktop/five_chess/sources'

cpSize = 29

img_board = pygame.image.load(fp+'pics/board.png')
img_cp1 = pygame.image.load(fp+'pics/cp_k_29.png')
img_cp2 = pygame.image.load(fp+'pics/cp_w_29.png')
img_panel = pygame.image.load(fp+'pics/panel.png')
img_icon = pygame.image.load(fp+'pics/catsmall.png')
pygame.display.set_icon(img_icon)

fps = 30

dispWidth = 900
dispHeight = 645

lineWidth = 1
lineWidth2 = 4
lineWidth3 = 4
boxWidth = 40

marginWidth = 24

N = 15
n_win = 5 ##

boardWidth = lineWidth*N+boxWidth*(N-1)

starty = (dispHeight-boardWidth)/2
startx = starty+0

infox = 2*marginWidth+boardWidth+48
infoy1 = startx+marginWidth+(lineWidth+boxWidth)*1
infoy2 = infoy1+(lineWidth+boxWidth)*4
infoWidth = (lineWidth+boxWidth)*4
infoHeight = (lineWidth+boxWidth)*3
bgWidth = (dispWidth-infox)-1

plyrInfo1 = {'score': 0, 'time': 0}
plyrInfo2 = {'score': 0, 'time': 0}

def hex2rgb(pxValue):
    v = pxValue/256
    b = pxValue-v*256
    pxValue = v
    v = pxValue/256
    g = pxValue-v*256
    pxValue = v
    v = pxValue/256
    r = pxValue-v*256
    return r, g, b
    
def darkenBackground():
    # pygame.draw.rect(setDisplay,bg,(0,0,dispWidth,dispHeight))
    pixels = pygame.PixelArray(setDisplay)
    for x in xrange(dispWidth):
        for y in xrange(dispHeight):
            r, g, b = hex2rgb(pixels[x][y])
            pixels[x][y] = pygame.Color(r/4,g/4,b/4)

def updateInfo(info1, info2, plyr):
    setDisplay.blit(img_panel, (infox, 0))
    if plyr == PLAYER1:
        pygame.draw.rect(setDisplay, lightgreen, (infox+2, infoy1+2, infoWidth-1,infoHeight-1), lineWidth3)
    else:
        pygame.draw.rect(setDisplay, lightgreen, (infox+2, infoy2+2, infoWidth-1,infoHeight-1), lineWidth3)

    ttlText = pygame.font.SysFont('Calibri', 24)
    scoreText = pygame.font.SysFont('Calibri', 20)
    timeText = pygame.font.SysFont('Calibri', 20)
    
    textttl = 'You'
    textsc = 'Score: %d' %info1['score']
    texttm = 'Time: %.2f s' %info1['time']
    textSurf, textRect = makeTextObjs(textttl, scoreText, red)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2)-30)
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(textsc, scoreText, green)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2))
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(texttm, scoreText, white)
    textRect.center = (int(infox+infoWidth/2), int(infoy1+infoHeight/2)+26)
    setDisplay.blit(textSurf, textRect)

    textttl = 'Your Friend'
    textsc = 'Score: %d' %info2['score']
    texttm = 'Time: %.2f s' %info2['time']
    textSurf, textRect = makeTextObjs(textttl, scoreText, red)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2)-30)
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(textsc, scoreText, green)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2))
    setDisplay.blit(textSurf, textRect)
    textSurf, textRect = makeTextObjs(texttm, scoreText, white)
    textRect.center = (int(infox+infoWidth/2), int(infoy2+infoHeight/2)+26)
    setDisplay.blit(textSurf, textRect)

def whatNext():
    for event in pygame.event.get([KEYDOWN, KEYUP, QUIT]):
        if event.type == QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            continue
        return event.key
    if getSpecMsg(SkypeClient, frndID) == CHECK_CONTINUE:
        return CHECK_CONTINUE
    return None

def makeTextObjs(text, font, tColor):
    textSurface = font.render(text, True, tColor)
    return textSurface, textSurface.get_rect()

def showTips(text, tSize, tColor):
    pygame.draw.rect(setDisplay,bg,(0,0,dispWidth,dispHeight))
    tipText = pygame.font.SysFont('Calibri', tSize)
    tipTextSurf, tipTextRect = makeTextObjs(text, tipText, tColor)
    tipTextRect.center = (int(dispWidth/2), int(dispHeight/2))
    setDisplay.blit(tipTextSurf, tipTextRect)
    pygame.display.update()
    fpsTime.tick()

def msgSurface(plyr, textColor):
    darkenBackground()
    
    smallText = pygame.font.SysFont('Calibri', 30)
    largeText = pygame.font.SysFont('Calibri', 65)

    if plyr == PLAYER1:
        text = 'You Win!'
    else:
        text = 'Your Friend Wins!'

    titleTextSurf, titleTextRect = makeTextObjs(text, largeText, textColor)
    titleTextRect.center = (int(dispWidth/2), int(dispHeight/2))
    setDisplay.blit(titleTextSurf, titleTextRect)

    typTextSurf, typTextRect = makeTextObjs('Press any key to continue...', smallText, white)
    typTextRect.center = (int(dispWidth/2), int(dispHeight/2)+120)
    setDisplay.blit(typTextSurf, typTextRect)
    pygame.display.update()
    fpsTime.tick()

    while whatNext() == None:
        for event in pygame.event.get([QUIT]):
            if event.type == QUIT:
                quit_game()

        pygame.display.update()
        fpsTime.tick()

    SkypeClient.SendMessage(frndID, CHECK_CONTINUE)
    runGame()

def runGame():
    showTips("Please go back to your shell/console...", 38, white)

    FIRSTPLYR = init_game()
    if FIRSTPLYR == PLAYER1:
        CPTYP1 = 'k'
        CPTYP2 = 'w'
    else:
        CPTYP1 = 'w'
        CPTYP2 = 'k'
    theWinner = 0
    currPlayer = FIRSTPLYR
    
    data = {'steps': 0}
    
    setDisplay.blit(img_board, (0,0))
    updateInfo(plyrInfo1, plyrInfo2, currPlayer)
    pygame.display.update()

    chessMat = []
    for dummy_iy in xrange(N):
        chessMat.append([0 for dummy_idx in xrange(N)])
		
	srchr = skywindAI.searcher()
    srchr.board = chessMat
    
    while True: # main game loop
        while theWinner == 0:
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    quit_game()

            # players play in turn
            t_start = pygame.time.get_ticks()
            
            if currPlayer == PLAYER1:
                if PLTYP == 'human':
                    row, col = getPiecePos()
                    while not isValid((row, col),chessMat):
                        row, col = getPiecePos()
                elif PLTYP == 'computer':
                    score, row, col = srchr.search(1, DEPTH)
                    if not isValid((row, col),chessMat):
                        row, col = sysIndexGen(chessMat,currPlayer)
                # Notify your friend:
                notifyFriend((row, col))
            elif currPlayer == PLAYER2:
                row, col = getPiecePosOnline()
                while not isValid((row, col),chessMat):
                    row, col = getPiecePosOnline()
                    
            t_end = pygame.time.get_ticks()

            # add new piece
            chessMat[row][col] = currPlayer
            theWinner = checkIfWins(chessMat, currPlayer)
            if currPlayer == PLAYER1:
                drawPiece((row, col), CPTYP1)
            else:
                drawPiece((row, col), CPTYP2)

            if play_sound:
                cpSound.play()

            t_call = t_end - t_start
            t_rem = T_MIN*1000 - t_call
            if t_rem > 0:
                pygame.time.wait(int(t_rem))
            elif t_call > T_MAX*1000:
                print 'Maximum time exceeded!'
                if currPlayer == PLAYER1:
                    theWinner = PLAYER2
                else:
                    theWinner = PLAYER1
 
            if currPlayer == PLAYER1:
                plyrInfo1['time'] += t_call/1000.0
                currPlayer = PLAYER2
            else:
                plyrInfo2['time'] += t_call/1000.0
                currPlayer = PLAYER1

            updateInfo(plyrInfo1,plyrInfo2,currPlayer)

            # print 'data: ', data ##
            # print '' ##

            pygame.display.update()
            fpsTime.tick(fps)

        print 'Winner: Player', theWinner
        printMat(chessMat)
        if theWinner == PLAYER1:
            plyrInfo1['score'] += 1
        else:
            plyrInfo2['score'] += 1
        
        msgSurface(theWinner, green)

def printMat(mat):
    for bdraw in mat:
        print bdraw
    print '=' * 45

def drawPiece(indice, BW):
    x = startx+lineWidth/2+indice[1]*(lineWidth+boxWidth)-(cpSize-1)/2
    y = starty+lineWidth/2+indice[0]*(lineWidth+boxWidth)-(cpSize-1)/2
    if BW == 'k':
        setDisplay.blit(img_cp1, (x,y))
    else:
        setDisplay.blit(img_cp2, (x,y))
        
def getPiecePos():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                row = int(round((y-starty-lineWidth/2.0)/(lineWidth+boxWidth)))
                col = int(round((x-startx-lineWidth/2.0)/(lineWidth+boxWidth)))
                return row, col

def ind2coord(indice):
##    row = indice[0]
##    col = indice[1]
##    s1 = '%.2f' %float(raw/100.0)
##    s2 = '%.2f' %float(col/100.0)
##    
##    return s1[2:]+s2[2:]
    s1 = chr(indice[0]+ord('A'))
    s2 = chr(indice[1]+ord('A'))
    return s1+s2

def coord2ind(s):
##    s1 = s[0:2]
##    s2 = s[2:4]
##    row = int(s1)
##    col = int(s2)
    row = ord(s[0])-ord('A')
    col = ord(s[1])-ord('A')
    return row, col

def getPiecePosOnline():
    recvSpecMsg(SkypeClient, frndID, CHECK_MOVE, 250)
    SkypeClient.SendMessage(frndID, CHECK_OK)
    coordStr = recvSpecMsg(SkypeClient, frndID, None, 100)
    row, col = coord2ind(coordStr)
    SkypeClient.SendMessage(frndID, CHECK_RECV)
    return row, col

def notifyFriend(indice):
    SkypeClient.SendMessage(frndID, CHECK_MOVE)
    recvSpecMsg(SkypeClient, frndID, CHECK_OK, 100)
    coordStr = ind2coord(indice)
    SkypeClient.SendMessage(frndID, coordStr)
    recvSpecMsg(SkypeClient, frndID, CHECK_RECV, 100)
    return True

def isValid(indice, mat):
    newRaw = indice[0]
    newCol = indice[1]
    if newRaw < 0 or newRaw > N-1:
        return False
    elif newCol < 0 or newCol > N-1:
        return False

    return mat[newRaw][newCol] == 0

def sysIndexGen(mat,player):
    for row in xrange(N):
        for col in xrange(N):
            if mat[row][col] is 0:
                return row, col

def checkIfWins(mat, player):
    flag = 'x'
    # rows:
    for row in xrange(N):
        s_raw = ''
        for col in xrange(N):
            if mat[row][col] == player:
                s_raw += flag
            else:
                s_raw += '0'
        isMatch = re.search(flag*n_win,s_raw)
        if isMatch is not None:
            return player
        
    # cols:
    for col in xrange(N):
        s_col = ''
        for row in xrange(N):
            if mat[row][col] == player:
                s_col += flag
            else:
                s_col += '0'
        isMatch = re.search(flag*n_win,s_col)
        if isMatch is not None:
            return player

    # (0,0) --> (1,1):
    for k in xrange(n_win-1,N,1):
        s_line = ''
        xs = xrange(0,k+1)
        for x in xs:
            y = k - x
            if mat[y][N-1-x] == player:
                s_line += flag
            else:
                s_line += '0'
        isMatch = re.search(flag*n_win,s_line)
        if isMatch is not None:
            return player
    for k in xrange(N,2*(N-1)-(n_win-1)+1,1):
        s_line = ''
        xs = xrange(k-(N-1),N)
        for x in xs:
            y = k - x
            if mat[y][N-1-x] == player:
                s_line += flag
            else:
                s_line += '0'
        isMatch = re.search(flag*n_win,s_line)
        if isMatch is not None:
            return player

    # (1,0) --> (0,1):
    for k in xrange(n_win-1,N,1):
        s_line = ''
        xs = xrange(0,k+1)
        for x in xs:
            y = k - x
            if mat[y][x] == player:
                s_line += flag
            else:
                s_line += '0'
        isMatch = re.search(flag*n_win,s_line)
        if isMatch is not None:
            return player
    for k in xrange(N,2*(N-1)-(n_win-1)+1,1):
        s_line = ''
        xs = xrange(k-(N-1),N)
        for x in xs:
            y = k - x
            if mat[y][x] == player:
                s_line += flag
            else:
                s_line += '0'
        isMatch = re.search(flag*n_win,s_line)
        if isMatch is not None:
            return player
        
    return 0

def MutualConfirm(S, specID, specMsg, maxLoops, delayTime, prompt):
    # If specMsg is None, te function returns your friend's message. And prompt is your message to be sent
    text = getSpecMsg(S, specID)
    if specMsg is None:
        if maxLoops < 0:
            if text == None:
                S.SendMessage(specID, prompt)
                pygame.time.wait(2*delayTime)
                while True:
                    for event in pygame.event.get([QUIT]):
                        if event.type == QUIT:
                            quit_game()
                    text = getSpecMsg(S, specID)
                    if text != None:
                        return text
                    pygame.time.wait(delayTime)
            else:
                S.SendMessage(specID, prompt)
                return text #####
        else:
            if text == None:
                S.SendMessage(specID, prompt)
                pygame.time.wait(2*delayTime)
                for dummy_idx in xrange(maxLoops):
                    for event in pygame.event.get([QUIT]):
                        if event.type == QUIT:
                            quit_game()
                    text = getSpecMsg(S, specID)
                    if text != None:
                        return text
                    pygame.time.wait(delayTime)
            else:
                S.SendMessage(specID, specMsg)
            return text
    else:
        if maxLoops > 0:
            if text != specMsg:
                S.SendMessage(specID, specMsg)
                pygame.time.wait(2*delayTime)
                for dummy_idx in xrange(maxLoops):
                    for event in pygame.event.get([QUIT]):
                        if event.type == QUIT:
                            quit_game()
                    if prompt != '':
                        print prompt, dummy_idx+1
                    text = getSpecMsg(S, specID)
                    if text == specMsg:
                        break
                    pygame.time.wait(delayTime)
            else:
                S.SendMessage(specID, specMsg)
            if text == specMsg:
                return True
            else:
                return False
        else:
            if text != specMsg:
                S.SendMessage(specID, specMsg)
                pygame.time.wait(2*delayTime)
                while True:
                    for event in pygame.event.get([QUIT]):
                        if event.type == QUIT:
                            quit_game()
                    text = getSpecMsg(S, specID)
                    if text == specMsg:
                        return True
                    pygame.time.wait(delayTime)
            else:
                S.SendMessage(specID, specMsg)
                return True

def init_Skype():
    frndName = raw_input("Please enter your friend's Skype Name: (starts with 'live:')\n")
    S = sky.Skype()
    if not S.Client.IsRunning:
        S.Start()
    S.Attach()

    # Test if connected:
    connected = MutualConfirm(S, frndName, CHECK_CONNECT, 500, 250, 'Attempting to connect with your friend...')
    if connected:
        print 'Connected!!!'
    else:
        print 'Failed to connect with your friend, try again.'
        quit_game()
    
    return S, frndName

def init_game():
    while True:
        iGuess = raw_input("Pick one color, black or white (k/w): ")
        uGuess = MutualConfirm(SkypeClient, frndID, None, -1, 250, iGuess)
        if iGuess != uGuess:
            ## # Confirm
            ## MutualConfirm(SkypeClient, frndID, CHECK_PLYR, -1, 250, '')
            ## YouAndMe = uGuess+iGuess
            ## IAndYou = MutualConfirm(SkypeClient, frndID, None, -1, 100, YouAndMe)
            if True: ## IAndYou == iGuess+uGuess:
                print "Deal!!!"
                if iGuess == 'k':
                    FIRSTPLYR = PLAYER1
                    print "You are BLACK; Your friend is WHITE."
                else:
                    FIRSTPLYR = PLAYER2
                    print "You are WHITE; Your friend is BLACK"
                return FIRSTPLYR
            else:
                print "Oops, let's do it one more time..."
                clearSpecMsg(SkypeClient, frndID)
                continue
        else:
            print "Oops, let's do it one more time..."

def quit_game():
    SkypeClient.SendMessage(frndID, CHECK_QUIT)
    pygame.quit()
    sys.exit()

while True:
    global fpsTime
    global cpSound
    global setDisplay
    global SkypeClient
    global frndID

    SkypeClient, frndID = init_Skype()
    fpsTime = pygame.time.Clock()
    setDisplay = pygame.display.set_mode((dispWidth,dispHeight))
    pygame.display.set_caption('Five Chess')

    if play_music:
        pygame.mixer.pre_init(44100)
        bgSound = pygame.mixer.Sound(fp+'music/BackgroundMusic.ogg')
        bgSound.set_volume(3)
        bgSound.play(-1)
    if play_sound:
        pygame.mixer.pre_init(44100)
        cpSound = pygame.mixer.Sound(fp+'music/Snd_click.ogg')
        cpSound.set_volume(12)

    runGame()
    
