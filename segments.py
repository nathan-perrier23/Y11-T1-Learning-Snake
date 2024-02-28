# import nessesary libaries
import pygame
import random

class SEGMENTS():
    def colorize(image, newColour): 
                
        image = image.copy() # create a copy of the image

        # zero out RGB values
        image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT) # sets the images opacity to max
        # add in new RGB values
        image.fill(newColour[0:3] + (0,), None, pygame.BLEND_RGBA_ADD) # replaces the colour with the new colour

        return image # returns the image
    
    def random_color():
        r = random.randint(0,255) # gets a random red value
        g = random.randint(0,100) # gets a random green value 
        b = random.randint(0,255) # gets a random blue value
        return (r,g,b) # returns the rgb values
    
   
                