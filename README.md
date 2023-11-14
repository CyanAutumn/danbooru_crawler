# danbooru_cawler 
一个基于scrapy的danbooru图片抓取工具

## 运行

初次运行需要安装环境

```
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python .\main.py
```

以后每次运行只需要

```
.\venv\Scripts\activate
python .\main.py
```

## 说明

调整需要抓取的tag可以更改/danbooru_crawler/settings.py文件内的SEARCH_KEYS值，多个tag用+相连

图片将输出在/pics/full文件夹内

如果运行一段时间后没有图片可能是Pillow版本过低，建议在虚拟环境下执行
```
pip uninstall Pillow
pip install Pillow
```