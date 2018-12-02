// ------------------------------------------ //
// CS50 Problem Set 5: Speller
//
// Summary: Implement a dictionary functionality
// for a spell-checker program that receives
// as inputs a dictionary (optional) and a text
// file to be spell-checked against the words in
// the dictionary
//
// Lucas Emidio Fernandes Dias
// 2nd August 2018
// ------------------------------------------ //

// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// define node for trie implementation of dictionary
typedef struct node
{
    bool is_word;                       // controls if current path is a word in dictionary
    struct node *children[LETTERS + 1]; // children array must fit all 26 letters of alphabet + apostrophe
}
node;

// global variables
node *root; // pointer to root of trie
int words = 0; // keep track of words stored in the dictionary

// Prototypes for auxiliar functions
void free_children_nodes(node *parent_node_ptr);

// Returns true if word is in dictionary else false
bool check(const char *word)
{

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
        unload();
        return false;
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
                trav -> children[i] = calloc(1, sizeof(node));
                if (trav -> children[i] == NULL)
                {
                    unload();
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

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // check for NULL pointer
    if (root == NULL)
    {
        return false;
    }
    // if not NULL, free all children nodes and root pointer
    else
    {
        free_children_nodes(root);
        free(root);
        return true;
    }
}

// Auxiliar functions
// Recursive function - frees all children nodes from a given parent node pointer
void free_children_nodes(node *parent_node_ptr)
{
    // iterate over all children nodes from parent pointer
    for (int i = 0; i < LETTERS + 1; i++)
    {
        // Base case: frees current child node
        if (parent_node_ptr -> children[i] == NULL)
        {
            free(parent_node_ptr -> children[i]);
        }
        // Recursive case: frees all children from current child node and then frees the current child node
        else
        {
            free_children_nodes(parent_node_ptr -> children[i]);
            free(parent_node_ptr -> children[i]);
        }
    }
}