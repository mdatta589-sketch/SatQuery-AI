import quickjs
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()
context = quickjs.Context()
try:
    context.eval(js)
    print("Syntax OK")
except quickjs.QuickJSSyntaxError as e:
    print(f"Syntax Error: {e}")
except Exception as e:
    print(f"Other Error: {e}")
