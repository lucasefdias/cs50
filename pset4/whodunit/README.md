# Questions

## What's `stdint.h`?

`stdint.h` is a header file in C that specifies a set of typedefs that specify exact-width integer types and minimum and maximum allowable values for each type, using a series of macros.
This header is useful for manipulation of hardware specific I/O registers requiring integer data of fixed widths, specific locations and exact alignments.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The main reason to use well-defined types in a program is portability. Using these keywords inside a program can make the code work independently from how the hardware it will run on interprets data types.
For example, you can have two different processors that interpret an `int` as being 8 bytes long or 16 bytes long. Using types like `uint8_t` can minimize portability problems and allow the programmer to
control exactly how the program should behave in any hardware, making it safe and predictable to run.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

They are 1 byte, 4 bytes, 4 bytes and 2 bytes respectively.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes used to identify any BMP file are `0x42 0x4D` in hexadecimal, which are the same as `BM` in ASCII.

## What's the difference between `bfSize` and `biSize`?

`bfSize` is the size (number of bytes) of the whole bitmap file (including the headers). `biSize` is the number of bytes required by the structure, which is the struct `BITMAPINFOHEADER`.

## What does it mean if `biHeight` is negative?

`biHeight` is an element inside the `BITMAPINFOHEADER` struct which determines the height of the bitmap (in pixels) and the image orientation. If `biHeight` is negative the orientation is top-down. This means that the first row to be rendered
is the top row, followed by the next row down. Therefore, the top row bytes are stored first in the BMP file.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The field in `BITMAPINFOHEADER` that specifies the BMP's color depth is `biBitCount`.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

`fopen` might return `NULL` in lines 24 and 32 of `copy.c` because the input and output files, respectively, might not exist.

## Why is the third argument to `fread` always `1` in our code?

`fread` is always `1` in our code because it the defines the number of elements to be read. The only elements being read are the infile's headers (`BITMAPFILEHEADER` and `BITMAPINFOHEADER`) and each one has its separate call of `fread`.
Therefore, we only need to specify `1` for the third argument of `fread` in each instance, passing each element's size in the second argument (`sizeof(<element>)`).

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`padding` in line 63 is calculated by the expression:

`int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;`

If `bi.biWidth` is `3` (note that `RGBTRIPLE` is always 3, because it encapsulates the three bytes for Red, Green and Blue in each pixel), then:

`int padding = (4 - (3 * 3) % 4) % 4;`
`int padding = (4 - (9) % 4) % 4;`
`int padding = (4 - 1) % 4;`
`int padding = (3) % 4;`
`int padding = 3;`

Therefore, the value assigned to padding is `3`.

## What does `fseek` do?

`int fseek(FILE *stream, long int offset, int whence)` is a function from the `stdio.h` library that offsets the file position of a given stream by a given offset value. `fseek` is given three arguments:

*`stream` − The pointer to a FILE object that identifies the stream.
*`offset` − The number of bytes to offset from whence.
*`whence` − The position from where offset is added. It is specified by one of three values:
    * `SEEK_SET` - Beginning of file;
    * `SEEK_CUR` - Current position of `stream` (file pointer);
    * `SEEK_END` - End of file.

## What is `SEEK_CUR`?

`SEEK_CUR` is a possible value for the third argument of the `fseek` function. It indicates that the offset value from the second argument of the function is to be dded to the current position of the file pointer
(which is the stream, passed in as the first argument of the function).
