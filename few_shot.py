import pandas as pd
import json
import os


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = []
        self.load_posts(file_path)

    def load_posts(self, file_path):
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Load JSON
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)

        # Normalize JSON to DataFrame
        self.df = pd.json_normalize(posts)

        # Ensure line_count exists and handle NaN
        if 'line_count' not in self.df.columns:
            raise KeyError("Column 'line_count' is missing from the data")

        self.df['line_count'] = self.df['line_count'].fillna(0)

        # Categorize post length
        self.df['length'] = self.df['line_count'].apply(self.categorize_length)

        # Collect unique tags safely
        all_tags = []
        if 'tags' in self.df.columns:
            for tags in self.df['tags'].dropna():
                if isinstance(tags, list):
                    all_tags.extend(tags)

        self.unique_tags = list(set(all_tags))

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_posts(self, length, language, tag):
        if self.df is None:
            return []

        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(
                lambda tags: isinstance(tags, list) and tag in tags
            ))
        ]

        return df_filtered.to_dict(orient="records")

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts(
        length="Medium",
        language="Hinglish",
        tag="Job Search"
    )

    print(posts)
