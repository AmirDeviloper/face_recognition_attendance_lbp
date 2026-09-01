# 🧠 LBP-Based Face Recognition Attendance System (Python)

🕒 **Note:** This project was originally developed in August 2023 and uploaded to GitHub in October 2025 for portfolio and documentation purposes. It has since been upgraded into a full desktop attendance application built on the original LBP recognition engine.

This Python project implements a facial recognition **attendance system** using the Local Binary Pattern (LBP) algorithm. It processes a dataset of 40 individuals (based on the Olivetti Faces dataset), each with 10 facial images, mapped to realistic identities and automatically split into training/testing sets. The system uses region-based LBP (dividing each image into a 3×3 grid of 9 zones) for improved recognition accuracy, wrapped in a Tkinter GUI that logs attendance directly to a daily Excel file.

The system includes:

* 🧠 **Region-Based LBP Feature Extraction** – Each face is divided into a 3×3 grid; LBP histograms are computed per region and concatenated into a single feature vector for finer-grained texture comparison

<img width="1280" height="939" alt="504928791-579bd72f-bf61-4ddf-9adc-f03da2d6a470" src="https://github.com/user-attachments/assets/f81f9b03-1dd4-476d-a1e6-55997e87ff6d" />

* 🧪 **k-NN Face Classification** – Identity prediction via Chi-square distance between histograms, with a configurable "hardness" threshold that rejects low-confidence matches and returns `Person Not Found` instead of guessing
* 🗂️ **Automated Dataset Preparation** – `dataset_changer.py` maps the raw Olivetti `sN` folders to real names, then splits each subject's images into an 8/2 train/test set automatically
* 🖥️ **Desktop GUI (Tkinter)** – A Persian-language interface for selecting a face image, running recognition in a background thread (keeping the UI responsive), and confirming the identified person before logging attendance
* 📊 **Excel-Based Attendance Log** – Each day gets its own `attendance_YYYY-MM-DD.xlsx` file with name, date, time, and status columns; duplicate check-ins on the same day are automatically blocked
* ✅ **Manual Absence Registration** – A single click marks every person who hasn't checked in that day as absent, filling in the roster automatically

<img width="1105" height="623" alt="504928791-579bd72f-bf61-4ddf-9adc-f03da2d6a471" src="https://github.com/user-attachments/assets/c8f86ea1-db7d-4551-9637-3cbf73df49cf" />

* ⚙️ **Centralized Configuration** – All paths, thresholds (`RECOGNATION_HARDNESS`, `RECOGNATION_NEIGHBERS`), and dataset-build flags live in `settings.py`
* 📊 **Accuracy Evaluation** – 98% recognition accuracy measured across the held-out test split (batch evaluation mode via `CHECK_ALL_TEST_DATA`)
* 🧩 **Modular Codebase** – Easy to extend with other descriptors, classifiers, or a different backing dataset

## 📁 Modules

* `lbp_face_recognizer.py` – Core `Image` and `LBPRrecognation` classes: LBP computation (full-image and 3×3 regional), histogram extraction, and Chi-square-distance-based k-NN matching
* `dataset_changer.py` – Builds the training/testing folder structure from the raw Olivetti dataset and maps subject folders to human-readable names
* `settings.py` – Central configuration: dataset paths, recognition thresholds, dataset-build/test-mode flags
* `lbp_attendence_final.py` – Main entry point: Tkinter GUI application and Excel-based attendance logging

⚙️ Requirements
To run this project, you'll need:

* 🐍 Python 3.8 or newer
* 📦 `numpy`, `opencv-python`, `pandas`, `openpyxl`
* 🖼️ A structured dataset of facial images (40 subjects × 10 images) — place the Olivetti dataset as `Olivetti_Dataset/s1` … `s40` next to the scripts, and let `dataset_changer.py` build `NewDataset/train` and `NewDataset/test` on first run (or set `CREATE_DATABASE = False` in `settings.py` if you already have a prepared dataset)

## ▶️ Usage

1. Unzip `Olivetti_Dataset.zip` on project root folder. 
2. Run `lbp_attendence_final.py`
3. On first launch (with `CREATE_DATABASE = True`), the dataset is automatically split into train/test folders
4. Use **"ثبت حضور با تشخیص چهره"** (Register attendance via face recognition) to select an image and check a person in
5. Use **"ثبت غیاب افراد"** (Register absences) to mark everyone who hasn't checked in that day as absent
6. Attendance records are saved to `attendance_<today's date>.xlsx`

Set `CHECK_ALL_TEST_DATA = True` in `settings.py` to instead run a full batch evaluation over the test set from the command line (no GUI), printing a prediction for every test image.

## 🛡️ License
This project is licensed under the MIT License.
By contributing, you agree that your contributions will be released under the same license.

## ✨ Highlights

* 🔍 Region-based LBP for enhanced feature granularity
* 🖥️ Full GUI attendance workflow, not just a recognition script
* 📁 Automated dataset preparation from raw Olivetti data
* 📊 Daily Excel attendance logs with duplicate protection and bulk absence marking
* 🧩 Clean and extensible Python modules

## 📬 Contact

Feel free to reach out if you have questions or feedback!  
Telegram: [@AmirDevil](https://t.me/AmirDevil)

## 🚀 Purpose

This project was developed to explore texture-based facial recognition, feature engineering, and dataset-driven evaluation in Python, and has since been extended into a practical, GUI-driven attendance tool. It reflects my interest in building intelligent systems for pattern analysis and biometric identification.
