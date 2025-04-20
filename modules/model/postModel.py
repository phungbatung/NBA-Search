class Post:
    def __init__(self, postId, userId, title, content, createdAt, comments=None):
        self.postId = postId
        self.userId = userId
        self.title = title
        self.content = content
        self.createdAt = createdAt
        self.comments = comments if comments is not None else []

    def __repr__(self):
        return (
            f"Post(postId={self.postId}, userId={self.userId}, "
            f"title='{self.title}', createdAt='{self.createdAt}')"
        )