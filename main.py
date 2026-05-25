import yt_dlp
import os
import subprocess

def download_video(search_query, output_dir=r"C:\"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ydl_opts = {
        'format': 'bestvideo[height<=144]+bestaudio/best[height<=144]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),

        'default_search': 'ytsearch',

        'quiet': True
    }

    print(f'Начинаем загрузку для: {search_query}')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    print(r"Готово! Видео скачано в D:\6. pics\vidiki")


if __name__ == '__main__':
    path = r"D:\6. pics\vidiki"
    while True:
        user_input = input("Вставьте URL или название видео (exit для выхода, open чтобы открыть): ")
        
        if user_input.lower() == "exit":
            break
        if user_input.lower() == "open":
            subprocess.Popen(f'explorer "{path}')
            continue
            
        download_video(user_input)