"""
Weekly Digest entry point.
Run manually or via GitHub Actions every Sunday.
"""
from src.digest import build_and_send_digest

if __name__ == "__main__":
    build_and_send_digest()
