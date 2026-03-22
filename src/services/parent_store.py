class ParentStore:

    def __init__(self):
        self.store = {}

    def add(self, parents):
        for p in parents:
            self.store[p["parent_id"]] = p["text"]

    def get(self, parent_ids):
        return [self.store[pid] for pid in parent_ids if pid in self.store]