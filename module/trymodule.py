try:
	import svgwrite
except ImportError:
	print("无法载入模块svgwrite，可使用pip install svgwrite安装")
try:
	import argparse
except ImportError:
	print("无法载入模块argparse，可使用pip install argparse安装")
try:
	import os
except ImportError:
	print("无法载入模块os，可使用pip install os安装")

os.system("dir")