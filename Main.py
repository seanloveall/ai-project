from __future__ import division
import sys
import math

from PIL import Image
from PIL import ImageFilter

#    shortcut for lazy rafi
sys.argv = ["placeholder",
            "C:/Users/rpcoo/Documents/GitHub/ai-project/input.txt",
            "C:/Users/rpcoo/Documents/GitHub/ai-project/input2.txt",
            "C:/Users/rpcoo/Documents/GitHub/ai-project/test/output.txt", "3" ]

print "  =====Image Recognition Software=====  \n"

def iround(num):
    #returns an int that has been rounded
    return int(round(num))

def ifloor(num):
    #returns an int that has been floored
    return int(math.floor(num))

def grayscale_image(img):
    #returns an image that is grayscale
    width, height = img.size
    
    for x in range(width):
        for y in range(height):
            red, green, blue = img.getpixel((x, y))

            #formula to convert color to grayscale
            col = iround(0.3 * red + 0.59 * green + 0.11 * blue)
            
            img.putpixel((x, y), (col, col, col))
            
    return img

def resize_and_crop(img, size):
    #returns an image that has been resized and cropped to specified size
    width, height = img.size
    img_ratio = float(width) / height
    nwidth, nheight = size
    ratio = float(nwidth) / nheight
    
    
    #Scales either vertically or horizontally and then crops the image
    if ratio > img_ratio:
        #scales vertically
        img = img.resize((nwidth, ifloor(nheight * img_ratio)), Image.ANTIALIAS)

        #crops in the middle
        box = (0, ifloor((img.size[1] - nheight) / 2), nwidth, ifloor((img.size[1] + nheight) / 2))
        img = img.crop(box)
    elif ratio < img_ratio:
        #scales horizontally
        img = img.resize((ifloor(size[0] * img_ratio), size[1]), Image.ANTIALIAS)

        #crops in the middle
        box = (ifloor((img.size[0] - nwidth) / 2), 0, ifloor((img.size[0] + nwidth) / 2), nheight)
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


#begin pattern recognition algorithms

if(sys.argv[4] == '1'):
    #### sean
    i = 0
    size = 50 #images will be reduced to size x size
    moe = 20 #margin of error
    avg0 = []
    avg1 = []
    avg0.append([[0 for x in range(size)] for x in range(size)])
    avg1.append([[0 for x in range(size)] for x in range(size)])
    images0 = [0] #keeps track of the total number of photos per average
    images1 = [0] #same as above
    print "Begin learning..."

    #Learning from the first dataset
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
                    flag += 1                                   #then add to another average as well or create a new average
                    for a in range(len(avg0)):
                        if a == 0: #skipping total average
                            continue
                        elif(abs((avg0[a][x][y] / (i+1)) - red) <= moe): #if within margin of error, then add to score
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
                elif(score[a] >= compare): #if score is higher than the compare, then we'll use this one
                    good = 1
                    images0[a] += 1
                    for x in range(width):
                        for y in range(height):
                            red, green, blue = image.getpixel((x, y))
                            avg0[a][x][y] += red
                    break
            if(good == 0): #if a score wasn't high enough to beat the comparison above, then create a new average
                avg0.append([[0 for x in range(size)] for x in range(size)])
                images0.append(1)
                a = len(avg0) - 1
                for x in range(width):
                    for y in range(height):
                        red, green, blue = image.getpixel((x, y))
                        avg0[a][x][y] += red
        i = i + 1

    print "Finished learning from first dataset..."

    #Learning from the second dataset
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
                    flag += 1                                    #then add to another average as well or create a new average
                    for a in range(len(avg1)):
                        if a == 0: #skipping total average
                            continue
                        elif(abs((avg1[a][x][y] / (i+1)) - red) <= moe): #if within margin of error, then add to score
                            if(a < len(score)):
                                score[a] += 1
                            else:
                                 while a < len(score):
                                     score.append(0)
                                 score.append(1)

                
        compare = round(size * size / 4)
        good = 0
        
        if(flag >= compare):
            for a in range(len(score)):
                if a == 0:  #skipping total average
                    continue
                elif(score[a] >= compare): #if score is higher than the compare, then we'll use this one
                    good = 1
                    images1[a] += 1
                    for x in range(width):
                        for y in range(height):
                            red, green, blue = image.getpixel((x, y))
                            avg1[a][x][y] += red
                    break
            if(good == 0): #if a score wasn't high enough to beat the comparison above, then create a new average
                avg1.append([[0 for x in range(size)] for x in range(size)])
                images1.append(1)
                a = len(avg1) - 1
                for x in range(width):
                    for y in range(height):
                        red, green, blue = image.getpixel((x, y))
                        avg1[a][x][y] += red
        i = i + 1

    print "Finished learning from second dataset..."

    print "Checking unknown photos..."

    #computing the average for each total sum
    for x in range(len(avg0[0])):
        for y in range(len(avg0[0])):
            for z in range(len(avg0)):
                avg0[z][x][y] = avg0[z][x][y] / images0[z]

    #computing the average for each total sum
    for x in range(len(avg1[0])):
        for y in range(len(avg1[0])):
            for z in range(len(avg1)):
                avg1[z][x][y] = avg1[z][x][y] / images1[z]


    #comparing the unknown files against the datasets to see what type the unknown file is
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
        maxscore0 = 0
        maxscore1 = 0
        for x in range(width):
            for y in range(height):
                red, green, blue = image.getpixel((x, y))

                #check first dataset
                num = abs(avg0[0][x][y] - red)
                if(num <= moe): #if within margin of error, give it a bonus point
                    score0 += 1
                    maxscore0 += 1
                num = float(num) / 255
                score0 = score0 + (1 - num)
                maxscore0 += 1

                for a in range(len(avg0)): #compare against other averages
                    if a == 0: #skip total average since it was already done above
                        continue
                    elif images0[a] == 1: #if only one image is in this average, then lower the margin of error
                        num = abs(avg0[a][x][y] - red)
                        if(num <= (float(moe)/2)):
                            num = float(num) / 255
                            score0 = score0 + ((1 - num) * 2) #weighted if within the more restricted margin of error
                            maxscore0 += 2
                    else:
                        num = abs(avg0[a][x][y] - red)
                        if(num <= moe): #if within margin of error, then add to score (weighted)
                            num = float(num) / 255
                            score0 = score0 + ((1 - num) * images0[a])
                            maxscore0 += images0[a]


                #check second dataset
                num = abs(avg1[0][x][y] - red)
                if(num <= moe):
                    score1 += 1
                    maxscore1 += 1
                num = float(num) / 255
                score1 = score1 + (1 - num)
                maxscore1 += 1

                for a in range(len(avg1)): #compare against other averages
                    if a == 0:
                        continue
                    elif images1[a] == 1: #if only one image is in this average, then lower the margin of error
                        num = abs(avg1[a][x][y] - red)
                        if(num <= (float(moe)/2)):
                            num = float(num) / 255
                            score1 = score1 + ((1 - num) * 2) #weighted if within the more restricted margin of error
                            maxscore1 += 2
                    else:
                        num = abs(avg1[a][x][y] - red)
                        if(num <= moe): #if within margin of error, then add to score (weighted)
                            num = float(num) / 255
                            score1 = score1 + ((1 - num) * images1[a])
                            maxscore1 += images1[a]

        #compare the scores to see which dataset the unknown photo most likely belongs to
        if(score0 > score1):
            num = score0 / maxscore0
            num = abs(1 - num)
        else:
            num = score1 / maxscore1
            if(num <= 0.5):
                num = num + 0.5

        unknownfiles[i][1] = round(num, 2)


        i = i + 1

    print "Finished comparing..."

    ####
elif(sys.argv[4] == '2'):
    # scoot
    i = 0
    avg0 = [[0 for x in range(50)] for x in range(50)] 
    avg1 = [[0 for x in range(50)] for x in range(50)]
    count0 = 2500/len(list0)
    count1 = 2500/len(list1)
    x = 0
    y = 0

    print "Beginning to learn from first dataset..."
    while i < len(list0):
        image = Image.open(list0[i])
        image = image.convert('RGB')
        image = grayscale_image(image)
        image = image.filter(ImageFilter.BLUR)
        image = resize_and_crop(image, (50, 50))
        
        width, height = image.size
        for j in range(int(count0)):
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

    print "Done with dataset 1. Beginning to learn from dataset 2..."
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
        for j in range(int(count1)):
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

    print "Done learning. Beginning to compare with unknown images..."
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
        #print score0
        #print score1
        num = round(float(score)/float(pix), 2)
        if(num < 0.5):
            #num = float(score0) / float(pix)
            #num = abs(num - 0.5)
            unknownfiles[i][1] = str(num)
        else:
            #num = float(score1) / float(pix)
            #if(num <= 0.5):
              #num = num + 0.5
            unknownfiles[i][1] = str(num)

        #
        #print unknownfiles[i][0], " ", (float(score)/float(2500))
        #print score, " ", score2
        i = i + 1

    print "Finished comparisons..."
    #print avg0
    #print avg1   
elif(sys.argv[4] == '3'):
    # rafi

    import numpy as np
    from sklearn import datasets, svm

    print "Learning from images...\n"    
    i = 0
    n_images = len(list0) + len(list1) #sum of images to learn from
    kdataset = np.zeros((n_images,50,50), dtype=np.float32) #known dataset
    while i < n_images: 
    #iterate through all images, convert to RGB, grayscale, resize and crop
    #and convert it into a Numpy array that will be added to the known dataset
    #array.
        if(i< len(list0)):
            image = Image.open(list0[i])
        else:
            image = Image.open(list1[i-(len(list0))]) #iterate through list1 when 
        image = image.convert('RGB')                  #list0 finishes
        image = grayscale_image(image)
        image = resize_and_crop(image, (50, 50))
        data = np.asarray(image, dtype=np.float32 )
        data /= 255.0 #normalize the vaules 
        data = data.mean(axis=2)
        ###print data[0]
        kdataset[i, ...] = data #add the image representation to the known dataset
        i = i + 1
    print "     Done.\n"
    print "Preparing unknown images for recognition.\n"

    j = 0
    n_uimages = len(unknownfiles) #number of unknown images
    ukdataset = np.zeros((n_uimages,50,50), dtype=np.float32) #unknown dataset
    while j < n_uimages:
    #perform the same proces as above, iterating through the unknownfiles array
    #and adding the image representations to the uknown dataset
        image = Image.open(unknownfiles[j][0])
        image = image.convert('RGB')
        image = grayscale_image(image)
        image = resize_and_crop(image, (50, 50))
        udata = np.asarray(image, dtype=np.float32 )
        udata /= 255.0
        udata = udata.mean(axis=2) 
        ###print data[0]
        ukdataset[j, ...] = udata
        j = j + 1
    print "     Done.\n"

    #reshaping the arrays is necessary to match the input requirements for
    #the fit function of the classifier
    kre = kdataset.reshape((n_images, -1)) #known dataset reshaping
    ukre = ukdataset.reshape((n_uimages,-1)) #unknown dataset reshaping

    #create two arrays to represent the features of the images. The algorithm
    #uses this array to learn to distinguish between the two types of images
    a = np.zeros((len(list0),), dtype=np.int)
    b = np.ones((len(list1),), dtype=np.int)
    targets = np.concatenate((a,b),axis=0)
    ###print targets

    #initiate the classifier, with the Simple Machine Vector algorithm
    classifier = svm.SVC(gamma=0.001)
    #fit the known dataset and their target designation to the classifier
    #this is where the program learns
    classifier.fit(kre,targets)

    #classifier uses the learned knowledge on the unknown dataset,
    #returning an array of the predicted values for each image in the
    #dataset
    print "Predicting...\n"
    predicted = classifier.predict(ukre)
    print "     Done.\n"
    ###print "Here are the results: \n"
    ###print predicted

    #assign the predicted values to the "to-be" output file
    for line in range(len(unknownfiles)):
         unknownfiles[line][1] = predicted[line]

#outputs the data
with open(sys.argv[3], 'w+') as outputfile:
    for elem in unknownfiles:
        outputfile.write(" ".join(str(v) for v in elem))
        outputfile.write("\n")
print "Results have been written into the output file."
