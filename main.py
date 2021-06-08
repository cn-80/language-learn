from collections import defaultdict
import inspect
import os
import re

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
    # Supported languages: https://cloud.google.com/translate/docs/languages
    LANGUAGES = (
        ('English', 'en'),
        ('French', 'fr'),
        # ('Chinese', 'zh'),
        # ('Hindi', 'hi'),
        # ('German', 'de'),
        ('Italian', 'it'),
        ('Portuguese', 'pt'),
    )

    def __init__(self, master=None):
        super().__init__(master)
        self.translation_client = TranslationClient()
        self.src_lang = 'en'
        self.dest_langs = [locale for (label, locale) in self.LANGUAGES if locale != self.src_lang]
        self.src_lines = []
        self.translated_lines = []
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.language_select_frame = ttk.Frame(self)
        self.src_lang_heading = ttk.Label(self.language_select_frame, text='Source Language:')
        self.src_lang_heading.pack(side='top')
        self.src_lang_options = []
        for (label, locale) in self.LANGUAGES:
            lang_opt = ttk.Checkbutton(self.language_select_frame, text=label)
            lang_opt.pack(side='top')
            self.src_lang_options.append(lang_opt)

        self.dest_lang_heading = ttk.Label(self.language_select_frame, text='Languages to Learn:')
        self.dest_lang_heading.pack(side='top')
        self.dest_lang_options = []
        for (label, locale) in self.LANGUAGES:
            lang_opt = ttk.Checkbutton(self.language_select_frame, text=label)
            lang_opt.pack(side='top')
            self.src_lang_options.append(lang_opt)
        self.language_select_frame.pack(side='left')

        self.lines_frame = ttk.Frame(self)
        self.src_text = tk.Text(self.lines_frame)
        self.src_text.insert('1.0', 'Hello, how are you? Would you like to learn a new language today? Press the "translate" button below to see translations for each sentence in different languages.')
        self.src_text.pack(side='top')
        self.translated_lines = []
        self.translated_lines_frame = ttk.Frame(self.lines_frame)
        self.translated_lines_frame.pack(side='bottom')
        self.translate_button = ttk.Button(
            self.lines_frame,
            text='Translate',
            command=self.translate
        )
        self.translate_button.pack(side='bottom')
        self.lines_frame.pack(side='right')

        self.quit_button = ttk.Button(
            self,
            text='Quit',
            command=self.master.destroy
        )
        self.quit_button.pack(side='bottom')

    def translate(self):
        self.src_lines = [
            text for text in
            [text.strip() for text in re.split(
                '[\.\?\!]',
                self.src_text.get('1.0', 'end-1c')
            )] if len(text) > 0
        ]
        for widget in self.translated_lines:
            widget.pack_forget()
            widget.destroy()
        response = self.translation_client.translate(
            self.src_lines,
            self.src_lang,
            self.dest_langs
        )
        for index in range(len(self.src_lines)):
            # Source Line
            widget = ttk.Label(
                self.translated_lines_frame,
                text='<<{}>> {}'.format(self.src_lang, self.src_lines[index])
            )
            self.translated_lines.append(widget)
            widget.pack(side='top')
            # Translated Lines
            for lang in self.dest_langs:
                widget = ttk.Label(
                    self.translated_lines_frame,
                    text=f'<<{lang}>> {response[lang][index]}'
                )
                self.translated_lines.append(widget)
                widget.pack(side='top')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
