"""
gui_app_adv.py — extended GUI with drag‑and‑drop and batch list display.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from typing import List

from ocr import extract_label


class OCRGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Bolashaq OCR Advanced')
        self.geometry('600x400')
        self._init_widgets()


    def _init_widgets(self):

        frm = tk.Frame(self)
        frm.pack(fill='both', expand=True, padx=10, pady=10)

        btn = tk.Button(frm, text='Add Images', command=self._add_images)
        btn.pack(anchor='w')

        self.tree = ttk.Treeview(frm, columns=('label',), show='headings')
        self.tree.heading('label', text='Detected Label')
        self.tree.pack(fill='both', expand=True, pady=5)

        save_btn = tk.Button(frm, text='Save CSV', command=self._save_csv)
        save_btn.pack(anchor='e')

        # Enable drag‑and‑drop on Windows
        try:
            from ctypes import windll
            windll.shell32.DragAcceptFiles(self.tree.winfo_id(), True)
            self.tree.drop_target_register('DND_Files')
            self.tree.dnd_bind('<<Drop>>', self._on_drop)
        except Exception:
            pass


    def _add_images(self):

        paths = filedialog.askopenfilenames(filetypes=[('Images', '*.jpg *.jpeg *.png *.bmp *.tif *.tiff')])
        self._process_files(list(map(Path, paths)))


    def _on_drop(self, event):
        files = self.tree.tk.splitlist(event.data)
        self._process_files(list(map(Path, files)))


    def _process_files(self, files: List[Path]):

        for f in files:
            label = extract_label(f)
            self.tree.insert('', 'end', values=(label or '<empty>',))

    def _save_csv(self):
        if not self.tree.get_children():
            messagebox.showwarning('Nothing to save', 'No results to save.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv')
        if not path:
            return
        import csv
        with open(path, 'w', newline='', encoding='utf-8-sig') as fh:
            writer = csv.writer(fh)
            writer.writerow(['label'])
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item)['values'])
        messagebox.showinfo('Saved', f'Saved to {path}')


def main():
    app = OCRGui()
    app.mainloop()

if __name__ == '__main__':
    main()
