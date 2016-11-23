print __doc__

import SimpleCV
import Queue
import threading

#display = SimpleCV.Display()
cam = SimpleCV.Camera(1)

#hsl hsv
class Producer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        print 'init producer'

    def run(self):
        print 'run producer'
        lastx=0
        lasty=0
        while True:
            #display.isNotDone():
            img = cam.getImage().flipHorizontal()
            dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
            segmented = dist.stretch(200,255)
            blobs = segmented.findBlobs()

            if blobs:
                    circles = blobs.filter([b.isCircle(0.6) for b in blobs])
                    if circles:
                        circle=circles[-1]
                        #img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLUE,3)
                        lastx=circle.x
                        lasty=circle.y
                        #self.queue.put({'x': circle.x, 'y':circle.y, 'radius': circle.radius, 'image': img})

            self.queue.put({'x': lastx, 'y':lasty})


            #img.show()


class Consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        print 'init Consumer'

    def run(self):
        print 'run Consumer'

        while True:
            #display.isNotDone():
            img = cam.getImage().flipHorizontal()
            obj=self.queue.get()
            try:
                img.drawCircle((obj['x'], obj['y']), 20,SimpleCV.Color.RED,3)
            finally:
                pass
            try:
                img.show()
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
