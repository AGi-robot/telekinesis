# Telekinesis

An experimental browser practice environment for testing an LLM's ability to observe a form, enter text and click a button. It uses a fresh temporary Chromium instance with a built-in page and network requests blocked. It does not connect to your normal browser, desktop, files, or accounts.

```bash
pip install -e .
python -m playwright install chromium
```

Use `PracticeBrowser` as a context manager, then call `observe`, `type_message` and `click_submit`. Agentic can expose these actions to a model for a small closed exercise.

For an opt-in desktop experiment, install `pip install -e '.[desktop]'`. `agi_telekinesis.desktop.Desktop` exposes primary-screen size, coordinate clicks, and printable ASCII typing. Each action requires an approval callback. PyAutoGUI requires a supported graphical desktop (Linux commonly needs X11); moving the pointer to a screen corner triggers its fail-safe. The caller supplies coordinates: this version does not interpret screenshots or support real browser navigation.
