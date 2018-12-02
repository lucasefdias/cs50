// Include libraries
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

// Default dictionary
#define DICTIONARY "dictionaries/large"

// number of letter in alphabet
#define LETTERS 26

// Prototypes
bool load(const char *dictionary);

// Global variables
// define node for trie implementation of dictionary
    typedef struct node
    {
        bool is_word;
        struct node *children[27];
    }
    node;

// global variables
node *root; // pointer to root of trie
int words = 0; // keep track of words stored in the dictionary

int main(int argc, char *argv[])
{
    // Check for correct number of args
    if (argc != 1 && argc != 2)
    {
        printf("Usage: ./load_test [dictionary]\n");
        return 1;
    }

    // Determine dictionary to use
    char *dictionary = (argc == 2) ? argv[1] : DICTIONARY;

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
    }

    return 0;
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
    printf("Printing root parameters:\n");
    printf("\nroot -> is_word = %i\n", root -> is_word);

    for(int i = 0; i< 27; i++)
    {
        if(root -> children[i] == NULL)
        {
            printf("root -> children[%i] = NULL\n", i);
        }
    }


    // create and set travel pointer equal to root of trie
    node *trav = root;

    // check all words of dictionary until EOF
    for (char c = fgetc(dict); c != EOF; c = fgetc(dict))
    {
        // if at the end of a word, set is_word to true, resets travel pointer to root and increase word counter
        if (c == '\n')
        {
            trav -> is_word = true;
            trav = root;
            words ++;
        }
        // else, evaluates character and creates new nodes for path as needed
        else if (c == '\'' || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
        {
            // index of c
            int i;

            // check for apostrophe and sets children index to be the last element in array
            if (c == '\'')
            {
                i = LETTERS;
            }
            // else, it is a letter
            else
            {
                i = tolower(c) - 'a';
            }

            // check if children[i] is NULL and create new node, zeroing the memory
            if (trav -> children[i] == NULL)
            {
                printf("trav -> children[%i] = NULL\n", i);

                trav -> children[i] = malloc(sizeof(node));
            }
            // go to next node
            trav = trav -> children[i];
        }
    }

    // close dictionary file
    fclose(dict);

    return true;
}