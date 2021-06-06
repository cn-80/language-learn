import inspect
import os

import tkinter as tk
from tkinter import ttk

from google.cloud import translate

class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project = os.environ.get('LANGUAGE_LEARN_GOOGLE_PROJECT')

    def translate(self, lines, src_lang, dest_langs):
        results = {}
        for dest_lang in dest_langs:
            request = {
                'parent': self.project,
                'mime_type': 'text/plain',
                'source_language_code': src_lang,
                'target_language_code': dest_lang,
                'contents': lines,
            }
            response = self.client.translate_text(request=request)
            results[dest_lang] = [
                translation.translated_text for translation in response.translations
            ]
        return results


class Application(tk.Frame):
    LANGUAGES = (
        ('English', 'en'),
        ('French', 'fr'),
    )

    def __init__(self, master=None):
        super().__init__(master)
        self.translation_client = TranslationClient()
        print(self.translation_client.translate(['Hello and welcome to Language Learn', 'This is the second sentence', 'Good day and good afternoon'], 'en', ['fr', 'zh']))
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
