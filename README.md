# NeteasyMusic

1. 一个利用 [wireshark][1] 抓包出来的pc客户端api制作的下载[网易云音乐][2]的音乐和Mv的一个小脚本。
2. 依赖的第三方库是 [request][3]

```
    usage: neteasymusic.py [-h] [-v] [-a ARTIST] [-b ALBUM] [-p PLAYLIST] [-m MV]
                           [-r ARTIST_MV] [-l ALBUM_MV] [-n PLAYLIST_MV]
                           [-s ONE_SONG] [-t ONE_MV] [--path PATH]  
    
    下载网易云音乐的歌曲和MV   

    optional arguments:
      -h, --help      show this help message and exit
      -v, --version   显示版本号
      -a ARTIST       下载歌手热歌，后面带歌手id。
      -b ALBUM        下载专辑歌曲，后面带专辑id。
      -p PLAYLIST     下载歌单歌曲，后面带歌单id
      -m MV           下载歌手相关Mv，后面带歌手id
      -r ARTIST_MV    下载歌手热歌中的Mv，后面带歌手id。
      -l ALBUM_MV     下载专辑Mv，后面带专辑id。
      -n PLAYLIST_MV  下载歌单Mv，后面带歌单id
      -s ONE_SONG     下载单首歌曲，后面带歌曲页面的id
      -t ONE_MV       下载单首Mv，后面带MV页面的id
      --path PATH     保存路径,默认在当前脚本运行目录
```

[1]: https://www.wireshark.org "抓包、抓包"
[2]: http://music.163.com "网易云音乐是一款专注于发现与分享的音乐产品，依托专业音乐人、DJ、好友推荐及社交功能，为用户打造全新的音乐生活。"
[3]: http://www.python-requests.org "Requests is an Apache2 Licensed HTTP library, written in Python, for human beings."