import os
import time

def find_recent(paths):
    now = time.time()
    for base in paths:
        if not os.path.exists(base): continue
        for root, dirs, files in os.walk(base):
            if 'node_modules' in dirs: dirs.remove('node_modules')
            if '.venv' in dirs: dirs.remove('.venv')
            if '.gemini' in root and 'system_generated' in root: continue
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    p = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(p)
                        if now - mtime < 1800: # last 30 minutes
                            print(f"{p} ({time.ctime(mtime)})")
                    except: pass

find_recent([r'C:\Users\admin\OneDrive\Documents', r'C:\Users\admin\Downloads', r'C:\Users\admin\Desktop'])
