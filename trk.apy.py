import pygame
import time
import random

pygame.init()

#Init pictures 
bif="background.png"
main="startWindow.png"
orangeWarningImg=pygame.image.load("orangeWarning.png")
redWarningImg=pygame.image.load("redWarning.png")
carImg=pygame.image.load('formula.png')

#Init sounds
crash_sound=pygame.mixer.Sound("supermario.wav")
coin=pygame.mixer.Sound("coin.wav")

#Init highscore
f = open("highscore.txt")
lines = f.read().splitlines()
if(len(lines)!=0):
        broj = lines[0]
else:
        broj = 0
f.close()

#Global variables
car_width=80
global HIGH_SCORE
HIGH_SCORE = int(broj)
FIRST_HIGH_SCORE = HIGH_SCORE
POMHIGH_SCORE=0
indicator= 0
display_width= 846
display_height= 600

#Init colors
black =(0, 0, 0)
green =(0, 118, 45)
red =(200, 0, 0)
blue =(102, 141, 242)
gold =(155, 198, 80)
red_hover =(150, 0, 0)
green_hover =(0, 240, 0)
red_crash =(242, 17, 9)

#Settings
icon = pygame.image.load("formula.png")
pygame.display.set_icon(icon)
gameDisplay=pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Trka!")

background=pygame.image.load(bif).convert()
main_menu=pygame.image.load(main).convert()
clock=pygame.time.Clock()


def write_to_file():
        if(FIRST_HIGH_SCORE<HIGH_SCORE):
                intputData = open("highscore.txt","w")
                intputData.write(str(HIGH_SCORE))
                intputData.close()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_to_file()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    write_to_file()
                    pygame.quit()
                    quit()
        pygame.mixer.music.stop()         
        
        textToWrite = "Press C to continue or Q to quit"
        largeText=pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, TextRect = text_objects(textToWrite, largeText)
        TextRect.center =((display_width/2), (display_height/2)) 
        gameDisplay.blit(TextSurf, TextRect)
    
        font=pygame.font.SysFont(None, 50)
        textToWrite=font.render("Pause", True, red)
        gameDisplay.blit(textToWrite, (350, 10))

        pygame.display.update()
        clock.tick(5)
        
    pygame.mixer.music.play(-1)
    
def score(count):
    font=pygame.font.SysFont(None, 50)
    textToWrite=font.render("Score:"+str(count), True, green)
    gameDisplay.blit(textToWrite, (15, 10))
    
def Hscore():
    font =pygame.font.SysFont(None, 50)
    textToWrite=font.render("HScore:"+str(HIGH_SCORE), True, gold)
    gameDisplay.blit(textToWrite, (15, 40))
    
def things(thingx, thingy, txt):
    thingImg=pygame.image.load(txt)
    gameDisplay.blit(thingImg, (thingx, thingy))
    
def car(x, y):
    gameDisplay.blit(carImg, (x, y))
#PAZNJA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def text_objects(textToWrite, font):
    string1='NEW HIGH SCORE!'
    if textToWrite== string1:
        textSurface=font.render(textToWrite, True, gold)
    else:
        textSurface=font.render(textToWrite, True, red_crash)
    return textSurface, textSurface.get_rect()

def message_display(textToWrite):
    largeText=pygame.font.Font('freesansbold.ttf', 70)
    TextSurf, TextRect = text_objects(textToWrite, largeText)
    TextRect.center =((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(3.5)
    Hscore()
    gameLoop()

def crash():
    global HIGH_SCORE
    global POMHIGH_SCORE
    global indicator
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    if POMHIGH_SCORE>0:
        indicator=1
    if HIGH_SCORE<POMHIGH_SCORE:
        HIGH_SCORE=POMHIGH_SCORE
        message_display('NEW HIGH SCORE!')
    else:
        message_display('You crashed :( ')
    
def minus():
    global HIGH_SCORE
    global POMHIGH_SCORE
    if POMHIGH_SCORE>0:
        global indicator
        indicator=1
    if HIGH_SCORE<POMHIGH_SCORE:
        HIGH_SCORE=POMHIGH_SCORE
        message_display('NEW HIGH SCORE!')
    else:
        message_display('Below 0 :(')
    
def button_action(msg, x, y, w, h, icolor, acolor, indicator):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w>mouse[0] > x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay, acolor, (x, y, w, h))
        if click[0]==1 and indicator==1:
            gameLoop()
        if click[0]==1 and indicator==0:
            pygame.quit()
            quit()
    else:
        pygame.draw.rect(gameDisplay, icolor, (x, y, w, h))
    smallText=pygame.font.Font("freesansbold.ttf", 40)
    textSurf, textRect=text_objects(msg, smallText)
    textRect.center=((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)
    
def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(main_menu, (0, 0))
        button_action("Play",300, 500, 200,100,green, green_hover, 1 )
        button_action("QUIT",600, 500, 200,100,red, red_hover, 0 )
       # pygame.draw.rect(gameDisplay, green,(300, 500, 200,150) )
       # pygame.draw.rect(gameDisplay, red_crash,(600, 500, 200,150) )
        pygame.display.update()
        clock.tick(15)
                
def gameLoop():
    
    pygame.mixer.music.play(-1)
    warning_indicator=0
    gameExit=True
    x=display_width*0.45
    y=display_height*0.8
    FPS=60
    x_moved=0
    crash_mud=0
    crash_sd=0

    rand=round(random.randrange(0, 1))
    rand2=round(random.randrange(0, 1))
    
    
    thing_startx=random.randrange(0, display_width-100)
    thing_starty=-random.randrange(100, display_height-100/4)
    
    thing_height=100
    thing_width=100

    thing2_startx=random.randrange(0, display_width-100)
    thing2_starty=-random.randrange((display_height-100)/4, (display_height-100)*2/3)
    thing2_width=100
    thing2_height=100

    thing3_startx=random.randrange(0, display_width-100)
    thing3_starty=-random.randrange((display_height-100)*2/3, display_height)
    thing3_width=100
    thing_speed=6
    thing2_speed=6
    thing3_speed=6 
    gameDisplay.blit(carImg, (x, y))
    count =0
    k=0
    moving=5
#    y_pomeraj = 0
    while gameExit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                write_to_file()
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_moved=-moving
                if event.key==pygame.K_RIGHT:
                    x_moved=moving
# Upgrade
#                if event.key==pygame.K_UP:
#                        y_pomeraj=-pomeraj
#                if event.key==pygame.K_DOWN:
#                       y_pomeraj=pomeraj

                if event.key == pygame.K_p:
                         pause()
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    x_moved=0

#                y_pomeraj = 0
#        if y+y_pomeraj<0:
#                y=0
#        else:
#                y+=y_pomeraj
        x+=x_moved
        
        if x>display_width-car_width or x<0:
            crash()
            
        if thing_starty>display_height:
            thing_startx=random.randrange(0, display_width-100)
            thing_starty=-random.randrange(100, display_height-100/4)
            
            
            
            if k1==1:
                count-=10
            rand=round(random.randrange(0, 1))
            rand2=round(random.randrange(0, 1))
            
        if thing2_starty>display_height:
            thing2_startx=random.randrange(0, display_width-100)
            thing2_starty=-random.randrange((display_height-100)/4, (display_height-100)*2/3)
            
            if k2==2:
                pygame.mixer.Sound.play(coin)
                count+=10
            
          
            rand=round(random.randrange(0, 1))
            rand2=round(random.randrange(0, 1))

        if thing3_starty>display_height:
            thing3_startx=random.randrange(0, display_width-100)
            thing3_starty=-random.randrange((display_height-100)*2/3, display_height)
            
            if k3==3:
                count-=10
            rand=round(random.randrange(0, 1))
            rand2=round(random.randrange(0, 1))
            
        if thing_starty>thing2_starty and thing_starty<thing2_starty+100:
                thing_starty+=thing2_starty+100-thing_starty
        if thing_starty>thing3_starty and thing_starty<thing3_starty+100:
                thing_starty+=thing3_starty+100-thing_starty
        if thing3_starty>thing_starty and thing3_starty<thing_starty+100:
                thing3_starty+=thing_starty+100-thing3_starty

        if thing3_starty>thing2_starty and thing3_starty<thing2_starty+100:
                thing3_starty+=thing2_starty+100-thing3_starty
                
        if thing2_starty>thing_starty and thing2_starty<thing_starty+100:
                thing2_starty+=thing_starty+100-thing2_starty
        if thing2_starty>thing3_starty and thing2_starty<thing3_starty+100:
                thing2_starty+=thing3_starty+100-thing2_starty
            
        gameDisplay.blit(background, (0, 0))
        if rand==0 or rand2==1:
            things(thing_startx, thing_starty, 'mud.jpg')
            thing_starty+=thing_speed
        if rand2==0:
            things(thing2_startx, thing2_starty, 'speed.png')
            things(thing3_startx, thing3_starty, 'stop.png')
            thing2_starty+=thing_speed
            thing3_starty+=thing_speed

        if y <= thing2_starty+thing_height:
            
            if x>=thing2_startx and x<=thing2_startx+thing2_width or x+car_width >=thing2_startx and x+car_width<=thing2_startx+thing2_width:
                
                k2=2
                
            else:
                k2=0
        if y <= thing_starty+thing_height:
            
            if x>=thing_startx and x<=thing_startx+thing2_width or x+car_width >=thing_startx and x+car_width<=thing_startx+thing_width:
                k1=1
                if crash_mud==1:
                    crash()
            
               
            else:
                k1=0
        if y <= thing3_starty+thing_height:
            
            if x>=thing3_startx and x<=thing3_startx+thing3_width or x+car_width >=thing3_startx and x+car_width<=thing3_startx+thing3_width:
                k3=3
                if crash_sd==1:
                    crash()
            
            else:
                k3=0
        
            
        if count>30 and count<50:
            
            thing_speed=7
            moving=7
            
        if count>=50 and count<70:
            
            thing_speed=8
            
        if count>=70:
            thing_speed=9
            moving=10
        if count>=100 and count<150:
            warning_indicator=0
            crash_mud=0
            crash_sd=0
            thing_speed=10
            moving=15
        if count>=150 and count<200:
            warning_indicator=1
            crash_mud=1
            crash_sd=0
            thing_speed=11
            moving=20
        if count>=200 and count<300:
            warning_indicator=2
            thing_speed=12
            crash_mud=1
            crash_sd=1
            moving=22
        if count>=300:
            
            thing_speed=15
            moving=25
            
        if count<0:
            minus()
        if warning_indicator==1:
            gameDisplay.blit(orangeWarningImg, (display_width-64, 10))
        elif warning_indicator==2:
            gameDisplay.blit(redWarningImg, (display_width-64, 10))
            
        global POMHIGH_SCORE
        POMHIGH_SCORE=count
        Hscore()
        score(count)
        car(x, y)
        pygame.display.update()
        clock.tick(FPS)

game_intro()        
gameLoop()
write_to_file()
pygame.quit()
quit()