#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:lgc
# datetime:2021/12/8 16:38
# Describe:
#  网易云音乐批量下载
# Tsing 2019.03.28

# 首先，找到你要下载的歌曲，用网页版打开，复制链接中的歌曲ID，如：http://music.163.com/#/song?id=476592630 这个链接ID就是 476592630
# 然后将ID替换到链接 http://music.163.com/song/media/outer/url?id=ID.mp3 中的ID位置即可获得歌曲的外链：http://music.163.com/song/media/outer/url?id=476592630.mp3
import os
# import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from lxml import etree
import requests						# 用于获取网页内容的模块
from bs4 import BeautifulSoup		# 用于解析网页源代码的模块
# 设置一个自增参数，表示歌曲的数目
class DOWN_LOAD:
	def __init__(self):
		self.header = {  # 伪造浏览器头部，不然获取不到网易云音乐的页面源代码。
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
				'Referer': 'http://93.174.95.27',
			}
		os.makedirs('./music', exist_ok=True) #创建文件夹
		self.num = 1

	def Down_load_music(self,songs):
		#<a href="/song?id=1814636483">艺术家</a>
		strr = str(songs)
		song_id =strr.split("id=")[1].split('">')[0]
		# song_id = s['href'][9:]  # 只截取歌曲链接中的 ID 部分，因为网页中链接的形式为 “/song?id=496870798”，从 = 号之后的就是歌曲的 ID 号。
		song_name = strr.split('">')[1].split('<')[0]  # 获取 a 标签的文本内容，即歌曲的名称。
		song_down_link = "http://music.163.com/song/media/outer/url?id=" + song_id + ".mp3"  # 根据歌曲的 ID 号拼接出下载的链接。歌曲直链获取的方法参考文前的注释部分。
		print("第 " + str(self.num) + " 首歌曲")
		print("正在下载...")

		response = requests.get(song_down_link, headers=self.header).content  # 亲测必须要加 headers 信息，不然获取不了。
		f = open('./music/' + song_name + ".mp3", 'wb')  # 以二进制的形式写入文件中
		f.write(response)
		f.close()
		print(f"{song_name}下载完成.\n\r")
		self.num = self.num + 1


	def down_load_hot_music(self):
		"""
		下载热门音乐
		:return:
		"""
		link = "http://music.163.com/discover/toplist?id=3778678"  # 这是网易云音乐热歌榜的链接（其实是嵌套在网页里面含有歌曲数据的页面框架的真实链接）
		# link = "https://music.163.com/#/discover/toplist?id=5453912201"	# 个人歌曲版
		r = requests.get(link, headers=self.header)  # 通过 requests 模块的 get 方法获取网页数据
		html = r.content  # 获取网页内容
		soup = BeautifulSoup(html, "html.parser")  # 通过 BeautifulSoup 模块解析网页，具体请参考官方文档。
		songs = soup.find("ul", class_="f-hide").select(
			"a")  # , limit=200 	# 通过分析网页源代码发现排行榜中的歌曲信息全部放在类名称为 f-hide 的 ul 中，于是根据特殊的类名称查找相应 ul，然后找到里面的全部 a 标签，限制数量为10，即排行榜的前 10 首歌。

		pool = ThreadPoolExecutor(max_workers=20)
		for result in pool.map(self.Down_load_music, songs):
			...

	def Down_load_one_music(self,song_name,song_id):
		"""
		下载指定的音乐
		:param song_name:
		:param song_id:
		:return:
		"""
		# song_name = '不抛弃不放弃'
		# song_id='1501780751'
		song_down_link = "http://music.163.com/song/media/outer/url?id=" + song_id + ".mp3"  # 根据歌曲的 ID 号拼接出下载的链接。歌曲直链获取的方法参考文前的注释部分。
		print("第 " + str(self.num) + " 首歌曲")
		print("正在下载...")
		response = requests.get(song_down_link, headers=self.header).content  # 亲测必须要加 headers 信息，不然获取不了。
		f = open('./music/' + str(song_name) + ".mp3", 'wb')  # 以二进制的形式写入文件中
		f.write(response)
		f.close()
		print(f"{song_name}下载完成.\n\r")
		self.num = self.num + 1

if __name__ == "__main__":
	DOWN_LOAD_ = DOWN_LOAD()
	song_name = ''
	song_id = ''
	model = input("请输入下载模式(0为下载网易云热门音乐；1为下载网易云单条音乐！):")
	if int(model) == 0:
		DOWN_LOAD_.down_load_hot_music()
	else:
		# song_name = '不抛弃不放弃'
		# song_id='1501780751'
		song_name = input('请输入歌曲名称:')
		song_id = input('请输入歌曲id:')
		print("song_name:", song_name)
		print("song_id:", song_id)
		DOWN_LOAD_.Down_load_one_music(song_name, song_id)