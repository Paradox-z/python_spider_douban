# Python网络爬虫软件系统

## 环境准备
Python编译器，PyCharm社区版，pip.ini镜像文件，chrome和chromedriver，selenium工具，Python第三方库

## 项目复现

### 1. 确定chrome版本，安装对应版本的chromedriver

### 2. Pycharm新建Python项目，进行虚拟环境搭建

### 3. 查看当前项目目录下的文件get_movie_data.py，定位107，executable_path=./chromedriver.exe当前路径，需修改为chromedriver的存储路径成为绝对路径

### 4. 最好先更换pip源，再使用命令pip install -r Pillow和pip install -r selenium 

#### 4.1 切换pip源的位置C:\Users\用户名\pip\pip.ini，默认情况下pip文件夹和pip.ini文件都未被创建，自行修改

### 5. 如果出现无法启动驱动的情况，大概率是发生了chrome自动升级的情况，解决办法是卸载后重装对应的版本，或者锁定升级服务项
