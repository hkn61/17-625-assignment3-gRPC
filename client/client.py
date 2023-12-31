import time
import grpc
import sys
import os

# Add the 'generated' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated')))

import reddit_pb2
import reddit_pb2_grpc

class RedditClient:

    def __init__(self, host, port):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = reddit_pb2_grpc.RedditServiceStub(self.channel)

    def close_channel(self):
        if self.channel:
            self.channel.close()

    def runCreatePost(self, id, title, text, score, video_url, image_url, author, state, publication_date, subreddit):
        if state == "NORMAL":
            state = reddit_pb2.Post.NORMAL
        elif state == "LOCKED":
            state = reddit_pb2.Post.LOCKED
        else:
            state = reddit_pb2.Post.HIDDEN

        if video_url and len(video_url) > 0:
            post = reddit_pb2.Post(
                id=id,
                title=title,
                text=text,
                score=score,
                video_url=video_url,
                author=author,
                state=state,
                publication_date=publication_date,
                subreddit=subreddit
            )
        elif image_url and len(image_url) > 0:
            post = reddit_pb2.Post(
                id=id,
                title=title,
                text=text,
                score=score,
                image_url=image_url,
                author=author,
                state=state,
                publication_date=publication_date,
                subreddit=subreddit
            )

        response = self.stub.CreatePost(reddit_pb2.CreatePostRequest(post=post))
        print("Post created:", response.post)
        return response.post

    def runUpvotePost(self, post_id):
        response = self.stub.UpvotePost(reddit_pb2.VoteRequest(post_id=post_id))
        print("Post upvoted:", response)
        return response.post

    def runDownvotePost(self, post_id):
        response = self.stub.DownvotePost(reddit_pb2.VoteRequest(post_id=post_id))
        print("Post downvoted:", response)
        return response.post

    def runRetrievePostContent(self, post_id):
        response = self.stub.RetrievePostContent(reddit_pb2.RetrievePostRequest(post_id=post_id))
        print("Post retrieved:", response.post)
        return response.post

    def runCreateComment(self, id, content, author, score, status, publication_date, parent_id):
        if status == "NORMAL":
            status = reddit_pb2.Comment.NORMAL
        else:
            status = reddit_pb2.Comment.HIDDEN

        comment = reddit_pb2.Comment(
            id=id,
            content=content,
            author=author,
            score=score,
            status=status,
            publication_date=publication_date,
            parent_id=parent_id
        )

        response = self.stub.CreateComment(reddit_pb2.CreateCommentRequest(comment=comment))
        print("Comment created:", response.comment)
        return response.comment

    def runUpvoteComment(self, comment_id):
        response = self.stub.UpvoteComment(reddit_pb2.VoteCommentRequest(comment_id=comment_id))
        print("Comment upvoted:", response)
        return response.comment

    def runDownvoteComment(self, comment_id):
        response = self.stub.DownvoteComment(reddit_pb2.VoteCommentRequest(comment_id=comment_id))
        print("Comment downvoted:", response)
        return response.comment

    def runGetTopComments(self, post_id, number_of_comments):
        response = self.stub.GetTopComments(reddit_pb2.GetTopCommentsRequest(post_id=post_id, number_of_comments=number_of_comments))
        print("Top comments retrieved:", response.comments)
        return response.comments

    def runExpandCommentBranch(self, comment_id, number_of_comments):
        # Example Comment ID and number of comments to retrieve
        # comment_id = "comment456"
        # number_of_comments = 1

        # Expand comment branch
        response = self.stub.ExpandCommentBranch(reddit_pb2.ExpandCommentBranchRequest(
            comment_id=comment_id,
            number_of_comments=number_of_comments
        ))

        # print("response: ", response)
        # print("response.comments:", response.comments)

        for branch in response.comments:
            print("Comment:\n", branch.comment)
            print("Sub Comments:")
            for sub_comment in branch.sub_comments:
                print(sub_comment)
                print()
        return response.comments

    def runMonitorUpdates(self):
        def request_generator():
            # Initial request with a post ID
            yield reddit_pb2.MonitorUpdatesRequest(post_id="post233")

            # Sleep for a bit before sending more requests
            time.sleep(2)

            # Additional requests with comment IDs
            yield reddit_pb2.MonitorUpdatesRequest(comment_id="comment111")
            time.sleep(1)
            yield reddit_pb2.MonitorUpdatesRequest(comment_id="comment456")

        try:
            for update in self.stub.MonitorUpdates(request_generator()):
                if update.HasField("post"):
                    print("Updated Post:", update.post)
                elif update.HasField("comment"):
                    print("Updated Comment:", update.comment)
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

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

if __name__ == '__main__':
    client = RedditClient("localhost", 50051)

    # Create a post
    print("\n---------------- Creating post... --------------\n")
    client.runCreatePost("post333", "reddit gRPC post 1", "This is a reddit gRPC post", 3, "https://www.youtube.com/watch?v=123456", "", "userAlex", "NORMAL", "2021-01-01", "subreddit234")

    # Upvote the post
    print("\n---------------- Upvote a post --------------\n")
    client.runUpvotePost("post233")

    # Downvote the post
    print("\n---------------- Downvote a post --------------\n")
    client.runDownvotePost("post233")

    # Retrieve the post
    print("\n---------------- Retrieve a post --------------\n")
    client.runRetrievePostContent("post233")

    # Create a comment
    print("\n---------------- Creating comment... --------------\n")
    client.runCreateComment("comment333", "This is a test comment", "userAlex", 0, "NORMAL", "2021-01-01", "post233")

    # Upvote the comment
    print("\n---------------- Upvote a comment --------------\n")
    client.runUpvoteComment("comment233")

    # Downvote the comment
    print("\n---------------- Downvote a comment --------------\n")
    client.runDownvoteComment("comment456")

    # Retrieve the top comments
    print("\n---------------- Retrieve top comments --------------\n")
    client.runGetTopComments("post123", 1)

    # Expand the comment branch
    print("\n---------------- Expand comment branch --------------\n")
    client.runExpandCommentBranch("comment456", 1)

    # the high level function
    print("\n---------------- Top Reply: --------------\n")
    top_reply = most_upvoted(client, "post123", 2)

    # Monitor updates
    print("\n---------------- Monitor updates --------------\n")
    client.runMonitorUpdates()
    
    # try:
    #     client.runExpandCommentBranch("comment456", 1)  
    # finally:
    #     client.close_channel()
