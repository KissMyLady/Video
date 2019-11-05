import os


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 不存在则创建为文件夹
        os.makedirs(path)  # 路径不存在会创建这个路径
        print("---  new folder...  ---")
        print('"---  OK  ---"')
    else:
        print
        "---  There is this folder!  ---"

def run(Path, toPath):
    files = os.listdir(Path)
    # print(files)
    for y in files:
        if '、' in y:
            # print(y)
            y = y.split('\\')[0]
            print(y[0:-4])
            yy = y[0:-4]
            print(yy)
            mkdir(r"{}\{}".format(toPath, yy))
        else:
            pass

# 已经封装好， 转入路径即可
Path = r'H:\我的文档\如何摄取信息'
toPath = r"I:\学习截图--集合\信息质量--学习"
run(Path, toPath)
