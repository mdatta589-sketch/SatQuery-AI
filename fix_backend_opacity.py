with open('backend/app/services/change_service.py', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace("rgba[dst_mask == 255] = [255, 60, 60, 150]", "rgba[dst_mask == 255] = [255, 40, 40, 200]")

with open('backend/app/services/change_service.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED BACKEND RED OPACITY")
