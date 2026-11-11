import os
import sys
import types

# Ensure current directory is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure parent directory is also on sys.path if available
parent_dir = os.path.dirname(backend_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Ensure 'backend' module is recognized when running standalone in backend/
try:
    import backend.app.main
except (ModuleNotFoundError, ImportError):
    import app
    b = types.ModuleType("backend")
    b.app = app
    sys.modules["backend"] = b
    sys.modules["backend.app"] = app

from backend.app.main import app
