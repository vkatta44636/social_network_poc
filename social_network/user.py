class User:
    """Represents a single user profile in the social network."""

    def __init__(self, user_id, name, bio=""):
        if not user_id:
            raise ValueError("user_id cannot be empty.")
        if not name:
            raise ValueError("name cannot be empty.")

        self.user_id = user_id
        self.name = name
        self.bio = bio

    def __repr__(self):
        return f"User(id={self.user_id!r}, name={self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id
