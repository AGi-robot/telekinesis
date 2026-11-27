from unittest.mock import Mock, patch

import pytest

from agi_telekinesis import PracticeBrowser


def test_failed_browser_setup_stops_playwright_even_when_close_fails():
    playwright = Mock()
    playwright.chromium.launch.return_value.new_page.side_effect = RuntimeError('page failed')
    playwright.chromium.launch.return_value.close.side_effect = RuntimeError('close failed')
    with patch('agi_telekinesis.sync_playwright') as start:
        start.return_value.start.return_value = playwright
        with pytest.raises(RuntimeError):
            PracticeBrowser().__enter__()
    playwright.stop.assert_called_once()
