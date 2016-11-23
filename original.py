'''
This is how to track a white ball example using SimpleCV

The parameters may need to be adjusted to match the RGB color
of your object.

The demo video can be found at:
http://www.youtube.com/watch?v=jihxqg3kr-g
'''
print __doc__

import SimpleCV

display = SimpleCV.Display()
cam = SimpleCV.Camera(prop_set = {"width": 640, "height": 480})
normaldisplay = True

pain_img = SimpleCV.Image("background.jpg") #cam.getImage().flipHorizontal()
while display.isNotDone():

    if display.mouseRight:
	normaldisplay = not(normaldisplay)
	print "Display Mode:", "Normal" if normaldisplay else "Segmented"

    img = cam.getImage().flipHorizontal()
    dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
    segmented = dist.stretch(200,255)
    blobs = segmented.findBlobs()
    if blobs:
	circles = blobs.filter([b.isCircle(0.6) for b in blobs])
	if circles:
            pain_img = SimpleCV.Image("background.jpg") #cam.getImage().flipHorizontal()
	    pain_img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.RED,3)

	if normaldisplay:
		pain_img.show()
	else:
		segmented.show()
