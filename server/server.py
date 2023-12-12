from concurrent import futures
import sys
import os
import time
import threading

# Add the 'generated' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated')))

import grpc
import reddit_pb2
import reddit_pb2_grpc
import sqlite

# posts = {
#     "post123": {
#         "id": "post123",
#         "title": "upvote post", 
#         "text": "Merry Christmas", 
#         "score": 1,
#         "video_url": "https://www.youtube.com/watch?v=123456",
#         "image_url": "",
#         "author": "userAlex",
#         "state": reddit_pb2.Post.NORMAL,
#         "publication_date": "2021-01-01",
#         "subreddit": "subreddit123"
#     },  # Example post
#     "post234": {
#         "id": "post234",
#         "title": "downvote post", 
#         "text": "Hi", 
#         "score": 5,
#         "video_url": "",
#         "image_url": "https://www.google.com/image.png",
#         "author": "userBob",
#         "state": reddit_pb2.Post.NORMAL,
#         "publication_date": "2021-01-01",
#         "subreddit": "subreddit123"
#     },  # Example post
# }

# comments = {
#     "comment123": {
#         "id": "comment123",
#         "content": "This is a comment",
#         "author": "userAlex",
#         "score": 2,
#         "status": reddit_pb2.Comment.NORMAL,
#         "publication_date": "2021-01-01",
#         "parent_id": "comment456"
#     },
#     "comment456": {
#         "id": "comment456",
#         "content": "This is a comment",
#         "author": "userBob",
#         "score": 3,
#         "status": reddit_pb2.Comment.NORMAL,
#         "publication_date": "2021-01-01",
#         "parent_id": "post123"
#     }
# }

post_state_map = {
    0: "NORMAL",    
    1: "LOCKED",
    2: "HIDDEN"
}

comment_status_map = {
    0: "NORMAL",    
    1: "HIDDEN"
}

class RedditService(reddit_pb2_grpc.RedditServiceServicer):
    def get_state(self, state_int):
        if state_int == 0:
            state = reddit_pb2.Post.NORMAL
        elif state_int == 1:
            state = reddit_pb2.Post.LOCKED
        elif state_int == 2:
            state = reddit_pb2.Post.HIDDEN
        return state
    
    def get_status(self, status_int):
        if status_int == 0:
            status = reddit_pb2.Comment.NORMAL
        elif status_int == 1:
            status = reddit_pb2.Comment.HIDDEN
        return status

    def CreatePost(self, request, context):
        post = request.post
        # print("post:", post.state)
        state_str = post_state_map[post.state]
        # print("state_str:", state_str)
        state = self.get_state(post.state)
        sqlite.insertPost(post.id, post.title, post.text, post.video_url, post.image_url, post.author, post.score, post.state, post.publication_date, post.subreddit)
        return reddit_pb2.CreatePostResponse(post=post)
    
    def UpvotePost(self, request, context):
        # return super().UpvotePost(request, context)
        post_id = request.post_id
        if not sqlite.checkPostExists(post_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        score = sqlite.getPostScore(post_id) + 1
        sqlite.updatePostScore(post_id, score)
        post = sqlite.retrievePost(post_id)
        # print("post:", post)
        if post[7] == '0' or post[7] == '1' or post[7] == '2':
            state = self.get_state(int(post[7]))
        else:
            state = post[7]
        if post[3] and len(post[3]) > 0:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                video_url=post[3],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
        elif post[4] and len(post[4]) > 0:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                image_url=post[4],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
        else:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
    
    def DownvotePost(self, request, context):
        post_id = request.post_id
        if not sqlite.checkPostExists(post_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        score = sqlite.getPostScore(post_id) - 1
        sqlite.updatePostScore(post_id, score)
        post = sqlite.retrievePost(post_id)
        # print("post:", post)
        if post[7] == '0' or post[7] == '1' or post[7] == '2':
            state = self.get_state(int(post[7]))
        else:
            state = post[7]
        if post[3] and len(post[3]) > 0:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                video_url=post[3],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
        elif post[4] and len(post[4]) > 0:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                image_url=post[4],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
        else:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
    
    def RetrievePostContent(self, request, context):
        post_id = request.post_id
        if not sqlite.checkPostExists(post_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        post = sqlite.retrievePost(post_id)
        # print("post:", post)
        if post[7] == '0' or post[7] == '1' or post[7] == '2':
            state = self.get_state(int(post[7]))
        else:
            state = post[7]
        if post[3] and len(post[3]) > 0:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                video_url=post[3],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
        elif post[4] and len(post[4]) > 0:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                image_url=post[4],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
        else:
            return reddit_pb2.RetrievePostResponse(post=reddit_pb2.Post(
                id=post[0],
                title=post[1],
                text=post[2],
                author=post[5],
                score=post[6],
                state=state,
                publication_date=post[8],
                subreddit=post[9]
            ))
    
    def CreateComment(self, request, context):
        comment = request.comment
        status = self.get_status(comment.status)
        sqlite.insertComment(comment.id, comment.content, comment.author, comment.score, comment.status, comment.publication_date, comment.parent_id)
        return reddit_pb2.CreateCommentResponse(comment=comment)

    def UpvoteComment(self, request, context):
        comment_id = request.comment_id
        if not sqlite.checkCommentExists(comment_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Comment not found")
        score = sqlite.getCommentScore(comment_id) + 1
        sqlite.updateCommentScore(comment_id, score)
        comment = sqlite.retrieveComment(comment_id)
        return reddit_pb2.VoteCommentResponse(comment=reddit_pb2.Comment(
            id=comment_id,
            content=comment[1],
            author=comment[2],
            score=comment[3],
            parent_id=comment[4],
            publication_date=comment[5]
        ))
    
    def DownvoteComment(self, request, context):
        comment_id = request.comment_id
        if not sqlite.checkCommentExists(comment_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Comment not found")
        score = sqlite.getCommentScore(comment_id) - 1
        sqlite.updateCommentScore(comment_id, score)
        comment = sqlite.retrieveComment(comment_id)
        return reddit_pb2.VoteCommentResponse(comment=reddit_pb2.Comment(
            id=comment_id,
            content=comment[1],
            author=comment[2],
            score=comment[3],
            parent_id=comment[4],
            publication_date=comment[5]
        ))
    
    def GetTopComments(self, request, context):
        post_id = request.post_id
        if not sqlite.checkPostExists(post_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        number_of_comments = request.number_of_comments
        if number_of_comments <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Number of comments must be greater than 0")

        top_comments = sqlite.retrieveTopComments(post_id, number_of_comments)
        response_comments = []
        for comment in top_comments:
            comment_id = comment[0]
            has_replies = sqlite.checkIfCommentHasReplies(comment_id)
            # print("comment_id:", comment_id)
            # print("has_replies:", has_replies)
            response_comments.append(reddit_pb2.CommentWithReplies(
                comment=reddit_pb2.Comment(
                    id=comment_id,
                    content=comment[1],
                    author=comment[2],
                    score=comment[3],
                    parent_id=comment[4],
                    publication_date=comment[5]
                ),
                has_replies=str(has_replies)
            ))

        return reddit_pb2.GetTopCommentsResponse(comments=response_comments)
    
    def ExpandCommentBranch(self, request, context):
        comment_id = request.comment_id
        num_comments = request.number_of_comments

        # Retrieve the top N sub-comments of the given comment
        # sub_comments = [c for c in comments.values() if c['parent_id'] == comment_id]
        # top_sub_comments = sorted(sub_comments, key=lambda x: x['score'], reverse=True)[:num_comments]

        top_sub_comments = sqlite.retrieveTopSubComments(comment_id, num_comments)

        # print("sub_comments:", sub_comments)
        # print("top_sub_comments:", top_sub_comments)

        # For each sub-comment, get their top N sub-comments
        comment_branches = []
        for sub_comment in top_sub_comments:
            sub_comment_id = sub_comment[0]
            # sub_sub_comments = [c for c in comments.values() if c['parent_id'] == sub_comment_id]
            # top_sub_sub_comments = sorted(sub_sub_comments, key=lambda x: x['score'], reverse=True)[:num_comments]
            
            top_sub_sub_comments = sqlite.retrieveTopSubComments(sub_comment_id, num_comments)

            # print("sub_comment:", sub_comment)
            # print("sub_sub_comments:", sub_sub_comments)
            # print("top_sub_sub_comments:", top_sub_sub_comments)

            comment_branches.append(reddit_pb2.CommentBranch(
                comment=_create_comment_response(sub_comment),
                sub_comments=[_create_comment_response(c) for c in top_sub_sub_comments]
            ))

        return reddit_pb2.ExpandCommentBranchResponse(comments=comment_branches)
    
    def MonitorUpdates(self, request_iterator, context):
        monitored_entities = {}

        for request in request_iterator:
            if request.HasField("post_id"):
                monitored_entities[request.post_id] = "post"
            elif request.HasField("comment_id"):
                monitored_entities[request.comment_id] = "comment"

        while True:
            for entity_id, entity_type in monitored_entities.items():
                if entity_type == "post" and sqlite.checkPostExists(entity_id):
                    post = sqlite.retrievePost(entity_id)
                    yield reddit_pb2.MonitorUpdatesResponse(
                        post=_create_post_response(post)
                    )
                elif entity_type == "comment" and sqlite.checkCommentExists(entity_id):
                    comment = sqlite.retrieveComment(entity_id)
                    yield reddit_pb2.MonitorUpdatesResponse(
                        comment=_create_comment_response_m(comment)
                    )
            time.sleep(1)  # Simulate delay

def _create_comment_response(comment):
    return reddit_pb2.Comment(
        id=comment[0],
        content=comment[1],
        author=comment[2],
        score=comment[3],
        parent_id=comment[6],
        publication_date=comment[5]
    )

def _create_post_response(post_data):
    # print("post_data:", post_data)
    if post_data[7] == '0':
        state = reddit_pb2.Post.NORMAL
    elif post_data[7] == '1':
        state = reddit_pb2.Post.LOCKED
    elif post_data[7] == '2':
        state = reddit_pb2.Post.HIDDEN
    return reddit_pb2.Post(
        id=post_data[0],
        title=post_data[1],
        text=post_data[2],
        video_url=post_data[3],
        image_url=post_data[4],
        author=post_data[5],
        score=post_data[6],
        state=state,
        publication_date=post_data[8],
        subreddit=post_data[9]
    )

def _create_comment_response_m(comment_data):
    if comment_data[4] == '0':
        status = reddit_pb2.Comment.NORMAL
    elif comment_data[4] == '1':
        status = reddit_pb2.Comment.HIDDEN
    return reddit_pb2.Comment(
        id=comment_data[0],
        content=comment_data[1],
        author=comment_data[2], 
        score=comment_data[3],
        parent_id=comment_data[6],
        publication_date=comment_data[5],
        status=status
    )
    
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