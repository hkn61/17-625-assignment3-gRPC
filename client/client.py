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

    def runCreatePost(self):
        post = reddit_pb2.Post(
            id="post233",
            title="reddit gRPC post 1",
            text="This is a reddit gRPC post",
            score=3,
            video_url="https://www.youtube.com/watch?v=123456",
            author="userAlex",
            state=reddit_pb2.Post.NORMAL,
            publication_date="2021-01-01",
            subreddit="subreddit234"
        )
        response = self.stub.CreatePost(reddit_pb2.CreatePostRequest(post=post))
        print("Post created:", response.post)
        return response.post

    def runUpvotePost(self):
        response = self.stub.UpvotePost(reddit_pb2.VoteRequest(post_id="post233"))
        print("Post upvoted:", response)
        return response.post

    def runDownvotePost(self):
        response = self.stub.DownvotePost(reddit_pb2.VoteRequest(post_id="post233"))
        print("Post downvoted:", response)
        return response.post

    def runRetrievePostContent(self, post_id):
        response = self.stub.RetrievePostContent(reddit_pb2.RetrievePostRequest(post_id=post_id))
        print("Post retrieved:", response.post)
        return response.post

    def runCreateComment(self):
        comment = reddit_pb2.Comment(
            id="comment567",
            content="This is a newly created comment",
            author="userChris",
            score=5,
            status=reddit_pb2.Comment.NORMAL,
            publication_date="2023-01-01",
            parent_id="post123"
        )
        response = self.stub.CreateComment(reddit_pb2.CreateCommentRequest(comment=comment))
        print("Comment created:", response.comment)
        return response.comment

    def runUpvoteComment(self):
        response = self.stub.UpvoteComment(reddit_pb2.VoteCommentRequest(comment_id="comment233"))
        print("Comment upvoted:", response)
        return response.comment

    def runDownvoteComment(self):
        response = self.stub.DownvoteComment(reddit_pb2.VoteCommentRequest(comment_id="comment233"))
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
            yield reddit_pb2.MonitorUpdatesRequest(comment_id="comment123")
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

def most_upvoted(api_client, post_id):
    # Retrieve the post
    post = api_client.runRetrievePostContent(post_id)
    if not post:
        return "Post not found", None

    # Retrieve the most upvoted comments under the post
    top_comments = api_client.runGetTopComments(post_id, 1)
    if not top_comments:
        return post, None

    # Expand the most upvoted comment (assuming top_comments is a list)
    # most_upvoted_comment = top_comments[0]

    # Retrieve the most upvoted reply under the most upvoted comment
    print("top_comments:", top_comments[0].comment.id)
    most_upvoted_reply = api_client.runExpandCommentBranch(top_comments[0].comment.id, 1)

    # return post, most_upvoted_reply
    return most_upvoted_reply

if __name__ == '__main__':
    client = RedditClient("localhost", 50051)
    # top_reply = most_upvoted(client, "post234")
    # print("----------- Top Reply:", top_reply if top_reply else "No replies found")

    client.runMonitorUpdates()
    
    # try:
    #     client.runExpandCommentBranch("comment456", 1)  
    # finally:
    #     client.close_channel()
