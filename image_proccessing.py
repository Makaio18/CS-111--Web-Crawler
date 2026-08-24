import sys
from byuimage import Image
import requests


    
##### flagS #####


 
###### Turns an image gray by changing the pixels of RGB to the avg of their sum
def grayscale(filename):
    grey_png = Image(filename)

    for x in range(grey_png.width):
        for y in range(grey_png.height):

            pixel = grey_png.get_pixel(x,y)
            average = (pixel.red + pixel.green + pixel.blue) / 3
            pixel.red = average
            pixel.green = average
            pixel.blue = average

    grey_png.save(filename)
   
    
   


#### Provides a warm tint on an image.
def sepia(filename):
    serpia_png = Image(filename)

    for x in range(serpia_png.width):
        for y in range(serpia_png.height):

            pixels = serpia_png.get_pixel(x,y)

            true_red = 0.393 * pixels.red + 0.769 * pixels.green + 0.189 * pixels.blue
            true_green = 0.349 * pixels.red + 0.686 * pixels.green + 0.168 * pixels.blue
            true_blue = 0.272 * pixels.red + 0.534 * pixels.green + 0.131 * pixels.blue

            pixels.red = true_red
            pixels.blue = true_blue
            pixels.green = true_green

            if pixels.red > 255:
                pixels.red = 255

    serpia_png.save(filename)


##flips an image by creating a blank image of the same L x W 
#then reads the 

def flipped(filename):
    flipped_png = Image (filename)
    new_image = Image.blank(flipped_png.width, flipped_png.height)

    for x in range(flipped_png.width):
        for y in range(flipped_png.height):
            
            pixel = flipped_png.get_pixel(x,y)

            pixel_red = pixel.red
            pixel_green = pixel.green
            pixel_blue = pixel.blue

            new_pixel = new_image.get_pixel(x,new_image.height -y - 1)

            new_pixel.red = pixel_red
            new_pixel.green = pixel_green
            new_pixel.blue = pixel_blue

    new_image.save(filename)



def mirror(filename):
    mirror_png = Image(filename)
    new_image = Image.blank(mirror_png.width, mirror_png.height)

    for x in range(mirror_png.width):
        for y in range(mirror_png.height):
            
            pixel = mirror_png.get_pixel(x,y)

            pixel_red = pixel.red
            pixel_green = pixel.green
            pixel_blue = pixel.blue

            new_pixel = new_image.get_pixel(new_image.width -x -1, y)

            new_pixel.red = pixel_red
            new_pixel.green = pixel_green
            new_pixel.blue = pixel_blue
        
    new_image.save(filename)

#"-s" or "-g" or "-f" or "-m"
def applyfilter(filename, flag, ):
   

    if flag == "-s":
        sepia(filename)

    elif flag == "-g":
        grayscale(filename)

    elif flag == "-f":
        flipped(filename)
    
    elif flag == "-m":
        mirror(filename)


   
    
    


