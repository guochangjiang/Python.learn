## linux下非root用户python3的安装与配置

### 下载
首先，从Python官方网站https://www.python.org/downloads/release下载最新版本的python源代码包(如[python3.5.1.tgz](https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz))

### 安装
使用以下命令进行安装：

```bash
tar -zxvf Python-3.5.1.tgz
cd Python-3.5.1
./configure --prefix=/home/xxx/programs/Python3  #准备安装的路径，在自己的家目录下
make && make install
```

###将python3添加到环境变量
为了不影响linux系统自带python2的正常使用，可仅将python3添加自己的环境变量中，命令如下：

```bash
export "PATH=\$PATH:/home/xx/programs/Python3/bin" >> ~/.bashrc
或者
mkdir ~/bin #在家目录创建bin目录
ln -s /home/xx/programs/Python3/bin/python3.5 /home/xxx/bin/python3
export "PATH=\$PATH:/home/xxx/bin" >> ~/.bashrc
source ~/.bashrc
```

### 安装模块的两种方法

#### 方法一：pip(会安装到默认路径，一般需要root权限)
可以使用安装python3时附带安装的pip3进行命令行在线安装：

```bash
pip3 install module.name
```

#### 方法二：下载模块包本地安装(一般用户可以使用该方法)
手动从web上下载模块代码包，如argparse-1.4.0.tar.gz，然后使用以下命令进行安装：

```bash
tar -zxvf argparse-1.4.0.tar.gz
cd argparse-1.4.0
python3 setup.py install
```

### 注意
需要注意的是，在编写python3代码脚本时，需要在其头部添加如下内容以指示该脚本需要使用python3进行解释和运行。

```python
#!/usr/bin/env python3
#-*- coding: utf-8 -*-
```