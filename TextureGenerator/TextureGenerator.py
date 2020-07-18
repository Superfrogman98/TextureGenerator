import numpy as np
import cv2 as cv
import copy as copy
import os
cwd = os.getcwd();
fileName = input("Input File: ");
#fileName = "ingots.txt";
nameSuffix = "image.png";
baseFile = 'test.png';
overlayFile = 'testOverlay.png';
outputLoc = cwd+'images\\';
nameSuffix = ".png"
nameTransformLoc = cwd+'\\images\\nameTransform'+nameSuffix.replace(".png",".csv");
colorMode = "Intensity";
inputLines = [];
colorStart = 5;
try:  
    inputFile = open(fileName, "r");
    inputLines = inputFile.readlines();
    baseFile = inputLines[0].replace('\n','');
    overlayFile = inputLines[1].replace('\n','');
    nameSuffix = inputLines[2].replace('\n','');
    outputLoc = inputLines[3].replace('\n','');
    colorMode = inputLines[4].replace('\n','');
    if(colorMode != "Intensity"):
        nameTransformLoc = inputLines[4].replace('\n','');
    inputFile.close();
except IOError:
    print("File not accessible");  

baseImage = cv.imread(baseFile,cv.IMREAD_UNCHANGED);
overlayImage = cv.imread(overlayFile,cv.IMREAD_UNCHANGED);
#convert the overlay image to grayscale, then back to BGRA format
overlayImageGrayscale =cv.cvtColor(cv.cvtColor(overlayImage,cv.COLOR_BGRA2GRAY),cv.COLOR_GRAY2BGRA);
#get the alpha channels and combine them
overlayAlpha = cv.extractChannel(overlayImage,3);
baseAlpha =cv.extractChannel(baseImage,3);
combinedAlphas = cv.bitwise_or(baseAlpha,overlayAlpha);

#copy the grayscale overlay to get the dimensions right
coloredOverlay = overlayImageGrayscale.copy();
cv.insertChannel(overlayAlpha,overlayImageGrayscale,3);
sizes = coloredOverlay.shape;
#cv.imwrite(outputLoc+"gray_over"+nameSuffix,overlayImageGrayscale);
#cv.imwrite(outputLoc+"base"+nameSuffix+".png",baseImage);
intensityMap = [];
for i in range(0,sizes[0]):
    intensityMap.insert(-1,[]);

for rows in range(0,sizes[0]):
    for cols in range(0,sizes[1]):
        pixel = overlayImageGrayscale[rows,cols];
        intensity = round(pixel[0]/255,2);
        intensityMap[rows].insert(len(intensityMap[rows]),intensity);
        #make any pixels with 0 alpha white so they don't mess with blending
        if(pixel[3] == 0):
            overlayImageGrayscale[rows,cols] = [255,255,255,0];     


for i in range(len(intensityMap)):
    for x in range(len(intensityMap[i])):
        if(overlayImageGrayscale[i,x][3]!=0):
            print ("{0:.2f}".format(intensityMap[i][x]) + " ", end =""); 
        else:
            print("     ", end ="");
    print ();
print("Intensity Mode");
nameOut = open(nameTransformLoc,"w");
nameOut.write("OriginalName,TransformedName\n");
for i in range (colorStart,len(inputLines)):
    line = inputLines[i].split('|');
    code = eval(line[1]);
    name = line[0].encode('ascii',errors='replace').decode().replace("?","-")
    print("Name: " + name + " Base Color: " + str(code));
    code = (code[2],code[1],code[0]);#convert to BGR
    for rows in range(0,sizes[0]):
        for cols in range(0,sizes[1]):
            pixel = overlayImageGrayscale[rows,cols];
            intensity = intensityMap[rows][cols];
            if(pixel[3] != 0):
                coloredOverlay[rows,cols] = [int(code[0]*intensity),int(code[1]*intensity),int(code[2]*intensity),pixel[3]];
            else:
                coloredOverlay[rows,cols] = [255,255,255,0];
    combinedImage= cv.bitwise_and(baseImage,coloredOverlay);
    cv.insertChannel(combinedAlphas,combinedImage,3);
    cv.imwrite(outputLoc+name+nameSuffix,combinedImage);
    #cv.imwrite(outputLoc+line[0]+"_overlay.png",coloredOverlay);
    nameOut.write(line[0]+","+name+"\n");
#cv.imwrite(outputLoc+nameSuffix,cv.insertChannel(combinedAlphas,baseImage,3));
print("Image Files output to: " + outputLoc);
print("Name Change File output to: " + nameTransformLoc);
nameOut.close();
#combinedImage= cv.bitwise_and(baseImage,overlayImage);
#cv.insertChannel(combinedAlphas,combinedImage,3);
#cv.imwrite(outputLoc+"Combined_Test.png",combinedImage);



#combinedImageGrayscale = cv.bitwise_and(baseImage,overlayImageGrayscale);
#cv.insertChannel(combinedAlphas,combinedImageGrayscale ,3);
#cv.imwrite(outputLoc+"Combined_Test_Gray.png",combinedImageGrayscale);

#cv.imshow('image',combinedImage);
cv.waitKey(0);
cv.destroyAllWindows();