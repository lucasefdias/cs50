// Helper functions for music

#include <cs50.h>
#include "helpers.h"
#include <math.h>
#include <string.h>

// Constants
#define EIGHTH_MULTIPLIER 8 // Multiplier for duration function
#define SEMITONES 12.0 // Number of semitones for frequency function
#define A4_FREQUENCY 440 // Reference for frenquency function
#define CENTRAL_OCTAVE 4 // Reference for octaves

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
    // Checks if note is outside of valid range (between C0 and B8) and returns error if it is not valid
    if (note[0] < 'A' || note[0] > 'G' || note[strlen(note) - 1] < '0' || note[strlen(note) - 1] > '8')
    {
        return 1;
    }

    // Frequency of a generic note NaOct f_NaOct, where:
    // N is a letter ('C' to 'B')
    // a is an accidental ('#', 'b' or none)
    // Oct is the octave (0 to 8)

    // Calculation:
    // f_NaOct = f_A4*f_N*f_a*f_Oct, where:
    // f_A4: frequency for A4 = 440Hz
    // f_N: "Note multipler", which takes in to account the semitones between `N` and 'A' from the same octave
    // f_a: "Accidental multiplier", which takes in to account the effect of the accidental of the note
    // f_Oct: "Octave multiplier", which takes in to account the effect of the octave of the note

    // Gets the letter (first element) and the octave (last element before '\0') from note
    char natural_note = note[0];
    int size = strlen(note);
    int octave = note[size - 1] - '0';

    // Initializes multipliers
    double note_multiplier = 1.0, accidental_multiplier = 1.0, octave_multiplier = 1.0;

    // Checks for accientals and increases or drops a semitone to reach matching natural note
    // #
    if (note[1] == '#')
    {
        accidental_multiplier = pow(2.0, 1.0 / SEMITONES);
    }
    // b
    else if (note[1] == 'b')
    {
        accidental_multiplier = pow(2.0, -1.0 / SEMITONES);
    }

    // Note distance multiplier
    // Finds the number of semitones between the note 'A' from the same octave
    int semitone_distance;

    // Selects semitone distance between the current note and 'A' from the same octave
    switch (natural_note)
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

    note_multiplier = pow(2.0, (double) semitone_distance / SEMITONES);

    // Corrects octave
    octave_multiplier = pow(2.0, octave - CENTRAL_OCTAVE);

    // Returns frequency
    double freq = A4_FREQUENCY * note_multiplier * accidental_multiplier * octave_multiplier;

    return round(freq);
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
