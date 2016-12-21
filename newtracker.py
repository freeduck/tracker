print __doc__

import SimpleCV
import Queue
from threading import Thread, Lock

display = SimpleCV.Display()
cam = SimpleCV.Camera(1)

img1 = SimpleCV.Image("background.jpg")
layer = img1.dl()
size = img1.size()
balllayer = SimpleCV.DrawingLayer(size)
img1.addDrawingLayer(balllayer)


def main():
    track(findBorders())

def findBorders():
    continue_looking = True
    rectangles = True
    while continue_looking and display.isNotDone():
        if display.mouseLeft:
                print "Right"
                layer.clear()
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

    print rectangles
    return rectangles



def track(rectangles):
    l = []
    for idx,rect in enumerate(rectangles):
                layer.rectangle((rect.x, 0), (5, img1.height),SimpleCV.Color.BLUE )
                l.insert(idx,rect)

    leftb = l[0].x
    rightb = l[1].x
    prevcircle = None
    count = 0
    circle = Noneb
    balllayer.setFontSize(24)

    while True:
            balllayer.clear()
            img =  cam.getImage().flipHorizontal()
            dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
            segmented = dist.stretch(200,255)
            blobs = segmented.findBlobs()

            if blobs:
                    circles = blobs.filter([b.isCircle(0.6) for b in blobs])
                    if circles:
                        circle=circles[-1]
                        if prevcircle and circle.x < leftb and prevcircle.x >= leftb:
                            count = count+1


                        prevcircle=circle
            balllayer.text(str(count),(10,10),color=SimpleCV.Color.GREEN)

            balllayer.circle((circle.x, circle.y), 20,SimpleCV.Color.RED,3)
            img1.applyLayers()
            img1.show()


main()
