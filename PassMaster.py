import tkinter as tk
from tkinter import messagebox, scrolledtext
import string
import random
import pyperclip
import json
import os

# الأحرف المتشابهة بصرياً
VISUALLY_SIMILAR = "l1IoO0"
SETTINGS_FILE = "settings.json"

# تحميل الإعدادات السابقة إن وجدت
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# حفظ الإعدادات الحالية
def save_settings():
    settings = {
        "length": length_slider.get(),
        "num_passwords": num_slider.get(),
        "upper": var_upper.get(),
        "lower": var_lower.get(),
        "digits": var_digits.get(),
        "symbols": var_symbols.get(),
        "custom_symbols": custom_entry.get(),
        "avoid_similar": var_avoid_similar.get(),
        "readable": var_readable.get(),
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f)

# توليد كلمة المرور
def generate_password():
    length = length_slider.get()
    num_passwords = num_slider.get()

    use_upper = var_upper.get()
    use_lower = var_lower.get()
    use_digits = var_digits.get()
    use_symbols = var_symbols.get()
    avoid_similar = var_avoid_similar.get()
    readable = var_readable.get()

    custom_symbols = custom_entry.get()

    characters = ''
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    if custom_symbols:
        characters += custom_symbols

    if not characters:
        messagebox.showerror("خطأ", "يجب اختيار نوع واحد على الأقل من الأحرف!")
        return

    if avoid_similar:
        characters = ''.join(ch for ch in characters if ch not in VISUALLY_SIMILAR)

    if not characters:
        messagebox.showerror("خطأ", "بعد إزالة الأحرف المتشابهة لم يتبق أحرف!")
        return

    passwords = []
    for _ in range(num_passwords):
        pw = ''.join(random.choice(characters) for _ in range(length))
        if readable:
            pw = '-'.join([pw[i:i+4] for i in range(0, len(pw), 4)])
        passwords.append(pw)

    output.delete("1.0", tk.END)
    output.insert(tk.END, "\n".join(passwords))
    save_settings()

def copy_to_clipboard():
    password = output.get("1.0", tk.END).strip()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("نسخ", "تم نسخ كلمة المرور إلى الحافظة")
    else:
        messagebox.showwarning("تنبيه", "لا توجد كلمة مرور لنسخها")

def clear_output():
    output.delete("1.0", tk.END)

# إنشاء الواجهة
root = tk.Tk()
root.title("🔐 مولد كلمات المرور الاحترافي")
root.geometry("650x600")

# خيارات الأحرف
options_frame = tk.LabelFrame(root, text="اختر أنواع الأحرف:", padx=10, pady=10)
options_frame.pack(pady=10)

var_upper = tk.BooleanVar()
var_lower = tk.BooleanVar()
var_digits = tk.BooleanVar()
var_symbols = tk.BooleanVar()

var_avoid_similar = tk.BooleanVar()
var_readable = tk.BooleanVar()

tk.Checkbutton(options_frame, text="أحرف كبيرة (A-Z)", variable=var_upper).grid(row=0, column=0, sticky="w")
tk.Checkbutton(options_frame, text="أحرف صغيرة (a-z)", variable=var_lower).grid(row=1, column=0, sticky="w")
tk.Checkbutton(options_frame, text="أرقام (0-9)", variable=var_digits).grid(row=0, column=1, sticky="w")
tk.Checkbutton(options_frame, text="رموز (!@#...)", variable=var_symbols).grid(row=1, column=1, sticky="w")

# مدخل الرموز الخاصة المخصصة
tk.Label(root, text="رموز إضافية تريد تضمينها (اختياري):").pack()
custom_entry = tk.Entry(root, width=50)
custom_entry.pack(pady=5)

# تجنب الأحرف المتشابهة والفواصل
other_frame = tk.Frame(root)
other_frame.pack(pady=5)
tk.Checkbutton(other_frame, text="تجنب الأحرف المتشابهة (l,1,I,O,0,o)", variable=var_avoid_similar).pack(anchor='w')
tk.Checkbutton(other_frame, text="سهولة القراءة (إضافة شرطات كل 4 أحرف)", variable=var_readable).pack(anchor='w')

# الطول وعدد كلمات المرور
tk.Label(root, text="اختر طول كلمة المرور:").pack()
length_slider = tk.Scale(root, from_=4, to=50, orient=tk.HORIZONTAL)
length_slider.pack()

tk.Label(root, text="عدد كلمات المرور التي تريد توليدها:").pack()
num_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
num_slider.pack()

# أزرار توليد ونسخ ومسح
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🎲 توليد كلمة المرور", command=generate_password).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="📋 نسخ", command=copy_to_clipboard).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="🧹 مسح", command=clear_output).pack(side=tk.LEFT, padx=5)

# عرض النتائج
output = scrolledtext.ScrolledText(root, height=10)
output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# تحميل الإعدادات المحفوظة
settings = load_settings()
length_slider.set(settings.get("length", 12))
num_slider.set(settings.get("num_passwords", 1))
var_upper.set(settings.get("upper", True))
var_lower.set(settings.get("lower", True))
var_digits.set(settings.get("digits", True))
var_symbols.set(settings.get("symbols", False))
custom_entry.insert(0, settings.get("custom_symbols", ""))
var_avoid_similar.set(settings.get("avoid_similar", False))
var_readable.set(settings.get("readable", False))

root.mainloop()
