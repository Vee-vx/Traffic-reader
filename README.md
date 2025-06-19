# 🚦 Traffic Reader

A Python-based application that reads traffic CSV data, visualizes hourly vehicle counts using histograms, and provides a simple GUI for multi-date processing. Built with Tkinter and Matplotlib.

---

## 📌 Project Summary

This project was developed for the **Software Development I (4COSC006C.1)** module as part of an individual coursework assignment. It focuses on processing traffic data from CSV files and visualizing hourly vehicle counts.

---

## ✅ Features Implemented

### 🔷 Task D – Histogram Visualization
- GUI application using Tkinter to display traffic histograms for a selected date.
- Data is grouped by two junctions:
  - **Elm Avenue/Rabbit Road**
  - **Hanley Highway/Westway**
- Color-coded bar charts (green for Elm, red for Hanley).
- Histogram window closes automatically after 30 seconds.

### 🔷 Task E – Multi-File Processor
- Loads multiple CSV files to process and analyze traffic data.
- Prompts user for date input, validates data, displays histogram, and saves results.
- Supports repeated interaction with user-friendly prompts.

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – GUI Interface
- **Matplotlib** – Data Visualization
- **CSV module** – File Parsing

---

## 🧪 Testing

Tested with the following input dates:
- `21/06/2024`
- `15/06/2024`
- `16/06/2024`
- `30/05/2020`
- Full run simulation with user interaction

---

## 📂 Project Structure

- `main.py`: Contains core classes and logic (`HistogramApp`, `MultiCSVProcessor`)
- `traffic_data_*.csv`: Input data files for traffic logs
- `README.md`: Project documentation (this file)

---

## 🚀 How to Run

```bash
python main.py
