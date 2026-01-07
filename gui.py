import tkinter as tk
import script_by_post_request as sbpr
import json
from pathlib import Path


class MainWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.main_window = tk.Frame(self.root, height=400, width=400)
        self.main_window.size
        self.main_window.pack()
        self.side_frame1= tk.Frame(self.main_window)
        self.side_frame2= tk.Frame(self.main_window)
        self.side_frame1.pack(side='left')
        self.side_frame2.pack(side='left')
        self.frame1 = tk.Frame(self.side_frame1)
        self.frame1.pack()
        self.frame2 = tk.Frame(self.side_frame1)
        self.frame2.pack()
        self.min_level_text = tk.StringVar()
        self.max_level_text = tk.StringVar()
        self.min_level_text.set('')
        self.max_level_text.set('')
        self.min_level_entry = tk.Entry(self.frame1, textvariable=self.min_level_text)
        self.max_level_entry = tk.Entry(self.frame1, textvariable=self.max_level_text)
        self.min_level_label = tk.Label(self.frame1, text='min level')
        self.max_level_label = tk.Label(self.frame1, text='max level')
        self.min_level_entry.grid(row=1, column=2)
        self.max_level_entry.grid(row=2, column=2)
        self.min_level_label.grid(row=1, column=1)
        self.max_level_label.grid(row=2, column=1)
        self.frame3 = tk.Frame(self.side_frame2)
        self.frame3.pack()
        self.message_box = tk.Text(self.frame3, state=tk.DISABLED, height=20)
        self.message_box.pack()
        self.search_btn = tk.Button(self.frame2, text='search', command=(lambda : self.request_from_gui(self.min_level_entry, self.max_level_entry)))
        self.rng_btn = tk.Button(self.frame2, text='random', command=(lambda : self.random_url_from_json_file()))
        self.search_btn.pack()
        self.rng_btn.pack()
        self.print_len_result_btn = tk.Button(self.frame2, text='print len result', command=(lambda: self.log_len_of_result()))
        self.print_len_result_btn.pack()
        self.new_window_btn = tk.Button(self.frame2, text='new window', command=self.create_new_window)
        self.new_window_btn.pack()
        self.open_exel_btn = tk.Button(self.frame2, text='open exel', command=sbpr.open_exel_file)
        self.open_exel_btn.pack()

    def print_min_text(self, entry:tk.Entry):
        text = entry.get()
        print(text)

    def level_from_gui(self, min_entry:tk.Entry, max_entry:tk.Entry):
        min_level = min_entry.get()
        max_level = max_entry.get()
        return min_level, max_level

    def request_from_gui(self, min_entry:tk.Entry, max_entry:tk.Entry):
        min_level, max_level = self.level_from_gui(min_entry, max_entry)
        request = sbpr.change_creature_level(sbpr.json_as_text, min_level, max_level)
        data = sbpr.make_request(request)
        df = sbpr.create_df_from_request(data)

    def open_json_responce(self):
        file_path = Path(__file__).parent/'full_api_response.json'
        data = None
        if file_path.exists():
            print("Файл найден! Открываю...")
            self.log_message(self.message_box, "Файл найден! Открываю...")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            print("Файл не найден. Проверьте название и путь.")
            self.log_message(self.message_box, "Файл не найден. Проверьте название и путь.")

        if data == None:
            print('data is empty')
            self.log_message(self.message_box, 'data is empty')
            return data 
        return data
    


    def random_url_from_json_file(self):
        file_path = Path(__file__).parent/'full_api_response.json'
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

    def log_len_of_result(self):
        data = self.open_json_responce()
        if data == None:
            print('data is empty')
            self.log_message(self.message_box, 'data is empty')
            return 
        print(len(data['hits']['hits']))
        self.log_message(self.message_box, len(data['hits']['hits']))

    def log_message(self, message_box:tk.Text, text:str):
        message_box.configure(state=tk.NORMAL)
        message_box.insert('end', f'{text}\n')
        message_box.configure(state=tk.DISABLED)

    def create_new_window(self):
        new_window = tk.Tk()
        new_window.mainloop()


main_window = MainWindow()
main_window.root.mainloop()

