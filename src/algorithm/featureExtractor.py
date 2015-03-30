# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# 算法子构件：特征向量提取模块
'''

import math
import config
from functions import drawTopoWithGrid

'''
# 特征提取器
'''
class FeatureExtractor:
	'''
	# 执行特征提取
	'''
	@staticmethod
	def extract(sketch):
		feature = [None] * config.ITERATE_CNT

		# curCGCntOneSide is short for currentChildGridCntOneSide
		curCGCntOneSide	= config.CHILD_GRID_CNT_ONE_SIDE_MAX
		# curCGSideLen is short for currentChildGridSideLen
		curCGSideLen	= config.STANDARD_GRID_SIDE_LEN / curCGCntOneSide
		# extract the feature in max resolution
		feature[config.ITERATE_CNT - 1] = FeatureExtractor.__extractByPath(sketch, 
				curCGSideLen, curCGCntOneSide)

		# extract feature of other resolution iteratively
		i = config.ITERATE_CNT - 2
		while i >= 0:
			curCGCntOneSide = curCGCntOneSide / 2
			curCGSideLen = config.STANDARD_GRID_SIDE_LEN / curCGCntOneSide
			feature[i] = FeatureExtractor.__extractByPath(sketch, 
					curCGSideLen, curCGCntOneSide)

			i -= 1

		return feature

	'''
	#沿着曲线不断提取特征值
	# sketch				待提取草图
	# childGridSideLen		子单元格边长（正方形）
	# childGridCntOneSide	网格每边有多少个子单元格
	'''
	@staticmethod
	def __extractByPath(sketch, childGridSideLen, childGridCntOneSide):
		layerFeature = [0] * childGridCntOneSide**2

		thisGrid	= [-1, -1]
		lastGrid	= [-1, -1]
		# curCGTag is short currentChildGridTag
		curCGTag	= [False] * 4
		xInChildGrid, yInChildGrid = 0, 0

		i = 0
		while i < len(sketch):
			thisGrid[0] = int(sketch[i][0] / childGridSideLen)
			if thisGrid[0] >= childGridCntOneSide:
				# edge process
				thisGrid[0] -= 1

			thisGrid[1] = int(sketch[i][1] / childGridSideLen)
			if thisGrid[1] >= childGridCntOneSide:
				# edge process
				thisGrid[1] -= 1

			if thisGrid[0] != lastGrid[0] or thisGrid[1] != lastGrid[1]:
				if -1 != lastGrid[0] and -1 != lastGrid[1]:
					# now enter a new child grid
					xInChildGrid = sketch[i-1][0] - lastGrid[0] * childGridSideLen
					yInChildGrid = sketch[i-1][1] - lastGrid[1] * childGridSideLen

					# now calculate the topo feature of sketch in last child grid
					FeatureExtractor.__recordTopoInfo(xInChildGrid, yInChildGrid, 
							childGridSideLen, curCGTag)
					layerFeature[lastGrid[1] * childGridCntOneSide + lastGrid[0]] \
							|= FeatureExtractor.__getCGFeature(curCGTag)
				else:
					# just enter the first child grid when begining, nothing need to do
					pass

				curCGTag = [False] * 4
				lastGrid = thisGrid[:]

				# record the topo info of this new grid which just be entered in
				xInChildGrid = sketch[i][0] - thisGrid[0] * childGridSideLen
				yInChildGrid = sketch[i][1] - thisGrid[1] * childGridSideLen
				FeatureExtractor.__recordTopoInfo(xInChildGrid, yInChildGrid, \
						childGridSideLen, curCGTag)

			# still in the last grid
			i += 1

		# the last grid should not be forget
		xInChildGrid = sketch[i-1][0] - lastGrid[0] * childGridSideLen
		yInChildGrid = sketch[i-1][1] - lastGrid[1] * childGridSideLen
		FeatureExtractor.__recordTopoInfo(xInChildGrid, yInChildGrid, childGridSideLen, curCGTag)
		layerFeature[lastGrid[1] * childGridCntOneSide + lastGrid[0]] \
				|= FeatureExtractor.__getCGFeature(curCGTag)

		return layerFeature

	'''
	# 记录点在子单元格中的区域特性
	# 区域标记(每子单元格分为4个区域)
	# *******
	# * 0 1 *
	# * 2 3 *
	# *******
	# xInGrid		点在子单元格中的x坐标（相对）
	# yInGrid		点在子单元格中的y坐标（相对）
	# gridSideLen	子单元格边长
	# cgTag			标记记录区（记录在此内存中，而不是通过return回传结果）
	'''
	@staticmethod
	def __recordTopoInfo(xInGrid, yInGrid, gridSideLen, cgTag):
		areaLen = gridSideLen / 2

		if xInGrid < areaLen and yInGrid < areaLen:
			cgTag[0] = True
		elif xInGrid >= areaLen and yInGrid < areaLen:
			cgTag[1] = True
		elif xInGrid < areaLen and yInGrid >= areaLen:
			cgTag[2] = True
		else:
			cgTag[3] = True

		return

	'''
	# 根据记录好的区域特性得到草图在此子单元格中的拓扑特征（草图的特征向量由多个子单元格的拓扑特征组成）
	# cgTag	记录好的草图在某子单元格的区域分布特性
	'''
	@staticmethod
	def __getCGFeature(cgTag):
		# cgFeature is short for childgridFeature
		cgFeature = 0

		if True == cgTag[0] and True == cgTag[1]:
			# topo appearance
			# * *
			# _ _
			cgFeature = config.FEATURE_LU_RU
		elif True == cgTag[2] and True == cgTag[3]:
			# topo appearance
			# _ _
			# * *
			cgFeature = config.FEATURE_LD_RD
		elif True == cgTag[0] and True == cgTag[2]:
			# topo appearance
			# * _
			# * _
			cgFeature = config.FEATURE_LU_LD
		elif True == cgTag[1] and True == cgTag[3]:
			# topo appearance
			# _ *
			# _ *
			cgFeature = config.FEATURE_RU_RD
		elif True == cgTag[0] and True == cgTag[3]:
			# topo appearance
			# * _
			# _ *
			cgFeature = config.FEATURE_LU_RD
		elif True == cgTag[1] and True == cgTag[2]:
			# topo appearance
			# _ *
			# * _
			cgFeature = config.FEATURE_LD_RU
		elif True == cgTag[0]:
			# topo appearance
			# * _
			# _ _
			cgFeature = config.FEATURE_LU
		elif True == cgTag[1]:
			# topo appearance
			# _ *
			# _ _
			cgFeature = config.FEATURE_RU
		elif True == cgTag[2]:
			# topo appearance
			# _ _
			# * _
			cgFeature = config.FEATURE_LD
		elif True == cgTag[3]:
			# topo appearance
			# _ _
			# _ *
			cgFeature = config.FEATURE_RD

		return cgFeature
