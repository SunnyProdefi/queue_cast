import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

from typing import List, Tuple


def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_days(month: int, leap: bool = False) -> int:
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and leap:
        return 29
    return days_in_month[month]


def date_to_day(date: float, year: int = 2025) -> int:
    month = int(date)
    day = int((date - month) * 100 + 0.5)
    leap = is_leap_year(year)
    total = 0
    for m in range(1, month):
        total += get_days(m, leap)
    total += day
    return total


def linear_fit(data: List[Tuple[float, int]]) -> Tuple[float, float]:
    n = len(data)
    if n < 2:
        raise ValueError("Need at least two data points for fitting")
    base_day = date_to_day(data[0][0])
    sumx = sumy = sumxy = sumx2 = 0.0
    for date, pos in data:
        x = date_to_day(date) - base_day
        y = pos
        sumx += x
        sumy += y
        sumxy += x * y
        sumx2 += x * x
    a = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
    b = (sumy - a * sumx) / n
    return a, b


def solve_for_zero(a: float, b: float) -> float:
    if a == 0:
        raise ValueError("Slope a cannot be zero")
    return -b / a


class QueueCastGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Queue Cast")
        self.records: List[Tuple[float, int]] = []

        self.data_file = "records.json"
        self.default_records = [
            (7.23, 2016),
            (7.30, 1974),
            (8.02, 1967),
            (8.07, 1947),
            (8.08, 1940),
            (8.09, 1930),
            (9.05, 1777),
        ]
        self.load_records()

        frame = ttk.Frame(root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Date (e.g., 7.23)").grid(row=0, column=0)
        self.date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.date_var, width=10).grid(row=0, column=1)

        ttk.Label(frame, text="Rank").grid(row=1, column=0)
        self.rank_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rank_var, width=10).grid(row=1, column=1)

        ttk.Button(frame, text="Add Record", command=self.add_record).grid(row=0, column=2, rowspan=2, padx=5)

        self.tree = ttk.Treeview(frame, columns=("date", "rank"), show="headings", height=6)
        self.tree.heading("date", text="Date")
        self.tree.heading("rank", text="Rank")
        self.tree.grid(row=2, column=0, columnspan=3, pady=5)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        ttk.Button(frame, text="Update Record", command=self.update_record).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Delete Record", command=self.delete_record).grid(row=3, column=1, pady=5)
        ttk.Button(frame, text="Estimate", command=self.estimate).grid(row=3, column=2, pady=5)

        self.result_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.result_var).grid(row=4, column=0, columnspan=3)

        # populate tree with existing records
        for date, rank in self.records:
            self.tree.insert("", tk.END, values=(f"{date:.2f}", rank))

    def add_record(self):
        try:
            date = float(self.date_var.get())
            rank = int(self.rank_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter numeric date and rank")
            return
        self.records.append((date, rank))
        self.tree.insert("", tk.END, values=(f"{date:.2f}", rank))
        self.save_records()
        self.date_var.set("")
        self.rank_var.set("")

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.date_var.set(values[0])
            self.rank_var.set(values[1])

    def update_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("No selection", "Please select a record to update")
            return
        try:
            date = float(self.date_var.get())
            rank = int(self.rank_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter numeric date and rank")
            return
        index = self.tree.index(selected[0])
        self.records[index] = (date, rank)
        self.tree.item(selected[0], values=(f"{date:.2f}", rank))
        self.save_records()

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("No selection", "Please select a record to delete")
            return
        index = self.tree.index(selected[0])
        self.tree.delete(selected[0])
        del self.records[index]
        self.save_records()
        self.date_var.set("")
        self.rank_var.set("")

    def load_records(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.records = [(float(d["date"]), int(d["rank"])) for d in data]
            except Exception:
                self.records = self.default_records.copy()
        else:
            self.records = self.default_records.copy()
            self.save_records()

    def save_records(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([{"date": d, "rank": r} for d, r in self.records], f, ensure_ascii=False, indent=2)

    def estimate(self):
        try:
            a, b = linear_fit(self.records)
            zero = solve_for_zero(a, b)
            self.result_var.set(f"Estimate: rank=0 in {zero:.2f} days from first record")
        except ValueError as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    QueueCastGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
