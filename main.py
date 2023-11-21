# YouTube Downloader
#
# 1. Distribution
# This source code is distributed through GitHub.
# 当ソースコードは GitHub を通して配布されています。
# Link: https://github.com/aonekoaoi/YTDownloader
#
# 2. Description
# See README.md on GitHub.
# GitHub の README.md を参照してください。
# Link: https://github.com/aonekoaoi/YTDownloader/blob/main/README.md
#
# 3. Development Environment
# - Microsoft Windows 10 Pro version 22H2 (OS build 19045.3208) 64-bit
# - Visual Studio Code version 1.83.0 64-bit
# - Python 3.11.3 64-bit
#
# 4. License
# Copyright (c) 2023 aonekoaoi
# Licensed under the MIT license.
# MIT ライセンスに基づく配布。
# Link(en): https://github.com/aonekoaoi/YTDownloader/blob/main/LICENSE.txt
# Link(ja): https://github.com/aonekoaoi/YTDownloader/blob/main/LICENSE_ja.txt

import os
import sys

import ffmpeg
import pytube

print("\n著作権は著作者に帰属します。そのためデータの取り扱いには注意してください。\n\nYouTube のリンクをコピーしてコンソールにペースト後、Enter で確定してください。")
link = str(input(">>"))
stream = pytube.YouTube(link)

# output フォルダをデスクトップに作成
desktop_path = os.path.expanduser("~/Desktop")
folder_path = os.path.join(desktop_path, "output")
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


def audio_fun(bps):
    """
    音声ビットレートの情報取得
    bps: 音声ビットレートを入力
    """
    audio = stream.streams.filter(abr=bps).first()
    return audio


# 音声ビットレートの情報取得
audio = audio_fun("256kbps")
if audio is None:
    audio = audio_fun("160kbps")
elif audio is None:
    audio = audio_fun("128kbps")
elif audio is None:
    audio = audio_fun("70kbps")
elif audio is None:
    audio = audio_fun("50kbps")
elif audio is None:
    # 以上の分岐処理で音声ビットレートが存在しない場合の処理
    audio = stream.streams.get_audio_only()
else:
    # すべての分岐処理で音声ビットレートが存在しない場合は強制終了
    print("音声ビットレートの情報取得ができません。\nお手数ですが YouTube のリンクか確認した上で、再度プログラミングを実行してください。\n")
    sys.exit()


def video_fun(p):
    """
    解像度の情報取得
    p: 解像度を入力
    """
    video = stream.streams.filter(res=p).first()
    return video


# 解像度の情報取得
video = video_fun("1080p")
if video is None:
    video = video_fun("720p")
elif video is None:
    video = video_fun("480p")
elif video is None:
    video = video_fun("360p")
elif video is None:
    video = video_fun("240p")
else:
    # すべての分岐処理で解像度が存在しない場合は強制終了
    print("解像度の情報取得ができません。\nお手数ですが YouTube のリンクか確認した上で、再度プログラミングを実行してください。\n")
    sys.exit()

# mp4a および mp4 形式をダウンロード
audio.download(folder_path, "audio.mp4a")
video.download(folder_path, "video.mp4")

audio_path = os.path.join(folder_path, "audio.mp4a")
audio_input = ffmpeg.input(audio_path)
audio_output = os.path.join(folder_path, "audio.mp3")

ffmpeg.output(
    audio_input,
    audio_output,
    format="mp3",  # mp4a -> mp3 に変更
    **{"b:a": "256k"}  # 256kbps に変更
).run(
    capture_stderr=True
)

# mp4a 形式の音声データを削除
os.remove(audio_path)

video_path = os.path.join(folder_path, "video.mp4")
video_input = ffmpeg.input(video_path)
video_output = os.path.join(folder_path, "video2.mp4")

ffmpeg.output(
    video_input,
    video_output,
    format="mp4",
    **{"b:v": "12000k"}  # 12000kbps に変更
).run(
    capture_stderr=True
)

# mp4 形式の動画データを削除（video.mp4）
os.remove(video_path)

# 音声データおよび動画データの合成
audio_path = os.path.join(folder_path, "audio.mp3")
audio_input = ffmpeg.input(audio_path)
video_path = os.path.join(folder_path, "video2.mp4")
video_input = ffmpeg.input(video_path)
complete = os.path.join(folder_path, f"{stream.title}.mp4")

ffmpeg.output(
    audio_input,
    video_input,
    complete,
    format="mp4",
    acodec="copy",
    vcodec="copy"
).run(
    capture_stderr=True
)

# mp3 および mp4 形式のデータを削除（audio.mp3 および video2.mp4）
os.remove(audio_path)
os.remove(video_path)

print("\nデスクトップの output フォルダ内に動画データを格納しました。\n")
