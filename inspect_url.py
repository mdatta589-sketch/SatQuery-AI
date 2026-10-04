with open('frontend/app.js', 'r', encoding='utf-8') as f:
    for line in f:
        if 'vqa/query' in line:
            print(repr(line.strip()))
