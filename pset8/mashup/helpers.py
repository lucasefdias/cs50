import feedparser
import urllib.parse


def lookup(geo):
    """Look up articles for geo"""

    # Check cache
    try:
        if geo in lookup.cache:
            return lookup.cache[geo]
    except AttributeError:
        lookup.cache = {}

    # Replace special characters
    escaped = urllib.parse.quote(geo, safe="")

    # Get feed from Google
    feed = feedparser.parse(f"https://news.google.com/news/rss/local/section/geo/{escaped}")

    # If no items in feed, get feed from Onion
    if not feed["items"]:
        feed = feedparser.parse("http://www.theonion.com/feeds/rss")

    # Cache results
    lookup.cache[geo] = [{"link": item["link"], "title": item["title"]} for item in feed["items"]]

    # Return results
    return lookup.cache[geo]


def add_wildcards(q):
    """Append wildcard operator to each token (search term) of the q parameter"""

    # Initializes array for storing term strings
    wild_q = []

    # Check for comma or spaces and split input string
    if q.count(",") or q.count(" "):

        # If input has commas, split terms using commas, else split using spaces
        if q.count(","):
            q = q.split(",")
        else:
            q = q.split(" ")

        # Sanitize each term in input and append wildcard
        for index, term in enumerate(q):

            term = term.strip()
            new_term = ""
            new_term += term + "*"

            # Append term to array
            wild_q.append(new_term)

    # Else, single-word search
    else:
        new_q = q + "*"
        wild_q.append(new_q)

    # Join list elements and return new q string
    new_q = " ".join(wild_q)

    return new_q