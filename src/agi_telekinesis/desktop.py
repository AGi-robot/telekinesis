"""Opt-in desktop actions, each authorized by the caller."""
from collections.abc import Callable


class Desktop:
    def __init__(self, approve: Callable[[str], bool]):
        import pyautogui
        self.gui = pyautogui
        self.approve = approve
        self.gui.FAILSAFE = True

    def screen_size(self) -> dict:
        size = self.gui.size()
        return {"width": size.width, "height": size.height}

    def click(self, x: int, y: int) -> dict:
        if type(x) is not int or type(y) is not int or not self.gui.onScreen(x, y):
            raise ValueError("coordinates must be integers within the primary screen")
        if not self.approve(f"Click screen coordinates ({x}, {y})?"):
            return {"status": "denied"}
        self.gui.click(x, y)
        return {"status": "clicked", "x": x, "y": y}

    def type_text(self, text: str) -> dict:
        if not isinstance(text, str) or len(text) > 200 or not text.isascii() or any(ord(c) < 32 or ord(c) > 126 for c in text):
            raise ValueError("text must be at most 200 printable ASCII characters")
        if not self.approve(f"Type into the focused window: {text!r}?"):
            return {"status": "denied"}
        self.gui.write(text, interval=0.01)
        return {"status": "typed", "characters": len(text)}
