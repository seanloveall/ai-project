import sys

from PIL import Image
from PIL import ImageFilter

def iround(num):
    return int(round(num))

def grayscale_image(img):
    width, height = img.size
    
    for x in range(width):
        for y in range(height):
            red, green, blue = img.getpixel((x, y))

            #formula found on the web to convert to grayscale
            col = iround(0.3 * red + 0.59 * green + 0.11 * blue)
            
            img.putpixel((x, y), (col, col, col))
            
    return img

def resize_and_crop(img, size):
    width, height = img.size
    img_ratio = float(width) / height
    nwidth, nheight = size
    ratio = float(nwidth) / nheight
    
    
    #Scales either vertically or horizontally and then crops the image
    if ratio > img_ratio:
        #scales vertically
        img = img.resize((nwidth, iround(nheight * img_ratio)), Image.ANTIALIAS)

        #crops in the middle
        box = (0, iround((img.size[1] - nheight) / 2), nwidth, iround((img.size[1] + nheight) / 2))
        img = img.crop(box)
    elif ratio < img_ratio:
        #scales horizontally
        img = img.resize((iround(size[0] * img_ratio), size[1]), Image.ANTIALIAS)

        #crops in the middle
        box = (iround((img.size[0] - nwidth) / 2), 0, iround((img.size[0] + nwidth) / 2), nheight)
        img = img.crop(box)
    else :
        #scales 1:1
        img = img.resize((nwidth, nheight), Image.ANTIALIAS)
        
    return img

    

if(len(sys.argv) != 5):
    print "Must provide 4 arguments, first two arguments are input files, third argument is output file, and 4th argument is which alogirthm to use"
    sys.exit(1)

knownfiles = []
unknownfiles = []

#gets the known files
with open(sys.argv[1]) as inputfile:
    knownfiles = inputfile.read().split('\n')

#gets the unknown files
with open(sys.argv[2]) as inputfile:
    unknownfiles = inputfile.read().split('\n')

#split up each line, also remove any lines that are empty
list0 = []
list1 = []
i = 0
while i < len(knownfiles):
    if(knownfiles[i] == ""):
        i = i + 1
    else:
        num = knownfiles[i][-1:]
        if(int(num) == 0):
            list0.append(knownfiles[i][:-2])
        elif(int(num) == 1):
            list1.append(knownfiles[i][:-2])

        i = i + 1


#add a value for each line, also remove any lines that are empty
i = 0
while i < len(unknownfiles):
    if(unknownfiles[i] == ""):
        unknownfiles.pop(i)
    else:
        unknownfiles[i] = [unknownfiles[i], 0]
        i = i + 1


#magic happens here

if(sys.argv[4] == '1'):
    #### sean
    i = 0
    avg0 = [[0 for x in range(50)] for x in range(50)] 
    avg1 = [[0 for x in range(50)] for x in range(50)] 
    while i < len(list0):
        image = Image.open(list0[i])
        image = image.convert('RGB')
        image = resize_and_crop(image, (50, 50))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        
        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                avg0[x][y] += red
                
        i = i + 1

    i = 0
    while i < len(list1):
        image = Image.open(list1[i])
        image = image.convert('RGB')
        image = resize_and_crop(image, (50, 50))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        
        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                avg1[x][y] += red
                
        i = i + 1

    for x in range(len(avg0)):
        for y in range(len(avg0[0])):
            avg0[x][y] = avg0[x][y] / 50

    for x in range(len(avg1)):
        for y in range(len(avg1[0])):
            avg1[x][y] = avg1[x][y] / 50


    i = 0
    while i < len(unknownfiles):
        image = Image.open(unknownfiles[i][0])
        image = image.convert('RGB')
        image = resize_and_crop(image, (50, 50))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)

        score0 = 0
        score1 = 0

        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                num = abs(avg0[x][y] - red)
                num = float(num) / 255
                score0 = score0 + (1 - (1 * num))

                num = abs(avg1[x][y] - red)
                num = float(num) / 255
                score1 = score1 + (1 - (1 * num))

        pix = 50 * 50
        print score0
        print score1
        if(score0 > score1):
            num = score0 / pix
            num = abs(num - 0.5)
            unknownfiles[i][1] = "0-"+str(num)
        else:
            num = score1 / pix
            if(num <= 0.5):
                num = num + 0.5
            unknownfiles[i][1] = "1-"+str(num)

        #unknownfiles[i][1] = num

        i = i + 1

        #take the absolute of average - image, the closer it is to 0, the more we add to score (anywhere between 0 and 100)
        #when done checking all pixels, take the score, average them, and that's our first score
        #repeat above for second score
        #then compare the scores, and the higher one score is, the more the it will lean that way

    #image = Image.open(list0[4])
    #image = grayscale_image(image)
    #image = image.filter(ImageFilter.BLUR)
    #image = resize_and_crop(image, (100, 100))
    #image.save("C:/Python27/test.jpg")
    ####
elif(sys.argv[4] == '2'):
    # scott
    print("hi scott")
elif(sys.argv[4] == '3'):
    # rafi
    print("hi rafi")




#outputs the data
with open(sys.argv[3], 'w+') as outputfile:
    for elem in unknownfiles:
        outputfile.write(" ".join(str(v) for v in elem))
        outputfile.write("\n")
