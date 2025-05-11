"""
Diagnostic script to help debug template rendering issues in the CultivAR application.
"""

import os
import sys
import glob
import json
import datetime

def find_templates():
    """Find all template files in the application."""
    template_dir = os.path.join('app', 'web', 'templates')
    templates = []
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                templates.append(rel_path)
    
    return templates

def find_login_templates():
    """Find all login-related template files."""
    templates = find_templates()
    return [t for t in templates if 'login' in t.lower()]

def find_route_definitions():
    """Find all route definitions in the application."""
    routes_file = os.path.join('app', 'routes', 'routes.py')
    routes = []
    
    if not os.path.exists(routes_file):
        return ["Error: routes.py file not found"]
    
    with open(routes_file, 'r') as f:
        content = f.read()
        
    # Find all @app.route decorators
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '@app.route(' in line:
            route_path = line.split('@app.route(')[1].split(')')[0]
            # Get the function name (next line or next non-empty line)
            func_name = ""
            j = i + 1
            while j < len(lines) and not func_name:
                if 'def ' in lines[j]:
                    func_name = lines[j].split('def ')[1].split('(')[0]
                j += 1
            
            # Find the template being rendered
            template = None
            j = i + 1
            while j < len(lines) and j < i + 20:  # Look at next 20 lines max
                if 'render_template(' in lines[j]:
                    template = lines[j].split('render_template(')[1].split(',')[0].strip("'\"")
                    break
                j += 1
            
            routes.append({
                'path': route_path,
                'function': func_name,
                'template': template
            })
    
    return routes

def check_template_exists(template_path):
    """Check if a template file exists."""
    full_path = os.path.join('app', 'web', 'templates', template_path)
    return os.path.exists(full_path)

def main():
    """Run the diagnostics."""
    print("CultivAR Template Diagnostics")
    print("============================")
    
    # Check template directory
    template_dir = os.path.join('app', 'web', 'templates')
    if not os.path.exists(template_dir):
        print(f"Error: Template directory not found: {template_dir}")
        return
    
    print(f"\nTemplate directory: {os.path.abspath(template_dir)}")
    
    # Find all templates
    templates = find_templates()
    print(f"\nFound {len(templates)} templates:")
    for t in templates:
        print(f"  - {t}")
    
    # Find login templates
    login_templates = find_login_templates()
    print(f"\nFound {len(login_templates)} login-related templates:")
    for t in login_templates:
        print(f"  - {t}")
    
    # Find route definitions
    routes = find_route_definitions()
    print(f"\nFound {len(routes)} route definitions:")
    for r in routes:
        template_status = ""
        if r.get('template'):
            exists = check_template_exists(r['template'])
            template_status = f" -> Template: {r['template']} ({'EXISTS' if exists else 'MISSING'})"
        print(f"  - {r.get('path', 'Unknown')} => {r.get('function', 'Unknown')}{template_status}")
    
    # Check specifically for login route
    login_routes = [r for r in routes if r.get('function') == 'login']
    if login_routes:
        print("\nLogin route details:")
        for r in login_routes:
            template = r.get('template', 'Unknown')
            exists = check_template_exists(template) if template != 'Unknown' else False
            print(f"  - Path: {r.get('path', 'Unknown')}")
            print(f"  - Function: {r.get('function', 'Unknown')}")
            print(f"  - Template: {template} ({'EXISTS' if exists else 'MISSING'})")
            
            if template != 'Unknown' and exists:
                full_path = os.path.join('app', 'web', 'templates', template)
                print(f"  - Full path: {os.path.abspath(full_path)}")
                
                # Check file size
                size = os.path.getsize(full_path)
                print(f"  - File size: {size} bytes")
                
                # Check last modified time
                mtime = os.path.getmtime(full_path)
                print(f"  - Last modified: {datetime.datetime.fromtimestamp(mtime)}")
    else:
        print("\nNo login route found!")

if __name__ == "__main__":
    main()