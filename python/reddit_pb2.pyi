from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePostRequest(_message.Message):
    __slots__ = ["post"]
    POST_FIELD_NUMBER: _ClassVar[int]
    post: Post
    def __init__(self, post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class CreatePostResponse(_message.Message):
    __slots__ = ["post"]
    POST_FIELD_NUMBER: _ClassVar[int]
    post: Post
    def __init__(self, post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class VoteRequest(_message.Message):
    __slots__ = ["post_id"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    def __init__(self, post_id: _Optional[str] = ...) -> None: ...

class VoteResponse(_message.Message):
    __slots__ = ["post"]
    POST_FIELD_NUMBER: _ClassVar[int]
    post: Post
    def __init__(self, post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class RetrievePostRequest(_message.Message):
    __slots__ = ["post_id"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    def __init__(self, post_id: _Optional[str] = ...) -> None: ...

class RetrievePostResponse(_message.Message):
    __slots__ = ["post"]
    POST_FIELD_NUMBER: _ClassVar[int]
    post: Post
    def __init__(self, post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class CreateCommentRequest(_message.Message):
    __slots__ = ["comment"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class CreateCommentResponse(_message.Message):
    __slots__ = ["comment"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class VoteCommentRequest(_message.Message):
    __slots__ = ["comment_id"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    def __init__(self, comment_id: _Optional[str] = ...) -> None: ...

class VoteCommentResponse(_message.Message):
    __slots__ = ["comment"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ...) -> None: ...

class GetTopCommentsRequest(_message.Message):
    __slots__ = ["post_id", "number_of_comments"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_COMMENTS_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    number_of_comments: int
    def __init__(self, post_id: _Optional[str] = ..., number_of_comments: _Optional[int] = ...) -> None: ...

class GetTopCommentsResponse(_message.Message):
    __slots__ = ["comments"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[CommentWithReplies]
    def __init__(self, comments: _Optional[_Iterable[_Union[CommentWithReplies, _Mapping]]] = ...) -> None: ...

class CommentWithReplies(_message.Message):
    __slots__ = ["comment", "has_replies"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    HAS_REPLIES_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    has_replies: bool
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ..., has_replies: bool = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["user_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["id", "title", "text", "video_url", "image_url", "author", "score", "state", "publication_date", "subreddit"]
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        NORMAL: _ClassVar[Post.State]
        LOCKED: _ClassVar[Post.State]
        HIDDEN: _ClassVar[Post.State]
    NORMAL: Post.State
    LOCKED: Post.State
    HIDDEN: Post.State
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    SUBREDDIT_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    text: str
    video_url: str
    image_url: str
    author: User
    score: int
    state: Post.State
    publication_date: str
    subreddit: Subreddit
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., text: _Optional[str] = ..., video_url: _Optional[str] = ..., image_url: _Optional[str] = ..., author: _Optional[_Union[User, _Mapping]] = ..., score: _Optional[int] = ..., state: _Optional[_Union[Post.State, str]] = ..., publication_date: _Optional[str] = ..., subreddit: _Optional[_Union[Subreddit, _Mapping]] = ...) -> None: ...

class Subreddit(_message.Message):
    __slots__ = ["id", "name", "visibility", "tags"]
    class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        PUBLIC: _ClassVar[Subreddit.Visibility]
        PRIVATE: _ClassVar[Subreddit.Visibility]
        HIDDEN: _ClassVar[Subreddit.Visibility]
    PUBLIC: Subreddit.Visibility
    PRIVATE: Subreddit.Visibility
    HIDDEN: Subreddit.Visibility
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    visibility: Subreddit.Visibility
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., visibility: _Optional[_Union[Subreddit.Visibility, str]] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["id", "content", "author", "score", "status", "publication_date", "parent_id"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        NORMAL: _ClassVar[Comment.Status]
        HIDDEN: _ClassVar[Comment.Status]
    NORMAL: Comment.Status
    HIDDEN: Comment.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    content: str
    author: User
    score: int
    status: Comment.Status
    publication_date: str
    parent_id: str
    def __init__(self, id: _Optional[str] = ..., content: _Optional[str] = ..., author: _Optional[_Union[User, _Mapping]] = ..., score: _Optional[int] = ..., status: _Optional[_Union[Comment.Status, str]] = ..., publication_date: _Optional[str] = ..., parent_id: _Optional[str] = ...) -> None: ...
