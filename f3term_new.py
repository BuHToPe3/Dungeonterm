#coding=utf-8

import pygame, sys, time, random, string    
from datetime import datetime
from datetime import timedelta
from pygame.locals import * 
import pygame.mixer

start_time = datetime.now()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() 
pygame.mixer.init()
(x,y,fontSize) = (10,40,20) 
myFont = pygame.font.SysFont("DejaVu Sans Mono", fontSize) 
bgColor = (0,8,0) 
screen = pygame.display.set_mode((800,600),0,32) 
pygame.display.set_caption("My First PyGame Windows")
background = pygame.image.load('f3term.png')
fontColor = (0xAA,0xFF,0xC3) 
fontHlColor = (0x00,0x08,0x00) 
bgHlColor = (0xAA,0xFF,0xC3) 
screen.blit(background, (0, 0))
pygame.display.flip()

done=False

i = 0
numScreens = 0
firstTime = 0
startTime = 0
myTime = 30
dY = 0
dX = 0 
numText = 0
numTries = 4
wordLen = 8
wordNum = 10
deltaY = 23
deltaX = 12
wordBase = ""
wordDisp = ""
garbStr = ""
statX = 0
statY = 0
WIDTH = 12
HEIGHT = 6
COLOR = (0xAA,0xFF,0xC3) 


fieldArea = []
textArea = []
statWord = []
wordChoice = []
servAreaTxt = ' ' * 192
servArea = []
posWords = []
activeWords = wordNum - 1

idAst = [67, 65, 63, 61]

leftBrakes = ['[', '(', '{', '<']
rightBrakes = [']', ')', '}', '>']

lasHlPos = 0
lastHlLen = 0

clock=pygame.time.Clock()

out_flag = 'bg'
print_flag = 0
bg_flag = 0

secretWord = ''

def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

class outSym(object):
    def __init__(self,x,y,width,height,char):
        self.data = [x,y,width,height,char]
	self.r = pygame.Rect(self.data[0]-self.data[2]/2, self.data[1]-self.data[3]/2, self.data[2], self.data[3])
        self.bg = background.subsurface(self.r)
    def __getitem__(self,item):
        return self.data[item]
    def __setitem__(self, idx, value):
        self.data[idx] = value
    @property
    def x(self):
        return self.data[0]
    @property
    def y(self):
        return self.data[1]
    @property
    def width(self):
        return self.data[2]
    @property
    def height(self):
        return self.data[3]
    @property
    def char(self):
        return self.data[4]
    def output(self):
        textImage = myFont.render(self.data[4],True,fontColor)
        textRect = textImage.get_rect()
        textRect.center = (self.data[0], self.data[1])
	screen.blit(textImage, textRect)
	pygame.display.update(self.r)
    def clear(self):
        screen.blit(self.bg, (self.data[0]-self.data[2]/2, self.data[1]-self.data[3]/2))
        pygame.display.update(self.r)
    def highlight(self):
        textImage = myFont.render(self.data[4],True,fontHlColor,bgHlColor)
        textRect = textImage.get_rect()
        textRect.center = (self.data[0], self.data[1])
	screen.blit(textImage, textRect)
	pygame.display.update(self.r)
    def bgreturn(self):
        textImage = myFont.render(self.data[4],True,fontColor)
        textRect = textImage.get_rect()
        textRect.center = (self.data[0], self.data[1])
        screen.blit(self.bg, (self.data[0]-self.data[2]/2, self.data[1]-self.data[3]/2))
	screen.blit(textImage, textRect)
	pygame.display.update(self.r)


def wordHl(wordPos,wordSize):
    global lastHlPos
    global lastHlLen
    i = 0
    while i < wordSize:
        textArea[i + wordPos].highlight()
        i += 1
    lastHlPos = wordPos
    lastHlLen = wordSize
    return

def wordBg():
    global lastHlPos
    global lastHlLen
    i = 0
    while i < lastHlLen:
        textArea[i + lastHlPos].bgreturn()
        i += 1
    lastHlPos = 0
    lastHlLen = 0
    return

def statWordWrite(myX, myY, typeStr):
    global deltaX
    global deltaY
    global dX
    global dY
    i = 0
    for char in typeStr:
        statWord.append(outSym(568 + deltaX * dX, myY + dY, 10, 20, char))
        statWord[i].output()
        i += 1
        dX += 1
    dY = 0
    dX = 0

def statWordClear():
    i = 0
    l = len(statWord)
    while i < l:
	statWord[i].clear()
        i += 1
    i = l - 1
    while i >= 0:
        del statWord[i]
        i -= 1
    return

def servWrite(typeStr):
    global deltaX
    global deltaY
    i = 0
    j = 0
    while i < 16:
        while j < 12:
            servArea.append(outSym(568 + deltaX * j, 125 + deltaY * i, 10, 20, typeStr[i*12+j]))
            servArea[i*12+j].output()
            j += 1
        i += 1
        j = 0
    return

def servClear():
    i = 0
    l = len(servArea)
    while i < l:
	servArea[i].clear()
        i += 1
    i = l - 1
    while i >= 0:
        del servArea[i]
        i -= 1
    return

def typeWriter(myX, myY, typeStr, interval, t):
    myTime = interval
    global deltaX
    global deltaY
    global dX
    global dY
    global statX
    global statY
    done = True
    startTime = millis()
    myLen = len(t)
    i = 0
    j = 0
    flag = 0 
    myTime = interval
    prtSnd = pygame.mixer.Sound('f3termprint.wav')
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    print "Enter"
                    myTime = interval / 4
        if flag == 0:
            char = typeStr[i]
            flag = 1
            if char == '\n':
                dY += deltaY
                dX = 0
            else:
                if char == '\r':
                    dX = 0
                else:
                    prtSnd.play(loops = 0, maxtime = myTime)
                    t.append(outSym(myX + deltaX * dX, myY + dY, 10, 20, char))
                    t[j + myLen].output()
                    j += 1
                    dX += 1
        curTime = millis()
        if curTime >= (startTime + myTime):
            i += 1
            if i >= len(typeStr):
                done = False
            flag = 0
	    startTime = curTime
    statX = myX + deltaX * dX
    statY = myY + dY
    dX = 0
    dY = 0
    return

def killAllText(t):
    global dX
    global dY
    i = 0
    l = len(t)
    while i < l:
	t[i].clear()
        i += 1
    i = l - 1
    while i >= 0:
        del t[i]
        i -= 1
    dX = 0
    dY = 0
    return


hello1Text = "WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK\n\n\
>SET TERMINAL INQUIRE\n\n\
RIT-V300\n\n\
>SET FILE/PROTECTION OWNER:RWED ACCOUNTS.F\n\
>SET HALT RESTART/MAINT\n\n\
Initializing Robco Industries(TM) MF Boot Agent v2.3.0\n\
RETROS BIOS\n\
RBIOS-4.02.08.00 52EE5.E7.E8\n\
Copyright 2201-2203 Robco Ind.\n\
Uppermem 64 KB\n\
Root (5A8)\n\
Maintenance Mode\n\n\
>RUN DEBUG/ACCOUNTS.F"

i = 0
triesAst= ''

while i < numTries:
    triesAst += '* '
    i += 1
typeWriter(10,10,hello1Text,30,fieldArea)
time.sleep(0.5)
killAllText(fieldArea)

def fieldFull():
    global wordBase
    global wordDisp
    global wordNum
    global wordLen
    global garbStr
    global helloText
    global wordChoice
    global secretWord
    global statX
    global statY
    global deltaX
    global deltaY
    i = 0
    triesAst= ''
    helloText = ''
    while i < numTries:
        triesAst += '* '
        i += 1
    typeWriter(10, 10, \
"ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL\nENTER PASSWORD\n\n{0} TRIES {1}\n\n".format(numTries,triesAst), \
10, fieldArea)
    i = 0
    f = open ('words8.txt','r')
    for line in f:
        wordBase += line.strip()
        i += 1
    f.close
    wordCnt = i
    i = 0
    n = 0
    step = int(wordCnt/wordNum)
    while i < wordNum:
        n = random.randint(i*step, i*step+step)
        wordChoice.append(wordBase[n*wordLen:n*wordLen+wordLen])
        wordDisp += wordBase[n*wordLen:n*wordLen+wordLen]
        i += 1
    secretWord = wordChoice[random.randint(0, wordNum - 1)]
    print secretWord
    i = 0
    j = 0
    wCnt = 0
    step = int(408/wordNum)
    while i < wordNum: 
        cPos = random.randint(0,step-wordLen)
        j = 0
        while j < cPos:
            garbStr += random.choice(string.punctuation)
            j += 1
        garbStr += wordDisp[i*wordLen:i*wordLen+wordLen]
        posWords.append((len(garbStr)-wordLen))
        wCnt += 1
	j += wordLen
	while j < step:
	    garbStr += random.choice(string.punctuation)
	    j += 1
   	i += 1
    j = len(garbStr)
    while j<408:
	garbStr += random.choice(string.punctuation)
	j += 1
    i = 0
    startHex = random.randint(0x1A00,0xFA00)

    workY = statY

    while i < 17:
        hexLeft = '{0:#4X}  '.format(startHex + i*12)
        statX = 10
        typeWriter(statX, statY, hexLeft, 10, fieldArea)
        typeWriter(statX, statY, garbStr[i*12:i*12+12] + "\n", 10, textArea)
        i += 1

    statY = workY
    i = 0

    while i < 17:
        statX = 248
        hexRight = '    {0:#4X}  '.format(startHex + (i+17)*12)
        typeWriter(statX, statY, hexRight, 10, fieldArea)
        typeWriter(statX, statY, garbStr[(i+17)*12:(i+17)*12+12]+"\n", 10, textArea)
        i += 1

    typeWriter(538,493," >",10, fieldArea)

    i = 0
    while i < wordNum:
        selWord = garbStr[posWords[i]:posWords[i]+wordLen]
        if selWord == secretWord:
            print "Password detected"
            del(posWords[i])
            break
        i += 1

fieldFull()

#s_time=millis()
#s = outSym(400,400,10,20,'A')

inverseBar_strings = (
"                ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
" oooooooooooooo ",
"                "   )

cursor, mask = pygame.cursors.compile(inverseBar_strings,'x','.','o')
pygame.mouse.set_cursor((16,16),(7,5),cursor,mask)

prevWord = ''
selWord = ''

wrdSnd = pygame.mixer.Sound('f3termprint.wav')

bMouse = 0    
firstpos = 0
startWord = 0
hlPos = 0
hlLen = 0

servWrite(servAreaTxt)


while done==False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    (curX,curY) = pygame.mouse.get_pos()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    numstr = int(curY / deltaY) + 1
    numchr = int(curX / deltaX)
    splText = helloText.split('\n',600/deltaY)
    curpos = -1
    selWord=''
    if(numstr >= 6 and numstr <= 22 and numchr >=8 and numchr <= 43):
        if(numchr >= 8 and numchr <= 20):
            curpos = (numstr - 6) * 12 + numchr - 8
        else:
            if(numchr >= 32 and numchr <= 43):
                curpos = 12 * 17 + (numstr - 6) * 12 + numchr - 32
        if(garbStr[curpos].isalpha()):
            i=0
            curchr=garbStr[curpos]
            while(curchr.isalpha() and (curpos+i) >= 0):
                i -= 1
                curchr = garbStr[curpos+i]
            i += 1
            firstpos = curpos + i
            hlPos = firstpos
            hlLen = wordLen
            startWord = firstpos
            i = 0
            curchr = garbStr[firstpos]
            while(curchr.isalpha() and (firstpos+i) <= 407):
                selWord += curchr
                i += 1
                curchr = garbStr[firstpos + i]
            if prevWord != selWord:
                wrdSnd.play()
                bMouse = 1
                wordBg()
                wordHl(hlPos,hlLen)
                statWordClear()
                statWordWrite(statX,statY,selWord)
                prevWord = selWord
        else:
            if garbStr[curpos] in leftBrakes:
                selWord = 'brakes'
                leftBorder = curpos
                rightBorder = int((curpos)/12+1)*12 - 1
                idxBrake = curpos
                numBrake = leftBrakes.index(garbStr[curpos])
                while idxBrake <= rightBorder:
                    if garbStr[idxBrake] == rightBrakes[numBrake]:
                        hlPos = curpos
                        hlLen = idxBrake + 1 - curpos
                        selWord = garbStr[leftBorder:idxBrake + 1]
                        break
                    if garbStr[idxBrake].isalpha():
                        break
                    idxBrake += 1
            else:
                if garbStr[curpos] in rightBrakes:
                    selWord = 'brakes'
                    rightBorder = curpos
                    leftBorder = int((curpos)/12)*12
                    idxBrake = curpos
                    numBrake = rightBrakes.index(garbStr[curpos])
                    while idxBrake >= leftBorder:
                        if garbStr[idxBrake] == leftBrakes[numBrake]:
                            hlPos = idxBrake
                            hlLen = rightBorder+1-idxBrake
                            selWord = garbStr[idxBrake:rightBorder+1]
                            break
                        if garbStr[idxBrake].isalpha():
                            break
                        idxBrake -= 1
            if ((selWord != prevWord and selWord != 'brakes') or (selWord != prevWord and prevWord != '')):
                if selWord == '' or selWord == 'brakes':
                    wordBg()
                    statWordClear()
                    selWord = ''
                else: 
                    wrdSnd.play()
                    bMouse = 1
                    wordBg()
                    statWordClear()
                    statWordWrite(statX, statY, selWord)
                    wordHl(hlPos,hlLen)
                prevWord = selWord
    else:
        statWordClear() 
        wordBg()        
        prevWord = ''
        selWord = ''
    if (b1 == True and bMouse == 1 and selWord != '' and selWord != 'brakes'):
    # Обрабатываем выбор слова
        print selWord    
        print secretWord
        if selWord[0].isalpha():
            # выбрано слово
            i = 0
            rightLet = 0
            while i < wordLen:
                if selWord[i] == secretWord[i]:
                    rightLet += 1
                i += 1
            prtLet = str(rightLet) + ' of ' + str(wordLen)
            servAreaTxt = servAreaTxt[24:] + (selWord + ' ' * (12 - len(selWord)) + prtLet + ' ' * (12 - len(prtLet)))
            servClear()
            servWrite(servAreaTxt)
            selWord = ''
            bMouse = 0
            i = 0
            if rightLet != wordLen:
                # Списываем попытку
                numTries -= 1
                ntX = fieldArea[53].x
                ntY = fieldArea[53].y
                fieldArea[53].clear()
                fieldArea[53] = outSym(ntX, ntY, 10, 20, str(numTries))
                fieldArea[53].output()
                fieldArea[idAst[numTries]].clear()
                if numTries == 0:
                # Залочились
                    exit()
        else:
            # выбрана последовательность знаков в скобках
            # заменяем спецзнаки точками, не трогая правую скобку
            i = 0
            while i < lastHlLen - 1:
                garbStr = garbStr[:lastHlPos+i] + '.' + garbStr[lastHlPos + i + 1:]
                textArea[lastHlPos + i].clear()
                ntX = textArea[lastHlPos + i].x
                ntY = textArea[lastHlPos + i].y
                textArea[lastHlPos + i] = outSym(ntX, ntY, 10, 20, '.')
                textArea[lastHlPos + i].output()
                i += 1

            resBrakes = random.randint(0,wordLen)
            if resBrakes == 1:
                # Восстанавливаем число попыток
                tmpWord = 'RESET TRIES '
                bMouse = 0
                servAreaTxt = servAreaTxt[12:] + tmpWord
                servClear()
                servWrite(servAreaTxt)
                numTries = 4
                ntX = fieldArea[53].x
                ntY = fieldArea[53].y
                fieldArea[53].clear()
                fieldArea[53] = outSym(ntX, ntY, 10, 20, str(numTries))
                fieldArea[53].output()
                i = 0
                while i < 4:
                    fieldArea[idAst[i]].output()
                    i += 1
            else:
                # Убираем "заглушку"
                tmpWord = 'REMOVE DUMMY'
                bMouse = 0
                servAreaTxt = servAreaTxt[12:] + tmpWord
                servClear()
                servWrite(servAreaTxt)
                if activeWords > 0:
                    # Не только пароль на экране
                    resBrakes = random.randint(0,activeWords - 1)
                    activeWords -= 1
                    i = 0
                    while i < wordLen:
                        txt = garbStr[:posWords[resBrakes]+i]
                        txt1 = garbStr[posWords[resBrakes] + i + 1:]
                        garbStr = garbStr[:posWords[resBrakes]+i] + '.' + garbStr[posWords[resBrakes] + i + 1:]
                        textArea[posWords[resBrakes]+i].clear()
                        ntX = textArea[posWords[resBrakes]+i].x
                        ntY = textArea[posWords[resBrakes]+i].y
                        textArea[posWords[resBrakes]+i] = outSym(ntX, ntY, 10, 20, '.')
                        textArea[posWords[resBrakes]+i].output()
                        i += 1
                    del posWords[resBrakes]
    clock.tick(30)
pygame.quit()


