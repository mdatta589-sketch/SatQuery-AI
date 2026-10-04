import os

for root, _, files in os.walk('backend'):
    for f in files:
        if f.endswith('.py'):
            with open(os.path.join(root, f), 'r', encoding='utf8') as file:
                if 'I can currently analyze' in file.read():
                    print(f"FOUND IN {os.path.join(root, f)}")
