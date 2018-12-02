from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Splits lines from a and b into two lists
    a_lines = a.splitlines()
    b_lines = b.splitlines()

    # Convert lists into sets to eliminate duplicates
    a_lines = set(a_lines)
    b_lines = set(b_lines)

    # Finds the intersection between the two sets (lines in both a and b)
    intersect = a_lines.intersection(b_lines)

    # Creates list for common lines and appends all elements from intersection
    common_lines = []

    for element in intersect:
        common_lines.append(element)

    return common_lines


def sentences(a, b):
    """Return sentences in both a and b"""

    # Splits sentences from a and b into two lists
    a_sentences = sent_tokenize(a)
    b_sentences = sent_tokenize(b)

    # Convert lists into sets to eliminate duplicates
    a_sentences = set(a_sentences)
    b_sentences = set(b_sentences)

    # Finds the intersection between the two sets (sentences in both a and b)
    intersect = a_sentences.intersection(b_sentences)

    # Creates list for common sentences and appends all elements from intersection
    common_sentences = []

    for element in intersect:
        common_sentences.append(element)

    return common_sentences


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # Splits sentences from a and b into two lists
    a_substrings = get_substrings(a, n)
    b_substrings = get_substrings(b, n)

    # Convert lists into sets to eliminate duplicates
    a_substrings = set(a_substrings)
    b_substrings = set(b_substrings)

    # Finds the intersection between the two sets (sentences in both a and b)
    intersect = a_substrings.intersection(b_substrings)

    # Creates list for common sentences and appends all elements from intersection
    common_substrings = []

    for element in intersect:
        common_substrings.append(element)

    return common_substrings


# Auxiliar function


def get_substrings(string, n):

    substring_list = []

    for i in range(len(string) - n + 1):
        substring_list.append(string[i:i+n])

    return substring_list
