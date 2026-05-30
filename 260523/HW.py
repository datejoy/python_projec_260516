# 作業: 猜數字遊戲，好看的介面
import tkinter as tk
from tkinter import ttk, messagebox
import random

class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("猜數字遊戲")
        self.root.geometry("520x620")
        self.root.minsize(460, 560)
        self.root.configure(bg="#0f172a")

        self.target = 0
        self.attempts = 0
        self.history = []

        self.setup_style()
        self.build_ui()
        self.new_game()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0f172a")
        style.configure("Card.TFrame", background="#111827")
        style.configure("TLabel", background="#0f172a", foreground="#e5e7eb", font=("微軟正黑體", 11))
        style.configure("Title.TLabel", background="#0f172a", foreground="#f8fafc", font=("微軟正黑體", 22, "bold"))
        style.configure("Sub.TLabel", background="#0f172a", foreground="#94a3b8", font=("微軟正黑體", 10))
        style.configure("CardTitle.TLabel", background="#111827", foreground="#f8fafc", font=("微軟正黑體", 12, "bold"))
        style.configure("Status.TLabel", background="#111827", foreground="#f8fafc", font=("微軟正黑體", 12, "bold"))
        style.configure("Hint.TLabel", background="#111827", foreground="#cbd5e1", font=("微軟正黑體", 10))
        style.configure("TButton", font=("微軟正黑體", 11, "bold"), padding=10)
        style.map("TButton", background=[("active", "#1d4ed8")], foreground=[("active", "#ffffff")])
        style.configure("Accent.TButton", background="#2563eb", foreground="white")
        style.configure(
            "Success.Horizontal.TProgressbar",
            troughcolor="#1f2937",
            background="#22c55e",
            bordercolor="#1f2937",
            lightcolor="#22c55e",
            darkcolor="#22c55e",
        )

    def build_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="猜數字遊戲", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="介於 1 到 100，系統會給你即時回饋。", style="Sub.TLabel").pack(anchor="w", pady=(6, 0))

        stats_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        stats_card.pack(fill="x", pady=(0, 14))
        ttk.Label(stats_card, text="遊戲狀態", style="CardTitle.TLabel").pack(anchor="w")
        self.status = ttk.Label(stats_card, text="準備開始", style="Status.TLabel")
        self.status.pack(anchor="w", pady=(8, 6))
        self.progress = ttk.Progressbar(stats_card, mode='indeterminate', style="Success.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(4, 8))
        self.detail = ttk.Label(stats_card, text="請開始猜數字", style="Hint.TLabel")
        self.detail.pack(anchor="w")

        input_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        input_card.pack(fill="x", pady=(0, 14))
        ttk.Label(input_card, text="輸入你的猜測", style="CardTitle.TLabel").pack(anchor="w")
        row = ttk.Frame(input_card)
        row.pack(fill="x", pady=(12, 0))

        self.entry = ttk.Entry(row, font=("微軟正黑體", 14))
        self.entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.entry.bind("<Return>", lambda e: self.check_guess())

        ttk.Button(row, text="送出", style="Accent.TButton", command=self.check_guess).pack(side="left", padx=(10, 0))

        btns = ttk.Frame(main)
        btns.pack(fill="x", pady=(0, 14))
        ttk.Button(btns, text="重新開始", command=self.new_game).pack(side="left", fill="x", expand=True)

        log_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        log_card.pack(fill="both", expand=True)
        ttk.Label(log_card, text="猜測紀錄", style="CardTitle.TLabel").pack(anchor="w")

        self.log = tk.Text(
            log_card,
            height=14,
            wrap="word",
            bg="#0b1220",
            fg="#e5e7eb",
            insertbackground="white",
            relief="flat",
            font=("微軟正黑體", 11),
        )
        self.log.pack(fill="both", expand=True, pady=(10, 0))
        self.log.configure(state="disabled")

        footer = ttk.Label(main, text="提示：數字越接近答案，回饋會越接近。", style="Sub.TLabel")
        footer.pack(anchor="center", pady=(12, 0))

    def new_game(self):
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.history = []
        self.progress.stop()
        self.progress.start(10)
        self.status.configure(text="新遊戲開始")
        self.detail.configure(text="請開始猜數字")
        self.clear_log()
        self.append_log("已開始新遊戲。請輸入 1~100 的數字。")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.configure(state="disabled")

    def append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")

    def feedback(self, guess):
        diff = abs(guess - self.target)
        if guess == self.target:
            return "恭喜答對了！"
        if diff <= 3:
            return "超級接近！"
        if diff <= 10:
            return "很接近。"
        if diff <= 20:
            return "有點遠。"
        return "差距還很大。"

    def check_guess(self):
        value = self.entry.get().strip()
        if not value.isdigit():
            messagebox.showwarning("輸入錯誤", "請輸入 1 到 100 的整數。")
            return

        guess = int(value)
        if not 1 <= guess <= 100:
            messagebox.showwarning("範圍錯誤", "請輸入 1 到 100 的整數。")
            return

        self.attempts += 1
        hint = self.feedback(guess)
        self.history.append(guess)
        direction = "大一點" if guess < self.target else "小一點"

        if guess == self.target:
            self.status.configure(text="你贏了！")
            self.detail.configure(text=f"你用了 {self.attempts} 次猜中。")
            self.append_log(f"{self.attempts}. {guess} -> {hint}")
            messagebox.showinfo("勝利", f"答對了！答案就是 {self.target}。你用了 {self.attempts} 次。")
            self.progress.stop()
            return

        self.status.configure(text=hint)
        self.detail.configure(text=f"目前猜測次數：{self.attempts}")
        self.append_log(f"{self.attempts}. {guess} -> {hint} 提示：{direction}")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()