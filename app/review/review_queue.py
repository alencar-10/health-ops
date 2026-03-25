import json
import os


class ReviewQueue:

    def __init__(self):

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../")
        )

        self.path = os.path.join(base_dir, "data", "review_queue.json")

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def load(self):

        with open(self.path) as f:
            return json.load(f)

    def save(self, data):

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, item):

        data = self.load()

        item["id"] = len(data) + 1

        data.append(item)

        self.save(data)

    def list_pending(self):

        return [x for x in self.load() if x["status"] == "PENDING"]

    def approve(self, item_id):

        data = self.load()

        for item in data:

            if item["id"] == item_id:

                item["status"] = "APPROVED"

        self.save(data)
