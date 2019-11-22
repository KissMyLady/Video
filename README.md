视频裁剪(图片拼接)
=====
## 说明  
* 1、功能  
    * 一、将视频按帧截图  
    * 二、将截图裁剪指定大小  
    * 三、截图(图片)拼接  

* 2、使用方法  
    * 一、复制粘贴，在IDE里仔细阅读源代码(很简单), 注释有详细说明  
    * 二、在GitHub向我提问  
    * 三、问我(QQ群:36877 9008), 私人小群  

* 3、声明  
    * 自己写的小工具，希望能帮助到各位  
    * 可以用OOP更进一步升级代码，欢迎前来讨论, QQ(群:36877 9008)
    * 可进一步优化升级方案， 例如，在视频截图时，计算型操作更频繁， 在图片合并时，IO操作更频繁，  
       可针对这个特性进行优化升级
## :computer: 以 下     
## 代码块一  
### 效果预览  
* 视频 》》 截图  
![1-1](https://github.com/KissMyLady/Exchaneg-video-to-photo/blob/master/Img/video-1-2.jpg)    
```Python 
# !/usr/bin/python
# !coding:utf-8
import cv2, random, os, time
from multiprocessing import Pool
start = time.time()


def main(file_name, N):
    rand = random.randint(2, 100) * 2  # 分配随机, 唯一编号
    # 读取视频
    vc = cv2.VideoCapture(r'H:\我的文档\哲学\{}.flv'.format(file_name))
    if vc.isOpened():            # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
        
    c, timeF = 1, 46             # 丢进去的视频，23帧为1s，意思就是每2秒截图一次
    while rval:                  # 循环读取视频帧
        rval, frame = vc.read()
        if (c % timeF == 0):     # 每隔timeF帧保存
            path = r'I:\study\{}'.format(N) + "\%s-%s-%s.jpg" % (rand, str(time.time()), c)
            cv2.imwrite(path, frame)
            print(path, '\t', 'complete')
        c = c + 1
        cv2.waitKey(1)
    vc.release()


if __name__ == '__main__':
    filepath = r'H:\我的文档\哲学'
    files = os.listdir(filepath)
    file_list = []             # 遍历，找到所有视频文件
    for y in files:            # 迭代每个文件
        file_name = y.split('\\')[0]
        file_list.append(file_name[0: -4])
    
    # 开启进程池
    pool = Pool(8)
    N = 1
    for i in file_list:
        print('开启进程池: ', i)
        pool.apply_async(main, args=(i, N))
        N += 1
    pool.close()
    pool.join()
    
    # 测试运行时间
    end = time.time()
    print('进程共耗耗时 :', end - start)
```

## 代码块二  
### 效果预览 
截图 》》 字幕裁剪  
![1-2](https://github.com/KissMyLady/Exchaneg-video-to-photo/blob/master/Img/viedo1-3.jpg)  
```Python
import cv2, os
from multiprocessing import Pool


def run(path, file_path):
    print(path)
    try:
        img = cv2.imread('{}'.format(path))  # 读取图片
        h, w, c = img.shape                  # 读取属性, 高, 宽, c
        h1 = int(int(h) * 0.8)               # 通过控制这里数字, 可以选择裁剪尺寸
        h2 = int(int(h) * 1)                 # 通过控制这里数字, 可以选择裁剪尺寸
        w1 = int(int(w) * 0)                 # 通过控制这里数字, 可以选择裁剪尺寸
        w2 = int(int(w) * 1)                 # 通过控制这里数字, 可以选择裁剪尺寸
    
        crop_img = img[h1: h2, w1: w2]       # 裁剪尺寸
        toPath = str(path).split('\\')[-1]
        finally_path = os.path.join('H:\cath_img\zhexue'+'\\'+file_path+'\\'+toPath)
        cv2.imwrite(finally_path, crop_img)  # 保存
        print('----------complete----------')
    except:
        print('>'*20, path,'\t', file_path)
        eree_data = str(path)+'\n'+ str(file_path)
        with open(r'G:\big data folder\11-22eree.txt', 'a', encoding='utf-8') as f:
            f.write(eree_data)
    finally:
        pass


def main(Path):
    files = os.listdir(Path)
    for y in files:
        y = y.split('\\')[0]
        yy = os.path.join(Path+'\\'+ y)
        print(yy)
        # yy = I:\study\ZHEXUE__SOURCE\1-1\20-1573058242.2784717-7774.jpg
        toPath = str(yy).split('\\')[-2]
        print(toPath)
        # toPath = 1-1
        run(yy ,toPath)


def get_all_file_name_run(Path):
    file_list = list()
    files = os.listdir(Path)
    for y in files:
        re_file = Path +'\\'+y
        file_list.append(re_file)
    return file_list


if __name__ == '__main__':
    path = r'I:\study\ZHEXUE__SOURCE'
    file_list_name_all = get_all_file_name_run(path)
    # 开启进程池
    pool = Pool(8)
    pool.map(main, [file_list_name for file_list_name in file_list_name_all])


```
## 代码块三
### 效果预览  
字幕裁剪 》》 长图拼接  
![1-3](https://github.com/KissMyLady/Exchaneg-video-to-photo/blob/master/Img/video-1-4.jpg)  
```Python
import PIL.Image as Image
import os, cv2
from multiprocessing import Pool


def Get_Img_All_File_Name(Path):
    image_names = list()
    files = os.listdir(Path)
    for y in files:
        y = y.split('\\')[0]
        y = '\\' + y
        image_names.append(y)
    return image_names


def image_compose(IMAGES_PATH, IMAGE_SAVE_PATH, IMAGE_COLUMN, IMAGE_ROW, image_names, weight, height):
    to_image = Image.new('RGB', (IMAGE_COLUMN * weight, IMAGE_ROW * height))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize((weight, height),
                                                                                                      Image.ANTIALIAS)
            
            to_image.paste(from_image, ((x - 1) * weight, (y - 1) * height))
            
    try:
        to_image.save(IMAGE_SAVE_PATH)  # 保存新图
        print(IMAGE_SAVE_PATH, '成  功')
    except:
        print('保存错误')
        print('---结束程序---')


def main(path_one):
    IMAGES_PATH = r'{}'.format(path_one)                # 完成前, 要合成图片的地址
    IMAGE_SAVE_PATH = r'{}\final.jpg'.format(path_one)  # 完成后, 直接在当前图片集下创建新合成文件
    # IMAGES_FORMAT = ['.jpg']        # 图片格式(仅告知)
    files = os.listdir(path_one)      # 获取当前文件夹下文件个数
    IMAGE_ROW = int(len(files))       # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_COLUMN = 1                  # 图片间隔，也就是合并成一张图后，一共有几列

    h_w_c = Get_Img_All_File_Name(path_one)
    n = 1
    for i in h_w_c:
        lujing_path = path_one + i
        img = cv2.imread('{}'.format(lujing_path))   # 读取图片
        h, w, c = img.shape                          # 获取图片集合下某一文件属性
        n += 1
        if n == 2:
            break
    weight, height = int(w), int(h)                  # 操作对象: 宽度, 高度
    image_names = Get_Img_All_File_Name(IMAGES_PATH) # 获取所有文件,属性判断, 最后传入处理函数
    if len(image_names) == IMAGE_ROW * IMAGE_COLUMN:
        print('Start')
        image_compose(IMAGES_PATH, IMAGE_SAVE_PATH, IMAGE_COLUMN, IMAGE_ROW, image_names, weight, height)  # 调用函数
    else:
        raise ValueError("参数不对，请核对")


if __name__ == '__main__':
    # 以上, 全部都实行了自动化, 此时, 只要传入path即可
    listdir_path = r'H:\cath_img\zhexue'
    files = os.listdir(listdir_path)
    
    path_list = list()
    # 遍历文件, 把子文件目录都存起来
    for y in files:
        file_new = listdir_path + '\\' + y
        path_list.append(file_new)
    
    # 开启进程, 这里的限制在于磁盘读写效率，cup不会满载
    pool = Pool(8)
    pool.map(main, [file_new for file_new in path_list])
```





### 排版  

笔记内容按照 [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines) 进行排版，以保证内容的可读性。  
不使用 `<img>` 这种方式来引用图片，而是用 `![]()` 标签，一方面够用，另一方面，今后可能也会采用这种方法居中显示图片。  

在线排版工具： [Text-Typesetting](https://github.com/CyC2018/Text-Typesetting)  

技术支持： [CyC2018](https://github.com/CyC2018/Text-Typesetting)  

### License  
本仓库的内容是平时个人学习拙见与网络大佬文章细节拼接，这样，省去了打字的劳苦，也很感谢世界上为此默默奉献的人，同时，会尽量保证给出资料引用的地址，其余就是知识讲解了。在您引用此仓库的内容或进行修改时，请署名以相同方式共享，感谢。  

转载文章不限制，记得起就写，懒得写就算了，不强求。  


