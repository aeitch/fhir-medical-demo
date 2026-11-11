import os
import sys

# Ensure repository root is on sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from backend.app.main import app

# Vercel's Python runtime will find 'app'
