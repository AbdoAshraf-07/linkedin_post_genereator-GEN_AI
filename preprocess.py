import json

import re

def process_posts(raw_file_path, processed_file_path):
    if processed_file_path is None:
        raise ValueError("processed_file_path must be provided")

    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)

    enriched_posts = []

    for post in posts:
        if 'text' not in post:
            continue

        metadata = extract_metadata(post['text'])
        post_with_metadata = {**post, **metadata}
        enriched_posts.append(post_with_metadata)


    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post.get('tags', [])
        post['tags'] = list({unified_tags.get(tag, tag) for tag in current_tags})

    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(enriched_posts, outfile, indent=4, ensure_ascii=False)


# --- Helper functions ---
def extract_metadata(text):
    """
    Extracts line count, language, and tags from a post's text.
    Language is detected as 'Hinglish' if both Hindi and English words are present, else 'English'.
    Tags are extracted using simple keyword heuristics.
    """
    # Line count
    line_count = text.count('\n') + 1

    # Simple language detection (very basic)
    hindi_pattern = r'[\u0900-\u097F]'
    if re.search(hindi_pattern, text):
        language = 'Hinglish'
    else:
        language = 'English'

    # Simple tag extraction (could be improved)
    tags = []
    tag_keywords = {
        'Job Search': ['job', 'interview', 'application', 'jobseekers', 'rejection'],
        'Mental Health': ['mental health', 'anxiety', 'self-doubt', 'breathe'],
        'Motivation': ['motivation', 'trust', 'growth', 'values', 'happiness', 'dream'],
        'Scams': ['scam', 'scams', 'fake', 'selected for a role'],
        'Productivity': ['productivity', 'time', 'save', 'saves'],
        'Leadership': ['manager', 'leadership'],
        'Self Improvement': ['improve', 'improving', 'skills', 'talent'],
        'Career Advice': ['career', 'company', 'brand', 'freshers'],
        'Online Dating': ['dating', 'ghosted'],
        'Influencer': ['influencer'],
        'Organic Growth': ['organic growth'],
        'Sapne': ['sapne'],
        'Time Management': ['time management'],
    }
    lowered = text.lower()
    for tag, keywords in tag_keywords.items():
        for kw in keywords:
            if kw in lowered:
                tags.append(tag)
                break
    # Fallback: if no tags found, use first 2 words as a tag
    if not tags:
        tags = ["Other"]

    return {
        'line_count': line_count,
        'language': language,
        'tags': tags
    }

def get_unified_tags(posts):
    """
    Unifies similar tags to a canonical form. For now, returns a mapping of tag to itself (no-op),
    but can be extended for more advanced unification.
    """
    # Example: unify 'Job Search', 'job search', 'Job search' to 'Job Search'
    tag_map = {}
    all_tags = set()
    for post in posts:
        for tag in post.get('tags', []):
            all_tags.add(tag)
    for tag in all_tags:
        tag_map[tag] = tag  # No-op, but could map variants to canonical
    return tag_map
