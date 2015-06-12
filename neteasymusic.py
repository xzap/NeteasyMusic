#!/usr/bin/env python
# -*- coding: utf-8 -*- #
### 一个利用wireshark抓包出来的pc客户端api制作的下载网易云音乐的音乐和Mv的一个小脚本。
### 使用方法直接运行就可以看到看了
### 依赖的第三方库是request

import requests
import hashlib
import base64
import os

class neteasymusic:
    def __init__(self):
        self.req = requests.Session()
        self.headers = {"Referer": "http://music.163.com/",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.138 Safari/537.36",
                        }
        self.cookies = {"appver": "1.5.2",
                        "os": "pc",
                        "channel": "netease",
                        "osver": "Microsoft-Windows-7-Professional-Service-Pack-1-build-7601-64bit",
                        }
        self.req.cookies.update(self.cookies)
        self.req.headers.update(self.headers)

###################下面是定义api，返回的都是json格式的列表########################

    def login(self, username, password, phone=False):
        '''
        登陆到网易云音乐
        '''
        action = 'http://music.163.com/api/login/'
        phone_action = 'http://music.163.com/api/login/cellphone/'
        password = password.encode('utf-8')
        data = {
            'username': username,
            'password': hashlib.md5(password).hexdigest(),
            'rememberLogin': 'true'
        }
        phone_data = {
            'phone': username,
            'password': hashlib.md5(password).hexdigest(),
            'rememberLogin': 'true'
        }
        try:
            if phone is True:
                r = self.req.post(phone_action, data = phone_data)
                return r.json()
            else:
                r = self.req.post(action, data = data)
                print (r.cookies)
                return r.json()
        except Exception as e:
            print(str(e))
            return {'code': 408}

    def encrypted_id(self,id):
        '''
        为下载mp3转换id
        '''
        byte1 = bytearray('3go8&$8*3*3h0k(2)2',"utf8")
        byte2 = bytearray(str(id),"utf8")
        byte1_len = len(byte1)
        for i in range(len(byte2)):
            byte2[i] = byte2[i]^byte1[i%byte1_len]
        m = hashlib.md5()
        m.update(byte2)
        result = m.digest()
        result=base64.encodebytes(result).decode()[:-1]
        result = result.replace('/', '_')
        result = result.replace('+', '-')
        return result   

    def search(self, s, s_type=1, offset=0, limit=100):
        '''
        搜索歌曲
        POST http://music.163.com/api/search/pc
        必要参数：
            s：搜索的内容
            offset：偏移量（分页用）
            limit：获取的数量
            type：搜索的类型
                歌曲 1
                专辑 10
                歌手 100
                歌单 1000
                用户 1002
                mv 1004
                歌词 1006
                主播电台 1009
        '''
        url = "http://music.163.com/api/search/pc"
        data = {"s":s,
                "offset": offset,
                "limit": limit,
                "type": s_type}
        r = self.req.post(url,data=data)
        #print (r.text)
        return r.json()["result"]['songs']  

    def song(self, uid):
        '''
        单曲信息
        Full request URI: http://music.163.com/api/song/detail/?id=28377211&ids=%5B28377211%5D
        GET  http://music.163.com/api/song/detail/  
        必要参数：   
            id：歌曲ID 
            ids：不知道干什么用的，用[]括起来的歌曲ID
        '''
        url = "http://music.163.com/api/song/detail/"  
        params = {"id": uid, "ids": "[%s]" % uid}
        r = self.req.get(url, params=params)
        return r.json() 

    def artist(self, uid):
        '''
        歌手信息
        Full request URI:  "http://music.163.com/api/artist/introduction?id=2116"
        '''
        url = "http://music.163.com/api/artist/introduction"
        params = {"id": uid}
        r = self.req.get(url,params=params)
        return r.json()  

    def artist_albums(self, uid, limit=20):
        '''
        歌手专辑
        Full request URI: http://music.163.com/api/artist/albums/166009?id=166009&offset=0&total=true&limit=5
        GET http://music.163.com/api/artist/albums/歌手ID
        必要参数：
            id: 歌手ID
            limit：获取的数量(不知道为什么这个必须加上）
        '''
        url = "http://music.163.com/api/artist/albums/%s" % uid
        params = {"id": uid, "limit": limit}
        r = self.req.get(url,params=params)
        return r.json()

    def artist_hotsong(self, uid):
        '''
        歌手热歌
        Full request URI: http://music.163.com/api/artist/166009?id=166009&offset=0&total=true&limit=5
        GET http://music.163.com/api/artist/albums/歌手ID
        必要参数：
            id: 歌手ID
            limit：获取的数量(不知道为什么这个必须加上）
        '''
        url = "http://music.163.com/api/artist/%s" % uid
        params = {"id": uid}
        r = self.req.get(url,params=params)
        return r.json() 

    def artist_mv(self, uid, limit=20):
        '''
        歌手MV
        http://music.163.com/api/artist/mvs?artistId=10198&offset=0&limit=20
        Full request URI: http://music.163.com/api/artist/mvs
        GET http://music.163.com/api/artist/albums/歌手ID
        必要参数：
        artistId: 歌手id
        limit：获取的数量
        '''
        url = "http://music.163.com/api/artist/mvs"
        params = {"artistId": uid, "limit": limit}
        r = self.req.get(url,params=params)
        # print (r.request.headers)
        return r.json()

    def album(self, uid, limit=30, ext="true", offset=0, total="ture" ):
        '''
        专辑信息
        Full request URI: http://music.163.com/api/album/2457012?ext=true&id=2457012&offset=0&total=true&limit=10
        GET http://music.163.com/api/album/专辑ID
        '''
        url = "http://music.163.com/api/album/%s" % uid
        params = {"id": uid, "ext": ext, "limit": limit, "total": total  }
        r = self.req.get(url, params=params)
        return r.json()

    def playlist(self, uid):
        '''
        歌单
        Full request URI: http://music.163.com/api/playlist/detail?id=37880978&updateTime=-1
        GET http://music.163.com/api/playlist/detail
        必要参数：
            id：歌单ID
        '''
        url =  "http://music.163.com/api/playlist/detail"
        params = {"id": uid}
        r = self.req.get(url, params=params)
        return r.json() 

    def lyric(self, uid, os="pc", lv=-1, kv=-1):
        '''
        歌词
        Full request URI: http://music.163.com/api/song/lyric?os=pc&id=93920&lv=-1&kv=-1&tv=-1
        GET http://music.163.com/api/song/lyric
        必要参数：
            id：歌曲ID
            lv：值为-1，我猜测应该是判断是否搜索lyric格式
            kv：值为-1，这个值貌似并不影响结果，意义不明
            tv：值为-1，是否搜索tlyric格式
        '''
        url = "http://music.163.com/api/song/lyric"
        params = {"id": uid, "os": os, "kv": kv, "lv": lv}
        r = self.req.get(url, params=params)
        return r.json()['lrc']['lyric']

    def mv(self, uid, s_type="mp4"):
        '''
        MV
        Full request URI: http://music.163.com/api/mv/detail?id=319104&type=mp4
        GET http://music.163.com/api/mv/detail
        必要参数：
            id：mvid
            type：值为mp4，视频格式，不清楚还有没有别的格式
        '''
        url = "http://music.163.com/api/mv/detail"
        params = {"id":uid, "type": s_type }
        r = self.req.get(url, params=params)
        return r.json()

    def user_playlist(self, uid, offset=0, limit=100):
        '''
        用户歌单
        http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=uid
        '''
        url = "http://music.163.com/api/user/playlist/"
        params = {"uid": uid, "offset": offset, "limit": limit }
        r = self.req.get(url, params=params)
        return r.json() 

    def radio(self) :
        '''
        电台
        '''
        url = "http://music.163.com/api/radio/get"  
        r = self.req.get(url)
        return r.json() 

################################定义api到此为止，下面是应用api了。#####################
    def get_track(self, tracks, fname):
        '''
        获取多轨列表中的歌曲信息
        '''
        result = []
        for track in tracks :
            name = track['name'].strip().replace(" ","_")
            album = track['album']['name'].strip().replace(" ","_")
            uuid = track['id']
            artists = track['artists']
            singer = "_".join([ artist['name'].strip().replace(" ","_") for artist in artists ]).replace(" ","_")
            try :
                sid = track['hMusic']['dfsId']
                ext = track['hMusic']['extension']
            except:
                sid = track['mMusic']['dfsId']
                ext = track['mMusic']['extension']
            filename = "%s-%s.%s" % (name, singer, ext)
            link = 'http://m1.music.126.net/{}/{}.{}'.format(self.encrypted_id(sid), sid,ext)
            result.append((uuid, fname, filename, link, True))
        return result

    def songofplaylist(self, uid):
        '''
        获取歌单中歌曲
        '''
        playlist = self.playlist(uid)['result']
        tracks =  playlist['tracks']
        playlist_name = playlist['name']        
        return  self.get_track(tracks,playlist_name)
        

    def songofalbum(self, uid):
        '''
        获取专辑中歌曲
        '''        
        album = self.album(uid)['album']
        tracks =  album['songs']
        album_name = album['name'].strip().replace(" ","_")
        return  self.get_track(tracks,album_name) 

    def songofartist(self,uid):
        '''
        获取歌手热歌中歌曲
        '''
        artist = self.artist_hotsong(uid)
        tracks =  artist['hotSongs']
        artist_name = artist['artist']['name'].strip().replace(" ","_")+"的热门歌曲"
        return  self.get_track(tracks,artist_name) 
        
    def get_mv(self, tracks, fname):
        result = []
        for track in tracks :
            name = track['name'].strip().replace(" ","_")
            album = track['album']['name'].strip().replace(" ","_")
            uuid = track['id']
            artists = track['artists']
            singer = "_".join([ artist['name'].strip().replace(" ","_") for artist in artists ]).replace(" ","_")
            mvid = track['mvid']
            if mvid == 0:
                continue
            else :
                mvbrs = self.mv(mvid)['data']['brs']
                maxbrs = max([ int(brs) for brs in mvbrs.keys()])
                mvlink = mvbrs[str(maxbrs)]
            filename = "%s-%s_%s.mp4" % (name, singer,maxbrs)
            result.append((mvid, fname, filename, mvlink, False))
        return result

    def mvofplaylist(self, uid):
        '''
        获取歌单中MV
        '''
        playlist = self.playlist(uid)['result']
        tracks =  playlist['tracks']
        playlist_name = playlist['name']
        return self.get_mv(tracks,playlist_name)  

    def mvofalbum(self, uid):
        '''
        获取专辑中MV
        '''        
        album = self.album(uid)['album']
        tracks =  album['songs']
        album_name = album['name'].strip().replace(" ","_")
        return self.get_mv(tracks,album_name)         

    def mvofartist(self,uid):
        '''
        获取指定歌手热歌中的MV
        '''
        artist = self.artist_hotsong(uid)
        tracks =  artist['hotSongs']
        artist_name = artist['artist']['name'].strip().replace(" ","_")+"的热门歌曲"
        return  self.get_track(tracks,artist_name) 

    def mvaboutartist(self, uid,limit=1000):
        '''
        获取指定歌手的相关mv
        '''
        artist = self.artist_hotsong(uid)
        artist_name = artist['artist']['name'].strip().replace(" ","_")+"的相关MV"
        mvs = self.artist_mv(uid,limit)['mvs']
        result=[]
        for mv in mvs :
            name = mv['name'].strip().replace(" ","_")
            singer = mv['artistName'].strip().replace(" ","_")
            mvid = mv['id']
            mvbrs = self.mv(mvid)['data']['brs']
            maxbrs = max([ int(brs) for brs in mvbrs.keys()])
            mvlink = mvbrs[str(maxbrs)]
            filename = "%s-%s_%s.mp4" % (name, singer,maxbrs)
            result.append((mvid, artist_name, filename, mvlink, False))
        return result

    def onesong(self, uid):
        tracks = self.song(uid)['songs']
        return  self.get_track(tracks,"单首歌曲下载") 

    def onemv(self,uid):
        mv = self.mv(uid)['data']
        mvid = uid
        name = mv['name'].strip().replace(" ","_")
        singer = mv['artistName'].strip().replace(" ","_")
        mvid = mv['id']
        mvbrs = self.mv(mvid)['data']['brs']
        maxbrs = max([ int(brs) for brs in mvbrs.keys()])
        mvlink = mvbrs[str(maxbrs)]
        filename = "%s-%s_%s.mp4" % (name, singer,maxbrs)
        result = [(mvid, '单部MV下载', filename, mvlink, False)]
        return result 

    # def download(self,downlist=[],path=os.path.realpath("/data/NeteasyMusic")):
    def download(self,downlist=[],path=os.getcwd()):
        path = os.path.realpath(path)
        cmd ="%s\n" \
        "  dir=%s\n" \
        "  out=%s\n" \
        "  header=Cookie: appver: 1.5.2;Referer:http://music.163.com;\n" \
        "  continue=true\n" \
        "  max-connection-per-server=5\n" \
        "  split=10\n" \
        "  parameterized-uri=true\n\n"
        downfile = os.path.join(path,"NeteasyMusic.down")
        if not os.path.exists(path): os.makedirs(path)
        if os.path.exists(downfile) : os.remove(downfile)
        ff = open(downfile,"w",encoding="utf-8")
        for i in downlist : 
            musicdir = os.path.realpath(os.path.join(path,i[1]))
            ff.write(cmd % (i[3], musicdir,i[2].replace("/","-")))           
        ff.close()
        shell = "aria2c -i "+ downfile
        # os.system(shell) 
        print (path,shell)

def main():
    n = neteasymusic()
    import argparse
    parser = argparse.ArgumentParser(description='下载网易云音乐的歌曲和MV')
    parser.add_argument("-v", "--version", version='%(prog)s 0.3',help='显示版本号',action="version")
    parser.add_argument("-a", action="store", dest="artist", help='下载歌手热歌，后面带歌手id。')
    parser.add_argument("-b", action="store", dest="album", help='下载专辑歌曲，后面带专辑id。')
    parser.add_argument("-p", action="store", dest="playlist", help='下载歌单歌曲，后面带歌单id')
    parser.add_argument("-m", action="store", dest="mv", help='下载歌手相关Mv，后面带歌手id')
    parser.add_argument("-r", action="store", dest="artist_mv", help='下载歌手热歌中的Mv，后面带歌手id。')
    parser.add_argument("-l", action="store", dest="album_mv", help='下载专辑Mv，后面带专辑id。')
    parser.add_argument("-n", action="store", dest="playlist_mv", help='下载歌单Mv，后面带歌单id')
    parser.add_argument("-s", action="store", dest="one_song", help='下载单首歌曲，后面带歌曲页面的id')
    parser.add_argument("-t", action="store", dest="one_mv", help='下载单首Mv，后面带MV页面的id')
    parser.add_argument("--path", action="store", help='保存路径,默认在当前脚本运行目录')
    args = parser.parse_args()
    if args.artist :
        uuid = args.artist
        if uuid.isdigit():
            content = n.songofartist(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.album :
        uuid = args.album
        if uuid.isdigit():
            content = n.songofalbum(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.playlist :
        uuid = args.playlist
        if uuid.isdigit():
            content = n.songofplaylist(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.mv :
        uuid = args.mv
        if uuid.isdigit():
            content = n.mvaboutartist(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.artist_mv :
        uuid = args.artist_mv
        if uuid.isdigit():
            content = n.mvofartist(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.album_mv :
        uuid = args.album_mv
        if uuid.isdigit():
            content = n.mvofalbum(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.playlist_mv :
        uuid = args.playlist_mv
        if uuid.isdigit():
            content = n.mvofplaylist(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.one_mv :
        uuid = args.one_mv
        if uuid.isdigit():
            content = n.onemv(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    elif args.one_song :
        uuid = args.one_song
        if uuid.isdigit():
            content = n.onesong(uuid)
            if args.path :
                n.download(content,args.path)
            else :
                n.download(content)
        else :
            print ("请输入纯数字id")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()