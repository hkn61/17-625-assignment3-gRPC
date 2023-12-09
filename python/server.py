from concurrent import futures

import grpc
import reddit_pb2
import reddit_pb2_grpc

posts = {
    "123": {
        "title": "upvote post", 
        "text": "Merry Christmas", 
        "score": 1,
        "video_url": "https://www.youtube.com/watch?v=123456",
        "image_url": "",
        "author": "userAlex",
        "state": reddit_pb2.Post.NORMAL,
        "publication_date": "2021-01-01",
        "subreddit": reddit_pb2.Subreddit(
            name="gRPC Subreddit",
            visibility=reddit_pb2.Subreddit.PUBLIC,
            tags=["grpc", "test"]
        )
    },  # Example post
    "234": {
        "title": "downvote post", 
        "text": "Hi", 
        "score": 5,
        "video_url": "",
        "image_url": "https://www.google.com/image.png",
        "author": "userBob",
        "state": reddit_pb2.Post.NORMAL,
        "publication_date": "2021-01-01",
        "subreddit": reddit_pb2.Subreddit(
            name="gRPC Subreddit2",
            visibility=reddit_pb2.Subreddit.PUBLIC,
            tags=["grpc", "test"]
        )
    },  # Example post
}

comments = {
    "comment123": {
        "content": "This is a comment",
        "author": "userAlex",
        "score": 3,
        "status": reddit_pb2.Comment.NORMAL,
        "publication_date": "2021-01-01",
        "parent_id": "comment456"
    },
    "comment456": {
        "content": "This is a comment",
        "author": "userBob",
        "score": 3,
        "status": reddit_pb2.Comment.NORMAL,
        "publication_date": "2021-01-01",
        "parent_id": "123"
    }
}

class RedditService(reddit_pb2_grpc.RedditServiceServicer):
    def CreatePost(self, request, context):
        post = request.post
        posts[post.id] = {
            "title": post.title if post.title else "",
            "text": post.text if post.text else "",
            "score": post.score if post.score else 0,
            "video_url": post.video_url if post.video_url else "",
            "image_url": post.image_url if post.image_url else "",
            "author": post.author if post.author else "",
            "state": post.state if post.state else reddit_pb2.Post.NORMAL,
            "publication_date": post.publication_date if post.publication_date else "",
            "subreddit": post.subreddit if post.subreddit else None
        }
        return reddit_pb2.CreatePostResponse(post=post)
    
    def UpvotePost(self, request, context):
        # return super().UpvotePost(request, context)
        post_id = request.post_id
        if post_id not in posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        posts[post_id]["score"] += 1
        return reddit_pb2.VoteResponse(post=reddit_pb2.Post(
            id=post_id,
            title=posts[post_id]["title"],
            score=posts[post_id]["score"]
        ))
    
    def DownvotePost(self, request, context):
        post_id = request.post_id
        if post_id not in posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        posts[post_id]["score"] -= 1
        return reddit_pb2.VoteResponse(post=reddit_pb2.Post(
            id=post_id,
            title=posts[post_id]["title"],
            score=posts[post_id]["score"]
        ))
    
    def RetrievePostContent(self, request, context):
        post_id = request.post_id
        if post_id not in posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
            id=post_id,
            title=posts[post_id]["title"],
            text=posts[post_id]["text"],
            score=posts[post_id]["score"],
            video_url=posts[post_id]["video_url"],
            image_url=posts[post_id]["image_url"],
            author=posts[post_id]["author"],
            state=posts[post_id]["state"],
            publication_date=posts[post_id]["publication_date"],
            subreddit=posts[post_id]["subreddit"]
        ))
    
    def CreateComment(self, request, context):
        comment = request.comment
        comments[comment.id] = {
            "content": comment.content if comment.content else "",
            "author": comment.author if comment.author else "",
            "score": comment.score if comment.score else 0,
            "status": comment.status if comment.status else reddit_pb2.Comment.NORMAL,
            "publication_date": comment.publication_date if comment.publication_date else "",
            "parent_id": comment.parent_id if comment.parent_id else ""
        }
        return reddit_pb2.CreateCommentResponse(comment=comment)

    def UpvoteComment(self, request, context):
        comment_id = request.comment_id
        if comment_id not in comments:
            context.abort(grpc.StatusCode.NOT_FOUND, "Comment not found")
        comments[comment_id]["score"] += 1
        return reddit_pb2.VoteCommentResponse(comment=reddit_pb2.Comment(
            id=comment_id,
            content=comments[comment_id]["content"],
            score=comments[comment_id]["score"]
        ))
    
    def DownvoteComment(self, request, context):
        comment_id = request.comment_id
        if comment_id not in comments:
            context.abort(grpc.StatusCode.NOT_FOUND, "Comment not found")
        comments[comment_id]["score"] -= 1
        return reddit_pb2.VoteCommentResponse(comment=reddit_pb2.Comment(
            id=comment_id,
            content=comments[comment_id]["content"],
            score=comments[comment_id]["score"]
        ))
    
    def GetTopComments(self, request, context):
        post_id = request.post_id
        if post_id not in posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        number_of_comments = request.number_of_comments
        if number_of_comments <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Number of comments must be greater than 0")

        # Filter comments belonging to the post and sort them
        post_comments = [c for c in comments.values() if c['parent_id'] == post_id]
        top_comments = sorted(post_comments, key=lambda x: x['score'], reverse=True)[:number_of_comments]
        response_comments = []
        for comment in top_comments:
            comment_id = comment['id']
            has_replies = any(c['parent_id'] == comment_id for c in comments.values())
            response_comments.append(reddit_pb2.CommentWithReplies(
                comment=reddit_pb2.Comment(
                    id=comment_id,
                    content=comment['content'],
                    author=comment['author'],
                    score=comment['score'],
                    parent_id=comment['parent_id'],
                    publication_date=comment['publication_date']
                ),
                has_replies=has_replies
            ))

        return reddit_pb2.GetTopCommentsResponse(comments=[
            reddit_pb2.CommentWithReplies(
                comment=reddit_pb2.Comment(
                    id=comment_id,
                    content=comments[comment_id]["content"],
                    score=comments[comment_id]["score"],
                    author=comments[comment_id]["author"],
                    status=comments[comment_id]["status"],
                    publication_date=comments[comment_id]["publication_date"],
                    parent_id=comments[comment_id]["parent_id"]
                ),
                has_replies=False
            ) for comment_id in comments
        ])
    
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reddit_pb2_grpc.add_RedditServiceServicer_to_server(RedditService(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    print("Server started on port {}".format(port))
    server.wait_for_termination()

if __name__ == '__main__':
    serve()