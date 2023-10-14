# python_spider_douban
##Project background: Python spider technology can be used to automatically collect data. This project is based on tools and third-party libraries to achieve keyword search, ranking selection, and other functions for Douban movie data.
##Project content: Design a program framework and implement the following functions:
**-1-**Initialize the UI framework and load the interface elements.
**-2-**Construct requests based on keywords and parse the returned data.
**-3-**Construct requests based on filtering conditions and parse the ranking interface data.
**-4-**Implement local storage for the parsed image and text data.
##Project highlights:
**-1-**The project applies multi-threading technology to enable asynchronous execution of multiple keyword queries.
**-2-**The UI interface can be extended with frames to support parallel processing of keyword search and ranking selection.
**-3-**A multimodal interface is implemented, displaying text and images, and clicking a button can view movie details and resource URLs.


##环境准备：Python编译器，PyCharm社区版，pip.ini镜像文件，chrome和chromedriver，selenium工具，Python第三方库

##项目复现：

###1. 确定chrome版本，安装对应版本的chromedriver

###2. Pycharm新建Python项目，进行虚拟环境搭建

###3. 查看当前项目目录下的文件get_movie_data.py，定位107，executable_path=./chromedriver.exe当前路径，需修改为chromedriver的存储路径成为绝对路径

###4. 最好先更换pip源，再使用命令pip install -r Pillow和pip install -r selenium 

####4.1 切换pip源的位置C:\Users\用户名\pip\pip.ini，默认情况下pip文件夹和pip.ini文件都未被创建，自行修改

###5. 如果出现无法启动驱动的情况，大概率是发生了chrome自动升级的情况，解决办法是卸载后重装对应的版本，或者锁定升级服务项
