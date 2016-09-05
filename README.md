# UCIproject

## Get Started

1. create a virtualenv for the python project
```bash
# "<XXXX>" 表示, 在此处插入XXXX描述的内容

# virtualenv 是一个虚拟环境, 它其实就是一个文件夹.
# 在你喜欢的地方创建一个存放你系统中所有virtualenv的文件夹, 如果已经有可以跳过

# 创建 你所有virtualenv环境的folder
# 这个文件夹的名字可以自己改动
mkdir </your/virtualenvs/folder>

# cd 到那个文件夹
cd </your/virtualenvs/folder>

# 在那个文件夹下, 创建一个叫"UCIproject"的virtualenv
virtualenv UCIproject

# 安装结束后, virtualenv "UCIproject"会自动被activate
```

2. pip install the requirements file. 
```bash
# activate "UCIproject"这个virtualenv, 如果你已经activate, 就不用跑下面的
# command
source </your/virtualenvs/folder>/UCIproject/bin/activate/
# 在这个virtualenv里面, 安装所有依赖包
pip install -r requirements.txt
```
3. start server
```bash
# 你需要一个.settings.conf 文件在本地run application
# 这个.settings.conf 文件应该位于 UCIproject/.settings.conf

# 本地运行server
cd UCIproject
SETTINGS_CONFIG=.settings.conf python application.py 

# 上面这个command的意思是: 让python 跑 application.py, 但是同时给python一个
# environment variable, 叫SETTINGS_CONFIG, 这个variable的值是你config file
# 的path
```
4. go to `localhost:5000`
