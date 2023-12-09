import grpc
import reddit_pb2
import reddit_pb2_grpc

def runCreatePost():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        post = reddit_pb2.Post(
            id="233",
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
        response = stub.CreatePost(reddit_pb2.CreatePostRequest(post=post))
        print("Post created:", response.post)

def runUpvotePost():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        response = stub.UpvotePost(reddit_pb2.VoteRequest(post_id="123"))
        print("Post upvoted:", response)

def runDownvotePost():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        response = stub.DownvotePost(reddit_pb2.VoteRequest(post_id="234"))
        print("Post downvoted:", response)

def runRetrievePostContent():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        response = stub.RetrievePostContent(reddit_pb2.RetrievePostRequest(post_id="123"))
        print("Post retrieved:", response.post)

def runCreateComment():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        comment = reddit_pb2.Comment(
            id="comment233",
            content="This is a newly created comment",
            author=reddit_pb2.User(user_id="userChris"),
            score=1,
            status=reddit_pb2.Comment.NORMAL,
            publication_date="2023-01-01",
            parent_id="comment456"
        )
        response = stub.CreateComment(reddit_pb2.CreateCommentRequest(comment=comment))
        print("Comment created:", response.comment)

def runUpvoteComment():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        response = stub.UpvoteComment(reddit_pb2.VoteCommentRequest(comment_id="comment123"))
        print("Comment upvoted:", response)

def runDownvoteComment():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reddit_pb2_grpc.RedditServiceStub(channel)
        response = stub.DownvoteComment(reddit_pb2.VoteCommentRequest(comment_id="comment456"))
        print("Comment downvoted:", response)

if __name__ == '__main__':
    runDownvoteComment()
