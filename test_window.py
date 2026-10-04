import rasterio
from rasterio.windows import Window, bounds
from rasterio.transform import from_origin

global_transform = from_origin(100000, 200000, 10, 10) # x=100000, y=200000, 10m pixels
window = Window(col_off=100, row_off=200, width=50, height=50)

# The window's own transform
window_transform = rasterio.windows.transform(window, global_transform)
print("Window transform origin:", window_transform.c, window_transform.f)

# Correct way to get bounds of the window in global coords:
correct_bounds = bounds(window, global_transform)
print("Correct bounds:", correct_bounds)

# What if we pass window_transform instead?
wrong_bounds = bounds(window, window_transform)
print("Wrong bounds:", wrong_bounds)

