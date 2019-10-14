import sys
import pygame
import pygameMenu


BLACK = (0,0,0)
WHITE = (255,255,255)

def nothing():
    pass

def start():
    print ("Game has started.")

def about():
    print ("No credits!")

def quitGame():
    pygame.quit()
    sys.exit()

pygame.init()
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Test Menu')

clock = pygame.time.Clock()

menu = pygameMenu.Menu(screen,640,480,"Consolas","Test Menu",True,nothing)
menu.add_option("Start",start)
menu.add_option("About",about)
menu.add_option("Quit",quitGame)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quitGame()
    menu.mainloop(events)

    # Program Logic

    
    screen.fill(BLACK)
    menu.enable()
    menu.draw()
    
    pygame.display.update()
    clock.tick(60)
