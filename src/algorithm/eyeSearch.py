# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# Entry of the Algorithm
'''

import config
import time
from normalizer	import Normalizer
from similarityCalculator import SimilarityCalculator
from templateService import Sketch, TemplateService

class EyeSearch:
	def __init__(self):
		self.database = TemplateService()
		self.database.readDatabase(config.TEMPLATE_PATH)

	'''
	# do retrieval
	# sketchPoints	sketch(just drawed by user) to be retrieval
	'''
	def retrieval(self, sketchPoints):
		t1 = time.time()
		sketch = self.__pointsToSketch(sketchPoints)

		result = self.database.getMostSimilarByWeight(sketch)
		# result = self.database.getMostSimilarByWeight(sketch, config.SCREEN_RATIO)

		t2 = time.time()

		print "time cost : " + str(t2-t1)

		return result[:5]

	'''
	# save sketch as template
	# need change it's name manully after saved to harddisk
	# sketchPoints	sketch(just drawed by user) to be save, 
	'''
	def saveAsTemplate(self, sketchPoints):
		sketch = self.__pointsToSketch(sketchPoints)
		self.database.saveTemplate(config.TEMPLATE_PATH, sketch)

	'''
	# draw template on the screen
	'''
	def showTemplate(self, idx):
		self.database.showTemplateByIdx(idx)

	'''
	# map sketchPoints to sketch
	'''
	def __pointsToSketch(self, sketchPoints):
		# step1, normalized
		sketchPoints = Normalizer.normalize(sketchPoints)
		# step2, to sketch
		sketch = Sketch('ToBeRetrieval', sketchPoints)
		
		return sketch
