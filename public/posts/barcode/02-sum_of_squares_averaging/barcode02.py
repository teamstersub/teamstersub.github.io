import time

import ffmpeg
import numpy as np
from PIL import Image
from tqdm import tqdm


# Start Time
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

# Read End Time
read_end_time = time.time()
read_time = read_end_time - start_time
print(f'Total read time: {read_time} seconds')


# Initialize barcode image as NP array of proper dimensions initialized to all zeros
# video.shape: [num_frames, height, width, colors]
num_frames = video.shape[0]

# Barcode to have 16x9 aspect ratio
output_height = round(num_frames * 9/16)


# Calculate Mean Image

# np array defined as rows (height), columns (width), colors (3 for Red, Green, Blue)
mean = np.zeros((output_height, num_frames, 3))

# Go frame by frame, calculating the mean value of each color independently
for i_frame in tqdm(range(num_frames)):
    frame = video[i_frame, :, :, :]

    mean[:, i_frame, 0] = np.mean(frame[:, :, 0]) # red
    mean[:, i_frame, 1] = np.mean(frame[:, :, 1]) # green
    mean[:, i_frame, 2] = np.mean(frame[:, :, 2]) # blue

# Convert to Pillow Image and save to file
mean = np.array(mean, dtype=np.uint8)
im_mean = Image.fromarray(mean)
im_mean.save('triumph_mean.png')

# Display Mean Processing time
mean_end_time = time.time()
mean_processing_time = mean_end_time - read_end_time
print(f'Total mean processing time: {mean_processing_time} seconds')


# Calculate Squared Mean Image

# np array defined as rows (height), columns (width), colors (3 for Red, Green, Blue)
mean_sq = np.zeros((output_height, num_frames, 3))

# Go frame by frame, take the squared value, and then calculate the mean value of each color independently
for i_frame in tqdm(range(num_frames)):
    frame = video[i_frame, :, :, :]
    frame_sq = np.array(frame, dtype=np.float64)
    frame_sq = np.square(frame_sq)

    mean_sq[:, i_frame, 0] = np.mean(frame_sq[:, :, 0]) # red
    mean_sq[:, i_frame, 1] = np.mean(frame_sq[:, :, 1]) # green
    mean_sq[:, i_frame, 2] = np.mean(frame_sq[:, :, 2]) # blue

# Take square root, convert to Pillow Image and save to file
mean_sq = np.sqrt(mean_sq)
mean_sq = np.array(mean_sq, dtype=np.uint8)
im_mean_sq = Image.fromarray(mean_sq)
im_mean_sq.save('triumph_mean_sq.png')


# Display Squared Mean Processing time
sq_end_time = time.time()
sq_processing_time = sq_end_time - mean_end_time
print(f'Total Squared Mean processing time: {sq_processing_time} seconds')

# Display total time
total_time = sq_end_time - start_time
print(f'Total time: {total_time} seconds')
