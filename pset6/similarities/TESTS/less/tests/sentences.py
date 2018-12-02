import cs50
import sys
from nltk.tokenize import sent_tokenize

def main():

    a = sys.argv[1]
    b = sys.argv[2]

     # Read files
    try:
        with open(a, "r") as file:
            file1 = file.read()
    except IOError:
        sys.exit(f"Could not read {a}")
    try:
        with open(b, "r") as file:
            file2 = file.read()
    except IOError:
        sys.exit(f"Could not read {b}")

    same_sentences = sentences(file1, file2)

    # print("Same lines: ")
    # for line in same_lines:
    #     print(line)

    sys.exit(0)


def sentences(a, b):

    """Return sentences in both a and b"""

    # print("a:")
    # print(a)
    # print("b:")
    # print(b)

    # Splits sentences from a and b into two lists
    a_sentences = sent_tokenize(a)
    b_sentences = sent_tokenize(b)

    # print("a_sentences:")
    # print(a_sentences)
    # print("b_sentences:")
    # print(b_sentences)

    # Convert lists into sets to eliminate duplicates
    a_sentences = set(a_sentences)
    b_sentences = set(b_sentences)

    # print("a_sentences:")
    # print(a_sentences)
    # print("b_sentences:")
    # print(b_sentences)

    # Finds the intersection between the two sets (sentences in both a and b)
    intersect = a_sentences.intersection(b_sentences)

    # print("Intersect:")
    # print(intersect)

    # Creates list for common sentences and appends all elements from intersection
    common_sentences = []

    for element in intersect:
        common_sentences.append(element)

    # for sentence in common_sentences:
    #     print(sentence)

    return common_sentences


if __name__ == '__main__':
    main()
