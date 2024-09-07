import requests
import re
import json
import os
from pprint import pprint
import subprocess

headers_ = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'referer':'https://www.bilibili.com/'

}
tar_url = input('请输入目标B站视频url:\n')

bv_id = re.findall(r'video/(BV.*)/',tar_url)
if len(bv_id)==0:
    bv_id=re.findall(r'video/(BV.*)',tar_url)[0]
else:
    bv_id = bv_id[0]
# print(bv_id)
tar_html_response = requests.get(url=tar_url,headers=headers_)

tar_html_text = tar_html_response.text
video_info = re.findall(r'</style><script>window.__playinfo__=(.*?)</script>',tar_html_text)[0]
# with open('tmp_bilibili.txt','w',encoding='utf-8') as tmp_output:
#     tmp_output.write(video_info)

video_info_json = json.loads(video_info)

# pprint(video_info_json)

audio_url = video_info_json['data']['dash']['audio'][0]['base_url']
video_url = video_info_json['data']['dash']['video'][0]['base_url']

# print(audio_url)

# print(video_url)
father_file_dir = 'new_Your_bilibili_videos_DownLoads'
child_file_dir = father_file_dir+'\\'+bv_id

if not os.path.exists(father_file_dir):
    os.makedirs(father_file_dir)

if not os.path.exists(child_file_dir):
    os.makedirs(child_file_dir)


audio_content = requests.get(url=audio_url,headers=headers_).content
video_content = requests.get(url=video_url,headers=headers_).content

output_audio_path = child_file_dir+'\\'+bv_id+'_audio.mp3'
output_video_path = child_file_dir+'\\'+bv_id+'_video.mp4'

merge_path = child_file_dir+'\\'+bv_id+'.mp4'


with open(f'{output_audio_path}','wb') as audio_output:
    audio_output.write(audio_content)
with open(f'{output_video_path}','wb') as video_output:
    video_output.write(video_content)

merge_cmd = f"ffmpeg -y -i {output_audio_path} -i {output_video_path} -c:v copy -c:a aac -strict experimental {merge_path}.mp4"
subprocess.run(merge_cmd)