# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015.
#
# dependent on pygame, can get it from : http://www.pygame.org
'''

import pygame
import sys
import config
from algorithm.eyeSearch import EyeSearch
from pygame.locals import *
from functions import *

def main():
	# init search engine
	eyeEngine = EyeSearch()
	# init pygame
	pygame.init()
	screen = pygame.display.set_mode((1366, 768), pygame.DOUBLEBUF)
	# pygame.display.flip()
	screen.fill((0,0,0))

	# got a virtual line pen, which can draw line directly
	config.LINE_PEN = virtualLinePen(screen)
	# got a virtual point pen, which can draw point directly
	config.POINT_PEN = virtualPointPen(screen)
	# got a virtual point pen, which can draw rect directly
	config.RECT_PEN = virtualRectPen(screen)

	# loop flag
	running = True
	# drawing flag, when left button been press down
	drawing = False
	# segment flag, True when the last segment over and now it's a new segment
	newSegment = False
	# is the last draw sketch searched already
	lastSketchProcessed = False
	# current showing template index
	curShowingTemplateIndex = 0
	# sketch point set
	sketch = []

	# event loop
	while running:
		pygame.time.wait(5)
		pygame.display.update()

		# draw the input grid
		drawGrid(config.LINE_PEN, config.INPUT_GRID_P, config.STANDARD_GRID_SIDE_LEN, 
				10)

		events = pygame.event.get()
		for e in events:
			if QUIT == e.type:
				# close event
				pygame.quit()
				running = False
				break
			elif MOUSEBUTTONDOWN == e.type:
				# some mouse button pressed
				pressedArr = pygame.mouse.get_pressed()
				for index in range(len(pressedArr)):
					if not pressedArr[index]:
						continue
					if 0 == index:
						# left button press down
						# user begin to drawing a sketch
						drawing = True
						newSegment = True
					elif 1 == index:
						# mid button press down
						# save sketch as template
						if len(sketch) > 10:
							eyeEngine.saveAsTemplate(sketch)
							lastSketchProcessed = True
					elif 2 == index:
						# right button press down
						# draw over, now search this sketch by engine
						if len(sketch) > 10 and False == lastSketchProcessed:
							result = eyeEngine.retrieval(sketch)
							print result
							print "\n"
							lastSketchProcessed = True
						else:
							# sketch illegal(point cnt is not enough) or a new try
							screen.fill((0, 0, 0))
							sketch = []
							lastSketchProcessed = False
						pass
			elif MOUSEBUTTONUP == e.type:
				if 1 == e.button:
					# left button released
					drawing = False
			elif MOUSEMOTION == e.type:
				# mouse moving action
				if drawing:
					# user is drawing, we will recording the path
					pos = pygame.mouse.get_pos()
					if pos[0] >= config.INPUT_GRID_P[0] and \
						pos[1] >= config.INPUT_GRID_P[1] and \
						pos[0] <= config.INPUT_GRID_P[0] + config.STANDARD_GRID_SIDE_LEN and \
						pos[1] <= config.INPUT_GRID_P[1] + config.STANDARD_GRID_SIDE_LEN:
						# position is legal
						point = (pos[0] - config.INPUT_GRID_P[0], pos[1] - config.INPUT_GRID_P[1])
						if True == newSegment:
							sketch.append(point)
							newSegment = False

							config.POINT_PEN((255, 255, 255), pos, 0)
						else:
							# make the line more uniformity
							line = bresehamDrawLine(sketch.pop(), list(point))
							sketch += line
							
							for p in sketch:
								config.POINT_PEN((255, 255, 255), (p[0] + config.INPUT_GRID_P[0], p[1] + config.INPUT_GRID_P[1]), 0)
			elif KEYDOWN == e.type:
				if K_DOWN == e.key:
					# 下方向键被按下
					screen.fill((0, 0, 0))
					curShowingTemplateIndex += 1
					if curShowingTemplateIndex > config.TEMPLATE_CNT:
						curShowingTemplateIndex = 1
					if config.TEMPLATE_CNT > 0:
						# draw the template specified by index
						eyeEngine.showTemplate(curShowingTemplateIndex)
				elif K_UP == e.key:
					# 上方向键被按下
					screen.fill((0, 0, 0))
					curShowingTemplateIndex -= 1
					if curShowingTemplateIndex < 1:
						curShowingTemplateIndex = config.TEMPLATE_CNT
					if config.TEMPLATE_CNT > 0:
						# draw the template specified by index
						eyeEngine.showTemplate(curShowingTemplateIndex)
	return


'''
* 返回一个闭包，调用该闭包并传入数据，该闭包将依据此数据绘制线条
'''
def virtualLinePen(screen):
	def drawLine(color, lineS, lineE, circle):
		pygame.draw.line(screen, color, lineS, lineE, circle)
	
	return drawLine

'''
* 返回一个闭包，调用该闭包并传入数据，该闭包将依据此数据绘制点
'''
def virtualPointPen(screen):
	def drawPoint(color, point, circle):
		pygame.draw.circle(screen, color, point, circle)
	
	return drawPoint

'''
* 返回一个闭包，调用该闭包并传入数据，该闭包将依据此数据绘制矩形
'''
def virtualRectPen(screen):
	def drawRect(color, rectInfo, circle):
		pygame.draw.rect(screen, color, rectInfo, circle)
	
	return drawRect

if __name__ == "__main__":
	main()
