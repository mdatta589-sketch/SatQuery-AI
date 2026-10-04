with open('frontend/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

bad_block = '''  if (dataset.is_analysis) {
      targetList = document.getElementById('list-analysis');
      document.getElementById('group-analysis').style.display = 'block';
      document.getElementById('group-stac').style.display = 'block';
  } else {
      targetList = document.getElementById('list-uploaded');
      document.getElementById('group-uploaded').style.display = 'block';
  }'''

good_block = '''  if (dataset.is_analysis) {
      targetList = document.getElementById('list-analysis');
      document.getElementById('group-analysis').style.display = 'block';
  } else if (dataset.is_stac) {
      targetList = document.getElementById('list-stac');
      document.getElementById('group-stac').style.display = 'block';
  } else {
      targetList = document.getElementById('list-uploaded');
      document.getElementById('group-uploaded').style.display = 'block';
  }'''

code = code.replace(bad_block, good_block)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
