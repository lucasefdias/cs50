// ------------------------------------------ //
// CS50 Problem Set 4: Recover
//
// Summary: Recover lost JPEG files from a
// given memory card
//
// Lucas Emidio Fernandes Dias
// 23 July 2018
// ------------------------------------------ //

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
// defines a "byte"for easier block searching
typedef uint8_t BYTE;
// define JPEG memory block size
#define JPEG_BLOCK 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n.");
        return 1;
    }

    // remember filename
    char *filename = argv[1];

    // open file
    FILE *fileptr = fopen(filename, "r");
    // checks if file can be opened for reading
    if (fileptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", filename);
        return 2;
    }

    // allocates memory for a buffer array equal to a JPEG block (512 bytes)
    BYTE *buffer = malloc(JPEG_BLOCK);

    // variable to store number of JPEGs found and array for image names (8 chars -> %03i.jpg + \0)
    int jpegs = 0;
    char *imgname = malloc(sizeof(char) * 8);

    // creates and opens first JPEG file
    sprintf(imgname, "%03i.jpg", jpegs);
    FILE *img = fopen(imgname, "w");

    // while EOF is not reached (when EOF is reached, fread returns a size smaller than the JPEG block)
    // reads a block of 512 bytes (1 byte read 512 times)
    while (fread(buffer, 1, JPEG_BLOCK, fileptr) == JPEG_BLOCK)
    {

        // checks if a new JPEG was found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            // checks if a JPEG was previously found and closes previous img file and creates new file
            if (jpegs > 0)
            {

                fclose(img);

                // creates image name and file
                sprintf(imgname, "%03i.jpg", jpegs);
                img = fopen(imgname, "w");
            }

            // writes buffer to image file
            fwrite(buffer, JPEG_BLOCK, 1, img);

            // increases jpeg counter
            jpegs++;

        }

        // if not at the start of a JPEG, check if a JPEG was already found and, if so, continues to write to img
        else
        {
            if (jpegs > 0)
            {
                // writes buffer to image file
                fwrite(buffer, JPEG_BLOCK, 1, img);
            }
        }

    }

    // closes remaining files
    fclose(fileptr);
    fclose(img);

    // frees buffer memory
    free(buffer);
    free(imgname);

    return 0;
}