import random
import tkinter as tk
from tkinter import ttk, messagebox


class GuessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("数字当てゲーム（tkinter版）")
        self.root.resizable(False, False)

        self.answer = None
        self.max_n = None
        self.trycount = 0

        # ===== 難易度エリア =====
        frm_top = ttk.LabelFrame(root, text="難易度を選べ（数値を入れて開始）")
        frm_top.grid(row=0, column=0, padx=12, pady=12, sticky="ew")

        self.var_mode = tk.StringVar(value="")
        ttk.Label(
            frm_top,
            text="1:簡単  2:普通  3:難しい  4:鬼 / 0:鬼畜（9999） / 10以下なら×500",
        ).grid(row=0, column=0, columnspan=6, sticky="w", pady=(2, 6))

        ttk.Label(frm_top, text="モード数値:").grid(row=1, column=0, sticky="e")
        ent = ttk.Entry(frm_top, textvariable=self.var_mode, width=8)
        ent.grid(row=1, column=1, sticky="w", padx=(4, 8))
        ent.bind("<Return>", lambda e: self.start_game())

        for i, (label, val) in enumerate(
            [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("0", 0)], start=2
        ):
            ttk.Button(
                frm_top,
                text=label,
                width=3,
                command=lambda v=val: self.quick_set_mode(v),
            ).grid(row=1, column=i, padx=2)

        ttk.Button(frm_top, text="開始", command=self.start_game).grid(
            row=1, column=7, padx=(8, 0)
        )

        # ===== プレイエリア =====
        frm_play = ttk.LabelFrame(root, text="勝負")
        frm_play.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="ew")

        self.lbl_range = ttk.Label(frm_play, text="未開始")
        self.lbl_range.grid(row=0, column=0, columnspan=2, sticky="w", pady=(2, 6))

        ttk.Label(frm_play, text="予想:").grid(row=1, column=0, sticky="e")
        self.var_guess = tk.StringVar()
        self.ent_guess = ttk.Entry(
            frm_play, textvariable=self.var_guess, width=10, state="disabled"
        )
        self.ent_guess.grid(row=1, column=1, sticky="w")
        self.ent_guess.bind("<Return>", lambda e: self.submit_guess())

        self.btn_submit = ttk.Button(
            frm_play, text="送信", command=self.submit_guess, state="disabled"
        )
        self.btn_submit.grid(row=1, column=2, padx=(8, 0))

        self.lbl_feedback = ttk.Label(frm_play, text="―")
        self.lbl_feedback.grid(row=2, column=0, columnspan=3, sticky="w", pady=(6, 2))

        self.lbl_tries = ttk.Label(frm_play, text="回数: 0")
        self.lbl_tries.grid(row=3, column=0, columnspan=3, sticky="w")

        ttk.Button(frm_play, text="リセット", command=self.reset_all).grid(
            row=4, column=2, pady=(8, 2), sticky="e"
        )

    # ===== ロジック =====
    def quick_set_mode(self, v: int):
        self.var_mode.set(str(v))
        self.start_game()

    def resolve_max(self, mode_int: int) -> int:
        if mode_int == 1:
            return 50
        elif mode_int == 2:
            return 100
        elif mode_int == 3:
            return 500
        elif mode_int == 4:
            return 1000
        elif mode_int == 0:
            self.lbl_feedback.config(text="ん？びびってんのｗ 鬼畜コース決定ｗ")
            return 9999
        elif mode_int <= 10:
            self.lbl_feedback.config(text="あーえらんじゃったかｗ（×500発動）")
            return mode_int * 500
        else:
            raise ValueError("なめてんの？")

    def start_game(self):
        try:
            mode_int = int(self.var_mode.get())
        except ValueError:
            messagebox.showwarning("注意", "モードは数字を入れてね")
            return

        try:
            self.max_n = self.resolve_max(mode_int)
        except ValueError as e:
            messagebox.showerror("エラー", str(e))
            return

        self.answer = random.randint(1, self.max_n)
        self.trycount = 0
        self.lbl_range.config(text=f"1 〜 {self.max_n} のどれかだ。かかってこい。")
        self.lbl_feedback.config(text="―")
        self.lbl_tries.config(text="回数: 0")
        self.ent_guess.config(state="normal")
        self.btn_submit.config(state="normal")
        self.var_guess.set("")
        self.ent_guess.focus_set()

    def submit_guess(self):
        if self.answer is None or self.max_n is None:
            return
        try:
            g = int(self.var_guess.get())
        except ValueError:
            self.lbl_feedback.config(text="数字入れろや")
            return

        if not (1 <= g <= self.max_n):
            self.lbl_feedback.config(text=f"範囲外。1〜{self.max_n} だぞ")
            return

        self.trycount += 1
        self.lbl_tries.config(text=f"回数: {self.trycount}")

        if g == self.answer:
            self.lbl_feedback.config(text=f"正解！ {self.trycount} 回で当てたな！")
            messagebox.showinfo(
                "勝ち", f"正解：{self.answer}\n{self.trycount}回でフィニッシュ！"
            )
            # 次ラウンド用に入力だけ止める（モード変えずに続行できる）
            self.ent_guess.config(state="disabled")
            self.btn_submit.config(state="disabled")
        elif g < self.answer:
            self.lbl_feedback.config(text="もっとうえ！")
        else:
            self.lbl_feedback.config(text="もっとした！")

        self.var_guess.set("")

    def reset_all(self):
        self.answer = None
        self.max_n = None
        self.trycount = 0
        self.var_mode.set("")
        self.var_guess.set("")
        self.lbl_range.config(text="未開始")
        self.lbl_feedback.config(text="―")
        self.lbl_tries.config(text="回数: 0")
        self.ent_guess.config(state="disabled")
        self.btn_submit.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    # 見た目ちょい整える（プラットフォーム依存で無視されてもOK）
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    app = GuessApp(root)
    root.mainloop()
