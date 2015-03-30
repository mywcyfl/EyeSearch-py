# -*- coding: utf-8 -*-

'''
# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015
#
# 配置文件
'''

# 调试环境开关（开启则将显示算法执行过程）
DEBUG = True

####################算法核心参数#####################
# 最大分辨率下网格（每一个边长上）被划分为的子网格数，
# 网格被划分为的总子格数等于该值的平方
CHILD_GRID_CNT_ONE_SIDE_MAX = 8
# 迭代层次数（每迭代一次，分辨率长和宽上各降低一倍）
ITERATE_CNT = 2
# 分层筛选比
SCREEN_RATIO = 0.5
# 标准网格边长（网格为正方形）
STANDARD_GRID_SIDE_LEN = 240
# 用于判断间距是否过大（导致前后两点其实已经属于两个线段）的分段标准因子
SEGMENT_JUDGE_FACTOR = 10
# 重采样点个数
RESAMPLE_POINT_CNT = 512
# 模板存放路径
TEMPLATE_PATH = 'template'
# 模板文件个数(通过读取文件得到)
TEMPLATE_CNT = 0

# 子网格特征值类型（本质上是草图在此子网格的区域分布（拓扑）类型）
#topology appearance
#   * *
#   _ _
FEATURE_LU_RU	= 0b0011
#topology appearance
#   _ _
#   * *
FEATURE_LD_RD	= 0b1100
#topology appearance
#   * _
#   * _
FEATURE_LU_LD	= 0b0101
#topology appearance
#   _ *
#   _ *
FEATURE_RU_RD	= 0b1010
#topology appearance
#   * _
#   _ *
FEATURE_LU_RD   = 0b1001
#topology appearance
#   _ *
#   * _
FEATURE_LD_RU   = 0b0110
#topology appearance
#   * _
#   _ _
FEATURE_LU      = 0b0001
#topology appearance
#   _ _
#   * _
FEATURE_LD      = 0b0100
#topology appearance
#   _ *
#   _ _
FEATURE_RU		= 0b0010
#topology appearance
#   _ _
#   _ *
FEATURE_RD      = 0b1000

####################界面参数#####################
# 线条绘制笔，全局性线条绘制接口
LINE_PEN = None
# 点绘制笔，全局性点绘制接口
POINT_PEN = None
# 矩形绘制笔，全局性矩形绘制接口
RECT_PEN = None

# 各种网格的间距(用于使得网格不会黏在一起)
GRID_SHOWED_INTERVAL = 5
# 绘制输入网格坐标（网格左上角顶点坐标）
INPUT_GRID_P = (10, 10)
# 规范化后输出网格1（用于debug模式下显示过程）
NORMALIZED_GRID1_P = (INPUT_GRID_P[0] + STANDARD_GRID_SIDE_LEN + GRID_SHOWED_INTERVAL,
		INPUT_GRID_P[1])
# 规范化后输出网格2（用于debug模式下显示过程）
NORMALIZED_GRID2_P = (NORMALIZED_GRID1_P[0] + STANDARD_GRID_SIDE_LEN + GRID_SHOWED_INTERVAL,
		NORMALIZED_GRID1_P[1])
# 规范化后输出网格3（用于debug模式下显示过程）
NORMALIZED_GRID3_P = (NORMALIZED_GRID2_P[0] + STANDARD_GRID_SIDE_LEN + GRID_SHOWED_INTERVAL,
		NORMALIZED_GRID2_P[1])
# 规范化后输出网格4（用于debug模式下显示过程）
NORMALIZED_GRID4_P = (NORMALIZED_GRID3_P[0] + STANDARD_GRID_SIDE_LEN + GRID_SHOWED_INTERVAL,
		NORMALIZED_GRID3_P[1])

# 特征向量输出网格1（用于debug模式下显示过程）
FEATURE_GRID1_P = (INPUT_GRID_P[0], INPUT_GRID_P[1] + STANDARD_GRID_SIDE_LEN + 100)

