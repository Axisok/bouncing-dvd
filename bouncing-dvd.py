#!/usr/bin/env python
#coding=utf-8

import gtk
import cairo
import sys
import random
import gobject
import time
import webbrowser
import re

class BouncingDVD(gtk.Window):
	__gsignals__ = {
		'expose-event': 'override'
		}

	def __init__(self):
		super(BouncingDVD, self).__init__()
		
		self.delay = 0
		self.speed = 4
		self.handicap = 1

		# finds valid arguments and do stuff with them.
		for i in range(0, len(sys.argv)):
			a = sys.argv[i]
			if (re.search("speed=\\d+", a) != None):
				self.speed = int(re.search("\\d+", a).group())
			if (re.search("handicap=\\d+", a) != None):
				self.handicap = int(re.search("\\d+", a).group())
			if (re.search("fullscreen", a) != None):
				self.fullscreen()

		# pre-load images, change imgs array for other/more images.
		imgs = ["resources/dvd-logo-1.png", "resources/dvd-logo-2.png", "resources/dvd-logo-3.png", "resources/dvd-logo-4.png", "resources/dvd-logo-5.png", "resources/dvd-logo-6.png"]
		self.imgs = []
		for i in range(0, len(imgs)):
			self.imgs.append(cairo.ImageSurface.create_from_png(imgs[i]))
		self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]

		self.set_app_paintable(True)
		# no decorations
		self.set_decorated(False)
		
		self.set_colormap(self.get_screen().get_rgba_colormap())
		# random starting position and directions
		self.x, self.y = gtk.gdk.screen_width()/2 - self.img.get_width()/2, gtk.gdk.screen_height()/2 - self.img.get_height()/2
		self.xspeed = [self.speed, -self.speed][random.randint(0, 1)]
		self.yspeed = [self.speed, -self.speed][random.randint(0, 1)]
		# keep the window above all others
		self.set_keep_above(True)

		self.connect("delete-event", gtk.main_quit)

	def do_expose_event(self, event):
		# draw on the screen.
		ctx = self.window.cairo_create()
		ctx.set_operator(cairo.OPERATOR_SOURCE)
		ctx.set_source_surface(self.img, self.x, self.y)
		ctx.paint()

	def update(self):
		# loop of the program, will bounce the image around, slightly changing speed in a hard-to-notice way.

		if (self.delay > 0):
			self.delay -= 1
		
		w, h = self.get_size()
		newx, newy = self.x + self.xspeed, self.y + self.yspeed
		if (newx > w - self.img.get_width()):
			newx = w - self.img.get_width()
			self.xspeed = -self.speed * [1.1, 1, 0.9][random.randint(0, 2)]
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
		if (newx < 0):
			newx = 0
			self.xspeed = self.speed * [1.1, 1, 0.9][random.randint(0, 2)]
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
		if (newy > h - self.img.get_height()):
			newy = h - self.img.get_height()
			self.yspeed = -self.speed * [1.1, 1, 0.9][random.randint(0, 2)]
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
		if (newy < 0):
			newy = 0
			self.yspeed = self.speed * [1.1, 1, 0.9][random.randint(0, 2)]
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
			
		if (self.delay == 0 and ((newx <= self.handicap and newy <= self.handicap) or (newx >= w - 300 - self.handicap and newy <= self.handicap) or (newx >= w - 300 - self.handicap and newy >= h - 200 - self.handicap) or (newx <= self.handicap and newy >= h - 200 - self.handicap))):
			webbrowser.open("https://www.youtube.com/watch?v=DXQ9sCpRwkw")
			self.delay = 240
			
		self.x = newx
		self.y = newy
		
		self.queue_draw()

		return True



def set_mask(win):
    # copied code that makes the window click-through.
    size=win.window.get_size()
    bitmap=gtk.gdk.Pixmap(win.window,size[0],size[1],1)

    cr = bitmap.cairo_create()
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.set_source_rgba(0.0,0.0,0.0,0.0)
    cr.rectangle((0,0)+size)
    cr.fill()
    
    win.window.input_shape_combine_mask(bitmap,0,0)

if __name__ == "__main__":
	w = BouncingDVD()
	w.show()

	# fullscreen doesn't work well depending on the desktop, hiding status bar for example.
	w.maximize()
	gobject.timeout_add(16, w.update)
	set_mask(w)
	gtk.main()
