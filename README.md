# EyeSearch (Python Version)
# author:wangxinwen, mail: mywcyfl@163.com
# all right reserved, 2013-2015.
#
# dependent on pygame, can get it from : http://www.pygame.org

README:
	EyeSearch是一个轻量级SBIR（Sketch-based Image Retireval Engine，草图检索引擎)，
	其核心基于“基于网格多级精确度递进式草图识别算法”，该算法识别物体的过程颇为类似
	于于人眼辨别物体的过程：先站在远处观察各物体模糊的形状进行初步排查，筛选掉一些
	外形差异极大的，然后站近一点做进一步观察与筛选，近一点距离可以观察到更多的细节，
	从而提高精度筛选掉一些上一步无法判别出的物体，如此递进直至剩下最后结果。

目录说明：
	./src/			为当前工程的源码目录，无需解释
	./src/algorithm 目录下为“基于网格多级精确度递进式识别算法”的实现，也即EyeSearch的算法部分，算法部分对外无依赖
	./src/template	为模板目录，其中存放了各类形状的模板

依赖说明：
	算法本身对外无依赖（也即./src/algorithm部分），但出于演示的目的我们借助了pygame来做交互，因此EyeSearch对pygame库有依赖，可由此处获得：http://www.pygame.org

操作说明：
	为了方便演示，我们借助pygame提供了简单的交互，你可借此体验EyeSearch并扩充模板库，以下是操作说明
	1.启动EyeSearch后（执行python app.py即可），将启动两个窗口，分别为Console控制台窗口和pygame窗口，所有信息将输出到Console窗口中，但所有的交互将在pygame窗口中进行。
	2.启动后pygame窗口的左上角有一个红色网格区域，此处为 “用户绘制区域”，在此处绘制后并按右键可以进行检索，检索结果信息将输出到pygame窗口中；绘制后按中键则表示将绘制图形添加为模板，模板文件将保存在./src/template/目录，但默认命名为unname*.template，你需要手动将其更正为你预期的模板名，模板存储后需要重启程序才生效。
	3.程序支持DEBUG模式，DEBUG模式下算法处理的过程会通过几个小网格给展示出来，这些展示有助于你理解算法的原理。DEBUG模式的开关在./src/config.py文件的最前面部分，默认为True。
	4.算法有部分参数需要配置，配置文件为./src/config.py，如果不清楚算法的原理及参数的意义和其对算法的影响，建议不要轻易改动它们（指这些参数）。

	具体按键说明如下：
	鼠标左键：用于绘制草图，但必须在“用户绘制区域”按下才起效。按下左键并移动即可绘制图形，EyeSearch支持多比划，因此你可以绘制完一条线后松开左键，然后移动到另一个位置，按下左键继续绘制。
	鼠标右键：识别，当草图绘制完成后按下鼠标右键即可识别。目前EyeSearch的强壮型做的不够好，因此部分特殊情况下识别会导致crash，如你绘制的线条极短，又如线条为直线（没有宽度或者高度）。
	鼠标中键：保存为模板，当草图绘制完成后可以按下鼠标中键将该图存储为模板，模板存储后需要程序下一次启动才生效。
	上方向键：查看上一个模板
	下方向键：查看下一个模板

补充：
	更多信息，请参见我的毕业论文《基于网格多级精确度递进式草图识别算法研究与设计》

联系方式：
	中山大学信息科学与技术学院计算机技术（专硕）15届毕业生，王新文，mywcyfl@163.com
