"""An isolated browser exercise for testing model tool use."""
from playwright.sync_api import sync_playwright

PAGE = """<!doctype html><html><body><h1>Practice form</h1>
<label for="message">Message</label><input id="message" maxlength="200">
<button id="submit" onclick="document.getElementById('result').textContent = document.getElementById('message').value">Submit</button>
<p id="result"></p></body></html>"""


class PracticeBrowser:
    """Own a temporary browser containing one local practice form."""

    def __init__(self, *, headless: bool = True):
        self.headless = headless

    def __enter__(self):
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            self.page.route("**/*", lambda route: route.abort())
            self.page.set_content(PAGE)
        except BaseException:
            if hasattr(self, "browser"):
                self.browser.close()
            self.playwright.stop()
            raise
        return self

    def __exit__(self, *args):
        try:
            self.browser.close()
        finally:
            self.playwright.stop()

    def observe(self) -> dict[str, str]:
        return {"page": "Practice form", "input_id": "message", "input_value": self.page.locator("#message").input_value(),
                "button_id": "submit", "result": self.page.locator("#result").inner_text()}

    def type_message(self, text: str) -> dict[str, str]:
        if not isinstance(text, str) or len(text) > 200:
            raise ValueError("text must be a string of at most 200 characters")
        self.page.locator("#message").fill(text)
        return self.observe()

    def click_submit(self) -> dict[str, str]:
        self.page.locator("#submit").click()
        return self.observe()
