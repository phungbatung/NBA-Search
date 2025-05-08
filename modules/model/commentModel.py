class Comment:
    def __init__(self, commentId, postId, userId, content, createdAt):
        self.commentId = commentId
        self.postId = postId
        self.userId = userId
        self.content = content
        self.createdAt = createdAt

    def __repr__(self):
        return (f"Comment(commentId={self.commentId}, postId={self.postId}, "
                f"userId={self.userId}, content='{self.content}', "
                f"createdAt={self.createdAt})")
    def to_dict(self):
        return {
            "commentId": self.commentId,
            "postId": self.postId,
            "userId": self.userId,
            "content": self.content,
            "createdAt": self.createdAt
        }