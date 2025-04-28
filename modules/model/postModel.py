class Post:
    def __init__(self, postId, userId, title, content, createdAt, comments=[]):
        self.postId = postId
        self.userId = userId
        self.title = title
        self.content = content
        self.createdAt = createdAt
        self.comments = comments

    def __repr__(self):
        return (
            f"Post(postId={self.postId}, userId={self.userId}, "
            f"title='{self.title}', createdAt='{self.createdAt}')"
        )
    def to_dict(self):
        return {
            "postId": self.postId,
            "userId": self.userId,
            "title": self.title,
            "content": self.content,
            "createdAt": self.createdAt,
            "comments": [c.to_dict() if hasattr(c, 'to_dict') else c for c in self.comments]
        }