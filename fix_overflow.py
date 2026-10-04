with open('frontend/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace("body {", "html { overflow: hidden; }\n\nbody {")

with open('frontend/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
