#!/usr/bin/python

from __future__ import division
from graphics import *
import math

# Dimensions of graphics window
height  = 800
width   = 1200

colors      = [0]

# Radius of shape about the Y axis
radius      = 1000

# Viewing angle, in degrees to the horizontal
va          = 10

# Wavelength of sine wave in pixels
wavelength  = 170

# Height of the figure at the centre (see exponential decay, below)
centre_amplitude = 500

# Plot granularity.  Affects texture but not overall shape
xstep = 1
zstep = 10

# Viewing angle doesn't change, so calculate its sine and cosine now (optimization).
var     = math.radians(va)
sinvar  = math.sin(var)
cosvar  = math.cos(var)

win = GraphWin(sys.argv[0], width, height, autoflush=False)
win.setCoords(-width/2, -height/2, width/2, height/2)


# Image is symmetrical, so iterate x over half the  full range (-radius to radius)
# and plot both halves at the same time (optimisation).
for x in range(-radius, 0, xstep):

   # Pre-set maximums for hidden surface removal later
   maxy = -height
   miny = height

   # Optimisation: calculate and store this once instead of for every z later
   xsquared = x*x

   # The start (and end) of the z range for this x.
   zlimit = int(math.sqrt(radius*radius - xsquared))


   # This range is really just -zlimit to zlimit, step zstep.  The reverse 
   # and addition here is just so that the range is symmetrical about zero,
   # making the pixels line up properly even at high viewing angles.
   # A simply range(-zlimit, zlimit) produces the same shape but the
   # texture is not uniform.
   for z in list(reversed(range(0, -zlimit, -zstep))) + range(0, zlimit, zstep):

      # Distance of this point from the Y axis, horizontally
      r   = math.sqrt(xsquared + z*z)

     
      # Amplitude of wave
      # Reciprocal decay: more pointy
      amplitude = 5000*(1/(0.5*r+1))
      # Exponential decay: smoother
      #amplitude = centre_amplitude*(0.990**r)

      # y is a sinusoid of r, giving the wavy shape.
      #y  = amplitude*math.sin(math.radians(r*(360/wavelength)))
      y  = amplitude*math.sin(math.radians(r*(360/wavelength)))

      # "Rotate" the 3D image towards the viewer, about the x axis, to give
      # the viewing angle projection
      projy = z*sinvar + y*cosvar
    

      # Plot the points
      if (projy > maxy) or (projy < miny):
         pt  = Point(x, projy)
         pt.draw(win)
         pt  = Point(-x, projy)
         pt.draw(win)

      # Hidden surface removal
      if projy > maxy:
         maxy = projy

      if projy < miny:
         miny = projy

   # Tp speed up the drawing, remove the indent of the following line
   # To slow down, increase the indent, putting it into the z loop 
   win.update()

# Wait for user to click on image or terminate program
print "Done"
win.getMouse() 
win.close()
