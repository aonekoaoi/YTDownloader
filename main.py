# YouTube Downloader
#
# Distribution
# The source code is distributed through GitHub.
# 当ソースコードはGitHubを通じて配布されている。
# GitHub: https://github.com/aonekoaoi/YTDownloader
#
# Description
# See README.md at GitHub.
# GitHubのREADME.mdを参照してください。
# GitHub: https://github.com/aonekoaoi/YTDownloader/blob/main/README.md
#
# Development Environment
# Microsoft Windows 10 Pro version 22H2 (OS build 19045.3208) 64-bit
# Visual Studio Code version 1.83.0 64-bit
# Python 3.11.3 64-bit
#
# Contact Us
# X (Twitter): https://twitter.com/aonekoaoi
#
# License
# Copyright (c) 2023 aonekoaoi
# Licensed under the MIT license.
# MiTライセンスに基づくライセンス。
# en: https://github.com/aonekoaoi/YTDownloader/blob/main/LICENSE.txt
# ja: https://github.com/aonekoaoi/YTDownloader/blob/main/LICENSE_ja.txt

import os
import sys
import ffmpeg
import pytube

print("\n著作権は著作者に帰属します。そのためデータの取り扱いには注意してください。\n\nYouTubeのURLをコピーしコンソールにペースト後、Enterで確定してください。")
url = str(input(">>"))
stream = pytube.YouTube(url)

# outputフォルダーをデスクトップに作成
desktop_path = os.path.expanduser("~/Desktop")
folder_path = os.path.join(desktop_path, "output")
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("\noutputフォルダーをデスクトップに作成しました。")
else:
    print("\noutputフォルダーがデスクトップに存在しています。そのためoutputフォルダーをデスクトップに作成できません。")


def audio_fun(bps):
    """
    音声ビットレートの情報取得動作
    bps: 音声ビットレートを代入
    """
    print(bps, "の音声ビットレートの情報取得中")
    audio = stream.streams.filter(abr=bps).first()
    return audio


print("\n音声ビットレートの情報取得開始")
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
    audio = stream.streams.get_audio_only()  # 上記の処理で音声ビットレートが存在しない場合の処理
else:
    print("音声ビットレートの情報取得ができません。\nお手数ですがYouTubeのURLかを確認した上で再度、プログラムを開始してください。\n")
    sys.exit()  # プログラムの強制終了
print("音声ビットレートの情報取得終了")


def video_fun(p):
    """
    解像度の情報取得動作
    p: 解像度を代入
    """
    print(p, "の解像度の情報取得中")
    video = stream.streams.filter(res=p).first()
    return video


print("\n解像度の情報取得開始")
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
    print("解像度の情報取得ができません。\nお手数ですがYouTubeのURLかを確認した上で再度、プログラムを開始してください。\n")
    sys.exit()  # プログラムの強制終了
print("解像度の情報取得終了")

print("\nダウンロードの開始")
audio.download(folder_path, "audio.mp4a")
video.download(folder_path, "video.mp4")
print("ダウンロードの終了")

print("\nフォーマットの変更開始")
audio_path = os.path.join(folder_path, "audio.mp4a")
audio_input = ffmpeg.input(audio_path)
audio_output = os.path.join(folder_path, "audio.mp3")

ffmpeg.output(
    # .mp3と256kbpsの変更
    audio_input,
    audio_output,
    format="mp3",
    **{"b:a": "256k"}
).run(
    capture_stderr=True
)
os.remove(audio_path)  # .mp4a形式のファイルを削除

video_path = os.path.join(folder_path, "video.mp4")
video_input = ffmpeg.input(video_path)
video_output = os.path.join(folder_path, "video2.mp4")

ffmpeg.output(
    # 12000kbpsの変更
    video_input,
    video_output,
    format="mp4",
    **{"b:v": "12000k"}
).run(
    capture_stderr=True
)
os.remove(video_path)  # .mp4形式のファイルを削除（video.mp4）
print("フォーマットの変更終了")

print("\n音声と動画の合成開始")
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
os.remove(audio_path)  # .mp3形式のファイルを削除
os.remove(video_path)  # .mp4形式のファイルを削除（video2.mp4）
print("音声と動画の合成終了")

print("\nデスクトップのoutputフォルダー内に「", f"{stream.title}.mp4 」が格納されています。\n")
