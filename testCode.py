import colour

import numpy as np




# Assuming sRGB encoded colour values.
RGB = np.array([255.0, 255, 255])

# Conversion to tristimulus values.
XYZ = colour.sRGB_to_XYZ(RGB / 255)

# Conversion to chromaticity coordinates.
xy = colour.XYZ_to_xy(XYZ)

# Conversion to correlated colour temperature in K.
CCT = colour.xy_to_CCT(xy, 'hernandez1999')
print(CCT)