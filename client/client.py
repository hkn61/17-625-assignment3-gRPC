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
            video_url="https://www.youtube.com/watch?v=123456",
            author=reddit_pb2.User(user_id="userAlex"),
            score=3,
            state=reddit_pb2.Post.NORMAL,
            publication_date="2021-01-01",
            subreddit=reddit_pb2.Subreddit(
                name="gRPC Subreddit",
                visibility=reddit_pb2.Subreddit.PUBLIC,
                tags=["grpc", "test"]
            )
        )
        response = self.stub.CreatePost(reddit_pb2.CreatePostRequest(post=post))
        print("Post created:", response.post)

    def runUpvotePost(self):
        response = self.stub.UpvotePost(reddit_pb2.VoteRequest(post_id="post123"))
        print("Post upvoted:", response)

    def runDownvotePost(self):
        response = self.stub.DownvotePost(reddit_pb2.VoteRequest(post_id="post234"))
        print("Post downvoted:", response)

    def runRetrievePostContent(self, post_id):
        response = self.stub.RetrievePostContent(reddit_pb2.RetrievePostRequest(post_id=post_id))
        print("Post retrieved:", response.post)

    def runCreateComment(self):
        comment = reddit_pb2.Comment(
            id="comment233",
            content="This is a newly created comment",
            author=reddit_pb2.User(user_id="userChris"),
            score=1,
            status=reddit_pb2.Comment.NORMAL,
            publication_date="2023-01-01",
            parent_id="comment456"
        )
        response = self.stub.CreateComment(reddit_pb2.CreateCommentRequest(comment=comment))
        print("Comment created:", response.comment)

    def runUpvoteComment(self):
        response = self.stub.UpvoteComment(reddit_pb2.VoteCommentRequest(comment_id="comment123"))
        print("Comment upvoted:", response)

    def runDownvoteComment(self):
        response = self.stub.DownvoteComment(reddit_pb2.VoteCommentRequest(comment_id="comment456"))
        print("Comment downvoted:", response)

    def runGetTopComments(self, post_id, number_of_comments):
        response = self.stub.GetTopComments(reddit_pb2.GetTopCommentsRequest(post_id=post_id, number_of_comments=number_of_comments))
        print("Top comments retrieved:", response.comments)

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
            print("Comment:", branch.comment)
            print("Sub Comments:")
            for sub_comment in branch.sub_comments:
                print("\t", sub_comment)

    def runMonitorUpdates(self):
        def request_generator():
            # Initial request with a post ID
            yield reddit_pb2.MonitorUpdatesRequest(post_id="post123")

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

if __name__ == '__main__':
    client = RedditClient("localhost", 50051)
    
    try:
        client.runExpandCommentBranch("comment456", 1)  
    finally:
        client.close_channel()