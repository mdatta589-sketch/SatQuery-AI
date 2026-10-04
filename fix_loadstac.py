with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

old_code = """        selectLayer(datasetMeta.id);
        document.getElementById('header-status').textContent = `STAC Scene loaded: ${datasetMeta.name}`;
        updateAnalysisSceneDropdown();
    } catch (e) {"""

new_code = """        selectLayer(datasetMeta.id);
        document.getElementById('header-status').textContent = `STAC Scene loaded: ${datasetMeta.name}`;
        updateAnalysisSceneDropdown();
        updateChangeAnalysisDropdowns();
    } catch (e) {"""

content = content.replace(old_code, new_code)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED loadStacScene dropdown update")
