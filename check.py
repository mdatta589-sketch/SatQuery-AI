def check_brackets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    stack = []
    line_no = 1
    for char in text:
        if char == '\n':
            line_no += 1
        elif char in '{[(':
            stack.append((char, line_no))
        elif char in ']})':
            if not stack:
                return f"Unmatched {char} at line {line_no}"
            top, top_line = stack.pop()
            if (top == '{' and char != '}') or \
               (top == '[' and char != ']') or \
               (top == '(' and char != ')'):
                return f"Mismatched {char} at line {line_no} (expected closing for {top} from line {top_line})"
    if stack:
        top, top_line = stack.pop()
        return f"Unclosed {top} from line {top_line}"
    return "Brackets balanced"

print(check_brackets('frontend/app.js'))
