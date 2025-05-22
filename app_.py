import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from fpdf import FPDF

entries = []

def add_entry():
    try:
        weight_kg = float(weight_entry.get())
        rate_pre_tone = float(rate_entry.get())
        total_cost = (weight_kg / 1000) * rate_pre_tone

        entry = {
            "Date": date_entry.get(),
            "Trip Type": trip_var.get(),
            "Truck No": truck_entry.get(),
            "Driver": driver_entry.get(),
            "From": from_entry.get(),
            "To": to_entry.get(),
            "Product": product_entry.get(),
            "Weight (Kg)": weight_kg,
            "Rate Pre Tone": rate_pre_tone,
            "Total Cost": round(total_cost, 2)
        }

        entries.append(entry)
        update_table()
        clear_fields()
        update_summary()

    except ValueError:
        messagebox.showerror("Input Error", "Weight और Rate को सही से दर्ज करें।")

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    for entry in entries:
        values = [entry[col] for col in tree["columns"]]
        tree.insert("", "end", values=values)

def clear_fields():
    for e in [date_entry, truck_entry, driver_entry, from_entry, to_entry, product_entry]:
        e.delete(0, tk.END)
    weight_entry.set("")
    rate_entry.set("")
    trip_var.set("Go")

def update_summary():
    go_total = sum(e["Total Cost"] for e in entries if e["Trip Type"] == "Go")
    return_total = sum(e["Total Cost"] for e in entries if e["Trip Type"] == "Return")
    try:
        fuel = float(fuel_entry.get())
    except:
        fuel = 0
    try:
        misc = float(misc_entry.get())
    except:
        misc = 0
    grand_total = go_total + return_total
    profit = grand_total - (fuel + misc)

    go_total_var.set(f"₹ {go_total:.2f}")
    return_total_var.set(f"₹ {return_total:.2f}")
    total_cost_var.set(f"₹ {grand_total:.2f}")
    profit_var.set(f"₹ {profit:.2f}")

def save_to_excel():
    df = pd.DataFrame(entries)
    df.to_excel("truck_records.xlsx", index=False)
    messagebox.showinfo("Saved", "Data saved to truck_records.xlsx")

def export_to_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    line_height = 8
    col_widths = [22, 16, 22, 22, 22, 22, 22, 22, 24, 24]

    headers = ["Date", "Trip Type", "Truck No", "Driver", "From", "To", "Product", "Weight (Kg)", "Rate Pre Tone", "Total Cost"]

    # Header row
    for i, header in enumerate(headers):
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(col_widths[i], line_height, header, border=1, fill=True)
    pdf.ln(line_height)

    # Data rows
    for entry in entries:
        for i, key in enumerate(headers):
            text = str(entry[key])
            pdf.cell(col_widths[i], line_height, text, border=1)
        pdf.ln(line_height)

    pdf.output("truck_report.pdf")
    messagebox.showinfo("PDF Exported", "📄 Clean table format exported to truck_report.pdf")

# --- UI Start ---
root = tk.Tk()
root.title("🚛 Truck Billing App")
root.geometry("1050x850")
root.config(bg="#f7f7f7")

tk.Label(root, text="🚛 Truck Transport Billing System", font=("Arial", 18, "bold"), bg="#f7f7f7").pack(pady=15)

form_frame = tk.Frame(root, bg="#f7f7f7")
form_frame.pack()

# --- Entry Fields ---
labels = [
    "Date (DD-MM-YYYY):", "Truck No:", "Driver Name:", "From:",
    "To:", "Product Name:"
]
entries_list = []

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label, bg="#f7f7f7", font=("Arial", 10)).grid(row=i, column=0, sticky='w', pady=3)
    entry = tk.Entry(form_frame, width=30)
    entry.grid(row=i, column=1, pady=3)
    entries_list.append(entry)

date_entry, truck_entry, driver_entry, from_entry, to_entry, product_entry = entries_list

# Weight (Kg)
tk.Label(form_frame, text="Weight (Kg):", bg="#f7f7f7", font=("Arial", 10)).grid(row=6, column=0, sticky='w', pady=3)
weight_values = [str(w) for w in range(10000, 60000, 5000)]
weight_entry = ttk.Combobox(form_frame, values=weight_values, width=28)
weight_entry.grid(row=6, column=1, pady=3)

# Rate Pre Tone
tk.Label(form_frame, text="Rate Pre Tone:", bg="#f7f7f7", font=("Arial", 10)).grid(row=7, column=0, sticky='w', pady=3)
rate_values = [str(r) for r in range(1000, 5500, 500)]
rate_entry = ttk.Combobox(form_frame, values=rate_values, width=28)
rate_entry.grid(row=7, column=1, pady=3)

# Trip Type
tk.Label(form_frame, text="Trip Type:", bg="#f7f7f7", font=("Arial", 10)).grid(row=8, column=0, sticky='w')
trip_var = tk.StringVar(value="Go")
trip_menu = ttk.Combobox(form_frame, textvariable=trip_var, values=["Go", "Return"], state="readonly", width=28)
trip_menu.grid(row=8, column=1, pady=3)

# --- Cost Inputs ---
tk.Label(form_frame, text="Fuel Cost:", bg="#f7f7f7", font=("Arial", 10)).grid(row=9, column=0, sticky='w', pady=3)
fuel_entry = tk.Entry(form_frame, width=30)
fuel_entry.grid(row=9, column=1, pady=3)

tk.Label(form_frame, text="Miscellaneous:", bg="#f7f7f7", font=("Arial", 10)).grid(row=10, column=0, sticky='w', pady=3)
misc_entry = tk.Entry(form_frame, width=30)
misc_entry.grid(row=10, column=1, pady=3)

# --- Action Buttons ---
btn_frame = tk.Frame(root, bg="#f7f7f7")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="➕ Add Entry", command=add_entry, bg="green", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="💾 Save to Excel", command=save_to_excel, bg="blue", fg="white", width=15).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="📄 Export to PDF", command=export_to_pdf, bg="orange", fg="white", width=15).grid(row=0, column=2, padx=10)

# --- Table View ---
columns = ["Date", "Trip Type", "Truck No", "Driver", "From", "To", "Product", "Weight (Kg)", "Rate Pre Tone", "Total Cost"]
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=90, anchor="center")
tree.pack(pady=15, fill='x')

# --- Summary Frame ---
summary_frame = tk.Frame(root, bg="#f7f7f7")
summary_frame.pack(pady=10)

go_total_var = tk.StringVar()
return_total_var = tk.StringVar()
total_cost_var = tk.StringVar()
profit_var = tk.StringVar()

summary_labels = [
    ("Go Trip Total:", go_total_var),
    ("Return Trip Total:", return_total_var),
    ("Total Cost:", total_cost_var),
    ("Total Profit:", profit_var)
]

for i, (label, var) in enumerate(summary_labels):
    tk.Label(summary_frame, text=label, font=("Arial", 10, "bold"), bg="#f7f7f7").grid(row=i, column=0, sticky='e', padx=10)
    tk.Label(summary_frame, textvariable=var, font=("Arial", 10), bg="#f7f7f7").grid(row=i, column=1, sticky='w')

root.mainloop()
