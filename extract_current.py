import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# I will replace from "btnQueryPanel.addEventListener('click', async () => {" 
# to the end of the btnQueryPanel block.
match = re.search(r"if \(btnQueryPanel\) \{\s*btnQueryPanel\.addEventListener\('click', async \(\) => \{(.*?)(?=\n    const btnExportPdf =)", content, flags=re.DOTALL)
if match:
    with open('current_handler.js', 'w', encoding='utf8') as out:
        out.write(match.group(0))
    print("SAVED CURRENT HANDLER")
