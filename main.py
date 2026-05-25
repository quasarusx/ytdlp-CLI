import yt_dlp
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import json


root = tk.Tk()
root.withdraw()

CONFIG_FILE = "config.json"
DEFAULT_VIDEO_PATH = r"C:\ytdlp-cli\downloads\video"
DEFAULT_AUDIO_PATH = r"C:\ytdlp-cli\downloads\audio"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения config.json, создаем новый...")

    default_config = {
        "video_path": DEFAULT_VIDEO_PATH,
        "audio_path": DEFAULT_AUDIO_PATH
    }
    save_config(default_config)
    return default_config


def save_config(config_data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)
    

config = load_config()



def download_video(search_query):

    output_dir = config.get("video_path", DEFAULT_VIDEO_PATH)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'default_search': 'ytsearch',
        'quiet': True
    }

    print(f'\nDownloading: {search_query}')
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        print(f"Done! Saved to: {output_dir}")
    except Exception as e:
        print(f"Error: {e}")



def download_audio(search_query):

    output_dir = config.get("audio_path", DEFAULT_AUDIO_PATH)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio[ext=webm]/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'default_search': 'ytsearch',
        'quiet': True,
    }

    print(f"\nDownloading: {search_query}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        print(f"Done! Saved to: {output_dir}")
    except Exception as e:
        print("Error: {e}")

if __name__ == '__main__':
    while True:
        try:
            user_input = int(input("""
            What do you want to download?
            Что вы хотите скачать?
            
            1. Video (Видео)
            2. Audio (Аудио)
            
            3. Open the downloads folder (Открыть папку загрузок)
                                
            4. Edit download path (Изменить путь скачивания)
            5. Check download path (Проверить путь скачивания)
                                   
            0. Exit
                                   
            >>> """))

            user_input = int(user_input)
            
            if user_input == 1:
                user_video_input = input("""
                Enter the URL or title of the video
                Введите URL адрес или название видео
                                        
                >>> """)
                if user_video_input:
                    download_video(user_video_input)

            elif user_input == 2:
                user_audio_input = input("""
                Enter the URL or title of the audio
                Введите URL адрес или название трека
                                        
                >>> """)
                if user_audio_input:
                    download_audio(user_audio_input)

            elif user_input == 0:
                print("Exit...")
                break
            
            elif user_input == 3:
                user_open_path = int(input("""
                Folder / Папка:
                1. Video (Видео)
                2. Audio (Аудио)    
                >>> """))

                if user_open_path == 1:
                    os.startfile(config["video_path"])
                elif user_open_path == 2:
                    os.startfile(config["audio_path"])

            elif user_input == 4:
                user_edit_path = int(input("""
                Which path? / Какой путь изменить?
                1. Video (Видео)
                2. Audio (Аудио)      
                >>> """))

                if user_edit_path == 1:
                    print("Select new video folder...")
                    new_path = filedialog.askdirectory()
                    if new_path:
                        config["video_path"] = os.path.normpath(new_path)
                        save_config(config)
                        print(f"Saved new path: {config['video_path']}")
                    else:
                        print("Canceled.")
                
                elif user_edit_path == 2:
                    print("Select new audio folder")
                    new_path = filedialog.askdirectory()
                    if new_path:
                        config["audio_path"] = os.path.normpath(new_path)
                        save_config(config)
                        print(f"Saved new path: {config['audio_path']}")
                    else:
                        print("Canceled.")
                    

            elif user_input == 5:
                print(f"\nVideo: {config['video_path']}\nAudio: {config['audio_path']}\n")
                input("Press Enter to continue...")

        except ValueError:
            print("Некорректное число...")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

