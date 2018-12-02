// --------------------------------- //
// Include libraries
// --------------------------------- //
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

// Default dictionary
#define DICTIONARY "dictionaries/large"

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// --------------------------------- //
// Prototypes
// --------------------------------- //
bool check(const char *word);
bool load(const char *dictionary);
unsigned int size(void);

// --------------------------------- //
// Global variables
// --------------------------------- //
// define node for trie implementation of dictionary
    typedef struct node
    {
        bool is_word;
        struct node *children[27];
    }
    node;

// global variables
node *root;          // pointer to root of trie
int words = 0;       // keep track of words stored in the dictionary


// --------------------------------- //
// MAIN
// --------------------------------- //

int main(int argc, char *argv[])
{
    // Check for correct number of args
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./load_test [dictionary] text\n");
        return 1;
    }

    // Determine dictionary to use
    char *dictionary = (argc == 3) ? argv[1] : DICTIONARY;

    printf("Selected dictionary: %s\n", dictionary);

    // Load dictionary
    bool loaded = load(dictionary);

    if (loaded)
    {
        printf("Dictionary successfully loaded!\n");
        printf("Number of words in dictionary: %i\n", words);

    }
    else
    {
        printf("Dictionary could not be loaded.\n");
        return 2;
    }

    // ------------------- //
    // CHECK SECTION       //
    // ------------------- //

    // Try to open text
    char *text = (argc == 3) ? argv[2] : argv[1];
    FILE *file = fopen(text, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", text);
        return 3;
    }

    // Prepare to report misspellings
    printf("\nMISSPELLED WORDS\n\n");

    // Prepare to spell-check
    int index = 0, misspellings = 0, words_in_text = 0;
    char word[LENGTH + 1];

    // Spell-check each word in text
    for (int c = fgetc(file); c != EOF; c = fgetc(file))
    {
        // Allow only alphabetical characters and apostrophes
        if (isalpha(c) || (c == '\'' && index > 0))
        {
            // Append character to word
            word[index] = c;
            index++;

            // Ignore alphabetical strings too long to be words
            if (index > LENGTH)
            {
                // Consume remainder of alphabetical string
                while ((c = fgetc(file)) != EOF && isalpha(c));

                // Prepare for new word
                index = 0;
            }
        }

        // Ignore words with numbers (like MS Word can)
        else if (isdigit(c))
        {
            // Consume remainder of alphanumeric string
            while ((c = fgetc(file)) != EOF && isalnum(c));

            // Prepare for new word
            index = 0;
        }

        // We must have found a whole word
        else if (index > 0)
        {
            // Terminate current word
            word[index] = '\0';

            // Update counter
            words_in_text++;

            // Check word's spelling
            bool misspelled = !check(word);

            // Print word if misspelled
            if (misspelled)
            {
                printf("%s\n", word);
                misspellings++;
            }

            // Prepare for next word
            index = 0;
        }
    }

    // Check whether there was an error
    if (ferror(file))
    {
        fclose(file);
        printf("Error reading %s.\n", text);
        return 4;
    }

    // Close text
    fclose(file);

    // Determine dictionary's size
    unsigned int n = size();

    // Report benchmarks
    printf("\nWORDS MISSPELLED:     %d\n", misspellings);
    printf("WORDS IN DICTIONARY:  %d\n", n);
    printf("WORDS IN TEXT:        %d\n", words_in_text);

    return 0;
}


// ------------------------------------------ //
// FUNCTIONS FOR TESTING
// ------------------------------------------ //

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // trie implementation

    // create travel pointer and set it to root of trie
    node *trav = root;

    // loop through word's characters until NULL pointer or end of word
    for (int i = 0, length = strlen(word); i < length; i++)
    {
        // index of character (lowercase all characters first - check is case-insensitive)
        int index = tolower(word[i]) - 'a';
        if (word[i] == '\'')
        {
            index = 26;
        }

        // for each character in input word, go to corresponding child and check if NULL
        // if NULL, word is mispelled, return false
        if (trav -> children[index] == NULL)
        {
            return false;
        }
        // else, go to next child node
        else
        {
            trav = trav -> children[index];
        }
    }

    // if word ended, check if is_word is true (word is in the dictionary)
    if (trav -> is_word == true)
    {
        return true;
    }
    // else, word is misspelled (not in the dictionary)
    else
    {
        return false;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // trie implementation

    // calloc root of trie
    root = calloc(1, sizeof(node));
    if (root == NULL)
    {
        return false;
    }

    // create and set travel pointer equal to root of trie
    node *trav = root;

    // check all words of dictionary until EOF
    for (int c = fgetc(dict); c != EOF; c = fgetc(dict))
    {
        // if at the end of a word, set is_word to true, resets travel pointer to root and increase word counter
        if (c == '\n')
        {
            trav -> is_word = true;
            trav = root;
            words ++;
        }
        // else, evaluates character and creates new nodes for path as needed
        else
        {
            // index of c (as described in the "Specification" section of Speller description, we can assume that c is either a
            // lowercase letter or an apostrophe)
            int i = c - 'a';

            // check for apostrophe and sets children index to be the last element in array
            if (c == '\'')
            {
                i = 26;
            }

            // check if children[i] is NULL and create new node, zeroing the memory
            if (trav -> children[i] == NULL)
            {
                trav -> children[i] = calloc(1, sizeof(node));
                // if no memory is available for malloc, return false
                if (trav -> children[i] == NULL)
                {
                    return false;
                }
            }
            // go to next node
            trav = trav -> children[i];
        }
    }

    // close dictionary file
    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // if dictionary is loaded, words > 0
    if (words > 0)
    {
        return words;
    }
    else
    {
        return 0;
    }
}