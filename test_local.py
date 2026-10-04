import sys
sys.path.append('backend')
from app.api.catalog import render_true_color

print("Attempting to render...")
res = render_true_color("S2A_MSIL2A_20230626T095041_N0509_R079_T33TTG_20230626T144004")
print(type(res))
