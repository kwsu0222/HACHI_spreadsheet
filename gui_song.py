import tkinter as tk
from tkinter import scrolledtext
from urllib.parse import urlparse, parse_qs
import re

def extract_id(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == "youtu.be":
        return parsed_url.path.lstrip('/')
    if parsed_url.netloc == "www.youtube.com":
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]  
    return None

def parse_time(time_str):
    time_parts = list(map(int, time_str.split(':')))
    if len(time_parts) == 2:  # 如果時間格式為 '分鐘:秒'
        return time_parts[0]*60 + time_parts[1]
    elif len(time_parts) == 3:  # 如果時間格式為 '小時:分鐘:秒'
        return time_parts[0]*3600 + time_parts[1]*60 + time_parts[2]

def append_time_to_url(song_list, url, include_song_name, output_text):
    time_pattern = r'([0-9]{1,2}:[0-9]{2}:[0-9]{2}|[0-9]{1,2}:[0-9]{2})'
    lines = song_list.split('\n')
    
    # 先輸出歌曲清單
    if include_song_name == "2":
        for line in lines:
            time_list = re.findall(time_pattern, line)
            if time_list:
                song_name = line.split(time_list[-1])[1].strip()
                song_name = re.split(r'[-/]', song_name)[0].strip()
                output_text.insert(tk.END, song_name + "\n")
    
    output_text.insert(tk.END, "\n網址清單:\n")
    # 再輸出網址
    for line in lines:
        time_list = re.findall(time_pattern, line)
        if time_list:
            seconds = parse_time(time_list[-1])  # 只處理最後一個時間點
            output_text.insert(tk.END, f'{url}{seconds}\n')

def run_program():
    choice = var.get()
    url = url_entry.get()
    song_list = song_list_text.get("1.0", tk.END)
    url = extract_id(url)
    url = f"https://youtu.be/{url}?t="
    output_text.delete("1.0", tk.END)
    append_time_to_url(song_list, url, choice, output_text)

root = tk.Tk()
root.title("Song List to URL Converter")

tk.Label(root, text="Enter URL:").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1)

tk.Label(root, text="Enter song list:").grid(row=1, column=0, sticky="nw")
song_list_text = scrolledtext.ScrolledText(root, width=50, height=10)
song_list_text.grid(row=1, column=1)

var = tk.StringVar(value="1")
tk.Radiobutton(root, text="Output URL only", variable=var, value="1").grid(row=2, column=0, sticky="w")
tk.Radiobutton(root, text="Output song name and URL", variable=var, value="2").grid(row=2, column=1, sticky="w")

tk.Button(root, text="Convert", command=run_program).grid(row=3, column=0, columnspan=2)

tk.Label(root, text="Output:").grid(row=4, column=0, sticky="nw")
output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.grid(row=4, column=1)

root.mainloop()
