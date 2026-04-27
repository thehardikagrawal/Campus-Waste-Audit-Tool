# ============================================================
#  Campus / Community Waste Audit Tool
#  Author  : [Your Name]
#  Date    : April 2025
#  Purpose : Read waste data from Excel, generate visual
#            charts (pie + bar), and display a summary.
# ============================================================

import tkinter as tk
from tkinter import messagebox
import os
import sys

# ── Third-party (pip install openpyxl matplotlib) ────────────
try:
    import openpyxl
    import matplotlib
    matplotlib.use("Agg")           # headless backend – no display needed
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"Missing library: {e}\nRun:  pip install openpyxl matplotlib")
    sys.exit(1)

# ── Configuration ────────────────────────────────────────────
EXCEL_FILE  = "Waste_Audit_Tool.xlsx"
PIE_OUTPUT  = "pie_chart.png"
BAR_OUTPUT  = "bar_graph.png"
COLORS      = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336"]

# ── Data loading ─────────────────────────────────────────────
def load_data():
    """Read category + weight columns from the Excel sheet."""
    if not os.path.exists(EXCEL_FILE):
        raise FileNotFoundError(f"'{EXCEL_FILE}' not found in the same folder.")

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active

    categories, weights = [], []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] and str(row[0]).upper() != "TOTAL":
            categories.append(str(row[0]))
            weights.append(float(row[2]))
    return categories, weights

# ── Chart generators ─────────────────────────────────────────
def make_pie(categories, weights):
    fig, ax = plt.subplots(figsize=(7, 5), facecolor="#FAFAFA")
    wedges, texts, autos = ax.pie(
        weights, labels=categories, autopct="%1.1f%%",
        colors=COLORS, startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=2),
        textprops=dict(fontsize=10)
    )
    for a in autos:
        a.set_fontweight("bold"); a.set_color("white")
    total = sum(weights)
    ax.set_title(f"Waste Distribution  (Total: {total:.1f} kg)",
                 fontsize=13, fontweight="bold", pad=18)
    plt.tight_layout()
    plt.savefig(PIE_OUTPUT, dpi=140, bbox_inches="tight")
    plt.close(fig)

def make_bar(categories, weights):
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#FAFAFA")
    bars = ax.bar(categories, weights, color=COLORS, width=0.55,
                  edgecolor="white", linewidth=1.5)
    for bar, val in zip(bars, weights):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.4,
                f"{val} kg", ha="center", va="bottom",
                fontsize=9, fontweight="bold")
    ax.set_title("Waste Quantity by Category", fontsize=13, fontweight="bold", pad=14)
    ax.set_xlabel("Category", fontsize=11)
    ax.set_ylabel("Weight (kg)", fontsize=11)
    ax.set_ylim(0, max(weights) * 1.25)
    ax.set_facecolor("#F5F5F5")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=15, ha="right", fontsize=9)
    plt.tight_layout()
    plt.savefig(BAR_OUTPUT, dpi=140, bbox_inches="tight")
    plt.close(fig)

# ── Main action ───────────────────────────────────────────────
def run_audit():
    btn.config(state="disabled", text="Processing…")
    root.update()
    try:
        categories, weights = load_data()
        make_pie(categories, weights)
        make_bar(categories, weights)

        total   = sum(weights)
        top_cat = categories[weights.index(max(weights))]
        summary = (
            f"✅  Audit Complete!\n\n"
            f"📦  Total Waste   : {total:.1f} kg\n"
            f"🏆  Top Category  : {top_cat} ({max(weights):.1f} kg)\n"
            f"📊  Categories    : {len(categories)}\n\n"
            f"Charts saved as:\n"
            f"  • {PIE_OUTPUT}\n"
            f"  • {BAR_OUTPUT}"
        )
        messagebox.showinfo("Waste Audit — Results", summary)
    except Exception as err:
        messagebox.showerror("Error", str(err))
    finally:
        btn.config(state="normal", text="▶  Run Waste Audit")

# ── GUI layout ────────────────────────────────────────────────
root = tk.Tk()
root.title("Campus Waste Audit Tool")
root.geometry("420x300")
root.resizable(False, False)
root.configure(bg="#E8F5E9")

tk.Label(root, text="🌿 Campus Waste Audit Tool",
         font=("Helvetica", 16, "bold"),
         bg="#2E7D32", fg="white",
         pady=12).pack(fill="x")

tk.Label(root,
         text="Click the button below to load the Excel data,\n"
              "calculate waste totals, and generate charts.",
         font=("Helvetica", 11), bg="#E8F5E9", fg="#333",
         pady=14).pack()

btn = tk.Button(root,
                text="▶  Run Waste Audit",
                font=("Helvetica", 13, "bold"),
                bg="#4CAF50", fg="white",
                activebackground="#388E3C",
                padx=20, pady=10,
                bd=0, cursor="hand2",
                command=run_audit)
btn.pack(pady=8)

tk.Label(root,
         text=f"📁 Reads from: {EXCEL_FILE}",
         font=("Helvetica", 9), bg="#E8F5E9", fg="#555").pack(pady=4)

tk.Label(root,
         text="Outputs: pie_chart.png  |  bar_graph.png",
         font=("Helvetica", 9), bg="#E8F5E9", fg="#777").pack()

root.mainloop()
