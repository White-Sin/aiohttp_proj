# models.py

import uuid
from datetime import datetime

class Ad:
    def __init__(self, title, description, owner):
        self.id = str(uuid.uuid4())  # уникальный идентификатор
        self.title = title
        self.description = description
        self.created_at = datetime.utcnow()
        self.owner = owner

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'owner': self.owner
        }

# Для хранения объявлений в памяти
ads_db = {}
