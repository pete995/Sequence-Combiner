import sys
import cv2
from os import listdir
from os.path import isfile, join
import numpy as np

def main():

    if (len(sys.argv) > 1):

        #get command line arguments
        useBlur = "useBlur" in sys.argv
        useDilate = "useDilate" in sys.argv
        tresHold = 50

        customWidth = 0
        customHeight = 0
        
        outputName = "out.jpg"
        for arg in sys.argv:
            if arg.startswith("o="):
                outputName = arg.replace("o=", "")
            elif arg.lower().startswith("treshold="):
                tresHold = int(arg.lower().replace("treshold=", ""))
            elif arg.lower().startswith("width="):
                customWidth = int(arg.lower().replace("width=", ""))
            elif arg.lower().startswith("height="):
                customHeight = int(arg.lower().replace("height=", ""))

        resize = customHeight != 0 and customWidth != 0

        folder = sys.argv[1]
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]

        path = folder + str("/" + str(onlyfiles[0]))
        diff = cv2.imread(path)

        if resize:
            diff = cv2.resize(diff, (customWidth, customHeight))

        imageHeight, imageWidth, numChannels = diff.shape

        images = [diff]

        #add images in folder to images array
        for file in onlyfiles[1:]:
            path = folder + str("/" + str(file))
            img = cv2.imread(path)
            if resize:
                img = cv2.resize(img, (customWidth, customHeight))
            images.append(img)

        #calculate and create median image
        median = np.zeros((imageHeight,imageWidth,3), np.uint8)
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                pixels = []
                for image in images:
                    channels_xy = image[y,x]
                    pixels.append(channels_xy)
                pixels = sorted(pixels, key=lambda tup: (-tup[1],tup[0],tup[2]))
                half = int(len(images) / 2)
                median[y,x] = pixels[half]

        grayMedian = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
        if useBlur:
            grayMedian = cv2.GaussianBlur(grayMedian, (21, 21), 0)

        result = np.zeros((imageHeight,imageWidth,3), np.uint8)
        for image in images:
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if (useBlur):
                grayImage = cv2.GaussianBlur(grayImage, (21, 21), 0)

            #detect difference between current image and median image
            diff = cv2.absdiff(grayImage, grayMedian)

            diff = cv2.threshold(diff, tresHold, 255, cv2.THRESH_BINARY)[1]
            if useDilate:
                diff = cv2.dilate(diff, None, iterations=20)

            for x in range(0,imageWidth):
                for y in range(0,imageHeight):
                    channels_xy = diff[y,x]
                    if channels_xy > 0:
                        result[y,x] = image[y,x]

        #replace black pixel in result with pixels from median image
        for x in range(0,imageWidth):
            for y in range(0,imageHeight):
                channels_xy = result[y,x]
                if (channels_xy)[0] == 0:
                    result[y,x] = median[y,x]

        cv2.imwrite(outputName, result)
    else:
        print("No folder passed into arguments")

if __name__ == "__main__":
    main()