import pytest
import os
import tempfile
from main import generate_bureau_page, generate_home_page, generate_event_page, generate_events_page

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        old_cwd = os.getcwd()
        os.chdir(tmpdirname)
        os.makedirs('assets/md', exist_ok=True)
        os.makedirs('public', exist_ok=True)
        yield tmpdirname
        os.chdir(old_cwd)

def test_generate_bureau_page(temp_dir):
    csv_content = "prénom,nom,fonction,email\nJohn,Doe,President,john@example.com"
    csv_file = "test_bureau.csv"
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write(csv_content)

    output_file = "bureau.html"
    generate_bureau_page(csv_file, output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "John Doe" in content
        assert "President" in content
        assert "john@example.com" in content

def test_generate_home_page(temp_dir):
    with open(os.path.join("assets", "md", "event-1.md"), "w", encoding="utf-8") as f:
        f.write("---\ntitle: Test Event\ndate: 2023-05-01\n---\nTest content")

    output_file = "index.html"
    generate_home_page(output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "Test Event" in content
        assert "2023-05-01" in content

def test_generate_event_page(temp_dir):
    event = {
        "title": "Test Event",
        "date": "2023-05-01",
        "content": "<p>Test content</p>",
        "image": "test_image.webp"
    }
    output_file = "event-1.html"
    generate_event_page(event, output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "Test Event" in content
        assert "2023-05-01" in content
        assert "Test content" in content
        assert "test_image.webp" in content

def test_generate_events_page(temp_dir):
    with open(os.path.join("assets", "md", "event-1.md"), "w", encoding="utf-8") as f:
        f.write("---\ntitle: Test Event 1\ndate: 2023-05-01\n---\nTest content 1")
    with open(os.path.join("assets", "md", "event-2.md"), "w", encoding="utf-8") as f:
        f.write("---\ntitle: Test Event 2\ndate: 2023-05-02\n---\nTest content 2")

    output_file = "evenements.html"
    generate_events_page(output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "Test Event 1" in content
        assert "Test Event 2" in content
        assert "2023-05-01" in content
        assert "2023-05-02" in content
