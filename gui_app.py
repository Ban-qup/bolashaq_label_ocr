"""Very small GUI wrapper around the OCR pipeline."""
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from ocr import extract_label

def select_and_process():
    path = filedialog.askopenfilename(
        title="Choose image",
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
            ("All files", "*.*"),
        ],
    )
    if not path:
        return
    label = extract_label(Path(path))
    if label:
        root.clipboard_clear()
        root.clipboard_append(label)
        messagebox.showinfo("Result", f"Detected label: {label}\n\n(The value was copied to clipboard.)")
    else:
        messagebox.showwarning("No label found", "Could not detect a serial number in the image.")

root = tk.Tk()
root.title("Bolashaq Label OCR")

btn = tk.Button(root, text="Open Image", width=20, height=2, command=select_and_process)
btn.pack(padx=40, pady=30)

info = tk.Label(root, text="Result copies to clipboard automatically", fg="gray")
info.pack(pady=(0, 20))

root.mainloop()
