#!/usr/bin/env python
#coding=utf-8

import gtk
import cairo
import sys
import random
import gobject
import time

class BouncingDVD(gtk.Window):
	__gsignals__ = {
		'expose-event': 'override'
		}

	def __init__(self):
		super(BouncingDVD, self).__init__()

		if (len(sys.argv) > 2):
			speed = int(sys.argv[2])
		else:
			speed = 4

		self.imgs = ["resources/dvd-logo-1.png", "resources/dvd-logo-2.png", "resources/dvd-logo-3.png", "resources/dvd-logo-4.png", "resources/dvd-logo-5.png", "resources/dvd-logo-6.png"]
		self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]

		self.set_app_paintable(True)
		# no decorations
		self.set_decorated(False)
		
		self.set_colormap(self.get_screen().get_rgba_colormap())
		# random starting position and directions
		self.move(random.randint(0, gtk.gdk.screen_width() - 300), random.randint(0, gtk.gdk.screen_height() - 200))
		self.xspeed = [speed, -speed][random.randint(0, 1)]
		self.yspeed = [speed, -speed][random.randint(0, 1)]
		# keep the window below or above other windows if required
		if (len(sys.argv) > 1):
			if (sys.argv[1] == "below"):
				self.set_keep_below(True)
			elif (sys.argv[1] == "above"):
				self.set_keep_above(True)
		else:
			self.set_keep_below(True)

		self.connect("delete-event", gtk.main_quit)

	def do_expose_event(self, event):
		self.set_icon_from_file(self.img)
		self.imgsfc = cairo.ImageSurface.create_from_png(self.img)
		ctx = self.window.cairo_create()
		ctx.set_operator(cairo.OPERATOR_SOURCE)
		ctx.set_source_surface(self.imgsfc, 0, 0)
		ctx.paint()

	def update(self):

		x, y = self.get_position()
		w, h = self.get_size()
		newx, newy = x + self.xspeed, y + self.yspeed
		if (newx > self.ww - w):
			newx = self.ww - w
			self.xspeed *= -1
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
			self.queue_draw()
		if (newx < self.wx):
			newx = self.wx
			self.xspeed *= -1
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
			self.queue_draw()
		if (newy > self.wh - h):
			newy = self.wh - h
			self.yspeed *= -1
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
			self.queue_draw()
		if (newy < self.wy):
			newy = self.wy
			self.yspeed *= -1
			self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
			self.queue_draw()
		self.move(newx, newy)

		return True



def size_req(win, req):
	win.wx, win.wy, win.ww, win.wh = 1927 - win.get_allocation()[2], 1087 - win.get_allocation()[3], win.get_allocation()[2], win.get_allocation()[3]
	print(win.wx, win.wy, win.ww, win.wh)
	win.disconnect(win.cid)
	win.unmaximize()
	win.set_size_request(300, 200)
	# add the loop
	gobject.timeout_add(16, win.update)

if __name__ == "__main__":
	w = BouncingDVD()
	w.show()
	# a stupid way to do something
	w.cid = w.connect('size-request', size_req)
	w.maximize()
	gtk.main()
