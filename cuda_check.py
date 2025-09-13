import torch
print(torch.cuda.is_available())        # Should print True
print(torch.cuda.get_device_name(0))    # Should print "NVIDIA GeForce RTX 4050"
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.0.8-Q16\\magick.exe"})
