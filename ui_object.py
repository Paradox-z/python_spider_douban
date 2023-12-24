# -*- coding:utf-8 -*-
from PIL import Image, ImageTk
from get_movie_data import moviedata
from get_movie_data import get_url_data_in_ranking_list
from get_movie_data import get_url_data_in_keyword
from tkinter import Tk
from tkinter import ttk
from tkinter import font
from tkinter import LabelFrame
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import END
from tkinter import Button
from tkinter import Frame
from tkinter import RIGHT
from tkinter import NSEW
from tkinter import NS
from tkinter import NW
from tkinter import N
from tkinter import Y
from tkinter import messagebox
from tkinter import DISABLED
from tkinter import NORMAL
from re import findall
from json import loads
from ssl import _create_unverified_context
from threading import Thread
from urllib.parse import quote
from webbrowser import open
import urllib
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context # SSL blocked

# Maybe we should do UI frame design with PyQT, that's the solution for enterprise testing and development.

def thread_it(func, *args):
    '''
    Packing functions into threads
    '''
    # create
    t = Thread(target=func, args=args)
    # daemon
    t.setDaemon(True)
    # start
    t.start()

def handler_adaptor(fun, **kwds):
    '''Adapters for event handling Functions'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

def save_img(img_url, file_name, file_path):
    """
    :param img_url:
    :param file_name:
    :param file_path:
    :return:
    """
    #default path
    try:
        # Determining whether a folder already exists
        if not os.path.exists(file_path):
            print('Folder',file_path,'not exist, rebuild.')
            os.makedirs(file_path)
        # Get file suffix
        file_suffix = os.path.splitext(img_url)[1]
        # Splice image name, include path
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)

        # Determining whether a folder already exists
        if not os.path.exists(filename):
            print('document', filename, 'not exist, rebuild.')
            # Download and save images
            urllib.request.urlretrieve(img_url, filename=filename)
        return filename

    except IOError as e:
        print('Fail to download images',e)
    except Exception as e:
        print('Error:',e)

def resize(w_box, h_box, pil_image):
    """
    Scale the image proportionally and limit it to the specified box.
    :param w_box,h_box: specified box
    :param pil_image: original image
    :return:
    """

    f1 = 1.0 * w_box / pil_image.size[0]  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / pil_image.size[1]
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(pil_image.size[0] * factor)
    height = int(pil_image.size[1] * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def get_mid_str(content, startStr, endStr):
    startIndex = content.find(startStr, 0)  # Locate the first character of the start string and start searching from the start position

    if startIndex >= 0:
        startIndex += len(startStr)
    else:
        return ""

    end_index = content.find(endStr, startIndex)  # To locate the end string, start from the beginning string.

    if end_index >= 0 and end_index >= startIndex:
        return content[startIndex:end_index]
    else:
        return ""

class ui_object:

    def __init__(self):
        self.jsondata = ""
        self.jsondata_keyword = ""

    def show_gui_movie_detail(self):
        '''
        Displaying film message and graphical user interface
        '''
        self.label_img['state'] = NORMAL
        self.label_movie_name['state'] = NORMAL
        self.label_movie_rating['state'] = NORMAL
        self.label_movie_time['state'] = NORMAL
        self.label_movie_type['state'] = NORMAL
        self.label_movie_actor['state'] = NORMAL

    def hidden_gui_movie_detail(self):
        self.label_img['state'] = DISABLED
        self.label_movie_name['state'] = DISABLED
        self.label_movie_rating['state'] = DISABLED
        self.label_movie_time['state'] = DISABLED
        self.label_movie_type['state'] = DISABLED
        self.label_movie_actor['state'] = DISABLED

    def show_imdb_rating(self):
        self.label_movie_rating_imdb.config(text='Loading ranking IMDb')
        self.b_0_imdb['state'] = DISABLED

        item = self.treeview.selection()
        if item:
            item_text = self.treeview.item(item, "values")
            movie_name = item_text[0]  # output movie_name
            for movie in self.jsondata:
                if movie['title'] == movie_name:

                    context = _create_unverified_context()  # Blocking SSL
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
                    req = urllib.request.Request(url=movie['url'], headers=headers)
                    f = urllib.request.urlopen(req, context=context)
                    response = f.read().decode()

                    self.clear_tree(self.treeview_play_online)
                    s = response
                    name = findall(r'<a class="playBtn" data-cn="(.*?)" data-impression-track', s)
                    down_url = findall(r'data-cn=".*?" href="(.*?)" target=', s)

                    res_list = []
                    for i in range(len(name)):
                        res_list.append([name[i], "VIP blocked", down_url[i]])
                    self.add_tree(res_list, self.treeview_play_online)

                    self.clear_tree(self.treeview_save_cloud_disk)
                    res_list = []
                    res_list.append(["56网盘搜索", "Verified", "https://www.56wangpan.com/search/o2kw" + quote(movie['title'])])
                    res_list.append(["小白盘", "Verified", "https://www.xiaobaipan.com/list-" + quote(movie['title']) + "-1.html" ])
                    self.add_tree(res_list, self.treeview_save_cloud_disk)

                    self.clear_tree(self.treeview_bt_download)
                    res_list = []
                    res_list.append(['LOL电影', 'Verified', 'http://www.993dy.com/index.php?m=vod-search&wd=' + quote(movie['title'])])
                    res_list.append(['看美剧', 'Verified', 'http://www.kanmeiju.net/index.php?s=/video/search/wd/' + quote(movie['title'])])
                    res_list.append(['飘花资源网', 'Verified', 'https://www.piaohua.com/plus/search.php?kwtype=0&keyword=' + quote(movie['title'])])
                    res_list.append(['中国高清网', 'Verified', 'http://gaoqing.la/?s=' + quote(movie['title'])])
                    self.add_tree(res_list, self.treeview_bt_download)

                    imdb_num = get_mid_str(response, 'IMDb:</span>', '<br>').strip()
                    imdb_url = "https://www.imdb.com/title/{}/".format(imdb_num)
                    print("Film name:{}, IMDb:{}".format(movie['title'], imdb_num))

                    f = urllib.request.urlopen(imdb_url)
                    data_imdb = f.read().decode()
                    rating_imdb = get_mid_str(data_imdb, '{"@type":"AggregateRating"', '}')
                    rating_imdb = rating_imdb.split(":")[-1]

                    self.label_movie_rating_imdb.config(text='IMDb rate:' + rating_imdb + '')

        self.b_0_imdb['state'] = NORMAL

    def project_statement_get_focus(self, event):
        self.project_statement.config(fg="blue", cursor="hand1")

    def project_statement_lose_focus(self, event):
        self.project_statement.config(fg="#FF0000")

    def show_movie_data(self, event):
        '''
        Displaying details for a selected movie
        '''
        # self.hidden_gui_movie_detail()
        self.b_0_imdb['state'] = NORMAL
        self.label_movie_rating_imdb.config(text = 'IMDb rate:')
        self.clear_tree(self.treeview_play_online)
        self.clear_tree(self.treeview_save_cloud_disk)
        self.clear_tree(self.treeview_bt_download)

        item = self.treeview.selection()
        if item:
            item_text = self.treeview.item(item, "values")
            movie_name = item_text[0] # output movie_name
            for movie in self.jsondata:
                if(movie['title'] == movie_name):
                    img_url = movie['cover_url']
                    movie_name = movie['title']
                    file_name = save_img(img_url, movie_name, 'img') # Download images
                    self.show_movie_img(file_name)
                    self.label_movie_name.config(text=movie['title'])
                    if(isinstance(movie['actors'],list)):
                        string_actors = "、".join(movie['actors'])
                    else:
                        string_actors = movie['actors']
                    self.label_movie_actor.config(text=string_actors)
                    self.label_movie_rating.config(text=str(movie['rating'][0]) + ' ' + str(movie['vote_count']) + 'rating')
                    self.label_movie_time.config(text=movie['release_date'])
                    self.label_movie_type.config(text=movie['types'])

                    break
        # self.show_gui_movie_detail()
    def show_movie_img(self, file_name):
        '''
        Refresh images
        :param file_name: image path
        :return:
        '''
        img_open = Image.open(file_name) # load local images
        pil_image_resized = resize(160, 230, img_open) # proportionally scaling local images
        img = ImageTk.PhotoImage(pil_image_resized) # pull images
        self.label_img.config(image=img, width = pil_image_resized.size[0], height = pil_image_resized.size[1])
        self.label_img.image = img

    def center_window(self, root, w, h):
        """
        Window centred
        :param root: root
        :param w: width
        :param h: height
        :return:
        """
        # get the screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # calculate x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def clear_tree(self, tree):
        '''
        clean tables
        '''
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def add_tree(self,list, tree):
        '''
        add data into tables
        '''
        i = 0
        for subList in list:
            tree.insert('', 'end', values=subList)
            i = i + 1
        tree.grid()

    def searh_movie_in_rating(self):
        self.clear_tree(self.treeview)
        self.b_0['state'] = DISABLED
        self.c_type['state'] = DISABLED
        self.t_count['state'] = DISABLED
        self.t_rating['state'] = DISABLED
        self.t_vote['state'] = DISABLED
        self.b_0_keyword['state'] = DISABLED
        self.t_vote_keyword['state'] = DISABLED
        self.b_0['text'] = 'Trying to search'
        self.jsondata = ""

        json_moviedata = loads(moviedata)
        for sub_moviedata in json_moviedata:
            if(sub_moviedata['title'] == self.c_type.get()):
                res_data = get_url_data_in_ranking_list(sub_moviedata['type'], self.t_count.get(), self.t_rating.get(), self.t_vote.get())
                if len(res_data) == 2:
                    res_list = res_data[0]
                    jsondata = res_data[1]

                    self.jsondata = jsondata
                    self.add_tree(res_list, self.treeview)

                else:
                    err_str = res_data[0]
                    messagebox.showinfo('Notification', err_str[:1000])

        self.b_0['state'] = NORMAL
        self.c_type['state'] = 'readonly'
        self.t_count['state'] = NORMAL
        self.t_rating['state'] = NORMAL
        self.t_vote['state'] = NORMAL
        self.b_0_keyword['state'] = NORMAL
        self.t_vote_keyword['state'] = NORMAL
        self.b_0['text'] = 'Search by ranking'

    def keyboard_t_vote_keyword(self, event):
        """
        :param event:
        :return:
        """
        thread_it(self.searh_movie_in_keyword)

    def searh_movie_in_keyword(self):
        self.clear_tree(self.treeview)
        self.b_0['state'] = DISABLED
        self.c_type['state'] = DISABLED
        self.t_count['state'] = DISABLED
        self.t_rating['state'] = DISABLED
        self.t_vote['state'] = DISABLED
        self.b_0_keyword['state'] = DISABLED
        self.t_vote_keyword['state'] = DISABLED
        self.b_0_keyword['text'] = 'Trying to search'
        self.jsondata = ""

        res_data = get_url_data_in_keyword(self.t_vote_keyword.get())
        if len(res_data) == 2:
            res_list = res_data[0]
            jsondata = res_data[1]

            self.jsondata = jsondata
            self.add_tree(res_list, self.treeview)
        else:
            err_str = res_data[0]
            messagebox.showinfo('Notification', err_str[:1000])

        # Formal status
        self.b_0['state'] = NORMAL
        self.c_type['state'] = 'readonly'
        self.t_count['state'] = NORMAL
        self.t_rating['state'] = NORMAL
        self.t_vote['state'] = NORMAL
        self.b_0_keyword['state'] = NORMAL
        self.t_vote_keyword['state'] = NORMAL
        self.b_0_keyword['text'] = 'Search by keywords'

    def open_in_browser_douban_url(self, event):
        """
        :param
        :return:
        """
        item = self.treeview.selection()
        if item:
            item_text = self.treeview.item(item, "values")
            movie_name = item_text[0]
            for movie in self.jsondata:
                if(movie['title'] == movie_name):
                    open(movie['url'])

    def open_in_browser(self, event):
        """
        :param
        :return:
        """
        item = self.treeview_play_online.selection()
        if(item):
            item_text = self.treeview_play_online.item(item, "values")
            url = item_text[2]
            open(url)

    def open_in_browser_cloud_disk(self, event):
        """
        :param
        :return:
        """
        item = self.treeview_save_cloud_disk.selection()
        if(item):
            item_text = self.treeview_save_cloud_disk.item(item, "values")
            url = item_text[2]
            open(url)

    def open_in_browser_bt_download(self, event):
        """
        :param
        :return:
        """
        item = self.treeview_bt_download.selection()
        if(item):
            item_text = self.treeview_bt_download.item(item, "values")
            url = item_text[2]
            open(url)

    def ui_process(self):
        """
        :param
        :return:
        """
        root = Tk()
        self.root = root
        # Setting the window position
        root.title("豆瓣电影助手(支持筛选、下载电影)")
        self.center_window(root, 1000, 565)
        root.resizable(0, 0)
        labelframe = LabelFrame(root, width=660, height=300, text="搜索电影")
        labelframe.place(x=5, y=5)
        self.labelframe = labelframe
        l_typeId = Label(labelframe, text='电影类型')
        l_typeId.place(x=0, y=10)
        self.l_typeId = l_typeId
        comvalue = StringVar()
        c_type = ttk.Combobox(labelframe, width=5, textvariable=comvalue, state='readonly')
        json_moviedata = loads(moviedata) # json
        movieList = []
        for sub_moviedata in json_moviedata:
            movieList.append(sub_moviedata['title'])
        c_type["values"] = movieList # initialisation
        c_type.current(9)  # Firse
        c_type.place(x=65, y=8)
        self.c_type = c_type
        # movie amount
        l_count = Label(labelframe, text='获取数量=')
        l_count.place(x=150, y=10)
        self.l_count = l_count
        # text frame
        t_count = Entry(labelframe, width=5)
        t_count.delete(0, END)
        t_count.insert(0, '100')
        t_count.place(x=220, y=7)
        self.t_count = t_count
        # ranking
        l_rating = Label(labelframe, text='影片评分>')
        l_rating.place(x=280, y=10)
        self.l_rating = l_rating
        # text frame
        t_rating = Entry(labelframe, width=5)
        t_rating.delete(0, END)
        t_rating.insert(0, '8.0')
        t_rating.place(x=350, y=7)
        self.t_rating = t_rating
        # amount
        l_vote = Label(labelframe, text='评价人数>')
        l_vote.place(x=410, y=10)
        self.l_vote = l_vote
        # text frame
        t_vote = Entry(labelframe, width=7)
        t_vote.delete(0, END)
        t_vote.insert(0, '100000')
        t_vote.place(x=480, y=7)
        self.t_vote = t_vote
        # Search button
        #lambda
        #thread_it
        b_0 = Button(labelframe, text="从排行榜搜索")
        b_0.place(x=560, y=10)
        self.b_0 = b_0
        # Frame location
        frame_root = Frame(labelframe, width=400)
        frame_l = Frame(frame_root)
        frame_r = Frame(frame_root)
        self.frame_root = frame_root
        self.frame_l = frame_l
        self.frame_r = frame_r
        # Table
        columns = ("影片名字", "影片评分", "同类排名", "评价人数")
        treeview = ttk.Treeview(frame_l, height=10, show="headings", columns=columns)

        treeview.column("影片名字", width=210, anchor='center')  # display column
        treeview.column("影片评分", width=210, anchor='center')
        treeview.column("同类排名", width=100, anchor='center')
        treeview.column("评价人数", width=100, anchor='center')

        treeview.heading("影片名字", text="影片名字")  # display head
        treeview.heading("影片评分", text="影片评分")
        treeview.heading("同类排名", text="同类排名")
        treeview.heading("评价人数", text="评价人数")
        # vertical scrollbar
        vbar = ttk.Scrollbar(frame_r, command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)

        treeview.pack()
        self.treeview = treeview
        vbar.pack(side=RIGHT, fill=Y)
        self.vbar = vbar
        # Frame location
        frame_l.grid(row=0, column=0, sticky=NSEW)
        frame_r.grid(row=0, column=1, sticky=NS)
        frame_root.place(x=5, y=70)

        # Name
        l_vote_keyword = Label(labelframe, text='影片名称')
        l_vote_keyword.place(x=0, y=40)
        self.l_vote_keyword = l_vote_keyword

        # text frame
        t_vote_keyword = Entry(labelframe, width=53)
        t_vote_keyword.delete(0, END)
        t_vote_keyword.insert(0, '新世纪福音战士')
        t_vote_keyword.place(x=66, y=37)
        self.t_vote_keyword = t_vote_keyword
        # Search button
        #lambda
        #thread_it
        b_0_keyword = Button(labelframe, text="从关键字搜索")
        b_0_keyword.place(x=560, y=40)
        self.b_0_keyword = b_0_keyword

        # Container modules
        labelframe_movie_detail = LabelFrame(root, text="影片详情")
        labelframe_movie_detail.place(x=670, y=5)
        self.labelframe_movie_detail = labelframe_movie_detail
        # Frame
        frame_left_movie_detail = Frame(labelframe_movie_detail, width=160,height=280)
        frame_left_movie_detail.grid(row=0, column=0)
        self.frame_left_movie_detail = frame_left_movie_detail

        frame_right_movie_detail = Frame(labelframe_movie_detail, width=160,height=280)
        frame_right_movie_detail.grid(row=0, column=1)
        self.frame_right_movie_detail = frame_right_movie_detail
        # image
        label_img = Label(frame_left_movie_detail, text="", anchor=N)
        label_img.place(x=0,y=0) #布局
        self.label_img = label_img
        # IMDB ranks
        ft_rating_imdb = font.Font(weight=font.BOLD)
        label_movie_rating_imdb = Label(frame_left_movie_detail, text="IMDB评分", fg='#7F00FF', font=ft_rating_imdb, anchor=NW)
        label_movie_rating_imdb.place(x=0, y=250)
        self.label_movie_rating_imdb = label_movie_rating_imdb
        # Search button
        b_0_imdb = Button(frame_left_movie_detail, text="详情")
        b_0_imdb.place(x=115, y=250)
        self.b_0_imdb = b_0_imdb
        # Name
        ft = font.Font(size=15, weight=font.BOLD)
        label_movie_name = Label(frame_right_movie_detail, text="影片名字", fg='#FF0000', font=ft,anchor=NW)
        label_movie_name.place(x=0, y=0)
        self.label_movie_name = label_movie_name
        # Ranking
        ft_rating = font.Font(weight=font.BOLD)
        label_movie_rating = Label(frame_right_movie_detail, text="影片评价", fg='#7F00FF', font=ft_rating, anchor=NW)
        label_movie_rating.place(x=0, y=30)
        self.label_movie_rating = label_movie_rating
        # Age
        ft_time = font.Font(weight=font.BOLD)
        label_movie_time = Label(frame_right_movie_detail, text="影片日期", fg='#666600', font=ft_time, anchor=NW)
        label_movie_time.place(x=0, y=60)
        self.label_movie_time = label_movie_time
        # Type
        ft_type = font.Font(weight=font.BOLD)
        label_movie_type = Label(frame_right_movie_detail, text="影片类型", fg='#330033', font=ft_type, anchor=NW)
        label_movie_type.place(x=0, y=90)
        self.label_movie_type = label_movie_type
        # Actor
        label_movie_actor = Label(frame_right_movie_detail, text="影片演员", wraplength=135, justify = 'left', anchor=NW)
        label_movie_actor.place(x=0, y=120)
        self.label_movie_actor = label_movie_actor

        labelframe_movie_play_online = LabelFrame(root, width=324, height=230, text="在线观看")
        labelframe_movie_play_online.place(x=5, y=305)
        self.labelframe_movie_play_online = labelframe_movie_play_online
        # Frame
        frame_root_play_online = Frame(labelframe_movie_play_online, width=324)
        frame_l_play_online = Frame(frame_root_play_online)
        frame_r_play_online = Frame(frame_root_play_online)
        self.frame_root_play_online = frame_root_play_online
        self.frame_l_play_online = frame_l_play_online
        self.frame_r_play_online = frame_r_play_online
        # Table
        columns_play_online = ("来源名称", "是否免费","播放地址")
        treeview_play_online = ttk.Treeview(frame_l_play_online, height=10, show="headings", columns=columns_play_online)
        treeview_play_online.column("来源名称", width=90, anchor='center')
        treeview_play_online.column("是否免费", width=80, anchor='center')
        treeview_play_online.column("播放地址", width=120, anchor='center')
        treeview_play_online.heading("来源名称", text="来源名称")
        treeview_play_online.heading("是否免费", text="是否免费")
        treeview_play_online.heading("播放地址", text="播放地址")
        # vertical scrollbar
        vbar_play_online = ttk.Scrollbar(frame_r_play_online, command=treeview_play_online.yview)
        treeview_play_online.configure(yscrollcommand=vbar_play_online.set)

        treeview_play_online.pack()
        self.treeview_play_online = treeview_play_online
        vbar_play_online.pack(side=RIGHT, fill=Y)
        self.vbar_play_online = vbar_play_online
        # Frame location
        frame_l_play_online.grid(row=0, column=0, sticky=NSEW)
        frame_r_play_online.grid(row=0, column=1, sticky=NS)
        frame_root_play_online.place(x=5, y=0)

        labelframe_movie_save_cloud_disk = LabelFrame(root, width=324, height=230, text="云盘搜索")
        labelframe_movie_save_cloud_disk.place(x=340, y=305)
        self.labelframe_movie_save_cloud_disk = labelframe_movie_save_cloud_disk
        # Frame
        frame_root_save_cloud_disk = Frame(labelframe_movie_save_cloud_disk, width=324)
        frame_l_save_cloud_disk = Frame(frame_root_save_cloud_disk)
        frame_r_save_cloud_disk = Frame(frame_root_save_cloud_disk)
        self.frame_root_save_cloud_disk = frame_root_save_cloud_disk
        self.frame_l_save_cloud_disk = frame_l_save_cloud_disk
        self.frame_r_save_cloud_disk = frame_r_save_cloud_disk
        # Table
        columns_save_cloud_disk = ("来源名称", "是否有效","播放地址")
        treeview_save_cloud_disk = ttk.Treeview(frame_l_save_cloud_disk, height=10, show="headings", columns=columns_save_cloud_disk)
        treeview_save_cloud_disk.column("来源名称", width=90, anchor='center')
        treeview_save_cloud_disk.column("是否有效", width=80, anchor='center')
        treeview_save_cloud_disk.column("播放地址", width=120, anchor='center')
        treeview_save_cloud_disk.heading("来源名称", text="来源名称")
        treeview_save_cloud_disk.heading("是否有效", text="是否有效")
        treeview_save_cloud_disk.heading("播放地址", text="播放地址")
        # vertical scrollbar
        vbar_save_cloud_disk = ttk.Scrollbar(frame_r_save_cloud_disk, command=treeview_save_cloud_disk.yview)
        treeview_save_cloud_disk.configure(yscrollcommand=vbar_save_cloud_disk.set)

        treeview_save_cloud_disk.pack()
        self.treeview_save_cloud_disk = treeview_save_cloud_disk
        vbar_save_cloud_disk.pack(side=RIGHT, fill=Y)
        self.vbar_save_cloud_disk = vbar_save_cloud_disk
        # Frame location
        frame_l_save_cloud_disk.grid(row=0, column=0, sticky=NSEW)
        frame_r_save_cloud_disk.grid(row=0, column=1, sticky=NS)
        frame_root_save_cloud_disk.place(x=5, y=0)

        labelframe_movie_bt_download = LabelFrame(root, width=324, height=230, text="影视下载")
        labelframe_movie_bt_download.place(x=670, y=305)
        self.labelframe_movie_bt_download = labelframe_movie_bt_download
        # Frame
        frame_root_bt_download = Frame(labelframe_movie_bt_download, width=324)
        frame_l_bt_download = Frame(frame_root_bt_download)
        frame_r_bt_download = Frame(frame_root_bt_download)
        self.frame_root_bt_download = frame_root_bt_download
        self.frame_l_bt_download = frame_l_bt_download
        self.frame_r_bt_download = frame_r_bt_download
        # Table
        columns_bt_download = ("来源名称", "是否有效","播放地址")
        treeview_bt_download = ttk.Treeview(frame_l_bt_download, height=10, show="headings", columns=columns_bt_download)
        treeview_bt_download.column("来源名称", width=90, anchor='center')
        treeview_bt_download.column("是否有效", width=80, anchor='center')
        treeview_bt_download.column("播放地址", width=120, anchor='center')
        treeview_bt_download.heading("来源名称", text="来源名称")
        treeview_bt_download.heading("是否有效", text="是否有效")
        treeview_bt_download.heading("播放地址", text="播放地址")
        # vertical scrollbar
        vbar_bt_download = ttk.Scrollbar(frame_r_bt_download, command=treeview_bt_download.yview)
        treeview_bt_download.configure(yscrollcommand=vbar_bt_download.set)

        treeview_bt_download.pack()
        self.treeview_bt_download = treeview_bt_download
        vbar_bt_download.pack(side=RIGHT, fill=Y)
        self.vbar_bt_download = vbar_bt_download

        frame_l_bt_download.grid(row=0, column=0, sticky=NSEW)
        frame_r_bt_download.grid(row=0, column=1, sticky=NS)
        frame_root_bt_download.place(x=5, y=0)

        ft = font.Font(size=14, weight=font.BOLD)
        project_statement = Label(root, text=".", fg='#000000', font=ft,anchor=NW)
        project_statement.place(x=5, y=540)
        self.project_statement = project_statement

        # bind event
        treeview.bind('<<TreeviewSelect>>', self.show_movie_data)
        treeview.bind('<Double-1>', self.open_in_browser_douban_url)
        treeview_play_online.bind('<Double-1>', self.open_in_browser)
        treeview_save_cloud_disk.bind('<Double-1>', self.open_in_browser_cloud_disk)
        treeview_bt_download.bind('<Double-1>', self.open_in_browser_bt_download)
        b_0.configure(command=lambda:thread_it(self.searh_movie_in_rating))
        b_0_keyword.configure(command=lambda:thread_it(self.searh_movie_in_keyword))
        b_0_imdb.configure(command=lambda: thread_it(self.show_imdb_rating))
        t_vote_keyword.bind('<Return>', handler_adaptor(self.keyboard_t_vote_keyword))
        project_statement.bind('<ButtonPress-1>', self.project_statement_show)
        project_statement.bind('<Enter>', self.project_statement_get_focus)
        project_statement.bind('<Leave>', self.project_statement_lose_focus)

        root.mainloop()
