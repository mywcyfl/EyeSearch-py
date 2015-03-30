# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# 存放一些辅助性函数的文件
#
'''
import pygame
import os.path
import cPickle as pickle

'''
# Breseham 画线算法（利用该算法获得连续分布的点）
# p1	线段起点
# p2	线段终点
'''
def bresehamDrawLine(p1, p2):
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	ux = -1
	uy = -1

	if dx > 0:
		ux = 1
	if dy > 0:
		uy = 1
	
	x = p1[0]
	y = p1[1]
	eps = 0
	points = []

	dx = abs(dx)
	dy = abs(dy)
	if dx > dy:
		while x != p2[0]:
			points.append([x, y])
			eps += dy
			if 2*eps >= dx:
				y += uy
				eps -= dx

			x += ux
	else:
		while y != p2[1]:
			points.append([x, y])
			eps += dx
			if 2*eps >= dy:
				x += ux
				eps -= dy

			y += uy
	
	return points

'''
# 绘制网格函数（可选，在网格中绘制子单元格分割线）
# linePen			线条绘制接口
# p					网格左上角顶点坐标
# sideLen			网格边长（正方形）
# childNumEachSide	子网格数（可选，如果存在则将同步绘制这些子网格）
'''
def drawGrid(linePen, p, sideLen, childNumEachSide=0):
	# left-up point, 网格左上角顶点坐标
	luP	= p
	# right-up point, 网格右上角顶点坐标
	ruP	= (p[0] + sideLen, p[1])
	# left-down point，网格左下角顶点坐标
	ldP = (p[0], p[1] + sideLen)
	# right-down point,网格右下角顶点坐标
	rdP = (p[0] + sideLen, p[1] + sideLen)
	# 绘制网格边界的颜色(RGB)
	gridColor = (255, 0, 0)

	# 绘制网格
	linePen(gridColor, luP, ruP, 1)
	linePen(gridColor, luP, ldP, 1)
	linePen(gridColor, ruP, rdP, 1)
	linePen(gridColor, ldP, rdP, 1)

	# 绘制子单元格（可选）
	if 0 != childNumEachSide:
		# 子单元格间距
		childGridSideLen = sideLen / childNumEachSide
		# 子单元格边界颜色(RGB)
		childGridColor = (128, 0, 0)

		start = 0
		while start + childGridSideLen < sideLen:
			start += childGridSideLen
			lineS = (p[0] + start, p[1])
			lineE = (p[0] + start, p[1] + sideLen)
			linePen(childGridColor, lineS, lineE, 1)

		start = 0
		while start + childGridSideLen < sideLen:
			start += childGridSideLen
			lineS = (p[0], p[1] + start)
			lineE = (p[0] + sideLen, p[1] + start)
			linePen(childGridColor, lineS, lineE, 1)

	return

'''
# 绘制附带拓扑特征（已离散化的草图）的网格函数（可选，可同时将草图曲线绘制出）
# linePen			线条绘制接口
# p					网格左上角顶点坐标
# sideLen			网格边长（正方形）
# childNumEachSide	子网格数（可选，如果存在则将同步绘制这些子网格）
# topoData			拓扑数据（需符合特定格式）
# points			草图曲线点集合（可选）
'''
def drawTopoWithGrid(rectPen, linePen, pointPen, p, sideLen, childNumEachSide, 
		topoData, points=[]):
	childGridLU = (0, 0)
	childGridSideLen = sideLen / childNumEachSide
	# one child grid contains four topo element
	topoElemenSideLen = childGridSideLen / 2
	rectColor = (128, 0, 0)

	i = 0
	rectLUX = 0
	rectLUY = 0
	rectWid = 0
	rectHgt = 0
	while i < len(topoData):
		row = i / childNumEachSide
		col = i % childNumEachSide
		childGridLU = (p[0] + col*childGridSideLen, p[1] + row*childGridSideLen)

		bit1Val = 1 if ((0b0001 & topoData[i]) > 0) else 0
		bit2Val = 1 if ((0b0010 & topoData[i]) > 0) else 0
		bit3Val = 1 if ((0b0100 & topoData[i]) > 0) else 0
		bit4Val = 1 if ((0b1000 & topoData[i]) > 0) else 0

		if 1 == bit1Val:
			rectLUX = childGridLU[0]
			rectLUY = childGridLU[1]
			rectWid = topoElemenSideLen
			rectHgt = topoElemenSideLen

			rectPen(rectColor, (rectLUX, rectLUY, rectWid, rectHgt), 0)

		if 1 == bit2Val:
			rectLUX = childGridLU[0] + topoElemenSideLen
			rectLUY = childGridLU[1]
			rectWid = topoElemenSideLen
			rectHgt = topoElemenSideLen

			rectPen(rectColor, (rectLUX, rectLUY, rectWid, rectHgt), 0)
		
		if 1 == bit3Val:
			rectLUX = childGridLU[0]
			rectLUY = childGridLU[1] + topoElemenSideLen
			rectWid = topoElemenSideLen
			rectHgt = topoElemenSideLen

			rectPen(rectColor, (rectLUX, rectLUY, rectWid, rectHgt), 0)
		
		if 1 == bit4Val:
			rectLUX = childGridLU[0] + topoElemenSideLen
			rectLUY = childGridLU[1] + topoElemenSideLen
			rectWid = topoElemenSideLen
			rectHgt = topoElemenSideLen

			rectPen(rectColor, (rectLUX, rectLUY, rectWid, rectHgt), 0)

		i += 1

	drawSketchWithGrid(linePen, pointPen, p, sideLen, childNumEachSide, points)

	return

'''
# 绘制附带草图曲线的网格函数
# linePen			线条绘制接口
# pointPen			点绘制接口
# p					网格左上角顶点坐标
# sideLen			网格边长（正方形）
# childNumEachSide	子网格数
# points			草图曲线点集合
'''
def drawSketchWithGrid(linePen, pointPen, p, sideLen, childNumEachSide, points):
	# 绘制格子
	drawGrid(linePen, p, sideLen, childNumEachSide)

	# 绘制草图曲线
	sketchColor = (255, 255, 255)
	for point in points:
		pointPen(sketchColor, (int(point[0] + p[0]), int(point[1] + p[1])), 0)

	return

