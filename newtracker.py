print __doc__

import SimpleCV
import Queue
from threading import Thread, Lock

display = SimpleCV.Display()
cam = SimpleCV.Camera(1)

img1 = SimpleCV.Image("background.jpg")
layer = img1.dl()

def main():
    findBorders()
    track()

def findBorders():
    continue_looking = True
    while continue_looking and display.isNotDone():
        if display.mouseLeft:
                print "Right"
                break
        layer.clear()
        img = cam.getImage().flipHorizontal()
        #layer = img.dl()
        dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
        segmented = dist.stretch(200,255)
        blobs = segmented.findBlobs()
        if blobs:
            rectangles = blobs.filter([b.isRectangle() for b in blobs])
            for rect in rectangles:
                layer.rectangle((rect.x, rect.y), (rect.width(), rect.height()),SimpleCV.Color.RED )

        img1.applyLayers()
        img1.show()


main()
