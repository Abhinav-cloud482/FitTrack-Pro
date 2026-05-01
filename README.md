# FitTrack-Pro

## FitTrack Pro

A complete **desktop fitness tracking application** built using Python.
It helps users calculate BMI, track calorie intake & burn, view history, and export reports — all with a clean graphical interface.


## Features

* User Authentication (Login & Register)
* BMI Calculation with Category Detection
* Daily Calorie Intake Estimation
* Calories Burned Based on Activity
* Personalized Diet & Exercise Suggestions
* Visual Charts using Matplotlib
* Export Fitness Report as PDF
* History Tracking using CSV
* Interactive GUI built with Tkinter


## Tech Stack

* **Python**
* **Tkinter** (GUI)
* **Matplotlib** (Charts)
* **FPDF** (PDF Export)
* **CSV** (Data Storage)


## Project Structure

```
FitTrack-Pro/
│
├── main.py          # Main application file
├── users.csv        # Stores user credentials
├── history.csv      # Stores fitness records
└── README.md        # Project documentation
```


## Installation & Setup

### Clone the repository

```bash
git clone https://github.com/your-username/FitTrack-Pro.git
cd FitTrack-Pro
```

### Install dependencies

```bash
pip install matplotlib fpdf
```

### Run the application

```bash
python main.py
```


## Screenshots

> (Add screenshots here after uploading images)


## How It Works

1. Register or login
2. Enter :-

   * Weight
   * Height
   * Age
   * Gender
   * Activity
3. Click **Calculate**
4. Get :-

   * BMI & Category
   * Calories Intake
   * Calories Burned
   * Diet Plan
   * Exercise Plan
5. View history or export report as PDF


## Sample Output

* BMI :-  22.53 (Normal)
* Calories :-  1755
* Burned :-  134 kcal
* Diet :-  Balanced Diet
* Exercise :-  Gym + Cardio


## Future Improvements

* Database integration (SQLite/MySQL)
* Password encryption
* Dark/Light theme toggle
* Mobile app version
* Cloud sync


## Disclaimer

This application provides general fitness guidance.
It is **not a substitute for professional medical advice**.


## Author

Developed by *Your Name*


