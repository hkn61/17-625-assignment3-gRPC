import sqlite3

conn = sqlite3.connect('reddit.db', check_same_thread=False)
cursor = conn.cursor()  

def initialize_database():
    # conn = sqlite3.connect('reddit.db')
    # cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Post (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        text TEXT,
                        video_url TEXT,
                        image_url TEXT,
                        author TEXT,
                        score INTEGER DEFAULT 0,
                        state TEXT NOT NULL,
                        publication_date TEXT NOT NULL,
                        subreddit_id TEXT
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Comment (
                        id TEXT PRIMARY KEY,
                        content TEXT,
                        author TEXT NOT NULL,
                        score INTEGER DEFAULT 0,
                        status TEXT NOT NULL,
                        publication_date TEXT NOT NULL,
                        parent_id TEXT
                      )''')

    # conn.commit()
    # conn.close()

def insertSamplePost():
    post_id = "post123"
    title = "Example Post Title"
    text = "This is the content of the example post."
    author = "user123"
    score = 10
    state = "NORMAL"  # Assuming 'NORMAL' is a valid state in your schema
    publication_date = "2023-01-01"
    subreddit_id = "subreddit123"

    try:
        cursor.execute('''INSERT INTO Post (id, title, text, author, score, state, publication_date, subreddit_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (post_id, title, text, author, score, state, publication_date, subreddit_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def insertPost(post_id, title, text, video_url, image_url, author, score, state, publication_date, subreddit_id):
    try:
        cursor.execute('''INSERT INTO Post (id, title, text, video_url, image_url, author, score, state, publication_date, subreddit_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (post_id, title, text, video_url, image_url, author, score, state, publication_date, subreddit_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def checkPostExists(post_id):
    try:
        cursor.execute('''SELECT * FROM Post WHERE id = ?''', 
                    (post_id,))
        post = cursor.fetchone()
        if post:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def getPostScore(post_id):
    try:
        cursor.execute('''SELECT score FROM Post WHERE id = ?''', 
                    (post_id,))
        score = cursor.fetchone()
        return score[0]
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def updatePostScore(post_id, score):
    try:
        cursor.execute('''UPDATE Post SET score = ?
                        WHERE id = ?''', 
                    (score, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def retrievePost(post_id):
    try:
        cursor.execute('''SELECT * FROM Post WHERE id = ?''', 
                    (post_id,))
        post = cursor.fetchone()
        return post
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def insertSampleComment():
    comment_id = "comment667"
    content = "This is the content of the example comment."
    author = "user123"
    score = 8
    status = "NORMAL"  # Assuming 'NORMAL' is a valid status in your schema
    publication_date = "2023-01-01"
    parent_id = "comment567"

    try:
        cursor.execute('''INSERT INTO Comment (id, content, author, score, status, publication_date, parent_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (comment_id, content, author, score, status, publication_date, parent_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def insertComment(comment_id, content, author, score, status, publication_date, parent_id):
    try:
        cursor.execute('''INSERT INTO Comment (id, content, author, score, status, publication_date, parent_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (comment_id, content, author, score, status, publication_date, parent_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def checkCommentExists(comment_id):
    try:
        cursor.execute('''SELECT * FROM Comment WHERE id = ?''', 
                    (comment_id,))
        comment = cursor.fetchone()
        if comment:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def retrieveComment(comment_id):
    try:
        cursor.execute('''SELECT * FROM Comment WHERE id = ?''', 
                    (comment_id,))
        comment = cursor.fetchone()
        return comment
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def getCommentScore(comment_id):
    try:
        cursor.execute('''SELECT score FROM Comment WHERE id = ?''', 
                    (comment_id,))
        score = cursor.fetchone()
        print(score[0])
        return score[0]
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def updateCommentScore(comment_id, score):
    try:
        cursor.execute('''UPDATE Comment SET score = ?
                        WHERE id = ?''', 
                    (score, comment_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# TODO: Retrieve top n comments
def retrieveTopComments(post_id, number_of_comments):
    try:
        cursor.execute('''SELECT * FROM Comment WHERE parent_id = ? ORDER BY score DESC LIMIT ?''', 
                    (post_id, number_of_comments))
        comments = cursor.fetchall()
        return comments
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        
def checkIfCommentHasReplies(comment_id):
    try:
        cursor.execute('''SELECT * FROM Comment WHERE parent_id = ?''', 
                    (comment_id,))
        comment = cursor.fetchone()
        if comment:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def retrieveTopSubComments(comment_id, number_of_comments):
    try:
        cursor.execute('''SELECT * FROM Comment WHERE parent_id = ? ORDER BY score DESC LIMIT ?''', 
                    (comment_id, number_of_comments))
        comments = cursor.fetchall()
        return comments
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def show_all_posts():
    # Connect to the SQLite database
    conn = sqlite3.connect('reddit.db')
    cursor = conn.cursor()

    try:
        # Execute a query to retrieve all posts
        cursor.execute('SELECT * FROM Post')
        
        # Fetch all rows from the query result
        posts = cursor.fetchall()
        
        # Check if posts are found
        if posts:
            print("All Posts:")
            for post in posts:
                print(post)  # Each post is a tuple representing a row from the Post table
        else:
            print("No posts found.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def show_all_comments():
    # Connect to the SQLite database
    conn = sqlite3.connect('reddit.db')
    cursor = conn.cursor()

    try:
        # Execute a query to retrieve all comments
        cursor.execute('SELECT * FROM Comment')
        
        # Fetch all rows from the query result
        comments = cursor.fetchall()
        
        # Check if comments are found
        if comments:
            print("All Comments:")
            for comment in comments:
                print(comment)  # Each comment is a tuple representing a row from the Comment table
        else:
            print("No comments found.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

# initialize_database()
# insertSamplePost()
show_all_posts()
# insertSampleComment()
show_all_comments()

# conn.commit()
# conn.close()
