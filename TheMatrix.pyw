import pygame
import random
import os
import time
import sys
import subprocess

InitLine = (-1, 0, None, 0, 5)
MetaSize = 5
SafeRnd = random.SystemRandom()
MaxLife = 16
TickRates = (1, 2, 2, 3, 3)
Density = 20
Rate = 3
ChngDensity = 1
EndChance = 30


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
#YELLOW = (0, 0, 255)
#BLACK = (255, 255, 255)
#GREEN = (255, 0, 255)
#WHITE = (0, 0, 0)


def Combine(a, b, Amt):
    return int(b[0] * Amt + a[0] * (1 - Amt)), int(b[1] * Amt + a[1] * (1 - Amt)), int(b[2] * Amt + a[2] * (1 - Amt))
def InitGrad(Lst, From, To):
    for c in xrange(len(Lst)):
        Lst[c] = Combine(From, To, float(c) / len(Lst))
LstTailGrad = [0] * MaxLife
LstHeadGrad = [0] * InitLine[4]

InitGrad(LstTailGrad, GREEN, BLACK)
LstTailGrad.reverse()
InitGrad(LstHeadGrad, WHITE, GREEN)

PrnChars = ['+', '<', '>', '=', ':', '-', '|']

for c in xrange(0, 26):
    PrnChars.append(unichr(ord('a') + c))
for c in xrange(1, 64):
    PrnChars.append(unichr(0xFF60 + c))
for c in xrange(0, 10):
    PrnChars.append(unichr(ord('0') + c))

def TickLine(Pos):
    global LstLines
    LstLine = LstLines[Pos]
    if len(LstLine) == 0:
        Num = 0
        for c in xrange(len(LstLines)):
            if len(LstLines[c]) > 0:
                Num += 1
        if 100 * (float(Num + 1) / len(LstLines)) <= Density and 100 * TickRate * SafeRnd.random() < Rate:
            LstLine = list(InitLine)
            LstLine[2] = TickRates[SafeRnd.randint(0, len(TickRates) - 1)]
            LstLines[Pos] = LstLine
        return False
    LstLine[3] -= 1
    if LstLine[3] <= 0:
        for c in xrange(MetaSize, len(LstLine)):
            if 100 * SafeRnd.random() < ChngDensity and (LstLine[0] < 0 or c - MetaSize >= MaxLife - LstLine[0]):
                LstLine[c] = PrnChars[SafeRnd.randint(0, len(PrnChars) - 1)]
        LstLine[3] = LstLine[2]
        if LstLine[0] == -1 and LstLine[1] + len(LstLine) - MetaSize < LineMax:
            LstLine.append(PrnChars[SafeRnd.randint(0, len(PrnChars) - 1)])
            if EndChance > 0 and SafeRnd.random() * 100 * TickRate < EndChance:
                LstLine[0] = MaxLife + 1
        if LstLine[0] == -1 and LstLine[1] + (len(LstLine) - MetaSize) >= LineMax:
            LstLine[0] = MaxLife
        elif LstLine[0] > 0:
            LstLine[0] -= 1
        elif LstLine[0] == 0 and len(LstLine) > MetaSize:
            LstLine.pop(MetaSize)
            LstLine[1] += 1
        elif LstLine[0] == 0:
            while len(LstLine) > 0:
                LstLine.pop()
        if len(LstLine) > 0 and LstLine[0] > 0 and LstLine[4] > 0:
            LstLine[4] -= 1
    else:
        return False
    return True
def DrawLine(LstLine):
    global CurrH
    global ChSize
    global AniFnt
    LineH = int(CurrH / ChSize[1])
    BmpDraw = pygame.Surface((ChSize[0], LineH * ChSize[1]))
    BmpDraw.fill(BLACK)
    if len(LstLine) == 0:
        BmpDraw.fill(BLACK)
    for c in xrange(len(InitLine), len(LstLine)):
        if (LstLine[0] == -1 or LstLine[0] == 16) and len(LstLine) - c >= LstLine[4]:
            BmpDraw.blit(AniFnt.render(LstLine[c], 1, GREEN, BLACK), pygame.rect.Rect(0, ChSize[1] * (c + LstLine[1] - len(InitLine)), ChSize[0], ChSize[1]))
        elif LstLine[0] >= 0 and c - MetaSize < MaxLife - LstLine[0]:
            BmpDraw.blit(AniFnt.render(LstLine[c], 1, LstTailGrad[c + LstLine[0] - len(InitLine)], BLACK), pygame.rect.Rect(0, ChSize[1] * (c + LstLine[1] - len(InitLine)), ChSize[0], ChSize[1]))
        elif len(LstLine) - c < LstLine[4]:
            BmpDraw.blit(AniFnt.render(LstLine[c], 1, LstHeadGrad[len(LstLine) - (c + 1)], BLACK), pygame.rect.Rect(0, ChSize[1] * (c + LstLine[1] - len(InitLine)), ChSize[0], ChSize[1]))
        else:
            BmpDraw.blit(AniFnt.render(LstLine[c], 1, GREEN, BLACK), pygame.rect.Rect(0, ChSize[1] * (c + LstLine[1] - len(InitLine)), ChSize[0], ChSize[1]))
    return pygame.transform.flip(BmpDraw, True, False)
pygame.font.init()
pygame.display.init()

CurrDir = "D:/PythonCode"
while not os.path.isdir(CurrDir) and ord(CurrDir[0]) < ord('Z'):
    CurrDir = chr(ord(CurrDir[0]) + 1) + CurrDir[1:]
if CurrDir[0] == 'Z':
    print "Error: Current drive directory not found"
    CurrDir = __file__.replace("\\", "/").rsplit("/", 1)[0]
    if not os.path.isdir(CurrDir + "./msgothic.ttc"):
        NotExit = False
        print " Exiting."

#AniFnt = pygame.font.SysFont("msgothicmspgothicmsuigothic", 14, False)
AniFnt = pygame.font.Font(CurrDir + "/msgothic.ttc", 16)
TxtFnt = pygame.font.SysFont("Courier New", 28, True)

ChSize = AniFnt.size("W")

OrigH = 320
OrigW = 640
CurrH = OrigH
CurrW = OrigW

MonW = pygame.display.Info().current_w
MonH = pygame.display.Info().current_h
#MonW = 1280
#MonH = 720
print "Width: " + str(MonW) + "\nHeight: " + str(MonH)

Surface = pygame.display.set_mode((CurrW, CurrH))
pygame.display.set_caption("The Matrix")
try:
    pygame.display.set_icon(pygame.image.load("MatrixIcon.png"))
except:
    pygame.display.set_icon(pygame.image.load("PythonCode/MatrixIcon.png"))
Surface.fill(BLACK)
pygame.display.update()
Delay = 2
#[Life, NumOffset, Tick Activate, CurrTick, End NewNess, ... Line]
LstLines = [list()] * (CurrW / ChSize[0])
LineMax = CurrH / ChSize[1]

IsFull = False
NotExit = True
TICK_EVT = pygame.USEREVENT
TICK_CAP = 40
TickRate = 20
pygame.time.set_timer(TICK_EVT, 1000/TickRate)
Paused = False
SwitchTick = False
Clk = pygame.time.get_ticks()
DispFps = False
TickNum = 0
FpsBmp = TxtFnt.render(str(TickRate), 1, YELLOW, (0,0,0))
FpsBmp.set_colorkey((0,0,0))
PrevRate = TickRate

ExitData = list()

while NotExit:
    Redraw = False
    Evt = pygame.event.wait()
    if Evt.type == pygame.QUIT:
        NotExit = False
    elif Evt.type == pygame.MOUSEBUTTONDOWN:
        if Evt.button == 1:
            print Evt.pos
    elif Evt.type == pygame.KEYDOWN:
        if Evt.key == pygame.K_F11:
            IsFull = not IsFull
            if IsFull:
                pygame.display.set_mode((MonW, MonH), pygame.FULLSCREEN)
                CurrW = MonW
                CurrH = MonH
            else:
                pygame.display.set_mode((OrigW, OrigH))
                CurrW = OrigW
                CurrH = OrigH
            LstLines = [list()] * (CurrW / ChSize[0])
            LineMax = CurrH / ChSize[1]
            Surface.fill(BLACK)
            Redraw = True
        elif Evt.key == ord(' '):
            Paused = not Paused
            if Paused:
                pygame.time.set_timer(TICK_EVT, 0)
            else:
                Clk = pygame.time.get_ticks()
                pygame.time.set_timer(TICK_EVT, 1000/TickRate)
        elif Evt.key == ord('f'):
            Paused = True
            pygame.time.set_timer(TICK_EVT, 0)
            pygame.event.post(pygame.event.Event(TICK_EVT, {}))
        elif Evt.key == ord('t'):
            Surface.fill(BLACK, pygame.rect.Rect(CurrW - FpsBmp.get_width(), 0, FpsBmp.get_width(), FpsBmp.get_height()))
            DispFps = not DispFps
        elif Evt.key == pygame.K_F5:
            ExitData.append(pygame.K_F4)
            ExitData.append(sys.executable)
        elif len(ExitData) > 0:
            if ExitData[0] == Evt.key:
                pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
            else:
                ExitData = list() 
    elif Evt.type == TICK_EVT:
        TickNum += 1
        if TickNum >= TickRate and DispFps:
            TickNum = 0
        if TickNum == 0 and PrevRate != TickRate:
            PrevRate = TickRate
            Surface.fill(BLACK, pygame.rect.Rect(CurrW - FpsBmp.get_width(), 0, FpsBmp.get_width(), FpsBmp.get_height()))
            FpsBmp = TxtFnt.render(str(TickRate), 1, YELLOW, (0,0,0))
            FpsBmp.set_colorkey((0,0,0))
        Beg = pygame.time.get_ticks()
        RangeMe = range(0, len(LstLines))
        random.shuffle(RangeMe, SafeRnd.random)
        for c in RangeMe:
            if TickLine(c):
                Bmp = DrawLine(LstLines[c])
                Surface.blit(Bmp, pygame.rect.Rect(c * ChSize[0], 0, ChSize[0], Bmp.get_height()))
                Redraw = True
        if DispFps:
            Surface.blit(FpsBmp, pygame.rect.Rect(CurrW - FpsBmp.get_width(), 0, FpsBmp.get_width(), FpsBmp.get_height()))
        End = pygame.time.get_ticks()
        if Paused:
            pass
        elif TickRate == 0:
            TickRate = 1
            pygame.time.set_timer(TICK_EVT, 1000/TickRate)
        elif ((End - Beg) > 1000/TickRate or pygame.event.peek(TICK_EVT)) and TickRate > 1:
            TickRate -= 1
            pygame.time.set_timer(TICK_EVT, 1000/TickRate)
        elif (End - Beg) < 1000/TickRate and TickRate < TICK_CAP:
            TickRate += 1
            pygame.time.set_timer(TICK_EVT, 1000/TickRate)
        Clk = Beg
    if Redraw:
        pygame.display.update()
pygame.quit()
print CurrDir
if len(ExitData) > 0:
    if ExitData[0] == pygame.K_F4:
        subprocess.Popen([ExitData[1], CurrDir[0:3] + "PythonCode/TheMatrix.pyw"], cwd = CurrDir[0:3] + "PythonCode")

