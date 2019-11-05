#!/usr/bin/python
# !coding:utf-8
import cv2, random
import os, time
from multiprocessing import Pool

start = time.time()


def main(file_name):
    # 总共有8进程，会导致编号混乱，在这里，每新开一个进程，就单独分配一个编号
    rand = random.randint(2, 50) * 2
    
    # 读入视频文件
    vc = cv2.VideoCapture(r'H:\我的文档\统计学\{}.flv'.format(file_name))
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
    # 视频帧计数间隔频率
    
    c, timeF = 1, 46  # 丢进去的视频，23帧为1s，意思就是每2秒截图一次
    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if (c % timeF == 0):  # 每隔timeF帧进行存储操作
            # 保 存
            cv2.imwrite('./%s-%s-%s.jpg' % (str(rand), str(time.time()), c), frame)
            print('complete {}'.format(c))
        c = c + 1
        cv2.waitKey(1)
    vc.release()


if __name__ == '__main__':
    filepath = r'H:\我的文档\如何摄取信息'
    files = os.listdir(filepath)
    # 遍历，找到所有视频文件
    file_list = []
    for y in files:
        # 迭代每个文件
        file_name = y.split('\\')[0]
        nn = file_name[0:-4]
        file_list.append(nn)
    
    pool = Pool(6)
    for i in file_list:
        # 开启6进程
        pool.apply_async(main, args=(i,))
    
    # 测试运行时间
    end = time.time()
    pool.close()
    pool.join()
    print('6进程共耗耗时 :', end - start)


