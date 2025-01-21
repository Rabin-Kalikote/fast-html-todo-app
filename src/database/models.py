class TodoItem:
    def __init__(self, title, body, creation_time, due_date=None, is_completed=False, tags=None):
        self.title = title
        self.body = body
        self.creation_time = creation_time
        self.due_date = due_date
        self.is_completed = is_completed
        self.tags = tags if tags is not None else []

    def toggle_completion(self):
        self.is_completed = not self.is_completed

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)