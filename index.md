Schmidt Academy Pair-Programming Practicum
==========================================

**Ink limiting** is an important technique to enable modern printing
technologies.  A typical color laser or inkjet printer uses four colors:  cyan,
magenta, yellow and black.  This is often called
[the CMYK color space](https://en.wikipedia.org/wiki/CMYK_color_model), and is
abbreviated CMYK; the "K" stands for "Key" rather than "blacK."  Each pixel may
have a value of 0-100% in each of these colors, with a total possible value of
400% (the sum over all 4 components).  The problem is, the fuser, which melts
the toner to the page, is unable to melt and fuse this much toner all at once.
Often the total value must be restricted to a much lower limit, such as a
maximum total of 240% over all channels.

> You may be interested to know that this approach is also necessary for color
> ink printing, as the ink requires a certain amount of time to dry, but the
> more ink applied to a given pixel, the longer it will take to dry.  Also, in
> newspaper printing, too much ink on a given area will soften or weaken the
> paper to the point of failure.

Reducing the total amount of toner required for each pixel relies on a simple
observation that equal parts of cyan, magenta and yellow will appear as black,
and may therefore be replaced with an equal amount of black.  The implication
is that multiple CMYK values will map to the same printed color, but with
varying amounts of toner required.

Additionally, not every color has an equal impact on the final print; small
variations in yellow are less perceptible to the human eye than small variations
in magenta or black.  Thus, one can develop very sophisticated techniques to
map input colors to output colors that are "close enough" and that also satisfy
the ink-limit requirements of the printing hardware.

Your Task
---------

For this pair-programming project, you will implement a Python program that
performs ink-limiting on an input CMYK image, producing an output CMYK image.
It must be invokable with this command:

    python ink_limit.py input_image.tiff output_image.tiff inklimit [other options]

You can expect that the input image is a 4-channel TIFF image in the CMYK color
space, with each channel being a value in the range 0-255.  The output image
should also be a TIFF image with the same color-space and channel values.

The input image file should not be modified by the program, and the program
does not have to support the same filename being used for both the input and
output image.  In fact, you may want to prohibit this.

The `inklimit` value is a number between 0 and 400, representing an ink-limit of
0% to 400%.  You may take an integer or a floating-point value for this
argument.

If you want to pass other options to your program, they should come after the
required arguments.

We are also providing an input image that satisfies the above requirements
[here](balloons.tiff), for you to experiment with.  You might try a
command like this to limit pixels to a 240% maximum total per pixel:

    python inklimit.py balloons.tiff out.tiff 240

Some notes:

*   If an `inklimit` value of 400 is specified, the input and output images
    should be indistinguishable from each other.

*   Lower `inklimit` values should produce an output image that looks as
    similar to the input image as possible, but differences may become
    increasingly evident as the `inklimit` value is lowered.

Guidance
--------

We expect that you will use [the `pillow` library](https://pillow.readthedocs.io/en/stable/)
(a fork of the well-known Python Imaging Library a.k.a. PIL) and
[NumPy](https://numpy.org/) to implement this program.  If these libraries are
not already part of your Python environment, you can type:

    pip install pillow
    pip install numpy

An input image can be loaded into a NumPy array with code like this:

    from PIL import Image
    import numpy as np

    # path ends with ".tiff"
    img = Image.open(path, 'r')
    arr = np.asarray(img)

Look at the array's *shape* to understand how the width, height and number of
channels are mapped into the array.

A NumPy array with 4 channels per pixel may be written out as a CMYK TIFF image
with code like this:

    img = Image.fromarray(arr, mode='CMYK')
    # path ends with ".tiff"
    img.save(path, compression='tiff_deflate')

You can access Python command-line arguments very easily; you merely need to
import [the built-in `sys` module](https://docs.python.org/3/library/sys.html),
and then use the `sys.argv` list to access the command-line arguments.  The
first argument `sys.argv[0]` will be the Python file being run, and subsequent
arguments are the command-line options passed to the program.

Additional Guidance
-------------------

There are many different directions you can take your implementation, depending
on your goals for the project.

*   A simple implementation may iterate through all pixels, mapping each input
    pixel to an output pixel.  While maximally flexible, this approach is also
    likely to be slow, and it would be good to consider how to indicate to the
    user how much longer they must wait for the program to complete.

*   Alternately, if your ink-limiting approach is simple enough, you may be
    able to leverage NumPy's array-level operations to perform the mapping
    very quickly and efficiently across the entire image, all at once.  This,
    however, may have consequences on the memory requirements for your program.

*   You may want to implement multiple ink-limiting approaches and provide
    command-line switches to choose which one is used by your program.

*   Consider the usability of your program.  Does it show usage information
    when the user inputs bad arguments?  Can the user request help?  Would it
    make sense to always display statistics of the ink-limiting operation
    when your program finishes?  Alternately, might you want to support a
    "verbose" flag that outputs more detailed information from your program?

Towards the end of your project, add a `README.md` file to your repository,
and document your overall goals for the project, as well as any additional
options your program may handle.

----

Copyright (c) 2022-2023 by the California Institute of Technology.
All rights reserved.

Test image is from the [Pexels free image website](https://www.pexels.com/photo/portriat-of-a-woman-in-a-dress-lying-in-a-meadow-12652637/).  Original photo taken by Anna Panchenko.

