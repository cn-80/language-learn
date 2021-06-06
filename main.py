import tkinter as tk
from tkinter import ttk

class Application(tk.Frame):
    LANGUAGES = (
        ('English', 'en'),
        ('French', 'fr'),
    )

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.src_lang_heading = ttk.Label(self, text='Source Language:')
        self.src_lang_heading.pack(side='top')
        self.src_lang_options = []
        for (label, locale) in self.LANGUAGES:
            lang_opt = ttk.Checkbutton(self, text=label)
            lang_opt.pack(side='top')
            self.src_lang_options.append(lang_opt)

        self.dest_lang_heading = ttk.Label(self, text='Languages to Learn:')
        self.dest_lang_heading.pack(side='top')
        self.dest_lang_options = []
        for (label, locale) in self.LANGUAGES:
            lang_opt = ttk.Checkbutton(self, text=label)
            lang_opt.pack(side='top')
            self.src_lang_options.append(lang_opt)

        self.quit = ttk.Button(
            self,
            text='QUIT',
            command=self.master.destroy
        )
        self.quit.pack(side='bottom')

    def show_select_language_dialog(self):
        pass

root = tk.Tk()
app = Application(master=root)
app.mainloop()
