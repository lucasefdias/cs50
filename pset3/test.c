// Helper functions for music

#include <cs50.h>
#include "helpers.h"
#include <math.h>
#include <string.h>
#include <stdio.h>

// Constants
#define EIGHTH_MULTIPLIER 8 // Multiplier for duration function
#define SEMITONES 12.0 // Number of semitones for frequency function
#define A4_FREQUENCY 440 // Reference for frenquency function

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // Converts fraction from string to int
    // Fraction[0] = numerator; fraction[2] = denominator
    int numerator = fraction[0] - '0';
    int denominator = fraction[2] - '0';

    return (numerator * EIGHTH_MULTIPLIER) / denominator;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // Copy original note string to iteration string
    char note_copy[] = "XXXX";
    strcpy(note_copy, note);

    // A4 - base case = 440Hz
    if(strcmp(note, "A4") == 0)
    {
        return A4_FREQUENCY;
    }
    // Octaves above A4 (octaves 5 through 8)
    else if (strcmp(note, "A4") > 0 && strcmp(note, "A8") <= 0)
    {
        // Drops one octave
        note_copy[1]--;

        return 2 * frequency(note_copy);
    }
    // Octaves below A4 (octaves 0 through 3)
    else if (strcmp(note, "A0") >= 0 && strcmp(note, "A4") < 0)
    {
        // Increases one octave
        note_copy[1]++;

        return frequency(note_copy) / 2;
    }
    // Accidentals (including A# and Ab): increases or drops semitone to reach natural note
    else if (note[1] == '#' || note[1] == 'b')
    {
        // Drop or increase one semitone
        note_copy[1] = note[2];
        note_copy[2] = '\0';
        // #: drops semitone to reach matching natural note
        if (note[1] == '#')
        {
            return round((long double) frequency(note_copy) * (long double) pow(2.0, (long double) 1.0 / SEMITONES));
        }
        // b: increases semitone to reach matching natural note
        else
        {
            return round((long double) frequency(note_copy) / (long double) pow(2.0, (long double) 1.0 / SEMITONES));
        }
    }

    // All other notes
    // Natural notes: calculates frequency based on semitone distance to "A"
    else
    {
        int semitone_distance;

        // Selects semitone distance between the current note and 'A' from the same octave
        switch (note[0])
        {
            case 'C':
                semitone_distance = -9;
                break;
            case 'D':
                semitone_distance = -7;
                break;
            case 'E':
                semitone_distance = -5;
                break;
            case 'F':
                semitone_distance = -4;
                break;
            case 'G':
                semitone_distance = -2;
                break;
            case 'B':
                semitone_distance = 2;
                break;
            default:
                semitone_distance = 0;
                break;
        }

        // Changes to A from the same octave for next iteration
        note_copy[0] = 'A';

        // Frequency: f_note_oct = f_A_oct * 2^(semitone_distance/12)
        return round((long double) frequency(note_copy) * (long double) pow(2.0, (long double) semitone_distance / SEMITONES));
    }

    // If none of the cases work, return error
    return 1;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // If first element of s is "" (return of get_string for newline input), returns 'true'
    if (strcmp(&s[0], "") == 0)
    {
        return true;
    }
    // Else, it is not a rest (returns false)
    else
    {
        return false;
    }
}
