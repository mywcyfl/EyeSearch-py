# -*- coding: utf-8 -*-
'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# 算法子构件：相似度计算模块
'''

import config

'''
# 相似度计算器
'''
class SimilarityCalculator:
	'''
	# 计算某层分辨率下两个特征向量间的相似度
	# layerFeature1		某草图1在某层下的特征向量
	# layerFeature2		某草图2在某层下的特征向量
	# featureLen	特征向量的长度（维度）
	'''
	@staticmethod
	def calculateSimiInOneResulotion(layerFeature1, layerFeature2, featureLen):
		score = 0
		
		i = 0
		while i < featureLen:
			score += SimilarityCalculator.__getCGFeatureSimilarity(
					layerFeature1[i], layerFeature2[i])
			i += 1

		return score

	'''
	# 计算两个子单元格上分布特征的相似度
	# cgFeature is short for childgridFeature
	'''
	@staticmethod
	def __getCGFeatureSimilarity(cgFeature1, cgFeature2):
		score		= 0

		bit1Similarity = -1 if (((0b0001&cgFeature1) ^ (0b0001&cgFeature2))>0) \
				else 0
		bit2Similarity = -1 if (((0b0010&cgFeature1) ^ (0b0010&cgFeature2))>0) \
				else 0
		bit3Similarity = -1 if (((0b0100&cgFeature1) ^ (0b0100&cgFeature2))>0) \
				else 0
		bit4Similarity = -1 if (((0b1000&cgFeature1) ^ (0b1000&cgFeature2))>0) \
				else 0

		score = bit1Similarity + bit2Similarity + bit3Similarity + bit4Similarity
		return score
