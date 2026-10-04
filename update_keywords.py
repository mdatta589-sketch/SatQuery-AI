with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

keywords_old = """            const changeKeywords = [
                'compare', 'difference', 'changed', 'changes', 
                'what changed', 'detect changes', 'change between these images', 
                'compare these images', 'how has this area changed', 
                'identify changed areas', 'show changes'
            ];"""
keywords_new = """            const changeKeywords = [
                'compare', 'difference', 'changed', 'changes', 
                'what changed', 'detect changes', 'change between these images', 
                'compare these images', 'how has this area changed', 
                'identify changed areas', 'show changes',
                'where changed', 'where did the change occur',
                'how much changed', 'how much of the area changed',
                'significant change', 'describe changes'
            ];"""

content = content.replace(keywords_old, keywords_new)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("KEYWORDS ADDED")
