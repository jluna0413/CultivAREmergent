from collections import defaultdict
from app.fastapi_app import app

def check_duplicate_prefixes():
    routes_by_prefix = defaultdict(list)
    for route in app.routes:
        routes_by_prefix[route.path.rsplit('/', 1)[0]].append(route.path)

    duplicates = {prefix: routes for prefix, routes in routes_by_prefix.items() if len(routes) > 1 and prefix}
    
    if duplicates:
        print("Duplicate prefixes found:")
        for prefix, routes in duplicates.items():
            print(f"  Prefix: {prefix}")
            for route in routes:
                print(f"    - {route}")
        return False
    else:
        print("No duplicate prefixes found.")
        return True

if __name__ == "__main__":
    check_duplicate_prefixes()
