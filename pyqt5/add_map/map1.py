import requests
import os

# 文件存放位置设置
BASE_PATH = os.path.join(os.path.abspath(os.curdir), 'disc')
BASE_PATH_res = os.path.join(os.path.abspath(os.curdir), 'result')

# 简单反爬虫 , 可以不写
headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}


def download_pic(x, y, z):
    try:
        # 下载图片
        key = 'a4ee5c551598a1889adfabff55a5fc27'
        for xi in x:
            for yi in y:
                url = "http://t3.tianditu.gov.cn/DataServer?T=vec_w&x={}&y={}&l={}&tk={}".format(xi, yi, z, key)
                # 保存文件名称
                fileName = os.path.join(BASE_PATH, "x={}y={}z={}.png".format(xi, yi, z))
                # 具体下载操作
                if (os.path.exists(fileName)) == False:
                    r = requests.get(url=url, headers=headers)
                    print(r.status_code)
                    if r.status_code == 200:
                        with open(fileName, 'wb') as f:
                            for chunk in r:
                                f.write(chunk)
                    else:
                        print("访问异常")
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    x = range(27326 - 1, 27326 + 2)
    y = range(13492 - 1, 13492 + 2)
    z = 15
    picSize = 256
    download_pic(x, y, z)
