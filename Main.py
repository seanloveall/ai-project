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
    size = 50
    moe = 40 #margin of error
    avg0 = []
    avg1 = []
    avg0.append([[0 for x in range(size)] for x in range(size)])
    avg1.append([[0 for x in range(size)] for x in range(size)])
    images0 = [0]
    images1 = [0]
    while i < len(list0):
        score = [0]
        flag = 0
        images0[0] += 1
        image = Image.open(list0[i])
        image = image.convert('RGB')
        image = resize_and_crop(image, (size, size))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        
        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                avg0[0][x][y] += red
                
                if(abs((avg0[0][x][y] / (i+1)) - red) > moe): #if the difference is greater than margin of error,
                    flag += 1                        #then add to another average as well or create a new average
                    for a in range(len(avg0)):
                        if a == 0: #this is the total average
                            continue
                        elif(abs((avg0[a][x][y] / (i+1)) - red) <= moe):
                            if(a < len(score)):
                                score[a] += 1
                            else:
                                 while a < len(score):
                                     score.append(0)
                                 score.append(1)

                
        compare = round(size * size / 4)
        good = 0
        #print score
        if(flag >= compare):
            for a in range(len(score)):
                if a == 0:  #skipping total average
                    continue
                elif(score[a] >= compare):
                    good = 1
                    images0[a] += 1
                    for x in range(width):
                        for y in range(height):
                            red, green, blue = image.getpixel((x, y))
                            avg0[a][x][y] += red
                    break
            if(good == 0):
                avg0.append([[0 for x in range(size)] for x in range(size)])
                images0.append(1)
                a = len(avg0) - 1
                for x in range(width):
                    for y in range(height):
                        red, green, blue = image.getpixel((x, y))
                        avg0[a][x][y] += red
        i = i + 1

    print "Done with list 0"
    print len(avg0)
    print len(images0)
    print images0

    
    i = 0
    while i < len(list1):
        score = [0]
        flag = 0
        images1[0] += 1
        image = Image.open(list1[i])
        image = image.convert('RGB')
        image = resize_and_crop(image, (size, size))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        
        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                avg1[0][x][y] += red
                
                if(abs((avg1[0][x][y] / (i+1)) - red) > moe): #if the difference is greater than margin of error,
                    flag += 1                        #then add to another average as well or create a new average
                    for a in range(len(avg1)):
                        if a == 0: #this is the total average
                            continue
                        elif(abs((avg1[a][x][y] / (i+1)) - red) <= moe):
                            if(a < len(score)):
                                score[a] += 1
                            else:
                                 while a < len(score):
                                     score.append(0)
                                 score.append(1)

                
        compare = round(size * size / 4)
        good = 0
        #print score
        if(flag >= compare):
            for a in range(len(score)):
                if a == 0:  #skipping total average
                    continue
                elif(score[a] >= compare):
                    good = 1
                    images1[a] += 1
                    for x in range(width):
                        for y in range(height):
                            red, green, blue = image.getpixel((x, y))
                            avg1[a][x][y] += red
                    break
            if(good == 0):
                avg1.append([[0 for x in range(size)] for x in range(size)])
                images1.append(1)
                a = len(avg1) - 1
                for x in range(width):
                    for y in range(height):
                        red, green, blue = image.getpixel((x, y))
                        avg1[a][x][y] += red
        i = i + 1

    print "Done with list 1"
    print len(avg1)
    print len(images1)
    print images1

    for x in range(len(avg0[0])):
        for y in range(len(avg0[0])):
            for z in range(len(avg0)):
                avg0[z][x][y] = avg0[z][x][y] / images0[z]
            #avg0[0][x][y] = avg0[0][x][y] / len(list0)

    for x in range(len(avg1[0])):
        for y in range(len(avg1[0])):
            for z in range(len(avg1)):
                avg1[z][x][y] = avg1[z][x][y] / images1[z]
            #avg1[0][x][y] = avg1[0][x][y] / len(list1)


    i = 0
    while i < len(unknownfiles):
        image = Image.open(unknownfiles[i][0])
        image = image.convert('RGB')
        image = resize_and_crop(image, (size, size))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)

        score0 = 0
        score1 = 0

        width, height = image.size
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))
                num = abs(avg0[0][x][y] - red)
                if(num <= moe): 
                    score0 += 1
                num = float(num) / 255
                score0 = score0 + (1 - num)

                for a in range(len(avg0)):
                    if a == 0:
                        continue
                    elif images0[a] == 1:
                        continue
                    num = abs(avg0[a][x][y] - red)
                    if(num <= moe):
                        num = float(num) / 255
                        score0 = score0 + ((1 - num) * images0[a])

                num = abs(avg1[0][x][y] - red)
                if(num <= moe):
                    score1 += 1
                num = float(num) / 255
                score1 = score1 + (1 - num)

                for a in range(len(avg1)):
                    if a == 0:
                        continue
                    elif images1[a] == 1:
                        continue
                    num = abs(avg1[a][x][y] - red)
                    if(num <= moe):
                        num = float(num) / 255
                        score1 = score1 + ((1 - num) * images1[a])

        pix = size * size
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

    if(x != 49 or y != 50):
        while(x != 49 or y != 50):
            image = Image.open(list0[i-1])
            image = image.convert('RGB')
            image = grayscale_image(image)
            image = image.filter(ImageFilter.BLUR)
            image = resize_and_crop(image, (50, 50))
        
            width, height = image.size
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
            avg1[x][y] = image.getpixel((x, y))
            if(x == 49 and y == 49):
                break
            elif(y == 49):
                x += 1
                y = 0
            else:
                y += 1

        i = i + 1

    if(x != 49 or y != 50):
        while(x != 49 or y != 50):
            image = Image.open(list1[i-1])
            image = image.convert('RGB')
            image = grayscale_image(image)
            image = image.filter(ImageFilter.BLUR)
            image = resize_and_crop(image, (50, 50))
        
            width, height = image.size
            avg1[x][y] = image.getpixel((x, y))
            if(x == 49 and y == 49):
                break
            elif(y == 49):
                x += 1
                y = 0
            else:
                y += 1

    #print avg0
    #print avg1
    #print x
    #print y

    #Learing complete. Beginning to compare with unknown images
    i = 0
    while i < len(unknownfiles):
        image = Image.open(unknownfiles[i][0])
        image = image.convert('RGB')
        image = resize_and_crop(image, (50, 50))
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)

        score = 0
        score0 = 0
        score1 = 0
        width, height = image.size
        for x in range(width):
            for y in range(height):
                temp0 = 0
                temp1 = 0
                red, green, blue = image.getpixel((x, y))
                temp0 = abs(avg0[x][y][0] - red)
                temp0 = temp0 + abs(avg0[x][y][1] - green)
                temp0 = temp0 + abs(avg0[x][y][2] - blue)

                temp1 = abs(avg1[x][y][0] - red)
                temp1 = temp1 + abs(avg1[x][y][1] - green)
                temp1 = temp1 + abs(avg1[x][y][2] - blue)

                if(temp0 < temp1):
                    score0 = score0 + 1
                elif(temp1 < temp0):
                    #score1 = score1 + 1
                    score = score + 1


        pix = 50 * 50
        print score0
        print score1
        num = float(score)/float(pix)
        if(num < 0.5):
            #num = float(score0) / float(pix)
            #num = abs(num - 0.5)
            unknownfiles[i][1] = "0-"+str(num)
        else:
            #num = float(score1) / float(pix)
            #if(num <= 0.5):
              #num = num + 0.5
            unknownfiles[i][1] = "1-"+str(num)

        #
        #print unknownfiles[i][0], " ", (float(score)/float(2500))
        #print score, " ", score2
        i = i + 1
    
    #print avg0
    #print avg1   
elif(sys.argv[4] == '3'):
    # rafi
    print("hi rafi")




#outputs the data
with open(sys.argv[3], 'w+') as outputfile:
    for elem in unknownfiles:
        outputfile.write(" ".join(str(v) for v in elem))
        outputfile.write("\n")
