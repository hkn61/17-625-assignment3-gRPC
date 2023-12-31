def most_upvoted(api_client, post_id, number_of_comments=1):
    # Retrieve the post
    post = api_client.runRetrievePostContent(post_id)
    if not post:
        return None

    # Retrieve the most upvoted comments under the post
    top_comments = api_client.runGetTopComments(post_id, number_of_comments)
    if not top_comments:
        return None

    # Expand the most upvoted comment (assuming top_comments is a list)
    # most_upvoted_comment = top_comments[0]

    # Retrieve the most upvoted reply under the most upvoted comment
    # print("top_comments:", top_comments[0].comment.id)
    most_upvoted_reply = api_client.runExpandCommentBranch(top_comments[0].comment.id, number_of_comments)
    print("~~~~~~~~~~ most_upvoted_reply:\n", most_upvoted_reply)

    # return post, most_upvoted_reply
    return most_upvoted_reply