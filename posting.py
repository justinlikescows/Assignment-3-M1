class Posting:
    def __init__(self, doc_id, term_freq=0, fields=None, positions=None):
        self.doc_id = doc_id
        self.term_freq = term_freq
        self.fields = fields if fields else []
        self.positions = positions if positions else []
        
    def add_occurrence(self, field, position):
        """
        Add an occurrence of the term in a specific field and position.
        """
        self.term_freq += 1
        self.fields.append(field)
        self.positions.append(position)