西窗烛 [![Build Status](https://travis-ci.org/hustlzp/xichuangzhu.svg?branch=master)](https://travis-ci.org/hustlzp/xichuangzhu)
===

http://www.xichuangzhu.com

何当共剪西窗烛，却话巴山夜雨时。——〔唐〕李商隐《夜雨寄北》

Lovely build with Flask & Bootstrap3.

移动版：

* [iOS App](https://itunes.apple.com/cn/app/xi-chuang-zhu/id912139104) ([source code](https://github.com/hustlzp/xichuangzhu-ios))

## 本地环境搭建

```
git clone https://github.com/hustlzp/xichuangzhu.git
cd xichuangzhu
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
bower install
```

Create database `xcz` and import `db/xcz.sql` into it.

Copy `config/development_sample.py` as `config/development.py` and update configs.

```
python manage.py run
```
