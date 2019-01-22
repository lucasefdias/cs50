# ----------------------------------------------------
# CS50 Final Project:
#
# Summary: Web App for connecting musicians and other
# music professionals.
# Enables every user to search for people
# based on their instrument and location.
#
# Lucas Emidio Fernandes Dias
# 30 December 2018
# ----------------------------------------------------

# Import modules
import os
import sqlite3

from datetime import datetime, timezone
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import (accept_connection, add_wildcards,
                    create_account, create_comment, create_connection, create_conversation, create_instrument, create_location, create_message, create_page, create_profile, create_post, create_occupation,
                    delete_account, delete_comment, delete_connection, delete_instrument, delete_page, delete_post, delete_occupation,
                    get_all_comments, get_all_connections, get_all_conversations, get_all_instruments, get_all_occupations, get_all_pages, get_all_posts,
                    get_comment, get_connection_by_id, get_messages,
                    get_connection, get_conversation, get_instrument, get_location, get_occupation, get_page, get_post, get_platforms, get_proficiency, get_results, get_user_profile,
                    lookup, login_required, save_picture, delete_picture,
                    update_comment, update_instrument, update_location, update_occupation, update_page,
                    create_indexes_user,
                    update_account, update_indexes_instruments, update_indexes_location, update_indexes_occupations, update_indexes_user, update_password, update_profile, update_post)

# Configure app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database config (create a connection)
conn = sqlite3.connect('project.db', check_same_thread=False)

# -------------------------------------------------------
# Routes
# -------------------------------------------------------

# -------------------------------------------------------
# LANDING
# -------------------------------------------------------
@app.route("/")
def index():
    """ Render landing page if user is not logged in """

    if 'user_id' in session:
        return redirect(url_for('feed'))

    else:
        return render_template("index.html")



# -------------------------------------------------------
# USER AUTH
# -------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """ Handles user login """

    # User is already logged in
    if 'user_id' in session:
        return redirect(url_for('feed'))

    # If request is sent via "POST"
    if request.method == "POST":

        # Check if form fields are not empty
        if not request.form.get("email"):
            flash("Must provide e-mail.", "danger")
            return redirect(url_for('login'))
        if not request.form.get("password"):
            flash("Must provide password.", "danger")
            return redirect(url_for('login'))

        # Checks if provided email exists in database
        cursor = conn.execute("SELECT * FROM users WHERE email=?",
                            (request.form.get("email"),))
        row = cursor.fetchone()
        if row is None:
            flash("User does not exist.", "danger")
            return redirect(url_for('login'))

        # Hashes provided password and compares with database hash
        if not check_password_hash(row[4], request.form.get("password")):
            flash("Incorrect password.", "danger")
            return redirect(url_for('login'))

        # Logs user in (stores session id)
        session["user_id"] = row[0]

        # Redirects to user feed
        flash(f"Welcome back, {row[1]}!", "success")
        return redirect(url_for('feed'))

    # Else, render login form
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """ Handles user logout """

    # Forgets session id
    session.clear()

    # Redirects to login page
    flash("Successfully logged out!", "success")
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Handles user registration """

    # User is already logged in
    if 'user_id' in session:
        return redirect(url_for('feed'))

    # Reached route via "POST"
    if request.method == "POST":

        # Check if form fields are not empty
        if not request.form.get("first"):
            flash("Must provide first name.", "danger")
            return redirect(url_for('register'))

        if not request.form.get("last"):
            flash("Must provide last name.", "danger")
            return redirect(url_for('register'))

        if not request.form.get("email"):
            flash("Must provide e-mail.", "danger")
            return redirect(url_for('register'))

        if not request.form.get("password"):
            flash("Must provide password.", "danger")
            return redirect(url_for('register'))

        if not request.form.get("confirmation"):
            flash("Must confirm password.", "danger")
            return redirect(url_for('register'))

        # Check if "Password" matches "Confirmation"
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don't match.", "danger")
            return redirect(url_for('register'))

        # Hashes password and inserts user into database
        hashed_pwd = generate_password_hash(request.form.get("password"))

        # Creates user object
        user = {}
        user["first"] = request.form.get("first")
        user["last"] = request.form.get("last")
        user["email"] = request.form.get("email")
        user["hashed"] = hashed_pwd

        # Creates user in database
        userid = create_account(conn, user)

        # Logs user in and redirects to profile page
        session["user_id"] = userid

        # Creates user profile in database
        create_profile(conn, userid)

        # Insert user entry into indexes virtual table
        create_indexes_user(conn, session["user_id"], user["first"], user["last"])

        # Redirects to profile page
        flash(f"Welcome, {user['first']}!", "success")
        flash("Fill in your details to make your profile stand out and to start connecting!", "primary")

        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    # Reached route via GET
    else:
        return render_template("register.html")


# -------------------------------------------------------
# USER
# -------------------------------------------------------
@app.route("/account", methods=["GET", "POST"])
def account():
    """ User account management """

    # If request is sent via "POST"
    if request.method == "POST":

        # Check if form fields are not empty
        if not request.form.get("email"):
            flash("Must provide e-mail.", "danger")
            return redirect(url_for('account'))

        # Checks if provided email exists in database
        cursor = conn.execute("SELECT * FROM users WHERE email=:email",
                            {"email": request.form.get("email")})
        row = cursor.fetchone()
        if row:
            flash("E-mail is already being used.", "danger")
            return redirect(url_for('account'))

        user = {}
        user["id"] = session["user_id"]
        user["email"] = request.form.get("email")

        # Update user info on database
        update_account(conn, user)

        # Redirects to user account
        flash("E-mail updated!", "success")
        return redirect(url_for('account'))

    # Else, render account page
    else:
        user = get_user_profile(conn, session["user_id"])

        return render_template("account.html", user=user)


@app.route("/password/change", methods=["GET", "POST"])
@login_required
def password_change():
    """ Enables password change """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("current"):
            flash("Must provide current password.", "danger")
            return redirect(url_for('password_change'))

        # Ensure current password is correct
        # Query database for user's current password
        cursor = conn.execute("SELECT hash FROM users WHERE id=:userid",
                            {"userid": session["user_id"]})
        row = cursor.fetchone()

        if not check_password_hash(row[0], request.form.get("current")):
            flash("Invalid current password.", "danger")
            return redirect(url_for('password_change'))

        # Ensure new password was submitted
        if not request.form.get("new"):
            flash("Must provide new password.", "danger")
            return redirect(url_for('password_change'))

        # Ensure new password confirmation was submitted
        if not request.form.get("confirmation"):
            flash("Must confirm new password.", "danger")
            return redirect(url_for('password_change'))

        # Ensure password and confirmation match
        if request.form.get("new") != request.form.get("confirmation"):
            flash("Passwords did not match.", "danger")
            return redirect(url_for('password_change'))

        # Hashes new password
        password_hash = generate_password_hash(request.form.get("new"))

        # Updates password in the database
        update_password(conn, session["user_id"], password_hash)

        # Redirect user to account page
        flash("Successfully altered password!", "success")
        return redirect(url_for('account'))

    # User reached route via GET
    else:
        return render_template("password.html")


@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    """ Enables a user to delete account """

    if request.method == "POST":

        # Delete post from database
        delete_account(app, conn, session["user_id"])

        # Forgets session id
        session.clear()

        # Redirects to register page
        flash("Account deleted!", "success")
        return redirect(url_for('register'))

    else:

        # Get user
        user = get_user_profile(conn, session["user_id"])

        content = {}
        content["id"] = user["id"]
        content["type"] = "Account"
        content["delete_url"] = "/account/delete"
        content["cancel_url"] = "/account"

        return render_template("delete.html", content=content)


# -------------------------------------------------------
# PROFILE
# -------------------------------------------------------

@app.route("/profile/<userid>")
@login_required
def profile(userid):
    """ Render profile page """

    # Get user profile
    user = get_user_profile(conn, userid)

    # Get connection between profile user and logged user
    connection = get_connection(conn, session["user_id"], int(userid))

    # Get location
    location = get_location(conn, userid)

    # Get user occupations
    occupations = get_all_occupations(conn, userid)

    # Get instruments
    instruments = get_all_instruments(conn, userid)

    # Get pages
    pages = get_all_pages(conn, userid)

    return render_template("profile.html", user=user, connection=connection, location=location, occupations=occupations, instruments=instruments, pages=pages)


@app.route("/profile/<userid>/edit", methods=["GET", "POST"])
@login_required
def profile_edit(userid):
    """ Handles profile update """

    if request.method == "POST":

        # Check if name fields are not empty
        if not request.form.get("first"):
            flash("Must provide first name.", "danger")
            return redirect("/profile/" + userid + "/edit")

        if not request.form.get("last"):
            flash("Must provide last name.", "danger")
            return redirect("/profile/" + userid + "/edit")

        # Creates profile object and stores form data and session id
        profile = {}
        profile["id"] = userid
        # Get form data
        profile["first"] = request.form.get("first")
        profile["last"] = request.form.get("last")
        profile["birth"] = request.form.get("birth")
        profile["gender"] = request.form.get("gender")
        profile["bio"] = request.form.get("bio")
        if profile["bio"] == '':
            bio = None

        # Checks if the user provided a picture, saves new picture, deletes old picture and stores new name
        if "picture" in request.files:

            picture = request.files["picture"]
            picture_name = save_picture(app, picture)
            old_picture_name = conn.execute("SELECT picture FROM profiles WHERE id=:userid", {'userid': session['user_id']}).fetchone()[0]

            if old_picture_name != 'default.jpg':
                delete_picture(app, old_picture_name)

        else:
            picture_name = conn.execute("SELECT picture FROM profiles WHERE id=:userid", {'userid': session['user_id']}).fetchone()[0]

        profile["picture"] = picture_name

        # Update database with form data
        update_profile(conn, profile)

        # Update indexes virtual table
        update_indexes_user(conn, session["user_id"], profile["first"], profile["last"])

        # Redirect user to profile page
        flash("Your profile has been updated.", "success")
        return redirect("/profile/" + userid + "/edit")

    else:
        if str(session["user_id"]) != userid:
            return redirect("/profile/" + userid + "/edit")

        # Get all user info for requested profile
        user = get_user_profile(conn, userid)

        # Location
        location = get_location(conn, userid)

        # User occupations
        occupations = get_all_occupations(conn, session["user_id"])

        # Get instruments and proficiency levels
        instruments = get_all_instruments(conn, session["user_id"])
        proficiency = get_proficiency(conn)

        # Get pages and platforms
        pages = get_all_pages(conn, session["user_id"])
        platforms = get_platforms(conn)

        return render_template("profile_edit.html", user=user, location=location, occupations=occupations, instruments=instruments, proficiency=proficiency, pages=pages, platforms=platforms)




# -------------------------------------------------------
# CONNECTIONS
# -------------------------------------------------------

@app.route("/connections")
@login_required
def connections():
    """ Render connections page """

    connections = get_all_connections(conn, session["user_id"])

    accepted_connections = []
    connection_requests = []

    # Separate connections requests from accepted connections
    for connection in connections:

        if connection["is_accepted"]:
            accepted_connections.append(connection)
        else:
            connection_requests.append(connection)

    return render_template("connections.html", connections=accepted_connections, requests=connection_requests)


@app.route("/connections/<otheruserid>/accept")
@login_required
def accept(otheruserid):
    """ Handles connection acceptance """

    # Queries database for connection
    connection = get_connection(conn, session["user_id"], int(otheruserid))

    # Checks for existing connection
    if connection == None:
        flash("Connection does not exist.", "danger")
        return redirect(url_for('connections'))

    # Checks permission for acceptance
    if session["user_id"] != connection["receiver_id"]:
        flash("You don't have permission to do that.", "danger")
        return redirect(url_for('connections'))

    # If everything is ok, accept connection and redirect
    accept_connection(conn, connection["id"])

    flash("Connection request accepted!", "success")
    return redirect(url_for('connections'))


@app.route("/profile/<userid>/connect/<requesterid>")
@login_required
def connect(userid, requesterid):
    """ Route for sending a connection request to a user """

    # Checks if connection between users exist
    connection = get_connection(conn, int(requesterid), int(userid))

    # If connection does not exist yet, create connection
    if connection == None:
        create_connection(conn, int(requesterid), int(userid))

    flash("Connection request sent!", "success")
    return redirect("/profile/" + userid)


@app.route("/connections/<connectionid>/delete", methods=["GET", "POST"])
@login_required
def connection_delete(connectionid):
    """ Enables user to delete a connection """

    if request.method == "POST":

        # Check post ownership
        connection = get_connection_by_id(conn, connectionid)

        # Check connection ownership
        if session["user_id"] != connection["sender_id"] and session["user_id"] != connection["receiver_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect(url_for('connections'))

        # Delete post from database
        delete_connection(conn, connectionid)

        # Redirect to connections page
        flash("Connection deleted!", "success")
        return redirect(url_for('connections'))

    else:

        # Get connection
        connection= get_connection_by_id(conn, connectionid)

        # Check connection ownership
        if session["user_id"] != connection["sender_id"] and session["user_id"] != connection["receiver_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect(url_for('connections'))

        content = {}
        content["id"] = connection["id"]
        content["type"] = "Connection"
        content["delete_url"] = "/connections/" + connectionid + "/delete"
        content["cancel_url"] = "/connections"

        return render_template("delete.html", content=content)


# -------------------------------------------------------
# POSTS
# -------------------------------------------------------
@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    """ Render user feed page """

    if request.method == "POST":

        # Checks for empty text field
        if not request.form.get("content"):
            flash("Post cannot be empty.", "danger")
            return redirect(url_for('feed'))

        # Insert post into database
        create_post(conn, session["user_id"], request.form.get("content"))

        # Redirect to feed
        flash("Post submitted!", "success")
        return redirect(url_for('feed'))

    else:

        posts = get_all_posts(conn)

        return render_template("feed.html", posts=posts)



@app.route("/post/<postid>", methods=["GET", "POST"])
@login_required
def post_page(postid):
    """ Enables users to post comments to a specific post """

    if request.method == "POST":

        # Checks for empty text field
        if not request.form.get("content"):
            flash("Comment cannot be empty.", "danger")
            return redirect("/post/" + postid)

        # Insert comment into database
        create_comment(conn, session["user_id"], postid, request.form.get("content"))

        # Redirect to feed
        flash("Comment submitted!", "success")
        return redirect("/post/" + postid)

    else:

        # Get post and related comments
        post = get_post(conn, postid)
        comments = get_all_comments(conn, postid)

        return render_template("post.html", post=post, comments=comments)


@app.route("/post/<postid>/edit", methods=["GET", "POST"])
@login_required
def post_edit(postid):
    """ Enables post owner to edit post """

    if request.method == "POST":

        # Checks for empty text field
        if not request.form.get("content"):
            flash("Post cannot be empty.", "danger")
            return redirect("/post/" + postid + "/edit")

        # Insert comment into database
        update_post(conn, postid, request.form.get("content"))

        # Redirect to post page
        flash("Post updated!", "success")
        return redirect("/post/" + postid)

    else:

        # Get post
        post = get_post(conn, postid)

        # Check post ownership
        if session["user_id"] != post["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + postid)

        return render_template("post_edit.html", post=post)


@app.route("/post/<postid>/delete", methods=["GET", "POST"])
@login_required
def post_delete(postid):
    """ Enables post owner to delete post """

    if request.method == "POST":

        # Check post ownership
        post = get_post(conn, postid)

        if session["user_id"] != post["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + post["id"])

        # Delete post from database
        delete_post(conn, postid)

        # Redirect to feed
        flash("Post deleted!", "success")
        return redirect(url_for('feed'))

    else:

        # Get post
        post= get_post(conn, postid)

        # Check post ownership
        if session["user_id"] != post["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + postid)

        content = {}
        content["id"] = post["id"]
        content["type"] = "Post"
        content["delete_url"] = "/post/" + postid + "/delete"
        content["cancel_url"] = "/post/" + postid

        return render_template("delete.html", content=content)


@app.route("/comment/<commentid>/edit", methods=["GET", "POST"])
@login_required
def comment_edit(commentid):
    """ Enables comment owner to edit comment """

    if request.method == "POST":

        # Check post ownership
        comment = get_comment(conn, commentid)
        if session["user_id"] != comment["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + str(comment["post_id"]))

        # Checks for empty text field
        if not request.form.get("content"):
            flash("Comment cannot be empty.", "danger")
            return redirect("/comment/" + commentid + "/edit")

        # Insert comment into database
        update_comment(conn, commentid, request.form.get("content"))

        # Redirect to post page
        flash("Comment updated!", "success")
        return redirect("/post/" + str(comment["post_id"]))

    else:

        # Get comment
        comment = get_comment(conn, commentid)

        # Check post ownership
        if session["user_id"] != comment["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + str(comment["post_id"]))

        return render_template("comment.html", comment=comment)


@app.route("/comment/<commentid>/delete", methods=["GET", "POST"])
@login_required
def comment_delete(commentid):
    """ Enables comment owner to delete comment """

    if request.method == "POST":

        # Check post ownership
        comment = get_comment(conn, commentid)

        if session["user_id"] != comment["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + str(comment["post_id"]))

        # Delete post from database
        delete_comment(conn, comment["post_id"], commentid)

        # Redirect to feed
        flash("Comment deleted!", "success")
        return redirect("/post/" + str(comment["post_id"]))

    else:

        # Get post
        comment = get_comment(conn, commentid)

        # Check post ownership
        if session["user_id"] != comment["author_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/post/" + str(comment["post_id"]))

        content = {}
        content["id"] = comment["id"]
        content["type"] = "Comment"
        content["delete_url"] = "/comment/" + commentid + "/delete"
        content["cancel_url"] = "/post/" + str(comment["post_id"])

        return render_template("delete.html", content=content)



# -------------------------------------------------------
# MESSAGES
# -------------------------------------------------------
@app.route("/messages")
@login_required
def messages():
    """ Render user messages page """

    conversations = get_all_conversations(conn, session["user_id"])

    return render_template("messages.html", conversations=conversations)


@app.route("/messages/<conversationid>/<interlocutorid>", methods=["GET", "POST"])
@login_required
def conversation(conversationid, interlocutorid):
    """ Render user messages page with a specific conversation loaded. """

    if request.method == "POST":

        # Checks for empty text field
        if not request.form.get("content"):
            flash("Message cannot be empty.", "danger")
            return redirect("/messages/" + conversationid)

        # Creates message object
        message = {}
        message["conversation_id"] = int(conversationid)
        message["sender_id"] = session["user_id"]
        message["receiver_id"] = int(interlocutorid)
        message["content"] = request.form.get("content")

        # Create message in database
        create_message(conn, message)

        # Redirect to feed
        flash("Message sent!", "success")
        return redirect("/messages/" + conversationid + "/" + interlocutorid)

    else:

        messages = get_messages(conn, int(conversationid))

        conversations = get_all_conversations(conn, session["user_id"])

        return render_template("conversation.html", messages=messages, conversation_id=int(conversationid), interlocutor_id=interlocutorid, conversations=conversations)



@app.route("/profile/<userid>/send/<requesterid>")
@login_required
def send_message(userid, requesterid):
    """ Route for checking if conversation exists and redirecting to existing conversation
        or creating and redirecting to newly created conversation """

    # Checks if conversation between users exist
    conversation = get_conversation(conn, userid, requesterid)

    # If conversation does not exist yet, create conversation
    if conversation == None:
        create_conversation(conn, int(requesterid), int(userid))
        conversation = get_conversation(conn, int(userid), int(requesterid))

    # Redirect to conversation page
    return redirect("/messages/" + str(conversation["id"]) + "/" + userid)


# -------------------------------------------------------
# OCCUPATIONS
# -------------------------------------------------------


@app.route("/occupations/new", methods=["POST"])
@login_required
def occupation_new():
    """ Add new occupation """

    if request.method == "POST":

        # Check if role field is not empty
        if not request.form.get("role"):
            flash("Must provide a role.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Get form data
        role = request.form.get("role")
        entity = request.form.get("entity")
        start = request.form.get("start")
        end = request.form.get("end")

        # Update database with form data
        create_occupation(conn, session["user_id"], role, entity, start, end)

        # Update indexes virtual table
        update_indexes_occupations(conn, session["user_id"])

        # Redirect user to profile page
        flash("New occupation added!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")


@app.route("/occupations/<occupationid>/edit", methods=["POST"])
@login_required
def occupation_edit(occupationid):
    """ Edit an existing occupation """

    if request.method == "POST":

        # Check if role field is not empty
        if not request.form.get("role"):
            flash("Must provide a role.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Get form data
        role = request.form.get("role")
        entity = request.form.get("entity")
        start = request.form.get("start")
        end = request.form.get("end")

        # Checks permission for editing
        occupation = get_occupation(conn, occupationid)

        if session["user_id"] != occupation["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]))

        # Update database with form data
        update_occupation(conn, occupationid, session["user_id"], role, entity, start, end)

        # Update indexes virtual table
        update_indexes_occupations(conn, session["user_id"])

        # Redirect user to profile edit page
        flash("Occupation updated!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")


@app.route("/occupations/<occupationid>/delete", methods=["GET", "POST"])
@login_required
def occupation_delete(occupationid):
    """ Enables a user to delete occupation """

    if request.method == "POST":

        # Check occupation ownership
        occupation = get_occupation(conn, occupationid)

        if session["user_id"] != occupation["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Delete post from database
        delete_occupation(conn, session["user_id"], occupationid)

        # Update indexes table
        update_indexes_occupations(conn, session["user_id"])

        # Redirect to feed
        flash("Occupation deleted!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:

        # Get occupation
        occupation = get_occupation(conn, occupationid)

        # Check post ownership
        if session["user_id"] != occupation["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        content = {}
        content["id"] = occupation["id"]
        content["type"] = "Occupation"
        content["delete_url"] = "/occupations/" + occupationid + "/delete"
        content["cancel_url"] = "/profile/" + str(session["user_id"]) + "/edit"

        return render_template("delete.html", content=content)




# -------------------------------------------------------
# INSTRUMENTS
# -------------------------------------------------------

@app.route("/instruments/new", methods=["POST"])
@login_required
def instrument_new():
    """ Add new instrument """

    if request.method == "POST":

        # Check if instrument field is not empty
        if not request.form.get("instrument"):
            flash("Must provide an instrument.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Get form data
        instrument = request.form.get("instrument")
        proficiency = request.form.get("proficiency")
        if proficiency == None:
            proficiency = 0

        # Update database with form data
        create_instrument(conn, session["user_id"], instrument, proficiency)

        # Update indexes virtual table
        update_indexes_instruments(conn, session["user_id"])

        # Redirect user to profile page
        flash("New instrument added!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")


@app.route("/instruments/<instrumentid>/edit", methods=["POST"])
@login_required
def instrument_edit(instrumentid):
    """ Edit an existing instrument """

    if request.method == "POST":

        # Check if role field is not empty
        if not request.form.get("instrument"):
            flash("Must provide an instrument.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Get form data
        instrument = request.form.get("instrument")
        proficiency = request.form.get("proficiency")
        if proficiency == None:
            proficiency = 0

        # Checks permission for editing
        instrument_obj = get_instrument(conn, instrumentid)

        if session["user_id"] != instrument_obj["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]))

        # Update database with form data
        update_instrument(conn, instrumentid, session["user_id"], instrument, proficiency)

        # Update indexes virtual table
        update_indexes_instruments(conn, session["user_id"])

        # Redirect user to profile edit page
        flash("Instrument updated!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")


@app.route("/instruments/<instrumentid>/delete", methods=["GET", "POST"])
@login_required
def instrument_delete(instrumentid):
    """ Enables a user to delete instrument """

    if request.method == "POST":

        # Check instrument ownership
        instrument = get_instrument(conn, instrumentid)

        if session["user_id"] != instrument["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Delete post from database
        delete_instrument(conn, session["user_id"], instrumentid)

        # Update indexes table
        update_indexes_instruments(conn, session["user_id"])

        # Redirect to feed
        flash("Instrument deleted!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:

        # Get occupation
        instrument = get_instrument(conn, instrumentid)

        # Check post ownership
        if session["user_id"] != instrument["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        content = {}
        content["id"] = instrument["id"]
        content["type"] = "Instrument"
        content["delete_url"] = "/instruments/" + instrumentid + "/delete"
        content["cancel_url"] = "/profile/" + str(session["user_id"]) + "/edit"

        return render_template("delete.html", content=content)



# -------------------------------------------------------
# LOCATION
# -------------------------------------------------------

@app.route("/lookup")
@login_required
def lookup_location():
    """ Searches a location """

    query = request.args.get("locationString")

    results = lookup(query)

    return jsonify(results)


@app.route("/location", methods=["GET", "POST"])
@login_required
def location():
    """ Updates the location for a user """

    if request.method == "POST":

        # Check if all fields are filled
        if not request.form.get("country"):
            flash("Must provide a country.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("state"):
            flash("Must provide a state.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("city"):
            flash("Must provide a city.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("geoname_id"):
            flash("Must provide geoname_id.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("full_name"):
            flash("Must provide full_name.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("country_isoalpha2"):
            flash("Must provide country_isoalpha2.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("country_isoalpha3"):
            flash("Must provide country_isoalpha3.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")
        if not request.form.get("admin1_code"):
            flash("Must provide admin1_code.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Create location object
        location ={}
        location["id"] = session["user_id"]
        location["country"] = request.form.get("country")
        location["state"] = request.form.get("state")
        location["city"] = request.form.get("city")
        location["geoname_id"] = request.form.get("geoname_id")
        location["full_name"] = request.form.get("full_name")
        location["country_isoalpha2"] = request.form.get("country_isoalpha2")
        location["country_isoalpha3"] = request.form.get("country_isoalpha3")
        location["admin1_code"] = request.form.get("admin1_code")
        location["latitude"] = request.form.get("latitude")
        location["longitude"] = request.form.get("longitude")

        # Checks to see if there is a location entry for the current user
        if get_location(conn, session["user_id"]):
            update_location(conn, location)
        else:
            create_location(conn, location)

        # Update location in indexes virtual table
        update_indexes_location(conn, location)

        flash("Location updated!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")




# -------------------------------------------------------
# SEARCH
# -------------------------------------------------------

@app.route("/search")
@login_required
def search():
    """ Searches a user query """

    query = request.args.get("q")

    wild_query = add_wildcards(query)

    results = get_results(conn, wild_query)

    return render_template("search.html", query=query, results=results)


# -------------------------------------------------------
# PAGES
# -------------------------------------------------------

@app.route("/pages/new", methods=["POST"])
def page_new():
    """ Add new page """

    if request.method == "POST":

        # Check if url field is not empty
        if not request.form.get("url"):
            flash("Must provide an url.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Get form data
        url = request.form.get("url")
        platform_id = request.form.get("platform")
        if platform_id == None:
            platform_id = 0

        # Update database with form data
        create_page(conn, session["user_id"], url, platform_id)

        # Redirect user to profile page
        flash("New page added!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")


@app.route("/pages/<pageid>/edit", methods=["POST"])
@login_required
def page_edit(pageid):
    """ Edit an existing page """

    if request.method == "POST":

        # Check if url field is not empty
        if not request.form.get("url"):
            flash("Must provide an URL.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Get form data
        url = request.form.get("url")
        platform_id = request.form.get("platform")
        if platform_id == None:
            platform_id = 0

        # Checks permission for editing
        page = get_page(conn, pageid)

        if session["user_id"] != page["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]))

        # Update database with form data
        update_page(conn, pageid, session["user_id"], url, platform_id)

        # Redirect user to profile edit page
        flash("Page updated!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:
        return redirect("/profile/" + str(session["user_id"]) + "/edit")


@app.route("/pages/<pageid>/delete", methods=["GET", "POST"])
@login_required
def page_delete(pageid):
    """ Enables a user to delete a page """

    if request.method == "POST":

        # Check instrument ownership
        page = get_page(conn, pageid)

        if session["user_id"] != page["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        # Delete post from database
        delete_page(conn, session["user_id"], pageid)

        # Redirect to feed
        flash("Page deleted!", "success")
        return redirect("/profile/" + str(session["user_id"]) + "/edit")

    else:

        # Get occupation
        page = get_page(conn, pageid)

        # Check post ownership
        if session["user_id"] != page["user_id"]:
            flash("You don't have permission to do that.", "danger")
            return redirect("/profile/" + str(session["user_id"]) + "/edit")

        content = {}
        content["id"] = page["id"]
        content["type"] = "Page"
        content["delete_url"] = "/pages/" + pageid + "/delete"
        content["cancel_url"] = "/profile/" + str(session["user_id"]) + "/edit"

        return render_template("delete.html", content=content)