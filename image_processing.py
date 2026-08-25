from byuimage import Image

"""
Modules:

Libs_________
    byuimage

functions______:
    grayscale(filename)
    sepia(filename)
    flipped(filename)
    mirror(filename)
    apply_filter
"""

##Turns an image gray by changing the pixels of RGB to the avvergae of their sum

def grayscale(filename):

    #saves copy of image as a image object
    grey_png = Image(filename)

    #loops over pixels (col by col) from left to right. the looping is kinda like a nested list
    for x in range(grey_png.width):
        for y in range(grey_png.height):

            # gets current pixel within image at said corrdianted of the imge, using method of image class. 
            pixel = grey_png.get_pixel(x,y)

            #sums the color values of the pixel at x,y cordinates and then divdes them by 3( to avg out to gray for speifcic pixel.)
            average = (pixel.red + pixel.green + pixel.blue) / 3

            #reaassigns RGB values of the current pixels to grey avg
            pixel.red = average
            pixel.green = average
            pixel.blue = average

    grey_png.save(filename)
   
    
   


#### Provides a warm tint on an image.
def sepia(filename):
    #saves file_name to an image object
    serpia_png = Image(filename)

    #loops over said image object
    for x in range(serpia_png.width):
        for y in range(serpia_png.height):

            #locates current pixel given x,y corrdinates, and then creates pixel object to manipulate
            pixels = serpia_png.get_pixel(x,y)


            #calulates the sepia filter for pixel object, and then saves R,G,B values to varibles.
            true_red = (0.393 * pixels.red) + (0.769 * pixels.green) + (0.189 * pixels.blue)

            true_green = (0.349 * pixels.red) + 0.686 * (pixels.green) + (0.168 * pixels.blue)

            true_blue = (0.272 * pixels.red) + (0.534 * pixels.green) + (0.131 * pixels.blue)

            # Reassigns the RGB values while keeping every channel in the
            # valid color range.
            pixels.red = min(255, true_red)
            pixels.green = min(255, true_green)
            pixels.blue = min(255, true_blue)

    serpia_png.save(filename)



#creates entire new image thas the same (L X W) of input imagem then iterates input image to fill in blank canvas)
#image doing a paint by numbers, where you use the box cover as refrence in order to paint the image upside down.

def flipped(filename):

    #creates image object for refrence  
    flipped_png = Image (filename)

    #Creates new image of the same length and widthm that that is a blank canvas
    new_image = Image.blank(flipped_png.width, flipped_png.height)

    #looping over the image. 
    for x in range(flipped_png.width):
        for y in range(flipped_png.height):

            #retreives current pixel object, as refrence
            pixel = flipped_png.get_pixel(x,y)

            #saves values from pixel object
            pixel_red = pixel.red
            pixel_green = pixel.green
            pixel_blue = pixel.blue

            #creates nedw pixel object, that will refrce the fliiped version of the image.
            #same roww, but opposite y from what the og image would use. 
            # (negative y allow srefrence towards end of lists,-1 is decmrent by 1 )
            new_pixel = new_image.get_pixel(x, new_image.height -y - 1)

            # reasssigns the valus of the pixels accodingly. 
            new_pixel.red = pixel_red
            new_pixel.green = pixel_green
            new_pixel.blue = pixel_blue

    #returnes new flipped image
    new_image.save(filename)



def mirror(filename):

    #saves file image as an image object
    mirror_png = Image(filename)

    #creates a blank canvas to paint with pixels from og input image
    new_image = Image.blank(mirror_png.width, mirror_png.height)


    # loops over the image
    for x in range(mirror_png.width):
        for y in range(mirror_png.height):

            #retrevies and creates pixel object to store
            pixel = mirror_png.get_pixel(x,y)

            #uses values from pixel object
            pixel_red = pixel.red
            pixel_green = pixel.green
            pixel_blue = pixel.blue

            #creates new pixel object that will populate new blank image
            #use negative x (starts from bottom of image, decremente by one)
            new_pixel = new_image.get_pixel(new_image.width -x -1, y)

            #values being re-assigned from orignal image to blank canvas
            new_pixel.red = pixel_red
            new_pixel.green = pixel_green
            new_pixel.blue = pixel_blue

    #returns full mirrred image object. 
    new_image.save(filename)


#"-s" or "-g" or "-f" or "-m"
# sequencing of the program, chaning the flow of logic based of flag given in parameters.
# validationn of flag is done before calls of fucntions( so validation is not needed here)
def apply_filter(filename, flag):

    if flag == "-s":
        sepia(filename)

    elif flag == "-g":
        grayscale(filename)

    elif flag == "-f":
        flipped(filename)
    
    elif flag == "-m":
        mirror(filename)


   
    
    
