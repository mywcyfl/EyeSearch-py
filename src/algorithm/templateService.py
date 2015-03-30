# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# 算法子构件：模板服务提供模块
'''

import os
import config
import cPickle as pickle
from functions import *
from featureExtractor import FeatureExtractor
from similarityCalculator import SimilarityCalculator

'''
# 模板类（单个模板）
'''
class Sketch:
	def __init__(self, name, sketchPoints, feature=None):
		self.name = name
		self.sketchPoints = sketchPoints
		self.feature = feature or FeatureExtractor.extract(self.sketchPoints)

	def getFeature(self):
		return self.feature

	def getSketch(self):
		return self.sketchPoints

	def getName(self):
		return self.name

'''
# 模板服务提供者
'''
class TemplateService:
	def __init__(self):
		self.database = []
		self.curSaveIndex = 1

	'''
	# load templates
	'''
	def readDatabase(self, path):
		if os.path.isdir(path):
			arr = os.listdir(path)
			# 获取模板个数
			config.TEMPLATE_CNT = len(arr)
			print "info: %d templates found, loading..." % config.TEMPLATE_CNT

			i = 0
			while i < config.TEMPLATE_CNT:
				name = arr[i].split('.')[0]
				f = file(path + r'\%s'%arr[i], 'rb')
				# load feature
				feature = [0] * config.ITERATE_CNT
				j = 0
				while j < config.ITERATE_CNT:
					feature[j] = pickle.load(f)
					j += 1
				# load points
				sketchPoints = pickle.load(f)
				template = Sketch(name, sketchPoints, feature)
				self.database.append(template)

				# print "  template %s loaded" % name
				i += 1

			print"info: %d templates loaded" % i
		else:
			print "warning: template dir '%s' not found" % path

	'''
	# search in templates and get the most similar one with weight
	# 加权法求解相似度最高的模板
	# sketch	待检索草图
	'''
	def getMostSimilarByWeight(self, sketch):
		if True == config.DEBUG:
			self.__showSketch(sketch)

		result = []

		j = 0
		while j < len(self.database):
			score = 0
			childGridCnt = config.CHILD_GRID_CNT_ONE_SIDE_MAX**2
			i = config.ITERATE_CNT - 1
			while i >= 0:
				s = SimilarityCalculator.calculateSimiInOneResulotion(
						sketch.feature[i], 
						self.database[j].feature[i],
						childGridCnt)
				s *= config.CHILD_GRID_CNT_ONE_SIDE_MAX**2/childGridCnt
				score += s
				# 降低一级分辨率，长和宽方向上子格数各降一半，总子格数为原来的1/4
				childGridCnt /= 4
				i -= 1

			result.append([self.database[j].name, score])
			j += 1

		result.sort(key = lambda l:(l[1]), reverse = True)
		return result

	'''
	# search in templates and get the most similar one pymid
	# 快速筛选法求解相似度最高的模板
	# sketch	待检索草图
	# ratio		分层筛选比
	'''
	def getMostSimilarPymid(self, sketch, ratio):
		if True == config.DEBUG:
			self.__showSketch(sketch)

		result = []
		for j in range(config.TEMPLATE_CNT):
			result.append([j, 'unknown', 0])

		print "len=%d"%len(result)
		
		i = 0
		while i < config.ITERATE_CNT:
			if i != config.ITERATE_CNT - 1:
				childGridCnt = (config.CHILD_GRID_CNT_ONE_SIDE_MAX**2)/(4**(config.ITERATE_CNT-1-i))
			else:
				childGridCnt = config.CHILD_GRID_CNT_ONE_SIDE_MAX**2


			resultTemp = []
			j = 0
			while j < len(result):
				feature1 = sketch.feature
				feature2 = self.database[result[j][0]].feature
				score = SimilarityCalculator.calculateSimiInOneResulotion(
						feature1[i],
						feature2[i],
						childGridCnt)
				
				score *= (config.CHILD_GRID_CNT_ONE_SIDE_MAX**2) / childGridCnt
				score += result[j][2]
				resultTemp.append([result[j][0], 
					self.database[result[j][0]].name, 
					score])

				j += 1

			resultTemp.sort(key=lambda l:(l[2]), reverse=True)
			restCnt = int(len(resultTemp)*ratio)
			result = resultTemp[:restCnt]

			if restCnt < 2:
				# left one template only, return it
				return result

			i += 1

		return result

	'''
	# save sketch as a template
	'''
	def saveTemplate(self, path, sketch):
		if not os.path.isdir(path):
			os.mkdir(path)

		templateName = r'\unname%d.template' % self.curSaveIndex
		self.curSaveIndex += 1
		f = file(path + templateName, 'wb')

		# save feature
		i = 0
		while i < config.ITERATE_CNT:
			pickle.dump(sketch.feature[i], f)
			i += 1
		# save points
		pickle.dump(sketch.getSketch(), f)

		f.close()
		print "info: saved as " + templateName

	'''
	#
	'''
	def showTemplateByIdx(self, idx):
		self.__showSketch(self.database[idx-1])

	'''
	#
	'''
	def __showSketch(self, sketch):
		i = 0
		gridLU = None
		while i < config.ITERATE_CNT: 
			gridLU = (config.FEATURE_GRID1_P[0] + i*(config.STANDARD_GRID_SIDE_LEN
				+ config.GRID_SHOWED_INTERVAL), config.FEATURE_GRID1_P[1])
			if i < config.ITERATE_CNT - 1:
				curChildGridCntOneSide = config.CHILD_GRID_CNT_ONE_SIDE_MAX/(
						(config.ITERATE_CNT - 1 - i)*2)
			else:
				curChildGridCntOneSide = config.CHILD_GRID_CNT_ONE_SIDE_MAX
				
			drawTopoWithGrid(config.RECT_PEN, config.LINE_PEN, config.POINT_PEN, 
					gridLU, config.STANDARD_GRID_SIDE_LEN, 
					curChildGridCntOneSide, sketch.feature[i], sketch.sketchPoints)
				
			i += 1
