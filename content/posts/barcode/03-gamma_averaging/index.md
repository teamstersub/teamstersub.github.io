---
title: 'Movie Barcode Part 3: Statistical Shenanigans'
date: 2025-01-06
tags: ['movie barcode', 'wu-tang']
---

Let's make movie barcodes with some statistical methods.


## The Problem of Simply Averaging (Intro to Gamma)

[![Triumph Movie Barcode - Mean](/posts/barcode/triumph_mean.png)](/posts/barcode/triumph_mean.png)

My first cut at a movie barcode, shown above, simply averaged the red, green, and blue channels of a frame (let's circle back to YUV vs RGB in a bit). 

However, there is a nonlinear relationship between how the values are stored in the file and how bright they appear to a viewer. Here are a couple of good articles that describe this in detail:

* [Cambridge in Colour: Understanding Gamma Correction](https://www.cambridgeincolour.com/tutorials/gamma-correction.htm)
* 

1. A camera sensor detects light linearly. Twice the photons coming in, twice the signal on the sensor.
2. However, our eyes do not perceive that doubling of photons as a doubling of brightness. A doubling of photons will appear less than twice as bright. Our eyes are much better at detecting subtle changes of darker parts of an image.
3. A camera has a fixed bit depth to encode the levels of brightness of an image. One standard is 8 bits, which is 2^8 = 256 levels of brightness. If the camera were to linearly encode the image data, that means values 1-128 would be the lowest half of the brightness and 129-256 would be the highest half of the brightness. However, because your eyes don't detect that doubling in brightness as a real doubl

took the average of the color values as they were stored in the file but that's not the same as how the data ultimately gets viewed. The video file is stored in the  color space 

The file was encoded in the REC.709 color space, which really needs to be taken into account 

Gamma, REC709, 

and convert the video file's native [YUV](https://en.wikipedia.org/wiki/YCbCr) values to [RGB](https://en.wikipedia.org/wiki/RGB_color_model) values.


## Triumph Video Info

I'm going to keep using Wu-Tang's "Triumph" music video for today's investigations. Here it is again, and you should watch it again, y'know, for science... and for the children:

{{< youtube cPRKsKwEdUQ >}}

[MediaInfo](https://mediaarea.net/en/MediaInfo) reports these parameters of interest in the file:

* Color primaries, transfer characteristics, matrix coefficients: BT.709, aka [Rec. 709](https://en.wikipedia.org/wiki/Rec._709).
* Resolution: 1920x1080, aka Full HD
* Color Space: [YUV, aka YCbCr](https://en.wikipedia.org/wiki/YCbCr), which separates the video signal into three components:
    * [Y](https://en.wikipedia.org/wiki/Luma_(video)) component that contains the luma (or brightness) information. This is encoded at the full resolution of the video file, so 1920x1080 for this file.
    * [Cb](https://en.wikipedia.org/wiki/B-Y) component that contains the blue color difference.
    * [Cr](https://en.wikipedia.org/wiki/R-Y) component that contains the red color difference.
* [Chroma Subsampling](https://en.wikipedia.org/wiki/Chroma_subsampling): 4:2:0, which defines the resolution of the Cb and Cr channels. 4:2:0 means the Cb and Cr channels have half the horizontal resolution and half the vertical resolution, so 960x540 for this file.
* Bit Depth: 8 bits, meaning each of the Y, U, V components is stored with 8 bits, or 2^8 = 256 discrete steps.

The key thing to note is that the video complies with the Rec. 709 standard, which defines a lot of parameters we need to understand to accurately calculate average color.


## Rec. 709 Overview

The [Rec. 709 standard][3]

## Averaging with Gamma


## How does FFMPEG read from the file?


## Averaging with YUV



Investigating this can lead down many deep technical rabbit holes worthy of their own investigations. Let's dip our toes into the world of the [REC.709] standard and learn a little bit about [color spaces](https://en.wikipedia.org/wiki/Color_space), [gamma](https://en.wikipedia.org/wiki/Gamma_correction), and [FFMPEG](https://www.ffmpeg.org/) along the way.




[3]: https://www.itu.int/rec/R-REC-BT.709-6-201506-I/en "