import os
from collections import Counter
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoStore:
    """Optional MongoDB Atlas persistence with automatic in-memory fallback.
    The app remains 100% functional even if MONGODB_URI is never configured.
    """

    _in_memory_records: list[dict[str, Any]] = []

    def __init__(self) -> None:
        self.uri = os.getenv("MONGODB_URI", "")
        self.collection = None
        if self.uri:
            try:
                client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
                client.admin.command("ping")
                self.collection = client["quantcoach"]["interactions"]
            except Exception:
                self.collection = None

    @property
    def connected(self) -> bool:
        return self.collection is not None

    def save_interaction(self, section: str, query: str, response: str, weak_spot: str | None = None) -> str | None:
        if self.collection:
            document: dict[str, Any] = {
                "section": section,
                "query": query,
                "response": response,
                "weak_spot": weak_spot or section,
                "rating": None,
                "created_at": datetime.now(timezone.utc),
            }
            try:
                return str(self.collection.insert_one(document).inserted_id)
            except PyMongoError:
                pass

        # In-memory fallback if MongoDB is not configured or offline
        record_id = f"mem_{len(self._in_memory_records) + 1}"
        self._in_memory_records.append({
            "id": record_id,
            "section": section,
            "query": query,
            "response": response,
            "weak_spot": weak_spot or section,
            "rating": None,
            "created_at": datetime.now(timezone.utc),
        })
        return record_id

    def set_rating(self, interaction_id: str | None, rating: int) -> bool:
        if not interaction_id:
            return False

        if self.collection:
            try:
                from bson import ObjectId
                return bool(self.collection.update_one(
                    {"_id": ObjectId(interaction_id)}, {"$set": {"rating": rating}}
                ).modified_count)
            except (PyMongoError, ValueError):
                pass

        # In-memory fallback
        for record in self._in_memory_records:
            if record["id"] == str(interaction_id):
                record["rating"] = rating
                return True
        return False

    def progress(self) -> list[dict[str, Any]]:
        if self.collection:
            try:
                return list(self.collection.aggregate([
                    {"$group": {
                        "_id": "$weak_spot", "attempts": {"$sum": 1},
                        "downvotes": {"$sum": {"$cond": [{"$eq": ["$rating", -1]}, 1, 0]}},
                    }},
                    {"$sort": {"downvotes": -1, "attempts": -1}}, {"$limit": 10},
                ]))
            except PyMongoError:
                pass

        # In-memory aggregation fallback
        if not self._in_memory_records:
            return []

        attempts: Counter[str] = Counter()
        downvotes: Counter[str] = Counter()
        for record in self._in_memory_records:
            ws = record.get("weak_spot") or "General"
            attempts[ws] += 1
            if record.get("rating") == -1:
                downvotes[ws] += 1

        rows = [
            {"_id": topic, "attempts": count, "downvotes": downvotes[topic]}
            for topic, count in attempts.items()
        ]
        rows.sort(key=lambda r: (r["downvotes"], r["attempts"]), reverse=True)
        return rows[:10]
