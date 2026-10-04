import sys
sys.path.insert(0, 'backend')
from app.main import app
from fastapi.routing import APIRouter

def print_routes(routes, prefix=""):
    for route in routes:
        if isinstance(route, APIRouter) or hasattr(route, "routes"):
            # If it's a mounted sub-router, recursively print
            print(f"Router mounted at {prefix}{getattr(route, 'path', '')}")
            print_routes(route.routes, prefix + getattr(route, 'path', ''))
        else:
            print(f"{getattr(route, 'methods', [])} {prefix}{getattr(route, 'path', route.path)}")

print("=== REGISTERED ROUTES ===")
print_routes(app.routes)
print("=========================")
