from dataset_changer import create_dataset_structure, names
from lbp_face_recognizer import LBPRrecognation
from settings import *

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import pandas as pd
from datetime import datetime
import threading

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("سیستم حضور و غیاب")
        self.root.geometry("400x300")
        
        self.recognizer = LBPRrecognation(TRAIN_DATASET_PATH, RECOGNATION_HARDNESS)
        
        self.excel_file = self.get_excel_file_path()
        
        self.create_widgets()
        
        self.ensure_excel_file_exists()
        
    def get_excel_file_path(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return f"attendance_{today}.xlsx"
    
    def ensure_excel_file_exists(self):
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=[
                'نام و نام خانوادگی', 
                'تاریخ حضور', 
                'ساعت حضور',
                'وضعیت حضور'
            ])
            df.to_excel(self.excel_file, index=False)
            print(f"today excel file created: {self.excel_file}")
    
    def create_widgets(self):
        title_label = tk.Label(
            self.root, 
            text="سیستم حضور و غیاب هوشمند",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        btn_face_recognition = tk.Button(
            self.root,
            text="ثبت حضور با تشخیص چهره",
            command=self.face_recognition_attendance,
            width=25,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        )
        btn_face_recognition.pack(pady=10)
        
        btn_manual_absence = tk.Button(
            self.root,
            text="ثبت غیاب افراد",
            command=self.manual_absence_registration,
            width=25,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Arial", 12)
        )
        btn_manual_absence.pack(pady=10)
        
        self.status_label = tk.Label(
            self.root,
            text="آماده به کار",
            font=("Arial", 10),
            fg="green"
        )
        self.status_label.pack(pady=20)
    
    def face_recognition_attendance(self):
        file_path = filedialog.askopenfilename(
            title="انتخاب فایل تصویر",
            filetypes=[("PGM files", "*.pgm"), ("All files", "*.*")]
        )
        
        if not file_path:
            messagebox.showerror("خطا", " فایلی انتخاب نشده است.")
            return
        
        if not file_path.lower().endswith('.pgm'):
            messagebox.showerror("خطا", "لطفاً یک فایل با پسوند .pgm انتخاب کنید.")
            return
        
        self.status_label.config(text="در حال پردازش تصویر...", fg="orange")
        
        thread = threading.Thread(
            target=self.process_face_recognition,
            args=(file_path,)
        )
        thread.start()
    
    def process_face_recognition(self, file_path):
        try:
            result = self.recognizer.find(file_path, RECOGNATION_NEIGHBERS)
            self.root.after(0, self.handle_recognition_result, result, file_path)
            
        except Exception as e:
            self.root.after(0, self.show_error, f"خطا در پردازش تصویر: {str(e)}")
    
    def handle_recognition_result(self, result, file_path):
        self.status_label.config(text="آماده به کار", fg="green")
        
        if result == PERSON_NOT_FOUND:
            messagebox.showwarning(
                "نتیجه تشخیص",
                "کاربر یافت نشد. لطفاً تصویر واضح‌تری انتخاب کنید."
            )
        else:
            response = messagebox.askyesno(
                "نتیجه تشخیص",
                f"کاربر شناسایی شده دارای مشخصات زیر است، اگر درست است گزینه بله را برای ثبت حضور انتخاب کنید.\n{result}"
            )
            
            if response:
                success = self.register_attendance(result)
                
                if success:
                    messagebox.showinfo(
                        "ثبت حضور",
                        f"حضور این شخص با موفقیت ثبت شد"
                    )
                else:
                    messagebox.showwarning(
                        "ثبت حضور",
                        f"این شخص امروز حضور و غیاب شده است"
                    )
    
    def register_attendance(self, person_name):
        try:
            df = pd.read_excel(self.excel_file)
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            today_attendance = df[
                (df['نام و نام خانوادگی'] == person_name) & 
                (df['تاریخ حضور'] == current_date)
            ]
            
            if not today_attendance.empty:
                return False
            
            new_record = {
                'نام و نام خانوادگی': person_name,
                'تاریخ حضور': current_date,
                'ساعت حضور': current_time,
                'وضعیت حضور': 'حاضر'
            }
            
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            
            df.to_excel(self.excel_file, index=False)

            print(f"{person_name} - حاضر")
            
            return True
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ثبت حضور: {str(e)}")
            return False
    
    def manual_absence_registration(self):

        person_list = list(names.values())
        
        if not person_list:
            messagebox.showwarning("هشدار", "هیچ نام معتبری وارد نشده است.")
            return
        
        absent_count = self.register_absences(person_list)
        
        messagebox.showinfo(
            "نتیجه ثبت غیاب",
            f"تعداد {absent_count} نفر به عنوان غایب ثبت شدند."
        )
    
    def register_absences(self, person_list):
        try:
            df = pd.read_excel(self.excel_file)
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            absent_count = 0
            
            for person_name in person_list:
                today_record = df[
                    (df['نام و نام خانوادگی'] == person_name) & 
                    (df['تاریخ حضور'] == current_date)
                ]
                
                if today_record.empty:
                    new_record = {
                        'نام و نام خانوادگی': person_name,
                        'تاریخ حضور': current_date,
                        'ساعت حضور': current_time,
                        'وضعیت حضور': 'غایب'
                    }
                    
                    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
                    absent_count += 1
                    print(f"{person_name} - غایب")
            
            if absent_count > 0:
                df.to_excel(self.excel_file, index=False)
            
            return absent_count
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در ثبت غیاب: {str(e)}")
            return 0
    
    def show_error(self, message):
        self.status_label.config(text="آماده به کار", fg="green")
        messagebox.showerror("خطا", message)

if __name__ == '__main__':
    if not os.path.exists('NewDataset') and CREATE_DATABASE:
        create_dataset_structure()

    if CHECK_ALL_TEST_DATA:
        recognizer = LBPRrecognation(TRAIN_DATASET_PATH, RECOGNATION_HARDNESS)

        for subdir, _, files in os.walk(TEST_DATASET_PATH):
            for file in files:
                if file.endswith('.pgm'):
                    print(recognizer.find(os.path.join(subdir, file), RECOGNATION_NEIGHBERS))
    else:
        root = tk.Tk()
        app = AttendanceSystem(root)
    
        root.configure(bg="#f0f0f0")
    
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
    
        root.mainloop()




