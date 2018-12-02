// ------------------------------------------ //
// CS50 Problem Set 4: Resize (less comfortable)
//
// Summary: Reveals a hidden message in a BMP
// file
//
// Lucas Emidio Fernandes Dias
// 16 July 2018
// ------------------------------------------ //

// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // keep track of infile parameters that change
    // width
    int inWidth = bi.biWidth;
    // height
    int inHeight = abs(bi.biHeight);
    // padding
    // determine padding for scanlines (infile)
    int inPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // change header for output file
    // BITMAPINFOHEADER
    // new width
    bi.biWidth *= n;
    // new height
    bi.biHeight *= n;
    // new padding (outfile)
    int outPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // new biSizeImage
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + outPadding) * abs(bi.biHeight);
    // new bfSize
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);


    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // allocate memory for an array to store outfile`s resized lines
    RGBTRIPLE *outfileLine = malloc(sizeof(RGBTRIPLE) * bi.biWidth);

    // iterate over infile's scanlines
    for (int i = 0; i < inHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < inWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // copy RGB triple to copy array
            for (int count = 0; count < n; count++)
            {
                outfileLine[j*n + count] = triple;
            }
        }

        // skip over infile padding, if any
        fseek(inptr, inPadding, SEEK_CUR);

        // write lines to outfile from copy array n times
        for (int j = 0; j < n; j++)
        {
            // write all RGB triples stored in the array
            for (int count = 0; count < bi.biWidth; count++)
            {
                fwrite(&outfileLine[count], sizeof(RGBTRIPLE), 1, outptr);
            }
            // then add outfile`s padding
            for (int k = 0; k < outPadding; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // free allocated memory
    free(outfileLine);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
