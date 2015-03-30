# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# 算法子构件：规范器模块
'''

import config
from functions import *
from math import sin, cos, atan2, sqrt, pi

def average(xs): 
	return sum(xs) / len(xs)
def pointDis(p1, p2):
	return float(sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))

'''
# 规范器，用于对草图进行规范化处理，使得其符合算法规定的系列规范
'''
class Normalizer:
	'''
	# 执行规范化
	# sketch	待规范草图
	'''
	@staticmethod
	def normalize(sketch):
		# 为了不改动原来的数据
		sketch = sketch[:]

		# step1: resample normalize
		sketch = Normalizer.__resampleNormalize(sketch, config.RESAMPLE_POINT_CNT)
		if True == config.DEBUG:
			drawSketchWithGrid(config.LINE_PEN, 
					config.POINT_PEN, 
					config.NORMALIZED_GRID1_P, 
					config.STANDARD_GRID_SIDE_LEN, 0, sketch)

		# step2: rotate normalize
		sketch = Normalizer.__rotateNormalize(sketch)
		if True == config.DEBUG:
			drawSketchWithGrid(config.LINE_PEN, 
					config.POINT_PEN, 
					config.NORMALIZED_GRID2_P, 
					config.STANDARD_GRID_SIDE_LEN, 0, sketch)


		# step3: scale normalize
		sketch = Normalizer.__scaleNormalize(sketch, config.STANDARD_GRID_SIDE_LEN)
		if True == config.DEBUG:
			drawSketchWithGrid(config.LINE_PEN, 
					config.POINT_PEN, 
					config.NORMALIZED_GRID3_P, 
					config.STANDARD_GRID_SIDE_LEN, 0, sketch)


		# step4: translate normalize
		sketch = Normalizer.__translateNormalize(sketch)
		if True == config.DEBUG:
			drawSketchWithGrid(config.LINE_PEN, 
					config.POINT_PEN, 
					config.NORMALIZED_GRID4_P, 
					config.STANDARD_GRID_SIDE_LEN, 0, sketch)


		return sketch

	'''
	# 重采样规范化
	# sketch		待规范化草图
	# resampleCnt	重采样点数（即以多少个采样点去重采样此草图）
	'''
	@staticmethod
	def __resampleNormalize(sketch, resampleCnt):
		# 重采样后的草图，第一个点也应该从之前的第一个点开始
		newSketch = [sketch[0]]
		# 重采样后两点间应该具有的间距
		interval = Normalizer.__pathLength(sketch) / float(resampleCnt - 1)
		# 线段分割长度，当两点间距超过此时，认为这两点属于两条线段（而不是一条）
		segmentJugeLen = max(Normalizer.__boundingBoxWidthAndHgt(sketch)) / config.SEGMENT_JUDGE_FACTOR

		dist = 0
		i = 1
		while i < len(sketch):
			p = sketch[i]
			d = pointDis(sketch[i-1], p)
			if d >= segmentJugeLen:
				# a new segment
				dist = 0
			elif (dist + d) >= interval:
				qx = sketch[i-1][0] + ((interval-dist)/d) * (p[0] - sketch[i-1][0])
				qy = sketch[i-1][1] + ((interval-dist)/d) * (p[1] - sketch[i-1][1])

				newSketch.append([qx, qy])
				sketch.insert(i, [qx, qy])
				dist = 0
			else:
				dist = dist + d
			
			i += 1

		return newSketch

	'''
	# 旋转规范化，使得草图具有符合算法要求的角度
	# sketch	待规范化草图
	'''
	@staticmethod
	def __rotateNormalize(sketch):
		cx, cy = Normalizer.__centroid(sketch)
		furthestDist	= 0
		furthestPoint	= [cx, cy]

		# got the furthest point
		for p in sketch:
			dist = pointDis([cx, cy], p)
			if dist > furthestDist:
				furthestPoint = p

		# rotate
		theta = atan2(cy - furthestPoint[1], cx - furthestPoint[0])
		newSketch = Normalizer.__rotateBy(sketch, -theta)

		return newSketch

	'''
	# 缩放规范化，使得草图具有符合算法要求的尺寸
	# sketch	待规范化草图
	'''
	@staticmethod
	def __scaleNormalize(sketch, standardSideLen):
		newSketch = []
		minX, minY, wid, hgt = Normalizer.__boundingBox(sketch)
		scaleW = float(standardSideLen) / wid
		scaleH = float(standardSideLen) / hgt

		for p in sketch:
			qx = p[0] * scaleW
			qy = p[1] * scaleH
			newSketch.append([qx, qy])

		return newSketch

	'''
	# 平移规范化，使得草图处于符合算法要求的区域（即坐标值的规范化）
	'''
	@staticmethod
	def __translateNormalize(sketch):
		minX, minY, width, hgt = Normalizer.__boundingBox(sketch)
		
		for p in sketch:
			p[0] -= minX
			p[1] -= minY

		return sketch

	'''
	# 求一个草图其轮廓曲线的总长度
	'''
	@staticmethod
	def __pathLength(sketch):
		pathLen = 0
		# 线段分割长度，当两点间距超过此时，认为这两点属于两条线段（而不是一条）
		segmentJugeLen = max(Normalizer.__boundingBoxWidthAndHgt(sketch)) / config.SEGMENT_JUDGE_FACTOR
		
		for i, p in enumerate(sketch[:len(sketch)-1]):
			dist = pointDis(p, sketch[i+1])
			if dist <= segmentJugeLen:
				pathLen += dist

		return pathLen

	'''
	# 求一个轮廓的几何中心
	'''
	@staticmethod
	def __centroid(sketch):
		return float(average([float(i[0]) for i in sketch])), float(average([float(i[1]) for i in sketch]))

	'''
	# 将草图整体按一定角度旋转
	'''
	@staticmethod
	def __rotateBy(sketch, theta):
		newSketch = []
		cx, cy = Normalizer.__centroid(sketch)
		cosV, sinV = cos(theta), sin(theta)

		for p in sketch:
			qx = (p[0] - cx) * cosV - (p[1] - cy) * sinV + cx
			qy = (p[0] - cx) * sinV + (p[1] - cy) * cosV + cy
			newSketch.append([qx, qy])

		return newSketch

	'''
	# 求得草图的最小外包围框
	'''
	@staticmethod
	def __boundingBox(sketch):
		minX, maxX = min((p[0] for p in sketch)), max((p[0] for p in sketch))
		minY, maxY = min((p[1] for p in sketch)), max((p[1] for p in sketch))

		return minX, minY, maxX-minX, maxY-minY

	'''
	# 求得草图的最小外包围框的宽和高
	'''
	@staticmethod
	def __boundingBoxWidthAndHgt(sketch):
		minX, minY, width, hgt = Normalizer.__boundingBox(sketch)
		return width, hgt
