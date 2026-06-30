"""Desktopová GUI aplikace pro hru Piškvorky (CrissCross).

Postaveno nad jednoduchým API z modules/api.py, nepracuje přímo
s Board / Player / Game.
"""

import tkinter as tk
from tkinter import messagebox

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
        board_frame = tk.Frame(self.root)
        board_frame.pack(padx=10, pady=10)

        for x in range(self.size):
            for y in range(self.size):
                btn = tk.Button(
                    board_frame,
                    text="",
                    width=2,
                    height=1,
                    font=("Courier", 10, "bold"),
                    command=lambda x=x, y=y: self._on_cell_click(x, y),
                )
                btn.grid(row=x, column=y)
                self.buttons[x][y] = btn

        controls = tk.Frame(self.root)
        controls.pack(pady=(0, 10))

        self.status_label = tk.Label(controls, text="", font=("Courier", 12))
        self.status_label.pack(side=tk.LEFT, padx=10)

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

        self.buttons[x][y].config(text=result["player"], state="disabled")
        self._update_status(result)

        if result["winner"]:
            messagebox.showinfo("Konec hry", f"Vyhrál hráč {result['winner']}!")
        elif result["is_full"]:
            messagebox.showinfo("Konec hry", "Remíza, deska je plná.")

    def _on_reset(self) -> None:
        self.api.reset()
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state="normal")
        self._update_status()

    # --- Pomocné metody ----------------------------------------------------

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
