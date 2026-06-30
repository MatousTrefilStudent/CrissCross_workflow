"""Desktopová GUI aplikace pro hru Piškvorky (CrissCross).

Postaveno nad jednoduchým API z modules/api.py, nepracuje přímo
s Board / Player / Game.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

try:
    from modules.api import GameAPI
except ImportError:  # pragma: no cover - allows direct execution as a script
    from modules.api import GameAPI


class CrissCrossGUI:
    """Tkinter okno se hrou Piškvorky."""

    def __init__(self, root: tk.Tk, size: int = 15):
        self.root = root
        self.size = size
        self.api = GameAPI(size)

        self.root.title("Piškvorky (CrissCross)")
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

        self._build_widgets()
        self._update_status()

    # --- Sestavení UI ----------------------------------------------------

    def _build_widgets(self) -> None:
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)

        self._render_board()

        controls = tk.Frame(self.root)
        controls.pack(pady=(0, 10))

        self.status_label = tk.Label(controls, text="", font=("Courier", 12))
        self.status_label.pack(side=tk.LEFT, padx=10)

        save_btn = tk.Button(controls, text="Uložit", command=self._on_save)
        save_btn.pack(side=tk.LEFT, padx=10)

        load_btn = tk.Button(controls, text="Načíst", command=self._on_load)
        load_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = tk.Button(controls, text="Nová hra", command=self._on_reset)
        reset_btn.pack(side=tk.LEFT, padx=10)

    # --- Obsluha událostí --------------------------------------------------

    def _on_cell_click(self, x: int, y: int) -> None:
        if self.api.is_game_over():
            return

        result = self.api.move(x, y)
        if not result["success"]:
            messagebox.showinfo(
                "Neplatný tah", "Na tomto políčku už je tah, nebo je mimo desku."
            )
            return

        self._refresh_board()
        self._update_status(result)

        if result["winner"]:
            messagebox.showinfo("Konec hry", f"Vyhrál hráč {result['winner']}!")
        elif result["is_full"]:
            messagebox.showinfo("Konec hry", "Remíza, deska je plná.")

    def _on_reset(self) -> None:
        size = self._prompt_board_size()
        if size is None:
            return

        self.api.new_game(size)
        self._render_board()
        self._update_status()

    def _on_save(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile="savegame.json",
            filetypes=[("JSON soubory", "*.json"), ("Všechny soubory", "*.*")],
        )
        if not path:
            return

        if self.api.save_game(path):
            messagebox.showinfo("Uloženo", f"Hra uložena do {path}")
        else:
            messagebox.showerror("Chyba", "Nepodařilo se uložit hru.")

    def _on_load(self) -> None:
        path = filedialog.askopenfilename(
            defaultextension=".json",
            initialfile="savegame.json",
            filetypes=[("JSON soubory", "*.json"), ("Všechny soubory", "*.*")],
        )
        if not path:
            return

        if self.api.load_game(path):
            self._render_board()
            self._update_status()
            messagebox.showinfo("Načteno", f"Hra načtena z {path}")
        else:
            messagebox.showerror("Chyba", "Nepodařilo se načíst hru.")

    # --- Pomocné metody ----------------------------------------------------

    def _prompt_board_size(self) -> int | None:
        current_size = self.api.get_size()
        size = simpledialog.askinteger(
            "Nová hra",
            "Zadejte velikost hracího pole:",
            initialvalue=current_size,
            minvalue=3,
            maxvalue=25,
        )
        if size is None:
            return None
        return size

    def _render_board(self) -> None:
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        size = self.api.get_size()
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

        for x in range(size):
            for y in range(size):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    width=2,
                    height=1,
                    font=("Courier", 10, "bold"),
                    command=lambda x=x, y=y: self._on_cell_click(x, y),
                )
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

        self._refresh_board()

    def _refresh_board(self) -> None:
        size = self.api.get_size()
        for x in range(size):
            for y in range(size):
                cell = self.api.get_cell(x, y)
                btn = self.buttons[x][y]
                if cell is None:
                    btn.config(text="", state="normal")
                else:
                    btn.config(text=cell, state="disabled")

    def _update_status(self, result: dict = None) -> None:
        if result and result.get("winner"):
            text = f"Vyhrál hráč {result['winner']}"
        elif result and result.get("is_full"):
            text = "Remíza"
        else:
            text = f"Na tahu: {self.api.get_current_player()}"
        self.status_label.config(text=text)


def main() -> None:
    root = tk.Tk()
    CrissCrossGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
