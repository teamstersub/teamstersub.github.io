---
title: 'Movie Barcode Part 1: Triumph'
description: Let's make a "Movie Barcode" of Wu-Tang's "Triumph" music video using Python!
date: 2025-01-01
tags: ['movie barcode', 'wu-tang']
cover:
    image: '/posts/barcode/triumph_barcode.png'
    caption: "Simple movie barcode of Wu-Tang's Triumph music video made in this post"
---

## Intro

A trend popped up on the interwebs in the early 2010s for "movie barcodes," where a movie is boiled down to a single image containing the average colors from each frame of the movie. Here are some fun examples:

* [moviebarcode on tumblr](https://moviebarcode.tumblr.com/)
* [movie_barcode on instagram](https://www.instagram.com/movie_barcode/?hl=en)
* [Thomas Poulet's Movie Barcode post](https://blog.thomaspoulet.fr/movie-barcode/)

I really enjoy how you can summarize a movie in a single frame. It's fun seeing if you can identify a movie by looking at its barcode. I also appreciate the various ways folks have presented their movie barcodes from simple color averages in a strip to a disc-like representation. There's an art to how you summarize and present a movie in a single image.

I've always been curious to make my own movie barcodes. No time like a decade after a trend has peaked to hop on board! But, hey, I figure this is a good excuse to play with some standard software packages and do something a little creative. So let's give this a shot.

Before jumping into full movies, I'm going to start by playing with shorter videos. The place to start, obviously, is with the music video for Wu-Tang Clan's 1997 banger "Triumph":

{{< youtube cPRKsKwEdUQ >}}

This is the first in a [series of posts diving into movie barcodes](/tags/barcode). I'll be exploring different ways to create them and how to optimize code.

Today's post will dive into getting the software environment set up and I'll make a first cut at simple code to create a simple Triumph barcode. I'm going to go a little overboard with the details of how to do the setup just to keep a record so I can do this again if needed. Feel free to skip over the Environment Setup section if it's too in the weeds.


## Environment Setup

### Install Homebrew and FFmpeg

I'm going to use [Homebrew](https://brew.sh/) to manage system required packages on my Mac. I installed Homebrew from the Terminal using instructions on the Homebrew homepage.

[FFmpeg](https://www.ffmpeg.org/) is a standard cross-platform package for working with video files that I've been meaning to get more familiar with. It can be installed easily on a Mac [with Homebrew](https://formulae.brew.sh/formula/ffmpeg):

```
brew install ffmpeg
```

### Install Conda and Setup Conda-Forge Repository

I'm going to start off by doing everything in [Python](https://www.python.org/). I like to use [Anaconda](https://www.anaconda.com/) to manage my python environments, specifically the minimal [Miniconda installer](https://docs.anaconda.com/miniconda/) and the [Conda-Forge](https://conda-forge.org/) repository. I installed Miniconda using the latest installer for my Macbook Pro with M1 Pro chip.

Your terminal window should now reflect that conda has been installed by showing the (base) environment in the prompt. It will look something like this:

```
(base) $
```

Once conda has been installed, add conda-forge as the highest priority channel:

```
conda config --add channels conda-forge
```

And set the channel priority to "strict" to ensure conda-forge is checked first anytime you install a new package.

```
conda config --set channel_priority strict
```

You can check that this was set correctly by checking the config:

```
conda config --get
```

The output should look something like this:

```
--set channel_priority strict
--add channels 'defaults'   # lowest priority
--add channels 'conda-forge'   # highest priority
```

### Setup Conda Environment

Alright, now we have Conda installed and are ready to setup our conda environment and install the needed packages. First, we'll create a new environment called "teamstersub" using python 3.13 (the latest at the time of this writing)

```
conda create --name teamstersub python=3.13
```

That will create a new environment called "teamstersub" with python 3.13 and dependencies. Then activate the environment:

```
conda activate teamstersub
```

The prompt will now change to reflect the (teamstersub) environment is active and look something like this:

```
(teamstersub) $
```

I'm going to stick to some standard python packages for this initial work:

* [yt-dlp](https://github.com/yt-dlp/yt-dlp): Download videos from YouTube. We'll want to download the video to a file to work with locally.
* [ffmpeg-python](https://github.com/kkroening/ffmpeg-python): Python bindings for FFmpeg. Note that this just binds python to the system FFmpeg installed using Homebrew so you need to do that. We'll use ffmpeg-python to load the video file into python and convert to a NumPy array.
* [NumPy](https://numpy.org/): Standard python array computing package. We're going to work with the video files as NumPy arrays and utilize some built-in functions to calculate our barcodes.
* [Pillow](https://python-pillow.org/): Python image library. We'll use this to save the movie barcode to an image file.

You can install each package one at a time:

```
conda install yt-dlp
conda install ffmpeg-python
conda install numpy
conda install pillow
```

Or all in one go:

```
conda install yt-dlp ffmpeg-python numpy pillow
```

I tend to install one by one but go all in if you like. To verify what packages are installed:

```
conda list
```

You should see the required packages for this project plus a whole bunch of other packages that they depend on.


## Download the Video

We're almost ready to write some code! Before that, download the video using yt-dlp, which is run from the command line. Here's how you download the video:

```
yt-dlp "<url>"
```

Copy the url and paste in inside quotes in the Terminal. I also had to clean up some '/' escape characters that pasted in. This downloaded a 1080p webm file for me. I renamed the file 'triumph.webm' after downloading to make it easier to work with.


## Video Info

Here's some info about the file from FFmpeg and [MediaInfo](https://mediaarea.net/en/MediaInfo):

* File Size: 157.6 MB
* Resolution: [1920 x 1080](https://www.adobe.com/creativecloud/video/discover/video-resolution.html)
* Bit Rate: 3,342 kb/s
* Time: 6:17
* Frame Rate: 23.976
* Total Frames: 9,047
* Codec: [VP9](https://en.wikipedia.org/wiki/VP9)
* Color Standard: [BT.709](https://en.wikipedia.org/wiki/Rec._709)
* Color Model: [YUV](https://en.wikipedia.org/wiki/YCbCr)
* Chroma: [4:2:0](https://en.wikipedia.org/wiki/Chroma_subsampling)
* Bit Depth: [8 bits](https://www.videomaker.com/article/c02/19251-understanding-bit-depth-and-color-rendition-for-video/)

I've highlighted links for some of these topics that I'll be investigating more in the future.

## Code

### Code Outline 

Alright, time for the fun part! Here's an outline of the code:

* Import packages
* Get video info using ffmpeg's probe
* Convert video to NumPy RGB array using ffmpeg. I just copied an [example](https://github.com/kkroening/ffmpeg-python/tree/master/examples#convert-video-to-numpy-array) from the ffmpeg-python documentation
* Initialize barcode image as NumPy array of all zeros. The image width will be the total number of video frames. I set the height so the image would have a friendly 16:9 aspect ratio
* Go frame by frame, calculate the average value of each color, and set that column of the barcode image to that color. The average is calculated using NumPy's "mean" method
* Convert the barcode image to a Pillow Image object
* Save to file
* Display the time it took to run the code

### Full Code

Here's the full code:

{{< highlight python >}}
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
{{< / highlight >}}


## The Results

[![Triumph Movie Barcode](/posts/barcode/triumph_barcode.png)](/posts/barcode/triumph_barcode.png)

There we go, a movie barcode for Triumph. Pretty cool. The cut-ins with the fiery background show up clearly. The jail house scenes near the end have a blue hue.

My code took a little over 3 minutes to create the 6 minute 18 second 1080p video... if that scales, I'm looking at around an hour to generate a barcode a 2 hour 1080p video. My code loaded all the video frames into video at the same time, and I'm guesing I'll quickly run out of memory and this won't work for that long of a video, either. Also seeing as I'd like to eventually scale up to do this for full 4K HDR movies, there's some code optimization in the future!

But before optimizing code, this barcode came out a little dark and I'd like to find ways to address that. What is the "average" color of a frame anyway? I'll investigate that next time!

--Teamster Sub

