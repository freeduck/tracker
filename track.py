'''
This is how to track a white ball example using SimpleCV

The parameters may need to be adjusted to match the RGB color
of your object.

The demo video can be found at:
http://www.youtube.com/watch?v=jihxqg3kr-g
'''
print __doc__

import SimpleCV
import Queue
import threading

display = SimpleCV.Display()
cam = SimpleCV.Camera()

#hsl hsv
class Producer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        print 'init producer'

    def run(self):
        print 'run producer'
        while display.isNotDone():
            if display.mouseRight:
                    normaldisplay = not(normaldisplay)
                    print "Display Mode:", "Normal" if normaldisplay else "Segmented"

            img = cam.getImage().flipHorizontal()
            dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
            segmented = dist.stretch(200,255)
            blobs = segmented.findBlobs()
            if blobs:
                    circles = blobs.filter([b.isCircle(0.2) for b in blobs])
                    if circles:
                        circle=circles[-1]
                        #img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLUE,3)
                        self.queue.put({'x': circle.x, 'y':circle.y, 'radius': circle.radius(), 'image': img})


            #img.show()


class Consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        print 'init Consumer'

    def run(self):
        print 'run Consumer'
        while display.isNotDone():
            obj=self.queue.get()
            try:
                obj['image'].drawCircle((obj['x'], obj['y']), obj['radius'],SimpleCV.Color.RED,3)
            finally:
                pass
            try:
                obj['image'].show()
            finally:
                pass

def main():
    print 'Calling main'
    queue = Queue.Queue(100)
    #drawQueue
    producer = Producer(queue)
    producer.setDaemon(True)
    producer.start()
    consumer = Consumer(queue)
    consumer.setDaemon(True)
    consumer.start()
    producer.join()
    consumer.join()

main()
