import os
import requests
import secrets
import sqlite3

from flask import flash, redirect, session
from functools import wraps
from PIL import Image, ImageOps


# -------------------------------------------------------------
# USER AUTH
# -------------------------------------------------------------

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# -------------------------------------------------------------
# USER
# -------------------------------------------------------------

def create_account(conn, user):
    """ Creates user account """

    # Tries to insert user into database
    try:
        with conn:
            cursor = conn.execute("""INSERT INTO users (first, last, email, hash, created_at)
                               VALUES (:first, :last, :email, :hashed, datetime('now'))""",
                                  {"first": user["first"], "last": user["last"],
                                   "email": user["email"], "hashed": user["hashed"]})
    except sqlite3.IntegrityError:
        flash("Failed to register user.", "danger")
        return redirect("/register")

    # Return user id
    return cursor.lastrowid


def update_account(conn, user):
    """ Updates user account """

    # Tries to update email in database
    try:
        with conn:
            conn.execute("""UPDATE users
                             SET email = :email
                             WHERE id = :userid""",
                         {"userid": user["id"], "email": user["email"]})
    except sqlite3.IntegrityError:
        flash("Failed to update e-mail.", "danger")
        return redirect("/account")


def update_password(conn, userid, password_hash):
    """ Updates user password """

    # Tries to update password in database
    try:
        with conn:
            conn.execute("""UPDATE users
                             SET hash = :password_hash
                             WHERE id = :userid""",
                         {"userid": userid, "password_hash": password_hash})
    except sqlite3.IntegrityError:
        flash("Failed to update password.", "danger")
        return redirect("/account")


def delete_account(app, conn, userid):
    """ Deletes a user account """

    # Tries to delete user entry in database and all user-related data
    try:
        with conn:
            # Profile

            # Get picture filename and delete file
            picture_filename = get_picture_filename(conn, userid)
            delete_picture(app, picture_filename)

            # Delete user profile
            conn.execute("""DELETE FROM profiles
                            WHERE id = :userid""",
                         {"userid": userid})
            # Comments
            conn.execute("""DELETE FROM comments
                            WHERE author_id = :userid""",
                         {"userid": userid})
            # Posts
            conn.execute("""DELETE FROM posts
                            WHERE author_id = :userid""",
                         {"userid": userid})
            # Connections
            conn.execute("""DELETE FROM connections
                            WHERE
                                sender_id = :userid
                                OR
                                receiver_id = :userid""",
                         {"userid": userid})
            # Messages
            conn.execute("""DELETE FROM messages
                            WHERE
                                sender_id = :userid
                                OR
                                receiver_id = :userid""",
                         {"userid": userid})
            # Conversations
            conn.execute("""DELETE FROM conversations
                            WHERE
                                starter_id = :userid
                                OR
                                interlocutor_id = :userid""",
                         {"userid": userid})
            # Location
            conn.execute("""DELETE FROM locations
                            WHERE id = :userid""",
                         {"userid": userid})
            # Occupations
            conn.execute("""DELETE FROM occupations
                            WHERE user_id = :userid""",
                         {"userid": userid})
            # Instruments
            conn.execute("""DELETE FROM instruments
                            WHERE user_id = :userid""",
                         {"userid": userid})
            # Pages
            conn.execute("""DELETE FROM pages
                            WHERE user_id = :userid""",
                         {"userid": userid})
            # Index
            conn.execute("""DELETE FROM indexes
                            WHERE id = :userid""",
                         {"userid": userid})
            # User
            conn.execute("""DELETE FROM users
                            WHERE id = :userid""",
                         {"userid": userid})
    except sqlite3.IntegrityError:
        flash("Failed to delete account.", "danger")
        return redirect("/account")

# -------------------------------------------------------------
# PROFILE
# -------------------------------------------------------------


def create_profile(conn, userid):
    """ Creates user profile """

    # Inserts new profile in database
    try:
        with conn:
            insert = conn.execute("""INSERT INTO profiles (id, updated_at)
                               VALUES (:userid, datetime('now'))""",
                                  {"userid": userid})
    except sqlite3.IntegrityError:
        flash("Failed to create user profile.", "danger")
        return redirect("/feed")


def get_user_profile(conn, userid):
    """ Queries all the info for user profile """

    # Query database for user information
    cursor = conn.execute("""SELECT users.*, profiles.*
                        FROM users
                        JOIN profiles ON users.id = profiles.id
                        WHERE users.id=?""",
                          (userid,))
    row = cursor.fetchone()
    if row is None:
        flash("Failed to load requested profile.", "danger")
        return redirect("/feed")

    # Create user object and store queried values
    user = {}
    user["id"] = row[0]
    user["first"] = row[1]
    user["last"] = row[2]
    user["email"] = row[3]
    user["hash"] = row[4]
    user["created_at"] = row[5]

    # Picture path corresponds to directory path + picture name (hashed) in database
    user["picture"] = get_picture_path(row[7])

    user["gender"] = row[8]
    user["birth"] = row[9]
    user["bio"] = row[10]
    user["updated_at"] = row[11]

    return user


def update_profile(conn, profile):
    """ Updates user profile """

    # Tries to update user profile in database
    try:
        with conn:
            conn.execute("""UPDATE users
                            SET first = :first,
                                last = :last
                            WHERE id=:userid
                            """,
                         {'first': profile["first"], 'last': profile["last"], 'userid': profile["id"]})

            conn.execute("""UPDATE profiles
                            SET picture = :picture,
                                birth = :birth,
                                gender = :gender,
                                bio = :bio
                            WHERE id=:userid
                            """,
                         {'picture': profile["picture"], 'birth': profile["birth"],
                          'gender': profile["gender"], 'bio': profile["bio"], 'userid': profile["id"]})
    except sqlite3.IntegrityError:
        flash("Failed to update user profile.", "danger")
        return redirect("/profile/" + profile["id"] + "/edit")


def save_picture(app, form_picture):
    """ Saves picture uploaded by the user in the profile update form """

    # Generate a random hex for new filename
    random_hex = secrets.token_hex(8)

    # Get the file extension
    _, f_ext = os.path.splitext(form_picture.filename)

    # Define new filename and file path
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, get_picture_path(picture_filename))

    # Resize and crop image for file system and performance optimization
    output_size = (200, 200)
    resized_img = Image.open(form_picture)
    resized_img = ImageOps.fit(resized_img, output_size, 0, 0, (0.5, 0.5))

    # Save resized image to file system and return the path to the image
    resized_img.save(picture_path)

    return picture_filename


def delete_picture(app, picture_filename):
    """ Deletes a picture from file system given the file path """

    picture_path = os.path.join(
        app.root_path, get_picture_path(picture_filename))
    os.remove(picture_path)


def get_picture_path(picture_name):
    """ Returns the relative path (from application.py) to the specified profile picture """

    picture_path = os.path.join('static/profile_pics', picture_name)

    return picture_path


def get_picture_filename(conn, userid):
    """ Returns user picture filename stored in database """

    # Query database for user information
    cursor = conn.execute("""SELECT picture
                        FROM profiles
                        WHERE id = :userid""",
                          {"userid": userid})
    row = cursor.fetchone()
    if row is None:
        flash("Failed to get picture filename.", "danger")
        return redirect("/feed")

    picture_filename = row[0]

    return picture_filename


# -------------------------------------------------------------
# POSTS
# -------------------------------------------------------------


def create_post(conn, userid, content):
    """ Creates a new post """

    # Tries to insert a new conversation entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO posts (author_id, content, date_published)
                           VALUES (:authorid, :content, datetime('now'))""",
                         {"authorid": userid, "content": content})
    except sqlite3.IntegrityError:
        flash("Failed to submit post.", "danger")
        return redirect("/feed")


def get_post(conn, postid):
    """ Queries a specific post with additional user info """

    # Query database for user information
    cursor = conn.execute("""SELECT posts.*, users.first, users.last, profiles.picture
                             FROM posts
                             JOIN users ON posts.author_id = users.id
                             JOIN profiles ON posts.author_id = profiles.id
                             WHERE posts.id = :postid""", {"postid": postid})
    row = cursor.fetchone()
    if row is None:
        flash("Failed to load post.", "danger")
        return redirect("/feed")

    post = {}
    post["id"] = row[0]
    post["author_id"] = row[1]
    post["content"] = row[2]
    post["date_published"] = row[3]
    post["author_first"] = row[4]
    post["author_last"] = row[5]
    post["author_picture"] = get_picture_path(row[6])

    return post


def get_all_posts(conn):
    """ Queries all posts with additional user info """

    # Query database for user information
    cursor = conn.execute("""SELECT posts.*, users.first, users.last, profiles.picture
                             FROM posts
                             JOIN users ON posts.author_id = users.id
                             JOIN profiles ON posts.author_id = profiles.id
                             ORDER BY posts.date_published DESC""")
    rows = cursor.fetchall()
    if rows is None:
        flash("Failed to load posts.", "danger")
        return redirect("/feed")

    # Create posts list and appends post objects
    posts = []
    for row in rows:

        post = {}
        post["id"] = row[0]
        post["author_id"] = row[1]
        post["content"] = row[2]
        post["date_published"] = row[3]
        post["author_first"] = row[4]
        post["author_last"] = row[5]
        post["author_picture"] = get_picture_path(row[6])

        posts.append(post)

    return posts


def update_post(conn, postid, content):
    """ Updates a post """

    # Tries to update post entry in database
    try:
        with conn:
            conn.execute("""UPDATE posts
                             SET content = :content
                             WHERE id = :postid""",
                         {"postid": postid, "content": content})
    except sqlite3.IntegrityError:
        flash("Failed to update post.", "danger")
        return redirect("/post/" + str(postid) + "/edit")


def delete_post(conn, postid):
    """ Deletes a post """

    # Tries to delete post entry in database
    try:
        with conn:
            conn.execute("""DELETE FROM posts
                            WHERE id = :postid""",
                         {"postid": postid})
    except sqlite3.IntegrityError:
        flash("Failed to delete post.", "danger")
        return redirect("/post/" + str(postid))


# -------------------------------------------------------------
# COMMENTS
# -------------------------------------------------------------

def create_comment(conn, userid, postid, content):
    """ Creates a new comment """

    # Tries to insert a new conversation entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO comments (author_id, post_id, content, date_published)
                           VALUES (:authorid, :postid, :content, datetime('now'))""",
                         {"authorid": userid,
                          "postid": postid, "content": content})
    except sqlite3.IntegrityError:
        flash("Failed to submit comment.", "danger")
        return redirect("/post/" + postid)


def get_all_comments(conn, postid):
    """ Queries all the comments for a specific post with comment author info """

    # Query database for user information
    cursor = conn.execute("""SELECT comments.*, users.first, users.last, profiles.picture
                             FROM comments
                             JOIN users ON comments.author_id = users.id
                             JOIN posts ON comments.post_id = posts.id
                             JOIN profiles ON comments.author_id = profiles.id
                             WHERE posts.id = :postid
                             ORDER BY comments.date_published ASC""", {"postid": postid})
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create comments list and appends comment objects
    comments = []
    for row in rows:

        comment = {}
        comment["id"] = row[0]
        comment["author_id"] = row[1]
        comment["post_id"] = row[2]
        comment["content"] = row[3]
        comment["date_published"] = row[4]
        comment["author_first"] = row[5]
        comment["author_last"] = row[6]
        comment["author_picture"] = get_picture_path(row[7])

        comments.append(comment)

    return comments


def get_comment(conn, commentid):
    """ Queries a specific comment """

    # Query database for user information
    cursor = conn.execute("""SELECT comments.*, users.first, users.last, profiles.picture
                             FROM comments
                             JOIN users ON comments.author_id = users.id
                             JOIN profiles ON comments.author_id = profiles.id
                             WHERE comments.id = :commentid""",
                          {"commentid": commentid})
    row = cursor.fetchone()
    if row is None:
        return None

    # Create comment object
    comment = {}
    comment["id"] = row[0]
    comment["author_id"] = row[1]
    comment["post_id"] = row[2]
    comment["content"] = row[3]
    comment["date_published"] = row[4]
    comment["author_first"] = row[5]
    comment["author_last"] = row[6]
    comment["author_picture"] = get_picture_path(row[7])

    return comment


def update_comment(conn, commentid, content):
    """ Updates a comment """

    # Tries to update comment entry in database
    try:
        with conn:
            conn.execute("""UPDATE comments
                             SET content = :content
                             WHERE id = :commentid""",
                         {"commentid": commentid, "content": content})
    except sqlite3.IntegrityError:
        flash("Failed to update comment.", "danger")
        return redirect("/comments/" + str(commentid) + "/edit")


def delete_comment(conn, postid, commentid):
    """ Deletes a comment """

    # Tries to delete comment entry in database
    try:
        with conn:
            conn.execute("""DELETE FROM comments
                            WHERE id = :commentid""",
                         {"commentid": commentid})
    except sqlite3.IntegrityError:
        flash("Failed to delete post.", "danger")
        return redirect("/post/" + str(postid))


# -------------------------------------------------------------
# MESSAGES
# -------------------------------------------------------------

def get_conversation(conn, userid, requesterid):
    """ Gets a conversation between users given their ids """

    # Query database for conversation
    cursor = conn.execute("""SELECT *
                             FROM conversations
                             WHERE
                                (starter_id = :userid AND interlocutor_id = :requesterid)
                                OR
                                (starter_id = :requesterid AND interlocutor_id = :userid)""",
                          {"userid": userid, "requesterid": requesterid})
    row = cursor.fetchone()
    if row is None:
        return row

    conversation = {}
    conversation["id"] = row[0]
    conversation["starter_id"] = row[1]
    conversation["interlocutor_id"] = row[2]
    conversation["date_started"] = row[3]
    conversation["last_updated"] = row[4]

    return conversation


def get_all_conversations(conn, userid):
    """ Gets all conversations for a given user with interlocutors' names and pictures"""

    # Query database for conversation
    cursor = conn.execute("""SELECT *
                             FROM conversations
                             WHERE
                                starter_id = :userid
                                OR
                                interlocutor_id = :userid
                             ORDER BY last_updated DESC""",
                          {"userid": userid})
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create conversations list and appends conversation objects
    conversations = []
    for row in rows:

        conversation = {}
        conversation["id"] = row[0]
        conversation["starter_id"] = row[1]
        conversation["interlocutor_id"] = row[2]
        conversation["date_started"] = row[3]
        conversation["last_updated"] = row[4]

        # Gets the interlocutor (user different than session user) details
        if userid != conversation["starter_id"]:
            interlocutor = get_user_profile(conn, conversation["starter_id"])
        else:
            interlocutor = get_user_profile(
                conn, conversation["interlocutor_id"])

        conversation["interlocutor_real_id"] = interlocutor["id"]
        conversation["interlocutor_first"] = interlocutor["first"]
        conversation["interlocutor_last"] = interlocutor["last"]
        conversation["interlocutor_picture"] = interlocutor["picture"]

        conversations.append(conversation)

    return conversations


def create_conversation(conn, starterid, interlocutorid):
    """ Creates a new conversation """

    # Tries to insert a new conversation entry in database
    try:
        with conn:
            cursor = conn.execute("""INSERT INTO conversations (starter_id, interlocutor_id, date_started, last_updated)
                               VALUES (:starterid, :interlocutorid, datetime('now'), datetime('now'))""",
                                  {"starterid": starterid, "interlocutorid": interlocutorid})
    except sqlite3.IntegrityError:
        flash("Failed to create conversation.", "danger")
        return redirect("/messages")


def create_message(conn, message):
    """ Creates a new message """

    # Tries to insert message into database
    try:
        with conn:
            conn.execute("""INSERT INTO messages (conversation_id, sender_id, receiver_id, content, date_sent)
                          VALUES (:conversationid, :senderid, :receiverid, :content, datetime('now'))""",
                         {"conversationid": message["conversation_id"], "senderid": message["sender_id"],
                          "receiverid": message["receiver_id"], "content": message["content"]})
    except sqlite3.IntegrityError:
        flash("Failed to send message.", "danger")
        return redirect("/messages/" + str(message["conversation_id"]) + "/" + str(message["receiver_id"]))


def get_messages(conn, conversationid):
    """ Gets all messages from a conversation with user details"""

    # Query database for conversation
    cursor = conn.execute("""SELECT messages.*, users.first, users.last, profiles.picture
                             FROM messages
                             JOIN users ON messages.sender_id = users.id
                             JOIN profiles ON messages.sender_id = profiles.id
                             WHERE conversation_id = :conversationid
                             ORDER BY date_sent ASC""",
                          {"conversationid": conversationid})
    rows = cursor.fetchall()

    # Create messages list and appends message objects
    messages = []
    for row in rows:

        message = {}
        message["id"] = row[0]
        message["conversation_id"] = row[1]
        message["sender_id"] = row[2]
        message["receiver_id"] = row[3]
        message["content"] = row[4]
        message["date_sent"] = row[5]
        message["date_seen"] = row[6]
        message["sender_first"] = row[7]
        message["sender_last"] = row[8]
        message["sender_picture"] = get_picture_path(row[9])

        messages.append(message)

    return messages

# -------------------------------------------------------------
# CONNECTIONS
# -------------------------------------------------------------


def create_connection(conn, senderid, receiverid):
    """ Creates a new connection """

    # Checks if connection between the two users already exists
    cursor = conn.execute("""SELECT *
                             FROM connections
                             WHERE
                                (sender_id = :senderid AND receiver_id = :receiverid)
                                OR
                                (sender_id = :receiverid AND receiver_id = :senderid)""",
                          {"senderid": senderid, "receiverid": receiverid})
    row = cursor.fetchone()
    if row:
        flash("Connection entry already exists.", "danger")
        return redirect("/connections")

    # Tries to insert a new connection entry in database
    try:
        with conn:
            cursor = conn.execute("""INSERT INTO connections (sender_id, receiver_id, date_sent)
                               VALUES (:senderid, :receiverid, datetime('now'))""",
                                  {"senderid": senderid, "receiverid": receiverid})
    except sqlite3.IntegrityError:
        flash("Failed to send connection request.", "danger")
        return redirect("/profile" + str(receiverid))


def accept_connection(conn, connectionid):
    """ Accepts a connection request """

    # Tries to insert a new connection entry in database
    try:
        with conn:
            cursor = conn.execute("""UPDATE connections
                                     SET is_accepted = 1,
                                         connection_date = datetime('now')
                                     WHERE id = :connectionid""", {"connectionid": connectionid})
    except sqlite3.IntegrityError:
        flash("Failed to accept connection request.", "danger")
        return redirect("/connections")


def get_all_connections(conn, userid):
    """ Gets all connections for a given user with other user's details """

    # Query database for connections
    cursor = conn.execute("""SELECT *
                             FROM connections
                             WHERE
                                sender_id = :userid
                                OR
                                receiver_id = :userid
                             ORDER BY date_sent DESC""",
                          {"userid": userid})
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create conversations list and appends conversation objects
    connections = []
    for row in rows:

        connection = {}
        connection["id"] = row[0]
        connection["sender_id"] = row[1]
        connection["receiver_id"] = row[2]
        connection["date_sent"] = row[3]
        connection["is_accepted"] = row[4]
        connection["date_connected"] = row[5]

        # Assigns a boolean value from numeric value in database
        if connection["is_accepted"]:
            connection["is_accepted"] = True
        else:
            connection["is_accepted"] = False

        # Gets the other user (user different than session user) details
        if userid != connection["sender_id"]:
            other_user = get_user_profile(conn, connection["sender_id"])
        else:
            other_user = get_user_profile(conn, connection["receiver_id"])

        connection["other_user_id"] = other_user["id"]
        connection["other_user_first"] = other_user["first"]
        connection["other_user_last"] = other_user["last"]
        connection["other_user_picture"] = other_user["picture"]

        connections.append(connection)

    return connections


def get_connection(conn, userid, other_userid):
    """ Gets a connection entry given both users' ids """

    # Query database for connection
    cursor = conn.execute("""SELECT *
                             FROM connections
                             WHERE
                                (sender_id = :userid AND receiver_id = :other_userid)
                                OR
                                (sender_id = :other_userid AND receiver_id = :userid)""",
                          {"userid": userid, "other_userid": other_userid})
    row = cursor.fetchone()
    if row is None:
        return row

    connection = {}
    connection["id"] = row[0]
    connection["sender_id"] = row[1]
    connection["receiver_id"] = row[2]
    connection["date_sent"] = row[3]
    connection["is_accepted"] = row[4]
    connection["connection_date"] = row[5]

    return connection


def get_connection_by_id(conn, connectionid):
    """ Gets a connection entry by id """

    # Query database for connection
    cursor = conn.execute("""SELECT *
                             FROM connections
                             WHERE id = :connectionid""",
                          {"connectionid": connectionid})
    row = cursor.fetchone()
    if row is None:
        return row

    connection = {}
    connection["id"] = row[0]
    connection["sender_id"] = row[1]
    connection["receiver_id"] = row[2]
    connection["date_sent"] = row[3]
    connection["is_accepted"] = row[4]
    connection["connection_date"] = row[5]

    return connection


def delete_connection(conn, connectionid):
    """ Deletes a connection """

    # Tries to delete connection entry in database
    try:
        with conn:
            conn.execute("""DELETE FROM connections
                            WHERE id = :connectionid""",
                         {"connectionid": connectionid})
    except sqlite3.IntegrityError:
        flash("Failed to delete connection.", "danger")
        return redirect("/connections")


# -------------------------------------------------------------
# OCCUPATIONS
# -------------------------------------------------------------

def create_occupation(conn, userid, role, entity, start, end):
    """ Creates a new occupation for specific user """

    # Tries to insert a new occupation entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO occupations (user_id, role, entity, start, end)
                           VALUES (:userid, :role, :entity, :start, :end)""",
                         {"userid": userid, "role": role, "entity": entity, "start": start, "end": end})
    except sqlite3.IntegrityError:
        flash("Failed to add occupation.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def get_all_occupations(conn, userid):
    """ Queries user occupation entries in database """

    # Query database for user information
    cursor = conn.execute("""SELECT *
                        FROM occupations
                        WHERE occupations.user_id=:userid
                        ORDER BY occupations.start DESC""",
                          {"userid": userid})
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create occupations list and store queried values
    occupations = []
    for row in rows:
        occupation = {}
        occupation["id"] = row[0]
        occupation["user_id"] = row[1]
        occupation["role"] = row[2]
        occupation["entity"] = row[3]
        occupation["start"] = row[4]
        occupation["end"] = row[5]

        occupations.append(occupation)

    return occupations


def get_occupation(conn, occupationid):
    """ Gets an occupation """

    # Query database for occupation
    cursor = conn.execute("""SELECT *
                             FROM occupations
                             WHERE id = :occupationid""",
                          {"occupationid": occupationid})
    row = cursor.fetchone()
    if row is None:
        return row

    occupation = {}
    occupation["id"] = row[0]
    occupation["user_id"] = row[1]
    occupation["role"] = row[2]
    occupation["entity"] = row[3]
    occupation["start"] = row[4]
    occupation["end"] = row[5]

    return occupation


def update_occupation(conn, occupationid, userid, role, entity, start, end):
    """ Updates an occupation """

    # Tries to update occupation entry in database
    try:
        with conn:
            conn.execute("""UPDATE occupations
                             SET role = :role,
                                 entity = :entity,
                                 start = :start,
                                 end = :end
                             WHERE id = :occupationid""",
                         {"occupationid": occupationid, "role": role,
                             "entity": entity, "start": start, "end": end})
    except sqlite3.IntegrityError:
        flash("Failed to update occupation.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def delete_occupation(conn, userid, occupationid):
    """ Deletes an occupation """

    # Tries to delete occupation entry in database
    try:
        with conn:
            conn.execute("""DELETE FROM occupations
                            WHERE id = :occupationid""",
                         {"occupationid": occupationid})
    except sqlite3.IntegrityError:
        flash("Failed to delete occupation.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


# -------------------------------------------------------------
# INSTRUMENT
# -------------------------------------------------------------

def create_instrument(conn, userid, instrument, proficiency):
    """ Creates a new instrument entry for specific user """

    # Tries to insert a new instrument entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO instruments (user_id, instrument, proficiency_id)
                           VALUES (:userid, :instrument, :proficiency)""",
                         {"userid": userid, "instrument": instrument, "proficiency": proficiency})
    except sqlite3.IntegrityError:
        flash("Failed to add instrument.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def get_proficiency(conn):
    """ Gets all profiency levels """

    # Query database for proficency levels
    cursor = conn.execute("""SELECT *
                        FROM proficiency
                        ORDER BY id ASC""")
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create occupations list and store queried values
    profiency = []
    for row in rows:
        skill_level = {}
        skill_level["id"] = row[0]
        skill_level["level"] = row[1]

        profiency.append(skill_level)

    return profiency


def get_all_instruments(conn, userid):
    """ Queries user instrument entries in database """

    # Query database for instruments
    cursor = conn.execute("""SELECT instruments.*, proficiency.level
                        FROM instruments
                        JOIN proficiency ON instruments.proficiency_id = proficiency.id
                        WHERE instruments.user_id=:userid
                        ORDER BY instruments.proficiency_id DESC, instruments.instrument ASC""",
                          {"userid": userid})
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create instruments list and store queried values
    instruments = []
    for row in rows:
        instrument = {}
        instrument["id"] = row[0]
        instrument["user_id"] = row[1]
        instrument["instrument"] = row[2]
        instrument["proficiency_id"] = row[3]
        instrument["proficiency"] = row[4]

        instruments.append(instrument)

    return instruments


def get_instrument(conn, instrumentid):
    """ Gets an instrument """

    # Query database for instrument
    cursor = conn.execute("""SELECT *
                             FROM instruments
                             WHERE id = :instrumentid""",
                          {"instrumentid": instrumentid})
    row = cursor.fetchone()
    if row is None:
        return row

    instrument = {}
    instrument["id"] = row[0]
    instrument["user_id"] = row[1]
    instrument["instrument"] = row[2]
    instrument["proficiency_id"] = row[3]

    return instrument


def update_instrument(conn, instrumentid, userid, instrument, proficiencyid):
    """ Updates an instrument """

    # Tries to update instrument entry in database
    try:
        with conn:
            conn.execute("""UPDATE instruments
                            SET instrument = :instrument,
                                proficiency_id = :proficiencyid
                            WHERE id = :instrumentid""",
                         {"instrumentid": instrumentid, "instrument": instrument, "proficiencyid": proficiencyid})
    except sqlite3.IntegrityError:
        flash("Failed to update instrument.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def delete_instrument(conn, userid, instrumentid):
    """ Deletes an instrument """

    # Tries to delete occupation entry in database
    try:
        with conn:
            conn.execute("""DELETE FROM instruments
                            WHERE id = :instrumentid""",
                         {"instrumentid": instrumentid})
    except sqlite3.IntegrityError:
        flash("Failed to delete instrument.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


# -------------------------------------------------------------
# LOCATION
# -------------------------------------------------------------

def lookup(search):
    """ Lookup a location using a search string and the Teleport API
        Docs: https://developers.teleport.org/api/ """

    # Create url and embed country and state details in response JSON
    url = f"https://api.teleport.org/api/cities/?search={search}"
    url += "&embed=city:search-results/city:item/{city:country,city:admin1_division}"

    # Request url and get JSON response
    r = requests.get(url)
    json_obj = r.json()

    api_search_results = json_obj["_embedded"]["city:search-results"]

    # Loop through every result in the JSON returned by the API and build a new object for each result
    results = []
    for item in api_search_results:

        result = {}
        result["matching_full_name"] = item['matching_full_name']
        result["full_name"] = item['_embedded']['city:item']["full_name"]
        result["geoname_id"] = item['_embedded']['city:item']["geoname_id"]
        result["latitude"] = item['_embedded']['city:item']["location"]["latlon"]["latitude"]
        result["longitude"] = item['_embedded']['city:item']["location"]["latlon"]["longitude"]
        result["city"] = item['_embedded']['city:item']["name"]
        result["admin1_geoname_id"] = item['_embedded']['city:item']["_embedded"]["city:admin1_division"]["geoname_id"]
        result["admin1_code"] = item['_embedded']['city:item']["_embedded"]["city:admin1_division"]["geonames_admin1_code"]
        result["admin1"] = item['_embedded']['city:item']["_embedded"]["city:admin1_division"]["name"]
        result["country_geoname_id"] = item['_embedded']['city:item']["_embedded"]["city:country"]["geoname_id"]
        result["country_isoalpha2"] = item['_embedded']['city:item']["_embedded"]["city:country"]["iso_alpha2"]
        result["country_isoalpha3"] = item['_embedded']['city:item']["_embedded"]["city:country"]["iso_alpha3"]
        result["country"] = item['_embedded']['city:item']["_embedded"]["city:country"]["name"]

        results.append(result)

    return results


def create_location(conn, location):
    """ Creates a new location entry for specific user """

    # Tries to insert a new instrument entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO locations (
                                id, geoname_id, full_name, country,
                                country_isoalpha2, country_isoalpha3, admin1,
                                admin1_code, city, latitude, longitude)
                           VALUES (
                               :userid, :geoname_id, :full_name, :country,
                               :country_isoalpha2, :country_isoalpha3, :admin1,
                               :admin1_code, :city, :latitude, :longitude)""",
                         {"userid": location["id"], "geoname_id": location["geoname_id"],
                          "full_name": location["full_name"], "country": location["country"],
                          "country_isoalpha2": location["country_isoalpha2"], "country_isoalpha3": location["country_isoalpha3"],
                          "admin1": location["state"], "admin1_code": location["admin1_code"], "city": location["city"],
                          "latitude": location["latitude"], "longitude": location["longitude"]})
    except sqlite3.IntegrityError:
        flash("Failed to add location.", "danger")
        return redirect("/profile/" + str(location["id"]) + "/edit")


def get_location(conn, userid):
    """ Get the location for a given user """

    # Query database for instrument
    cursor = conn.execute("""SELECT *
                             FROM locations
                             WHERE id = :userid""",
                          {"userid": userid})
    row = cursor.fetchone()
    if row is None:
        return row

    location = {}
    location["id"] = row[0]
    location["geoname_id"] = row[1]
    location["full_name"] = row[2]
    location["country"] = row[3]
    location["country_isoalpha2"] = row[4]
    location["country_isoalpha3"] = row[5]
    location["admin1"] = row[6]
    location["admin1_code"] = row[7]
    location["city"] = row[8]
    location["latitude"] = row[9]
    location["longitude"] = row[10]

    return location


def update_location(conn, location):
    """ Updates an location """

    # Tries to update instrument entry in database
    try:
        with conn:
            conn.execute("""UPDATE locations
                            SET geoname_id = :geoname_id, full_name = :full_name,
                                country = :country, country_isoalpha2 = :country_isoalpha2, country_isoalpha3 = :country_isoalpha3,
                                admin1 = :admin1, admin1_code = :admin1_code,
                                city = :city, latitude = :latitude, longitude = :longitude
                            WHERE id = :userid""",
                         {"userid": location["id"], "geoname_id": location["geoname_id"],
                          "full_name": location["full_name"], "country": location["country"],
                          "country_isoalpha2": location["country_isoalpha2"], "country_isoalpha3": location["country_isoalpha3"],
                          "admin1": location["state"], "admin1_code": location["admin1_code"], "city": location["city"],
                          "latitude": location["latitude"], "longitude": location["longitude"]})
    except sqlite3.IntegrityError:
        flash("Failed to update location.", "danger")
        return redirect("/profile/" + str(location["id"]) + "/edit")


# -------------------------------------------------------------
# INDEXES
# -------------------------------------------------------------
def create_indexes_user(conn, userid, first, last):
    """ Inserts a new user entry into indexes virtual table """

    # Tries to insert a new instrument entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO indexes (id, first, last)
                           VALUES (:userid, :first, :last)""",
                         {"userid": userid, "first": first, "last": last})
    except sqlite3.IntegrityError:
        flash("Failed to add user to indexes.", "danger")
        return redirect("/feed")


def update_indexes_user(conn, userid, first, last):
    """ Updates indexes virtual table with user name """

    # Tries to update instrument entry in database
    try:
        with conn:
            conn.execute("""UPDATE indexes
                            SET first = :first, last = :last
                            WHERE CAST(id AS NUMERIC) = :userid""",
                         {"userid": userid, "first": first, "last": last})
    except sqlite3.IntegrityError:
        flash("Failed to update indexes.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def update_indexes_location(conn, location):
    """ Updates indexes virtual table with user name """

    # Tries to update instrument entry in database
    try:
        with conn:
            conn.execute("""UPDATE indexes
                            SET full_name = :full_name, country = :country,
                                country_isoalpha2 = :country_isoalpha2, country_isoalpha3 = :country_isoalpha3,
                                admin1 = :admin1, admin1_code = :admin1_code, city =:city
                            WHERE CAST(id AS NUMERIC) = :userid""",
                         {"userid": location["id"], "full_name": location["full_name"], "country": location["country"],
                          "country_isoalpha2": location["country_isoalpha2"], "country_isoalpha3": location["country_isoalpha3"],
                          "admin1": location["state"], "admin1_code": location["admin1_code"], "city": location["city"]})
    except sqlite3.IntegrityError:
        flash("Failed to update indexes.", "danger")
        return redirect("/profile/" + str(location["id"]) + "/edit")


def update_indexes_occupations(conn, userid):
    """ Updates indexes virtual table with user occupation strings """

    # Builds role and entity strings
    occupation_strings = build_indexes_occupation_strings(conn, userid)

    # Tries to update instrument entry in database
    try:
        with conn:
            conn.execute("""UPDATE indexes
                            SET role = :role,
                                entity = :entity
                            WHERE CAST(id AS NUMERIC) = :userid""",
                         {"userid": userid, "role": occupation_strings["role"], "entity": occupation_strings["entity"]})
    except sqlite3.IntegrityError:
        flash("Failed to update indexes.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def update_indexes_instruments(conn, userid):
    """ Updates indexes virtual table with user instrument strings """

    # Builds role and entity strings
    instrument_strings = build_indexes_instrument_strings(conn, userid)

    # Tries to update instrument entry in database
    try:
        with conn:
            conn.execute("""UPDATE indexes
                            SET instrument = :instrument,
                                proficiency_id = :proficiency_id
                            WHERE CAST(id AS NUMERIC) = :userid""",
                         {"userid": userid, "instrument": instrument_strings["instrument"], "proficiency_id": instrument_strings["proficiency_id"]})
    except sqlite3.IntegrityError:
        flash("Failed to update indexes.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def build_indexes_occupation_strings(conn, userid):
    """ Builds role and entity strings for indexes virtual table """

    occupations = get_all_occupations(conn, userid)

    role_string = ""
    entity_string = ""

    for index, occupation in enumerate(occupations):

        role_string += occupation["role"]
        entity_string += occupation["entity"]
        # Use a token separator
        if index < len(occupations) - 1:
            role_string += ","
            entity_string += ","

    occupation_strings = {}
    occupation_strings["role"] = role_string
    occupation_strings["entity"] = entity_string

    return occupation_strings


def build_indexes_instrument_strings(conn, userid):
    """ Builds instrument and proficiency_id strings for indexes virtual table """

    instruments = get_all_instruments(conn, userid)

    instrument_string = ""
    proficiency_string = ""

    for index, instrument in enumerate(instruments):

        instrument_string += instrument["instrument"]
        proficiency_string += str(instrument["proficiency_id"])
        # Use a token separator
        if index < len(instruments) - 1:
            instrument_string += ","
            proficiency_string += ","

    instrument_strings = {}
    instrument_strings["instrument"] = instrument_string
    instrument_strings["proficiency_id"] = proficiency_string

    return instrument_strings


# -------------------------------------------------------------
# SEARCH
# -------------------------------------------------------------

def get_results(conn, query):
    """ Return matching results for a query """

    # Query database for instruments
    cursor = conn.execute("""SELECT users.id, users.first, users.last, profiles.picture
                        FROM users
                        JOIN profiles ON users.id = profiles.id
                        JOIN indexes ON users.id = indexes.id
                        WHERE indexes MATCH :query""",
                          {"query": query})
    rows = cursor.fetchall()
    if rows is None:
        return None

    # Create results list and store queried values
    results = []
    for row in rows:
        result = {}
        result["id"] = row[0]
        result["first"] = row[1]
        result["last"] = row[2]
        # Picture path corresponds to directory path + picture name (hashed) in database
        result["picture"] = get_picture_path(row[3])

        results.append(result)

    return results


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


# -------------------------------------------------------------
# PAGES
# -------------------------------------------------------------


def create_page(conn, userid, url, platform_id):
    """ Creates a new page entry for specific user """

    # Tries to insert a new page entry in database
    try:
        with conn:
            conn.execute("""INSERT INTO pages (user_id, url, platform_id)
                           VALUES (:userid, :url, :platform_id)""",
                         {"userid": userid, "url": url, "platform_id": platform_id})
    except sqlite3.IntegrityError:
        flash("Failed to add page.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def get_platforms(conn):
    """ Gets all platforms """

    # Query database for platforms
    cursor = conn.execute("""SELECT *
                        FROM platforms
                        ORDER BY id ASC""")
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create platform list and store queried values
    platforms = []
    for row in rows:
        platform = {}
        platform["id"] = row[0]
        platform["platform"] = row[1]

        platforms.append(platform)

    return platforms


def get_all_pages(conn, userid):
    """ Queries user social media and web page entries in database """

    # Query database for pages
    cursor = conn.execute("""SELECT pages.*, platforms.platform
                        FROM pages
                        JOIN platforms ON pages.platform_id = platforms.id
                        WHERE pages.user_id=:userid""",
                          {"userid": userid})
    rows = cursor.fetchall()
    if rows is None:
        return []

    # Create pages list and store queried values
    pages = []
    for row in rows:
        page = {}
        page["id"] = row[0]
        page["user_id"] = row[1]
        page["url"] = row[2]
        page["platform_id"] = row[3]
        page["platform"] = row[4]

        pages.append(page)

    return pages


def get_page(conn, pageid):
    """ Gets a page """

    # Query database for page
    cursor = conn.execute("""SELECT *
                             FROM pages
                             WHERE id = :pageid""",
                          {"pageid": pageid})
    row = cursor.fetchone()
    if row is None:
        return row

    page = {}
    page["id"] = row[0]
    page["user_id"] = row[1]
    page["url"] = row[2]
    page["platform_id"] = row[3]

    return page


def update_page(conn, pageid, userid, url, platform_id):
    """ Updates a page """

    # Tries to update page entry in database
    try:
        with conn:
            conn.execute("""UPDATE pages
                            SET url = :url,
                                platform_id = :platform_id
                            WHERE id = :pageid""",
                         {"pageid": pageid, "url": url, "platform_id": platform_id})
    except sqlite3.IntegrityError:
        flash("Failed to update page.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")


def delete_page(conn, userid, pageid):
    """ Deletes a page """

    # Tries to delete page entry in database
    try:
        with conn:
            conn.execute("""DELETE FROM pages
                            WHERE id = :pageid""",
                         {"pageid": pageid})
    except sqlite3.IntegrityError:
        flash("Failed to delete page.", "danger")
        return redirect("/profile/" + str(userid) + "/edit")
