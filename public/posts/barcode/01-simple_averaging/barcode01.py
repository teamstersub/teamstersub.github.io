import time

import ffmpeg
import numpy as np
from PIL import Image


# Measure program execution time
start_time = time.time()

# I renamed the downloaded video file to be simpler to work with
filename = 'triumph.webm'

# Get Video info
probe = ffmpeg.probe(filename)
video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
width = int(video_info['width'])
height = int(video_info['height'])

# Use ffmpeg to convert video file to NumPy array
# From https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#convert-video-to-numpy-array
out, _ = (
    ffmpeg
    .input(filename)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run(capture_stdout=True)
)
video = (
    np
    .frombuffer(out, np.uint8)
    .reshape([-1, height, width, 3])
)

# Initialize barcode image as NP array of proper dimensions initialized to all zeros

# video.shape: [num_frames, height, width, colors]
num_frames = video.shape[0]

# Barcode to have 16x9 aspect ratio
output_height = round(num_frames * 9/16)

# np array defined as rows (height), columns (width), colors (3 for Red, Green, Blue)
barcode = np.zeros((output_height, num_frames, 3))

# Go frame by frame, calculating the mean value of each color independently
for i_frame in range(num_frames):
    frame = video[i_frame, :, :, :]

    barcode[:, i_frame, 0] = np.mean(frame[:, :, 0]) # red
    barcode[:, i_frame, 1] = np.mean(frame[:, :, 1]) # green
    barcode[:, i_frame, 2] = np.mean(frame[:, :, 2]) # blue

# Convert to Pillow Image and save to file
barcode = np.array(barcode, dtype=np.uint8)
im = Image.fromarray(barcode)
im.save('triumph_barcode.png')

# Display total execution time
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Total elapsed time: {elapsed_time} seconds')