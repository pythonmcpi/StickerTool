# For compiling with cx_freeze, here is the module list:
# Name                            -     Usage
# pygame                          -     pygame, pygame.locals
# sys                             -     sys
# time                            -     time
# tkinter                         -     tkinter, filedialog, messagebox
#
# Pillow (PIL)                    -     RGBA transparency
# End list
import pygame
from pygame.locals import *
import sys
import time
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

# ===[ Image scaling system to avoid distortion ]=== #
"""
aspect_scale.py - Scaling surfaces keeping their aspect ratio
Raiser, Frank - Sep 6, 2k++
crashchaos at gmx.net

This is a pretty simple and basic function that is a kind of
enhancement to pygame.transform.scale. It scales a surface
(using pygame.transform.scale) but keeps the surface's aspect
ratio intact. So you will not get distorted images after scaling.
A pretty basic functionality indeed but also a pretty useful one.

Usage:
is straightforward.. just create your surface and pass it as
first parameter. Then pass the width and height of the box to
which size your surface shall be scaled as a tuple in the second
parameter. The aspect_scale method will then return you the scaled
surface (which does not neccessarily have the size of the specified
box of course)

Dependency:
a pygame version supporting pygame.transform (pygame-1.1+)
"""

def aspect_scale(img,b):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    bx, by = b
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    if int(sx) > 0 and int(sy) > 0:
        return pygame.transform.scale(img, (int(sx),int(sy)))
    else:
        return aspect_scale(img,(100,100))
# ==========[ End code snippet ]=========== #

# initialize program engine
pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Image Processer')
# Set sticker default size
stickersize = [100,100]
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

# text setup
text = pygame.font.SysFont("Consolas",12)
# Loop until the user clicks close button
done = False
ctrl = False
alt = False
background = None
sticker = None
backgroundLoaded = False
stickerLoaded = False
placed = False

# Tk init
root = tkinter.Tk()
root.withdraw()

messagebox.showinfo("Welcome","Welcome to Image Processor, made by PythonPro.")
while not done:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #####----------[ Add the EDIT variable ]----------#####
            if messagebox.askokcancel("Exit","Do you want to quit Image Processor?"):
                if messagebox.askyesno("Save","Do you want to save?"):
                    messagebox.showinfo("Save","Hit ctrl+s to save, then exit by hitting no save.")
                else:
                    messagebox.showinfo("Thank you","Thank you for using Image Processor.")
                    done = True
        elif event.type == pygame.VIDEORESIZE:
            # WindowResize event: Resizes the window to desired size
            size = [event.w,event.h]
            screen = pygame.display.set_mode((event.w,event.h),HWSURFACE|DOUBLEBUF|RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                # Control Key held down
                ctrl = True
            elif event.key == pygame.K_RALT or event.key == pygame.K_LALT:
                # Alt Key held down
                alt = True
            elif event.key == pygame.K_s:
                #####----------[ Need to update and also enable saving using a menu ]----------#####
                if ctrl:
                    if not backgroundLoaded:
                        screen.fill((0,0,0))
                        render = text.render("You need to select an image to paste a sticker on first!",False,(255,255,255))
                        screen.blit(render,(0,0))
                        pygame.display.update()
                        time.sleep(1)
                    elif not stickerLoaded:
                        screen.fill((0,0,0))
                        render = text.render("You need to select and place a sticker first!",False,(255,255,255))
                        screen.blit(render,(0,0))
                        pygame.display.update()
                        time.sleep(1)
                    elif not placed:
                        screen.fill((0,0,0))
                        render = text.render("You need to place the sticker first!",False,(255,255,255))
                        screen.blit(render,(0,0))
                        pygame.display.update()
                        time.sleep(1)
                    else:
                        # Saving - Text
                        screen.fill((0,0,0))
                        render = text.render("Saving",False,(255,255,255))
                        screen.blit(render,(0,0))
                        pygame.display.update()
                        time.sleep(0.5)
                        while True:
                            # Saves only with PNG files!
                            savefilename = filedialog.asksaveasfilename(initialdir = "%CD%",title = "Save your edited picture",filetypes = (("png files","*.png"),("all files","*.*")))
                            if savefilename == "":
                                break
                            else:
                                savefilename = savefilename + ".PNG"
                            # Saving - Now uses Pillow
                            '''
                            save = background
                            save.blit(sticker,pos)
                            pygame.image.save(save,savefilename)
                            del save
                            '''
                            save = Image.open(filename)
                            stickerimg = Image.open(stickerfilename)
                            save.paste(stickerimg,pos,stickerimg)
                            save.save(savefilename,"PNG")
                            break
            elif event.key == pygame.K_o:
                #####----------[ Need to update and also enable opening using a menu ]----------#####
                if ctrl:
                    screen.fill((0,0,0))
                    render = text.render("Opening background file...",False,(255,255,255))
                    screen.blit(render,(250,250))
                    pygame.display.update()
                    time.sleep(0.5)
                    filename = filedialog.askopenfilename(initialdir = "%CD%",title = "Open your photo to edit",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
                    background = pygame.image.load(filename)
                    background = aspect_scale(background, size)
                    screen.fill((0,0,0))
                    render = text.render("Use ctrl + i to open sunglasses file",False,(255,255,255))
                    screen.blit(render,(250,250))
                    pygame.display.update()
                    time.sleep(1)
                    backgroundLoaded = True
            elif event.key == pygame.K_i:
                #####----------[ Need to update and also enable choosing using a menu ]----------#####
                if ctrl:
                    # Sticker files are now default to PNG (transparency!)
                    screen.fill((0,0,0))
                    render = text.render("Opening sticker file...",False,(255,255,255))
                    screen.blit(render,(250,250))
                    pygame.display.update()
                    time.sleep(0.5)
                    stickerfilename = filedialog.askopenfilename(initialdir = "%CD%",title = "Open your sticker to use",filetypes = (("png files","*.png"),("jpeg files","*.jpg"),("all files","*.*")))
                    sticker = pygame.image.load(stickerfilename)
                    sticker = aspect_scale(sticker,stickersize)
                    placed = False
                    stickerLoaded = True
            elif event.key == pygame.K_h:
                messagebox.showinfo("Help","Welcome to help. This feature not implemented yet.")
                # ===============================================================================[Feature]==============================================================================================
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                # Control Key not held
                ctrl = False
            elif event.key == pygame.K_RALT or event.key == pygame.K_LALT:
                # Alt Key not held
                alt = False
        elif event.type == pygame.MOUSEMOTION:
            # Update the mouse location
            mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left Click
                #####----------[ Need to allow for clicking in the menu, add x,y coord check ]----------#####
                # Places the sticker
                placed = True
                pos = mouse_pos
            if event.button == 2: # Middle Click
                #####----------[ Need to also be able to use the menu for this ]----------#####
                # Resets the sticker size
                stickersize = [100,100]
                sticker = pygame.image.load(stickerfilename)
                sticker = aspect_scale(sticker,stickersize)
            if event.button == 3: # Right Click
                #####----------[ Need to be able to use the menu for this as well ]----------#####
                # Unplaces the sticker
                placed = False
                try:
                    del pos
                except:
                    pass
            if event.button == 4: # Scroll Up
                #####----------[ Need to be able to do this in the menu ]----------#####
                # Makes the sticker bigger
                stickersize = [stickersize[0]+15,stickersize[1]+15]
                sticker = pygame.image.load(stickerfilename)
                sticker = aspect_scale(sticker,stickersize)
            if event.button == 5: # Scroll Down
                #####----------[ Need to be able to do this in the menu ]----------#####
                # Makes the sticker smaller
                if stickersize[0] > 0:
                    stickersize = [stickersize[0]-15,stickersize[1]-15]
                    sticker = pygame.image.load(stickerfilename)
                    sticker = aspect_scale(sticker,stickersize)
    # write program logic here
    ## Well... I don't really have any program "logic". Everything is triggered by an event. I'm triggered now XD
    
    # clear the screen before (re)drawing
    screen.fill(BLACK) 
    # write draw code here
    if background != None:
        screen.blit(background,(0,0))
    if sticker != None:
        if not placed:
            #####----------[ Center the sticker on the mouse instead of having the top left corner ]----------#####
            # Draw the sticker at the mouse's position
            screen.blit(sticker,mouse_pos)
        if placed:
            ###-----{ Render the sticker same as above ^ }-----###
            # Draw the sticker at the placed position
            screen.blit(sticker,pos)
    # update the screen
    pygame.display.update()
    # run at 60 fps
    clock.tick(60)
 
# close the window and quit
pygame.quit()
sys.exit()
