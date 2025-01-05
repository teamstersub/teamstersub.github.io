---
title: 'Movie Barcode Part 2: What is Average Color?'
description: Let's learn about Rec. 709 and make a better movie barcode!
cover:
    image: '/posts/barcode/triumph_mean_sq.png'
date: 2025-01-03
tags: ['movie barcode', 'wu-tang']
---

## Intro

I started my exploration of movie barcodes in my [last post](/posts/barcode/barcode01) by making a simple barcode of Wu-Tang's classic "Triumph" music video: 

[![Triumph Movie Barcode - Mean](/posts/barcode/triumph_mean.png)](/posts/barcode/triumph_mean.png)

I used FFMPEG to load the [YUV](https://en.wikipedia.org/wiki/YCbCr) video file into Python as an [RGB](https://en.wikipedia.org/wiki/RGB_color_model) NumPy array and then took the mean value of the red, green, and blue values of each frame and sequenced them with the first frame on the left to the last frame on the right of the output image.

This worked to create a simple barcode, but the barcode came out a little dark when compared to the video. This is because my code didn't take into account the nonlinear nature of how the video file is stored. Investigating this can lead down many deep technical rabbit holes worthy of their own investigations. Let's dip our toes into the world of the [REC.709] standard and learn a little bit about [color spaces](https://en.wikipedia.org/wiki/Color_space), [gamma](https://en.wikipedia.org/wiki/Gamma_correction), and [FFMPEG](https://www.ffmpeg.org/) along the way.


## Triumph Video Info

I'm going to keep using Wu-Tang's "Triumph" music video for today's investigations. Here it is again, and you should watch it again, y'know, for science... and for the children:

{{< youtube cPRKsKwEdUQ >}}

[MediaInfo](https://mediaarea.net/en/MediaInfo) reports these parameters of interest in the file:

* Color primaries, transfer characteristics, matrix coefficients: BT.709, aka [Rec. 709](https://en.wikipedia.org/wiki/Rec._709), the encompassing video standard I'll dive into more in the next section
* Resolution: 1920x1080, aka Full HD
* Color Space: [YUV, aka YCbCr](https://en.wikipedia.org/wiki/YCbCr), which separates the video signal into three components:
    * [Y](https://en.wikipedia.org/wiki/Luma_(video)) component that contains the luma (or brightness) information. This is encoded at the full resolution of the video file, so 1920x1080 for this file.
    * [Cb](https://en.wikipedia.org/wiki/B-Y) component that contains the blue color difference.
    * [Cr](https://en.wikipedia.org/wiki/R-Y) component that contains the red color difference.
* [Chroma Subsampling](https://en.wikipedia.org/wiki/Chroma_subsampling): 4:2:0, which defines the resolution of the Cb and Cr channels. 4:2:0 means the Cb and Cr channels have half the horizontal resolution and half the vertical resolution, so 960x540 for this file.
* Bit Depth: 8 bits, meaning each of the Y, U, V components is stored with 8 bits, or 2^8 = 256 discrete steps.

## YUV



## REC.709

[![Triumph Movie Barcode - Mean](/posts/barcode/triumph_mean.png)](/posts/barcode/triumph_mean.png)
[![Triumph Movie Barcode - Mean Squared](/posts/barcode/triumph_mean_sq.png)](/posts/barcode/triumph_mean_sq.png)
[![Triumph Movie Barcode - Median](/posts/barcode/triumph_median.png)](/posts/barcode/triumph_median.png)


[1]: https://www.itu.int/rec/R-REC-BT.709-6-201506-I/en