from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_streamlit_app_renders_without_secrets_or_api_calls():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    assert app.title[0].value == "Resume Review Assistant"
    assert app.get("file_uploader")
    assert app.get("text_area")