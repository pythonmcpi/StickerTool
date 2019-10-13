# For compiling with cx_freeze, here is the module list:
# Name                            -     Usage
# pygame                          -     pygame, pygame.locals
# sys                             -     sys
# time                            -     time
# tkinter                         -     tkinter, filedialog, messagebox
# End list
import pygame
from pygame.locals import *
import sys
import time
import tkinter
from tkinter import filedialog
from tkinter import messagebox

# Image scaling system to avoid distortion
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
# End code snippet

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
background = None
sticker = None
placed = False

# Tk init
root = tkinter.Tk()
root.withdraw()

messagebox.showinfo("Welcome","Welcome to Image Processor, made by PythonPro.")
while not done:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if messagebox.askokcancel("Exit","Do you want to quit Image Processor?"):
                if messagebox.askyesno("Save","Do you want to save?"):
                    messagebox.showinfo("Save","Hit ctrl+s to save, then exit by hitting no save.")
                else:
                    messagebox.showinfo("Thank you","Thank you for using Image Processor.")
                    done = True
        elif event.type == pygame.VIDEORESIZE:
            size = [event.w,event.h]
            screen = pygame.display.set_mode((event.w,event.h),HWSURFACE|DOUBLEBUF|RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                ctrl = True
            elif event.key == pygame.K_s:
                if ctrl:
                    screen.fill((0,0,0))
                    render = text.render("Saving",False,(255,255,255))
                    screen.blit(render,(0,0))
                    pygame.display.update()
                    time.sleep(0.5)
                    while True:
                        filename = filedialog.asksaveasfilename(initialdir = "%CD%",title = "Save your edited picture",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
                        if filename == "":
                            break
                        else:
                            filename = filename + ".jpg"
                        save = background
                        save.blit(sticker,pos)
                        pygame.image.save(save,filename)
                        del save
                        break
            elif event.key == pygame.K_o:
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
            elif event.key == pygame.K_i:
                if ctrl:
                    screen.fill((0,0,0))
                    render = text.render("Opening sticker file...",False,(255,255,255))
                    screen.blit(render,(250,250))
                    pygame.display.update()
                    time.sleep(0.5)
                    stickerfilename = filedialog.askopenfilename(initialdir = "%CD%",title = "Open your sticker to use",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))
                    sticker = pygame.image.load(stickerfilename)
                    sticker = aspect_scale(sticker,stickersize)
                    placed = False
            elif event.key == pygame.K_h:
                messagebox.showinfo("Help","Welcome to help. This is still a incomplete feature, and you are not a develoer, so you may not acess this function. P.S. Developer mode is not a feature yet.")
                # ===============================================================================[Feature]==============================================================================================
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                ctrl = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                placed = True
                pos = mouse_pos
            if event.button == 2:
                stickersize = [100,100]
                sticker = pygame.image.load(stickerfilename)
                sticker = aspect_scale(sticker,stickersize)
            if event.button == 3:
                placed = False
                del pos
            if event.button == 4:
                stickersize = [stickersize[0]+15,stickersize[1]+15]
                sticker = pygame.image.load(stickerfilename)
                sticker = aspect_scale(sticker,stickersize)
            if event.button == 5:
                if stickersize[0] > 0:
                    stickersize = [stickersize[0]-15,stickersize[1]-15]
                    sticker = pygame.image.load(stickerfilename)
                    sticker = aspect_scale(sticker,stickersize)
    # write program logic here
    
    # clear the screen before drawing
    screen.fill(BLACK) 
    # write draw code here
    if background != None:
        screen.blit(background,(0,0))
    if sticker != None:
        if not placed:
            screen.blit(sticker,mouse_pos)
        if placed:
            screen.blit(sticker,pos)
    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(60)
 
# close the window and quit
pygame.quit()
sys.exit()
