import tkinter as tk
import script_by_post_request as sbpr
import json
from pathlib import Path

root = tk.Tk()

main_window = tk.Frame(root, height=400, width=400)
main_window.size
main_window.pack()
frame1 = tk.Frame(main_window)
frame1.pack()
frame2 = tk.Frame(main_window)
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

def random_url_from_json_file():
    print(Path(__file__).parent)
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



search_btn = tk.Button(frame2, text='search', command=(lambda : request_from_gui(min_level_entry, max_level_entry)))
rng_btn = tk.Button(frame2, text='random', command=(lambda : random_url_from_json_file()))
search_btn.pack()
rng_btn.pack()
print_min_btn = tk.Button(frame2, text='print_min', command=(lambda x = min_level_entry: print_min_text(x)))
print_min_btn.pack()

root.mainloop()

