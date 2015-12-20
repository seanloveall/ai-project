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
        print i
        print 
        image = Image.open(list0[i])
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        image = resize_and_crop(image, (50, 50))
        
        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                avg0[x][y] += red
                
        i = i + 1

    print avg0[30][20]

    #image = Image.open(list0[4])
    #image = grayscale_image(image)
    #image = image.filter(ImageFilter.BLUR)
    #image = resize_and_crop(image, (100, 100))
    #image.save("C:/Python27/test.jpg")
    ####
elif(sys.argv[4] == '2'):
    # scott
    i = 0
    avg0 = [[0 for x in range(50)] for x in range(50)] 
    avg1 = [[0 for x in range(50)] for x in range(50)]
    count0 = 2500/len(list0)
    count1 = 2500/len(list1)
    x = 0
    y = 0
    while i < len(list0):
        image = Image.open(list0[i])
        image = image.convert('RGB')
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        image = resize_and_crop(image, (50, 50))
        
        width, height = image.size
        for j in range(count0):
            #print x
            #print y
            avg0[x][y] = image.getpixel((x, y))
            if(x == 49 and y == 49):
                break
            elif(y == 49):
                x += 1
                y = 0
            else:
                y += 1

        i = i + 1

    #starting to create it for list1
    x = 0
    y = 0
    i = 0
    while i < len(list1):
        image = Image.open(list1[i])
        image = image.convert('RGB')
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        image = resize_and_crop(image, (50, 50))
        
        width, height = image.size
        for j in range(count1):
            #print x
            #print y
            avg1[x][y] = image.getpixel((x, y))
            if(x == 49 and y == 49):
                break
            elif(y == 49):
                x += 1
                y = 0
            else:
                y += 1

        i = i + 1
    
    print avg0
    print avg1
elif(sys.argv[4] == '3'):
    # rafi
    print("hi rafi")




#outputs the data
with open(sys.argv[3], 'w+') as outputfile:
    for elem in unknownfiles:
        outputfile.write(" ".join(str(v) for v in elem))
        outputfile.write("\n")
