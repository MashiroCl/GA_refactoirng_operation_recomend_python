import utils.time as time

class Comment:
    def __init__(self, comment:str):
        self.commenter = comment.get("user").get("login", None)
        self.updated_at = time.format_prtime(comment.get("updated_at", None))

    def to_list(self):
        return [self.commenter, self.updated_at]