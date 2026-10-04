import os
import time
for root, dirs, files in os.walk('.'):
    if 'node_modules' in dirs: dirs.remove('node_modules')
    if '.git' in dirs: dirs.remove('.git')
    if 'temp' in dirs: dirs.remove('temp')
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            path = os.path.join(root, f)
            print(f"{path} - {time.ctime(os.path.getmtime(path))}")
