import sys
import os

# Add the parent directory (project root) to sys.path so Python can find app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test if home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200


def test_shorten_url(client):
    """Test URL shortening functionality."""
    response = client.post("/shorten", data={"url": "https://example.com"})
    assert response.status_code == 200
    assert b"Short URL" in response.data  # Ensure "Short URL" is in the response


def test_redirect(client):
    """Test if shortened URL redirects properly."""
    response = client.post("/shorten", data={"url": "https://example.com"})
    assert response.status_code == 200

    # Extract short URL from response
    short_url = response.data.decode().split('href="/')[1].split('"')[0]
    
    redirect_response = client.get(f"/{short_url}", follow_redirects=False)
    assert redirect_response.status_code == 302  # 302 Found (Redirect)
    assert redirect_response.headers["Location"] == "https://example.com"
