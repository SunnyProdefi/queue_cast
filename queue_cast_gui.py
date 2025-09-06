import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
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

        ttk.Button(frame, text="Estimate", command=self.estimate).grid(row=3, column=0, columnspan=3, pady=5)

        self.result_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.result_var).grid(row=4, column=0, columnspan=3)

    def add_record(self):
        try:
            date = float(self.date_var.get())
            rank = int(self.rank_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter numeric date and rank")
            return
        self.records.append((date, rank))
        self.tree.insert("", tk.END, values=(f"{date:.2f}", rank))
        self.date_var.set("")
        self.rank_var.set("")

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
