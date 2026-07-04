import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False

tickers = {
    "台積電": "2330.TW",
    "聯電": "2303.TW",
    "聯發科": "2454.TW",
    "鴻海": "2317.TW",
}


def load_data():
    data = yf.download(
        list(tickers.values()),
        start="2026-01-01",
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    close = data["Close"]
    code_to_name = {v: k for k, v in tickers.items()}
    close = close.rename(columns=code_to_name)
    returns = close.pct_change().dropna()
    corr = returns.corr()
    return close, returns, corr


def build_heatmap_figure(corr):
    fig = Figure(figsize=(5.5, 4.5), dpi=100)
    ax = fig.add_subplot(111)
    im = ax.imshow(corr.values, cmap="RdYlBu", vmin=-1, vmax=1, aspect="equal")

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, fontsize=10)
    ax.set_yticklabels(corr.columns, fontsize=10)

    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            val = corr.values[i, j]
            color = "white" if abs(val) > 0.55 else "black"
            ax.text(j, i, f"{val:.4f}", ha="center", va="center", fontsize=12, color=color)

    fig.colorbar(im, ax=ax, shrink=0.85)
    ax.set_title("日報酬率相關係數熱力圖", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig


class App(tk.Tk):
    def __init__(self, close, returns, corr):
        super().__init__()
        self.title("台股相關係數分析")
        self.geometry("1280x780")
        self.configure(bg="#f0f2f6")
        self.close = close
        self.returns = returns
        self.corr = corr

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Microsoft JhengHei", 18, "bold"), foreground="#1f2937", background="#f0f2f6")
        style.configure("Sub.TLabel", font=("Microsoft JhengHei", 10), foreground="#6b7280", background="#f0f2f6")
        style.configure("Card.TFrame", background="white", relief="solid", borderwidth=1)
        style.configure("CardTitle.TLabel", font=("Microsoft JhengHei", 12, "bold"), foreground="#1f2937", background="white")
        style.configure("Info.TLabel", font=("Microsoft JhengHei", 9), foreground="#9ca3af", background="white")

        self._build_header()
        main_row = ttk.Frame(self, style="Card.TFrame")
        main_row.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        main_row.columnconfigure(0, weight=3)
        main_row.columnconfigure(1, weight=2)
        main_row.rowconfigure(0, weight=1)

        left_panel = ttk.Frame(main_row, style="Card.TFrame")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self._build_heatmap_panel(left_panel)

        right_panel = ttk.Frame(main_row, style="Card.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_panel.rowconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        self._build_price_panel(right_panel)
        self._build_return_panel(right_panel)

        self._build_footer(corr)

    def _build_header(self):
        header = tk.Frame(self, bg="#f0f2f6")
        header.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(header, text="📊 台股相關係數分析", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="資料來源：Yahoo Finance ｜ 2026/01/01 至今", style="Sub.TLabel").pack(anchor="w")

    def _build_heatmap_panel(self, parent):
        title = ttk.Label(parent, text="相關係數熱力圖", style="CardTitle.TLabel")
        title.pack(anchor="w", padx=12, pady=(10, 0))

        fig = build_heatmap_figure(self.corr)
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_price_panel(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", relief="solid", borderwidth=1)
        card.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)

        header_frame = tk.Frame(card, bg="white")
        header_frame.pack(fill="x", padx=12, pady=(8, 0))
        ttk.Label(header_frame, text="收盤價（近 30 日）", style="CardTitle.TLabel").pack(side="left")

        tree = ttk.Treeview(card, columns=list(self.close.columns), show="headings", height=8)
        for col in list(self.close.columns):
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="e")
        vsb = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        vsb.pack(side="right", fill="y", pady=5)

        for idx, row in self.close.tail(30).iterrows():
            tree.insert("", "end", values=[f"{v:.2f}" for v in row])

    def _build_return_panel(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", relief="solid", borderwidth=1)
        card.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)

        header_frame = tk.Frame(card, bg="white")
        header_frame.pack(fill="x", padx=12, pady=(8, 0))
        ttk.Label(header_frame, text="日報酬率（近 30 日）", style="CardTitle.TLabel").pack(side="left")

        tree = ttk.Treeview(card, columns=list(self.returns.columns), show="headings", height=8)
        for col in list(self.returns.columns):
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="e")
        vsb = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
        vsb.pack(side="right", fill="y", pady=5)

        for idx, row in self.returns.tail(30).iterrows():
            tree.insert("", "end", values=[f"{v:.2%}" for v in row])

    def _build_footer(self, corr):
        footer = tk.Frame(self, bg="#f0f2f6")
        footer.pack(fill="x", padx=20, pady=(0, 12))

        content = tk.Frame(footer, bg="white", relief="solid", borderwidth=1)
        content.pack(fill="x")

        info_frame = tk.Frame(content, bg="white")
        info_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(info_frame, text="相關係數矩陣", style="CardTitle.TLabel").pack(anchor="w")

        table_frame = tk.Frame(info_frame, bg="white")
        table_frame.pack(fill="x", pady=(5, 0))

        names = list(corr.columns)
        for i, name in enumerate(names):
            tk.Label(table_frame, text=name, font=("Microsoft JhengHei", 9, "bold"),
                     bg="#f8f9fa", width=8, relief="ridge").grid(row=0, column=i + 1, sticky="ew")
            tk.Label(table_frame, text=name, font=("Microsoft JhengHei", 9, "bold"),
                     bg="#f8f9fa", width=8, relief="ridge").grid(row=i + 1, column=0, sticky="ew")
            for j, name2 in enumerate(names):
                val = corr.iloc[i, j]
                bg_color = "#e74c3c" if val > 0.7 else ("#f39c12" if val > 0.4 else "#ecf0f1")
                fg_color = "white" if val > 0.4 else "#2c3e50"
                tk.Label(table_frame, text=f"{val:.4f}", font=("Consolas", 9),
                         bg=bg_color, fg=fg_color, width=10, relief="ridge").grid(row=i + 1, column=j + 1, sticky="ew")

        info_text = (
            "💡 解讀：相關係數越接近 1 表示走勢越同步，"
            "越接近 -1 表示走勢相反，接近 0 則無關。"
        )
        ttk.Label(info_frame, text=info_text, style="Sub.TLabel", background="white").pack(anchor="w", pady=(8, 0))


def main():
    print("正在下載股價資料...")
    close, returns, corr = load_data()
    print("資料下載完成！")
    App(close, returns, corr).mainloop()


if __name__ == "__main__":
    main()
