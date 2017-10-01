import pygame
from pygame.locals import *
import sys, time, math

from PIL import ImageGrab

def safe_float(vals, strings):
    result = list(vals)
    for i, s in enumerate(strings):
        try:
            val = float(s)
            result[i] = val
        except: pass
    return result


pygame.init()
pygame.font.init()
fsize = 18
font = pygame.font.SysFont(pygame.font.get_default_font(),18)

bgcolor = (255,255,255)
fgcolor = (0,0,0)
txtcolor = (0,0,0)

axsize = 16
axcolor = (0,192,0)
hicolor = (255,255,0, 128)

csize = 8

craw = ImageGrab.grabclipboard()
clip = pygame.image.fromstring(craw.tobytes(), craw.size, craw.mode)
w,h = clip.get_size()

size = (w+axsize, h+axsize+fsize)

screen = pygame.display.set_mode(size)

pygame.display.set_caption('graphWaker')

xmin = size[0]*.1
xmax = size[0]*.9
ymin = size[1]*.9
ymax = size[1]*.1

scales = ['0', '1', '0', '1']

xvmin = 0
xvmax = 1
yvmin = 0
yvmax = 1


scalesel = 0
wscale = w/4

axmove = False
axsel = 0

keys = map(str, range(10))
keys.extend(['.','-'])

sfmt = '{:0.3}'

pygame.mouse.set_visible(False)

firstsel = True

while 1:
    time.sleep(.05)
    mpos = pygame.mouse.get_pos()
    dx = 0
    dy = 0
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in map(ord,keys):
                if firstsel: scales[scalesel] = ''
                firstsel = False
                scales[scalesel] += chr(event.key)
            elif event.key == K_BACKSPACE:
                scales[scalesel] = scales[scalesel][:-1]
                if firstsel: scales[scalesel] = ''
                firstsel = False
            elif event.key == K_TAB:
                scalesel += 1
                firstsel = True
                if scalesel == 4: scalesel=0
            elif event.key == K_LEFT:
                dx = -1
            elif event.key == K_RIGHT:
                dx = 1
            elif event.key == K_UP:
                dy = -1
            elif event.key == K_DOWN:
                dy = 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mpos[1] > size[1]-axsize and mpos[0] > axsize:
                    axmove = True
                    d0 = abs(mpos[0]-xmin)
                    d1 = abs(mpos[0]-xmax)
                    if d0 < d1: axsel = 0
                    else: axsel = 1
                elif mpos[0] < axsize and mpos[1] > fsize:
                    axmove = True
                    d0 = abs(mpos[1]-ymin)
                    d1 = abs(mpos[1]-ymax)
                    if d0 < d1: axsel = 2
                    else: axsel = 3
                elif mpos[1] < fsize:
                    scalesel = int((mpos[0]-axsize)/wscale)
                    firstsel = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                axmove = False

    xvmin, xvmax, yvmin, yvmax = safe_float([xvmin, xvmax, yvmin, yvmax], scales)

    if axmove:
        if axsel == 0:
            xmin = mpos[0]
        elif axsel == 1:
            xmax = mpos[0]
        elif axsel == 2:
            ymin = mpos[1]
        elif axsel == 3:
            ymax = mpos[1]
    else:
        if dx != 0 and scalesel in [0,1]:
            if scalesel == 0: xmin += dx
            else: xmax += dx
        elif dy != 0 and scalesel in [2,3]:
            if scalesel == 2: ymin += dy
            else: ymax += dy



    xscale = (xvmax - xvmin)/(xmax-xmin)
    yscale = (yvmax - yvmin)/(ymax-ymin)

    xpos = xvmin + (mpos[0] - xmin)*xscale
    ypos = yvmin + (mpos[1] - ymin)*yscale

    screen.fill(bgcolor)

    screen.blit(clip, (axsize, fsize))
    pygame.draw.rect(screen, fgcolor, (axsize, fsize, w,h), 2)

    for i,x in enumerate((xmin,xmax)):
        color = axcolor
        if i == scalesel:
            color = hicolor
        pygame.draw.line(screen, color, (x, fsize), (x, size[1]))

    for i,y in enumerate((ymin,ymax)):
        color = axcolor
        if i == scalesel-2:
            color = hicolor
        pygame.draw.line(screen, color, (0, y), (size[0], y))

    for i, val in enumerate(scales):
        if scalesel != i:
            scaletxt = font.render(val, True, txtcolor)
        else:
            ehicolor= hicolor
            if firstsel: ehicolor = (0,255,0)
            try: float(val)
            except: ehicolor = (255,0,0,128)
            scaletxt = font.render(val, True, txtcolor, ehicolor)
        screen.blit(scaletxt, (axsize+i*wscale, (fsize-scaletxt.get_height())/2))

    if not axmove and mpos[0] > axsize and mpos[1] > fsize and mpos[1] < size[1]-axsize:
        txt = font.render(('({}, {})'.format(*[sfmt]*2)).format(xpos, ypos), True, txtcolor, bgcolor)
        screen.blit(txt, map(lambda x: x+1, mpos))

    pygame.draw.line(screen, fgcolor, (mpos[0]-csize, mpos[1]), (mpos[0]+csize, mpos[1]))
    pygame.draw.line(screen, fgcolor, (mpos[0], mpos[1]-csize), (mpos[0], mpos[1]+csize))
    
    pygame.display.flip()


