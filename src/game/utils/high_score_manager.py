# src/game/utils/high_score_manager.py

import os
import json

HIGH_SCORE_FILE = "assets/high_score.json"
MAX_SCORE = 10

class HighScoreManager:
    def __init__(self):
        self.high_scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(HIGH_SCORE_FILE):
            return []
        with open(HIGH_SCORE_FILE, "r") as f:
            return json.load(f)

    def save_scores(self, scores):
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(self.high_scores, f, indent=4)

    def is_high_score(self, score):
        if len(self.high_scores) < MAX_SCORE:
            return True
        return score > self.high_scores[-1]["score"]

    def add_score(self, name, score):
        self.high_scores.append({"name": name, "score": score})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:MAX_SCORE]
        self.save_scores(self.high_scores)