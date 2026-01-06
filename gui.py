import tkinter as tk
import script_by_post_request as sbpr
import json
from pathlib import Path

root = tk.Tk()

main_window = tk.Frame(root, height=400, width=400)
main_window.size
main_window.pack()
side_frame1= tk.Frame(main_window)
side_frame2= tk.Frame(main_window)
side_frame1.pack(side='left')
side_frame2.pack(side='left')
frame1 = tk.Frame(side_frame1)
frame1.pack()
frame2 = tk.Frame(side_frame1)
frame2.pack()
min_level_text = tk.StringVar()
max_level_text = tk.StringVar()
min_level_text.set('')
max_level_text.set('')
min_level_entry = tk.Entry(frame1, textvariable=min_level_text)
max_level_entry = tk.Entry(frame1, textvariable=max_level_text)
min_level_label = tk.Label(frame1, text='min level')
max_level_label = tk.Label(frame1, text='max level')
min_level_entry.grid(row=1, column=2)
max_level_entry.grid(row=2, column=2)
min_level_label.grid(row=1, column=1)
max_level_label.grid(row=2, column=1)
frame3 = tk.Frame(side_frame2)
frame3.pack()
message_box = tk.Text(frame3, state=tk.DISABLED, height=20)
message_box.pack()


print(min_level_entry.get())

def print_min_text(entry):
    text = entry.get()
    print(text)

def level_from_gui(min_entry, max_entry):
    min_level = min_entry.get()
    max_level = max_entry.get()
    return min_level, max_level

def request_from_gui(min_entry, max_entry):
    min_level, max_level = level_from_gui(min_entry, max_entry)
    request = sbpr.change_creature_level(sbpr.json_as_text, min_level, max_level)
    sbpr.make_request(request)

def open_json_responce():
    file_path = Path(__file__).parent/'full_api_response.json'
    data = None
    if file_path.exists():
        print("Файл найден! Открываю...")
        log_message(message_box, "Файл найден! Открываю...")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        print("Файл не найден. Проверьте название и путь.")
        log_message(message_box, "Файл не найден. Проверьте название и путь.")

    if data == None:
        print('data is empty')
        log_message(message_box, 'data is empty')
        return data 
    return data
    


def random_url_from_json_file():
    file_path = Path(__file__).parent/'full_api_response.json'
    print(file_path)
    data = None
    if file_path.exists():
        print("Файл найден! Открываю...")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        print("Файл не найден. Проверьте название и путь.")

    if data == None:
        return print('data is empty')
    
    sbpr.get_random_url(data)

def log_len_of_result():
    data = open_json_responce()
    if data == None:
        print('data is empty')
        log_message(message_box, 'data is empty')
        return 
    print(len(data['hits']['hits']))
    log_message(message_box, len(data['hits']['hits']))

def log_message(message_box:tk.Text, text:str):
    message_box.configure(state=tk.NORMAL)
    message_box.insert('end', f'{text}\n')
    message_box.configure(state=tk.DISABLED)


search_btn = tk.Button(frame2, text='search', command=(lambda : request_from_gui(min_level_entry, max_level_entry)))
rng_btn = tk.Button(frame2, text='random', command=(lambda : random_url_from_json_file()))
search_btn.pack()
rng_btn.pack()
print_len_result_btn = tk.Button(frame2, text='print len result', command=(lambda: log_len_of_result()))
print_len_result_btn.pack()

root.mainloop()

