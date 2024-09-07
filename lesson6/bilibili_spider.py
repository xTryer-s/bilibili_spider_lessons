import requests
import re
import json
import os
import subprocess
from pprint import pprint

tar_url = input('请输入您想下载的b站视频url:\n')

bv_id = re.findall(r'video/(BV.*?)/',tar_url)[0]

headers_ = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'referer':'https://www.bilibili.com/'
}
# 向视频页发送请求
tar_html_response = requests.get(url=tar_url,headers=headers_)


# print(tar_html_response.text)

# with open('output_html.txt','w',encoding='utf-8') as tmp_output:
#     tmp_output.write(tar_html_response.text)

# 过滤得到我们所需要的视频信息
play_info = re.findall(r'<script>window.__playinfo__=(.*?)</script>',tar_html_response.text)[0]
play_info_json = json.loads(play_info)

# 获取audio video 的存储url
audio_url = play_info_json['data']['dash']['audio'][0]['base_url']
video_url = ''

videos_save_info = play_info_json['data']['dash']['video']
avc_flag = False

for tmp_video_info in videos_save_info:
    tmp_video_info_codecs =tmp_video_info['codecs']
    tmp_video_info_url = tmp_video_info['base_url']
    if 'avc' in tmp_video_info_codecs:
        video_url = tmp_video_info_url
        avc_flag = True
        break





# print(audio_url)

# print(video_url)

# 向audio video 数据发送请求 下载数据
audio_content = requests.get(url=audio_url,headers=headers_).content
video_content = requests.get(url=video_url,headers=headers_).content

father_dir = 'Bilibili_videos'
child_dir = father_dir+'\\'+bv_id

if not os.path.exists(father_dir):
    os.makedirs(father_dir)

if not os.path.exists(child_dir):
    os.makedirs(child_dir)

audio_output_path = child_dir+'\\'+f'{bv_id}_audio.mp3'
video_output_path = child_dir+'\\'+f'{bv_id}_video.mp4'

# 以二进制格式把视频 音频 数据保存在本地
with open(audio_output_path,'wb') as audio_write:
    audio_write.write(audio_content)

with open(video_output_path,'wb') as video_write:
    video_write.write(video_content)

if avc_flag==False:
    print('无法音频与视频的合并')
    exit()
    
merge_path = child_dir+'\\'+f'{bv_id}.mp4'
# ffmpeg 对音频文件和视频文件进行合并
merge_cmd = f'ffmpeg -y -i {audio_output_path} -i {video_output_path} -c:v copy -c:a aac -strict experimental {merge_path}'
subprocess.run(merge_cmd)