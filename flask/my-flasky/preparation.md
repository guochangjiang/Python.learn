使用flask进行web开发推荐使用虚拟环境，其过程如下：

1. 安装virtualenv
	pip install virtualenv
2. 创建虚拟环境venv
	virtualenv venv
3. 激活venv
	source venv/bin/activate #linux
	venv\Scripts\activate #windows

> 此时，Python解释器的路径会被添加到PATH中，不过只是临时的，只会在当前环境中生效。如要回到全局环境，可运行命令：`venv\Scripts\deactivate`