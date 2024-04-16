import tkinter as tk
from tkinter import filedialog
import pygame
import os
import random
import threading

# 初始化pygame
pygame.init()


# 音频文件路径
# audio_folder = filedialog.askdirectory()


def tooch_audio() -> str:
    _audio_folder = filedialog.askdirectory()
    return _audio_folder
    # path_label.config(text=folder_path)


# 创建一个窗口
root = tk.Tk()
root.title("语音播放器")
root.geometry("300x100")

# 按钮被锁定标志
button_locked = False


def play_random_voice():
    global button_locked
    if button_locked or not audio_files:
        return
    button_locked = True

    # 在单独的线程中播放音频
    threading.Thread(target=_play_voice).start()


def _play_voice():
    file_path = random.choice(audio_files)
    # 播放文件
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # 使用after方法定期检查音乐是否播放完毕
    def check_music_end():
        if not pygame.mixer.music.get_busy():
            global button_locked
            button_locked = False
        else:
            root.after(100, check_music_end)  # 每隔100毫秒检查一次

    check_music_end()


audio_folder = tooch_audio()
select_button = tk.Button(root, text="选择文件夹", command=audio_folder)
select_button.pack()

# 加载所有音频文件
audio_files = [os.path.join(audio_folder, file) for file in os.listdir(audio_folder)
               if file.endswith(('.wav', '.mp3', 'flac'))]

# 播放按钮
play_button = tk.Button(root, text="播放随机语音", command=play_random_voice)
play_button.pack()

# 主事件循环
root.mainloop()

# 退出pygame
pygame.quit()
