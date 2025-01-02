---
title: 'Movie Barcode Part 2: What is Average Color?'
description: Let's learn about REC.709 and make a better movie barcode!
cover:
    image: '/posts/barcode/triumph_mean_sq.png'
date: 2025-01-03
tags: ['movie barcode', 'wu-tang']
---

[![Triumph Movie Barcode - Mean](/posts/barcode/triumph_mean.png)](/posts/barcode/triumph_mean.png)
[![Triumph Movie Barcode - Mean Squared](/posts/barcode/triumph_mean_sq.png)](/posts/barcode/triumph_mean_sq.png)
[![Triumph Movie Barcode - Median](/posts/barcode/triumph_median.png)](/posts/barcode/triumph_median.png)

## Intro

I started my exploration of movie barcodes in my [last post](/posts/barcode/barcode01) by making a simple barcode of Wu-Tang's classic "Triumph" music video. I used FFMPEG to load the video into Python as a NumPy array and then averaged the red, green, and blue values of each frame to create the barcode. I noticed that the barcode produced from my code was a little dark when compared to the video. We'll look at how to fix that in this post, where we'll be investigating the concepts of [color spaces](https://en.wikipedia.org/wiki/Color_space), transformations, and [gamma](https://en.wikipedia.org/wiki/Gamma_correction), oh my!


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


## REC.709


## 