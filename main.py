import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import csv, os
from fpdf import FPDF

# -----------------------------
# File Setup (FIXED)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER_FILE = os.path.join(BASE_DIR, "users.csv")
HISTORY_FILE = os.path.join(BASE_DIR, "history.csv")

def init_file(file, headers):
    try:
        if not os.path.exists(file):
            with open(file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(headers)
    except PermissionError:
        messagebox.showerror("Error", f"Permission denied:\n{file}")

init_file(USER_FILE, ["username","password"])
init_file(HISTORY_FILE, ["username","BMI","Category","Calories","Burned"])

current_user = ""

# -----------------------------
# Health Functions
# -----------------------------
def calculate_bmi(w,h): return w/((h/100)**2)

def bmi_category(b):
    return "Underweight" if b<18.5 else "Normal" if b<24.9 else "Overweight" if b<29.9 else "Obese"

def calorie_intake(w,h,a,g):
    return 10*w+6.25*h-5*a+(5 if g=="Male" else -161)

def calories_burned(w,act):
    met={"Walking":3.5,"Running":7,"Cycling":6,"Yoga":3,"Gym":5}
    return round(met.get(act,3.5)*w*0.0175*30,2)

def diet_plan(c):
    return {"Underweight":"Milk, Nuts, Eggs",
            "Normal":"Balanced Diet",
            "Overweight":"Low Carb",
            "Obese":"Strict Diet"}[c]

def exercise_plan(c):
    return {"Underweight":"Strength Training",
            "Normal":"Gym + Cardio",
            "Overweight":"HIIT",
            "Obese":"Walking"}[c]

# -----------------------------
# CSV FUNCTIONS
# -----------------------------
def register_user(u,p):
    with open(USER_FILE,"a",newline="",encoding="utf-8") as f:
        csv.writer(f).writerow([u,p])

def validate_login(u,p):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE,encoding="utf-8") as f:
        for row in list(csv.reader(f))[1:]:
            if row[0]==u and row[1]==p:
                return True
    return False

def save_history(u,b,c,cal,burn):
    with open(HISTORY_FILE,"a",newline="",encoding="utf-8") as f:
        csv.writer(f).writerow([u,round(b,2),c,int(cal),burn])

def get_user_history(u):
    data=[]
    if not os.path.exists(HISTORY_FILE):
        return data
    with open(HISTORY_FILE,encoding="utf-8") as f:
        for row in list(csv.reader(f))[1:]:
            if row[0]==u:
                data.append(row)
    return data

# -----------------------------
# Chart
# -----------------------------
def show_chart(cal,burn):
    plt.figure()
    plt.bar(["Intake","Burned"],[cal,burn])
    plt.title("Calories Chart")
    plt.show()

# -----------------------------
# PDF Export
# -----------------------------
def export_pdf():
    data = get_user_history(current_user)
    if not data:
        messagebox.showinfo("Info","No data to export")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,txt=f"{current_user} Fitness Report",ln=True)

    for row in data:
        pdf.cell(200,10,txt=str(row),ln=True)

    filename = os.path.join(BASE_DIR, f"{current_user}_report.pdf")
    pdf.output(filename)

    messagebox.showinfo("Success", f"Saved as:\n{filename}")

# -----------------------------
# History Viewer
# -----------------------------
def view_history():
    win = tk.Toplevel(root)
    win.title("History")
    win.geometry("600x400")

    tree = ttk.Treeview(win, columns=("BMI","Cat","Cal","Burn"), show="headings")

    for col in ("BMI","Cat","Cal","Burn"):
        tree.heading(col, text=col)

    for row in get_user_history(current_user):
        tree.insert("",tk.END,values=row[1:])

    tree.pack(fill="both",expand=True)

# -----------------------------
# Calculate
# -----------------------------
def calculate():
    try:
        w = float(weight.get())
        h = float(height.get())
        a = int(age.get())
        g = gender.get()
        act = activity.get()

        bmi = calculate_bmi(w,h)
        cat = bmi_category(bmi)
        cal = calorie_intake(w,h,a,g)
        burn = calories_burned(w,act)

        result.set(
            f"BMI: {bmi:.2f} ({cat})\n"
            f"Calories: {int(cal)} | Burned: {burn}\n"
            f"Diet: {diet_plan(cat)}\n"
            f"Exercise: {exercise_plan(cat)}"
        )

        save_history(current_user,bmi,cat,cal,burn)
        show_chart(cal,burn)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid Input\n{e}")

# -----------------------------
# Auth
# -----------------------------
def login():
    global current_user
    if validate_login(user.get(),pwd.get()):
        current_user=user.get()
        login_frame.pack_forget()
        main_app()
    else:
        messagebox.showerror("Error","Invalid Login")

def open_register():
    login_frame.pack_forget()
    reg_frame.pack(expand=True)

def register():
    if not reg_user.get() or not reg_pwd.get():
        messagebox.showwarning("Error","Fill all fields")
        return
    register_user(reg_user.get(),reg_pwd.get())
    messagebox.showinfo("Success","Registered Successfully")
    reg_frame.pack_forget()
    login_frame.pack(expand=True)

# -----------------------------
# Main UI
# -----------------------------
def main_app():
    global weight,height,age,gender,activity,result

    frame = tk.Frame(root,bg="#1e1e2f")
    frame.pack(fill="both",expand=True)

    tk.Label(frame,text="Fitness Dashboard",
             font=("Arial",26,"bold"),
             fg="white",bg="#1e1e2f").pack(pady=10)

    form = tk.Frame(frame,bg="#2c2c3e")
    form.pack(pady=15)

    def lbl(t,r):
        tk.Label(form,text=t,font=("Arial",14,"bold"),
                 fg="white",bg="#2c2c3e").grid(row=r,column=0,pady=5)

    weight=tk.Entry(form,font=("Arial",14))
    height=tk.Entry(form,font=("Arial",14))
    age=tk.Entry(form,font=("Arial",14))

    lbl("Weight",0); weight.grid(row=0,column=1)
    lbl("Height",1); height.grid(row=1,column=1)
    lbl("Age",2); age.grid(row=2,column=1)

    gender=tk.StringVar(value="Male")
    ttk.Combobox(form,textvariable=gender,
                 values=["Male","Female"]).grid(row=3,column=1)

    activity=tk.StringVar(value="Walking")
    ttk.Combobox(form,textvariable=activity,
                 values=["Walking","Running","Cycling","Yoga","Gym"]).grid(row=4,column=1)

    tk.Button(form,text="Calculate",command=calculate,
              font=("Arial",14,"bold"),
              bg="green",fg="white").grid(row=5,columnspan=2,pady=10)

    tk.Button(frame,text="View History",command=view_history).pack(pady=5)
    tk.Button(frame,text="Export PDF",command=export_pdf).pack(pady=5)

    result=tk.StringVar()
    tk.Label(frame,textvariable=result,
             font=("Arial",14,"bold"),
             fg="#00ffcc",bg="#1e1e2f").pack(pady=10)

# -----------------------------
# Root
# -----------------------------
root=tk.Tk()
root.title("Fitness App")
root.geometry("700x650")
root.configure(bg="#1e1e2f")

# Login UI
login_frame=tk.Frame(root,bg="#1e1e2f")

tk.Label(login_frame,text="Login",
         font=("Arial",22,"bold"),
         fg="white",bg="#1e1e2f").pack(pady=10)

user=tk.Entry(login_frame,font=("Arial",14))
pwd=tk.Entry(login_frame,show="*",font=("Arial",14))

tk.Label(login_frame,text="Username",bg="#1e1e2f",fg="white").pack()
user.pack()
tk.Label(login_frame,text="Password",bg="#1e1e2f",fg="white").pack()
pwd.pack()

tk.Button(login_frame,text="Login",command=login,
          bg="green",fg="white").pack(pady=10)

tk.Button(login_frame,text="Register",command=open_register).pack()

login_frame.pack(expand=True)

# Register UI
reg_frame=tk.Frame(root,bg="#1e1e2f")

tk.Label(reg_frame,text="Register",
         font=("Arial",22,"bold"),
         fg="white",bg="#1e1e2f").pack(pady=10)

reg_user=tk.Entry(reg_frame,font=("Arial",14))
reg_pwd=tk.Entry(reg_frame,show="*",font=("Arial",14))

tk.Label(reg_frame,text="Username",bg="#1e1e2f",fg="white").pack()
reg_user.pack()
tk.Label(reg_frame,text="Password",bg="#1e1e2f",fg="white").pack()
reg_pwd.pack()

tk.Button(reg_frame,text="Submit",command=register,
          bg="green",fg="white").pack(pady=10)

tk.Button(reg_frame,text="Back",
          command=lambda:[reg_frame.pack_forget(),login_frame.pack(expand=True)]
          ).pack()

root.mainloop()
