with open('frontend/app.js', 'r', encoding='utf8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "if (btnQueryPanel) {" in line and "btnQueryPanel.addEventListener('click', async () => {" in lines[i+1]:
        start_idx = i
        break

if start_idx != -1:
    brace_count = 0
    for i in range(start_idx, len(lines)):
        brace_count += lines[i].count('{')
        brace_count -= lines[i].count('}')
        if brace_count == 0 and i > start_idx + 2:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    with open('frontend/app.js', 'w', encoding='utf8') as f:
        f.writelines(lines[:start_idx])
        f.write("    // --- NEW BTNQUERYPANEL HANDLER INJECTED HERE ---\n")
        f.writelines(lines[end_idx+1:])
    print(f"REMOVED BLOCK FROM {start_idx} to {end_idx}")
else:
    print("FAILED TO FIND BLOCK")
