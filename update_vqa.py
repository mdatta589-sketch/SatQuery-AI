with open('backend/app/services/change_service.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

new_vqa_method = """    def answer_change_vqa(self, image_before_id: str, image_after_id: str, question: str, aoi: dict | None = None) -> dict:
        import time
        start_time = time.time()
        
        # 1. Run change analysis
        analysis_result = self.analyze_change(image_before_id, image_after_id, aoi)
        
        if analysis_result.get("status") != "success":
            return {
                "task": "change_vqa",
                "status": "error",
                "question": question,
                "error": analysis_result.get("error", "Change Analysis failed before VQA could be answered."),
                "execution": {
                    "task": "change_vqa",
                    "model": "change_interpreter",
                    "provider": "local",
                    "status": "error"
                }
            }
            
        # 2. Extract statistics
        change_pct = analysis_result.get("change_percentage", 0.0)
        changed_pixels = analysis_result.get("changed_pixel_count", 0)
        valid_pixels = analysis_result.get("total_valid_pixel_count", 0)
        method = analysis_result.get("method", "Baseline Raster Difference")
        threshold = analysis_result.get("threshold", 0.25)
        
        # Format dates from IDs (e.g. S2B_MSIL2A_20250328T050659_...)
        def extract_date(scene_id):
            parts = scene_id.split('_')
            for part in parts:
                if len(part) >= 8 and part[:8].isdigit() and (len(part) == 8 or part[8] == 'T'):
                    return f"{part[:4]}-{part[4:6]}-{part[6:8]}"
            return scene_id
            
        before_date = extract_date(image_before_id)
        after_date = extract_date(image_after_id)
        
        # 3. Generate natural language answer
        # Very simple intent handling
        q_lower = question.lower()
        if "how much" in q_lower or "percentage" in q_lower or "area" in q_lower:
            answer = f"Approximately {change_pct:.2f}% of the valid area was classified as changed between {before_date} and {after_date}."
        elif "where" in q_lower or "location" in q_lower:
            answer = f"The detected changes are highlighted in red on the map within the selected Area of Interest. A total of {changed_pixels:,} pixels changed."
        elif "significant" in q_lower:
            if change_pct > 5.0:
                answer = f"Yes, there is significant change. Approximately {change_pct:.2f}% of the area changed."
            elif change_pct > 1.0:
                answer = f"There is moderate change. Approximately {change_pct:.2f}% of the area changed."
            else:
                answer = f"There is no significant change. Only {change_pct:.2f}% of the area changed."
        else:
            answer = f"The selected AOI shows detectable change between {before_date} and {after_date}. Approximately {change_pct:.2f}% of the valid area was classified as changed using the {method.replace('_', ' ')} method."
            
        exec_time = int((time.time() - start_time) * 1000)
        
        return {
            "task": "change_vqa",
            "status": "success",
            "question": question,
            "answer": answer,
            "change_percentage": change_pct,
            "changed_pixel_count": changed_pixels,
            "total_valid_pixel_count": valid_pixels,
            "threshold": threshold,
            "method": method,
            "before_scene": f"Sentinel-2 — {before_date}",
            "after_scene": f"Sentinel-2 — {after_date}",
            "evidence": analysis_result.get("evidence", []),
            "execution_time_ms": exec_time,
            "execution": {
                "task": "change_vqa",
                "model": "change_interpreter",
                "provider": "local",
                "status": "success"
            }
        }"""

content = re.sub(r"    def answer_change_vqa\(self, image_before_id: str, image_after_id: str, question: str, aoi: dict \| None = None\) -> dict:.*?(?=\n\n|\Z)", new_vqa_method, content, flags=re.DOTALL)

with open('backend/app/services/change_service.py', 'w', encoding='utf8') as f:
    f.write(content)
print("UPDATED BACKEND METHOD")
