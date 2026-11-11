import os
import sys
import types

# 1. Determine paths
api_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(api_dir)

# Add search paths
for p in [base_dir, os.path.dirname(base_dir)]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

# 2. Locate where 'app' lives
if os.path.isdir(os.path.join(base_dir, "app")):
    backend_root = base_dir
elif os.path.isdir(os.path.join(base_dir, "backend", "app")):
    backend_root = os.path.join(base_dir, "backend")
else:
    backend_root = base_dir

# 3. Create 'backend' namespace module so 'from backend.app...' resolves cleanly
if "backend" not in sys.modules:
    b = types.ModuleType("backend")
    b.__path__ = [backend_root]
    sys.modules["backend"] = b
else:
    b = sys.modules["backend"]
    if not hasattr(b, "__path__"):
        b.__path__ = [backend_root]

from backend.app.main import app
