# tests/test_uploader.py
import pytest
from unittest.mock import AsyncMock
from src.uploader import FileUploader

@pytest.mark.asyncio
async def test_upload_files():
    mock_bot = AsyncMock()
    uploader = FileUploader(mock_bot, -1002338060250, 4342)
    await uploader.upload_files("tests/test_files")
    mock_bot.send_document.assert_called()
