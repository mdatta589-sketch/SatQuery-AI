with open('backend/app/api/catalog.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

old_search = r"""        search = catalog.search\(
            collections=\[request.collection\],
            bbox=request.bbox,
            datetime=datetime_range,
            query=\{"eo:cloud_cover": \{"lt": request.max_cloud_cover\}\},
            max_items=request.limit,
            sortby=\[\{"field": "datetime", "direction": "desc"\}\]
        \)"""

new_search = """        query_params = {}
        if request.collection == "sentinel-2-l2a":
            query_params["eo:cloud_cover"] = {"lt": request.max_cloud_cover}
            
        search_args = {
            "collections": [request.collection],
            "bbox": request.bbox,
            "datetime": datetime_range,
            "max_items": request.limit,
            "sortby": [{"field": "datetime", "direction": "desc"}]
        }
        if query_params:
            search_args["query"] = query_params
            
        search = catalog.search(**search_args)"""

content = re.sub(old_search, new_search, content)
with open('backend/app/api/catalog.py', 'w', encoding='utf8') as f:
    f.write(content)
print("Updated catalog search to support non-optical collections")
