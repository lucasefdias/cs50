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


def build_query_string(column_names, term_strings):
    """Builds the SELECT query for /search route given the columns and terms (two arrays)"""

    # Initialize query string
    query_string = "SELECT * FROM places WHERE ("

    # Loop through columns array
    for col_index, column in enumerate(column_names):

        query_string += "("

        # Loop through all terms to build the OR clause correctly
        for term_index, term_string in enumerate(term_strings):

            # Concatenate column name
            query_string += column

            # Concatenate 'LIKE' clause
            query_string += " LIKE '"

            # Concatenate search term
            query_string += term_string

            # Concatenate 'OR' clause if not at the end of loop
            if term_index < len(term_strings) - 1:
                query_string += "' OR "
            else:
                query_string += "')"

        # Concatenate 'OR' clause if not at the end of loop
        if col_index < len(column_names) - 1:
            query_string += " OR "

    # Concatenate last part of query string
    query_string += ") LIMIT 10"

    # Return the resulting query string
    return query_string


def build_term_strings(q):
    """Build the query strings for the search terms typed by the user"""

    # Initializes array for storing term strings
    term_strings = []

    # Check for comma or spaces and split input string
    if q.count(",") or q.count(" "):

        # If input has commas, split terms using commas, else split using spaces
        if q.count(","):
            q = q.split(",")
        else:
            q = q.split(" ")

        # Sanitize each term in input and add wildcard before and after
        for index, term in enumerate(q):

            term = term.strip()
            term_string =""

            # If not first search term, add wildcard before
            if index > 0:
                term_string += "%"

            term_string += term + "%"

            # Append term to array
            term_strings.append(term_string)


    # Else, single-word search
    else:
        term_string = "%" + q + "%"
        term_strings.append(term_string)

    # Return array with all term strings
    return term_strings




@app.route("/populate")
def populate():

    # Query database for places table
    places = db.execute("SELECT * FROM places")

    # Loop through each row of places
    for place in places:

        # Loop through all columns used as indexes
        for column in ["postal_code", "place_name", "admin_name1", "admin_code1", "latitude", "longitude"]:

            # Create virtual table row for insertion
            vt_row = []

            # Append place_id to vt_row
            vt_row.append(place["place_id"])

            # Append current column to vt_row
            vt_row.append(place[column])

            # Insert vt_row into places_index
            new_row = db.execute("INSERT INTO places_index(place_id, data) VALUES (:place_id, :data)", place_id=vt_row[0], data=vt_row[1])

    # Retrieve full virtual table for error checking
    virtual_table = db.execute("SELECT * FROM places_index")

    return jsonify(virtual_table)


# Viewing virtual table data
@app.route("/virtual")
def virtual():

    places_index = db.execute("SELECT * FROM places_index ORDER BY place_id")

    return jsonify(places_index)





# RANKING FUNCTIONS
def rank(raw_match_info):
    """ handle match_info called w/default args 'pcx' - based on the example rank
    function http://sqlite.org/fts3.html#appendix_a """

    match_info = _parse_match_info(raw_match_info)
    score = 0.0
    p, c = match_info[:2]
    for phrase_num in range(p):
        phrase_info_idx = 2 + (phrase_num * c * 3)
        for col_num in range(c):
            col_idx = phrase_info_idx + (col_num * 3)
            x1, x2 = match_info[col_idx:col_idx + 2]
            if x1 > 0:
                score += float(x1) / x2
    return -score



def _parse_match_info(buf):
    """ Parses the matchinfo BLOB """

    bufsize = len(buf)  # Length in bytes.
    return [struct.unpack('@I', buf[i:i+4])[0] for i in range(0, bufsize, 4)]