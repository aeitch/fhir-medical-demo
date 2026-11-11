import os
import sys
import types
import traceback

try:
    # 1. Determine paths
    api_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(api_dir)

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

    if "backend" not in sys.modules:
        b = types.ModuleType("backend")
        b.__path__ = [backend_root]
        sys.modules["backend"] = b
    else:
        b = sys.modules["backend"]
        if not hasattr(b, "__path__"):
            b.__path__ = [backend_root]

    from backend.app.main import app

except Exception as err:
    err_msg = str(err)
    tb = traceback.format_exc()
    
    # Minimal fallback ASGI app to report startup errors directly in the browser
    async def app(scope, receive, send):
        if scope["type"] == "http":
            response_body = f'{{"error": "Startup failed", "detail": "{err_msg}", "traceback": {repr(tb)}}}'.encode("utf-8")
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"content-length", str(len(response_body)).encode("utf-8")],
                    [b"access-control-allow-origin", b"*"],
                ],
            })
            await send({
                "type": "http.response.body",
                "body": response_body,
            })
