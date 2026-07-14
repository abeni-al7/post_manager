"""
Category classifier for Addis Fortune articles.
Determines the category based on file path, title, and content.
"""
import re


# Category keywords mapping
CATEGORY_KEYWORDS = {
    "Business": [
        "business",
        "economy",
        "economic",
        "bank",
        "nbe",
        "financial",
        "currency",
        "inflation",
        "investment",
        "trade",
        "export",
        "import",
        "market",
        "share",
        "stock",
        "company",
        "corporate",
        "midroc",
        "cement",
        "construction",
    ],
    "Politics": [
        "government",
        "parliament",
        "election",
        "political",
        "party",
        "minister",
        "prime minister",
        "policy",
        "law",
        "court",
        "judiciary",
        "opposition",
    ],
    "Opinion": [
        "opinion",
        "viewpoint",
        "perspective",
        "commentary",
        "editor",
        "column",
    ],
    "News": [
        "news",
        "report",
        "update",
        "announcement",
    ],
    "Life Matters": [
        "life",
        "health",
        "education",
        "culture",
        "society",
        "community",
    ],
    "Sports": [
        "sport",
        "football",
        "soccer",
        "athletics",
        "olympic",
        "championship",
    ],
    "Entertainment": [
        "entertainment",
        "movie",
        "music",
        "art",
        "theater",
        "cinema",
    ],
    "Technology": [
        "technology",
        "tech",
        "software",
        "hardware",
        "internet",
        "digital",
        "computer",
    ],
    "Environment": [
        "environment",
        "climate",
        "pollution",
        "green",
        "sustainability",
        "energy",
    ],
}


def classify_category(filepath: str, title: str | None, content: str | None) -> str:
    """
    Classify an article into a category based on its filepath, title, and content.
    
    Priority:
    1. Check the filepath for category hints (e.g., "opinion.htm", "businessopportunities.htm")
    2. Check the title for keywords
    3. Check the content for keywords
    4. Default to "News" if no match found
    """
    # Combine all text for keyword matching
    combined_text = ""
    
    # Add filepath hints
    path_lower = filepath.lower()
    
    # Check filepath for direct category hints
    if "opinion" in path_lower or "viewpoint" in path_lower or "perspective" in path_lower:
        return "Opinion"
    if "business" in path_lower or "opportunities" in path_lower:
        return "Business"
    if "lifematters" in path_lower:
        return "Life Matters"
    if "commentary" in path_lower:
        return "Opinion"
    if "gossip" in path_lower:
        return "Entertainment"
    if "restaurant" in path_lower:
        return "Life Matters"
    
    # Build combined text for keyword matching
    if title:
        combined_text += " " + title.lower()
    if content:
        combined_text += " " + content.lower()
    
    # Score each category
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Count occurrences of each keyword
            score += len(re.findall(r"\b" + re.escape(keyword) + r"\b", combined_text))
        scores[category] = score
    
    # Return the category with the highest score, or "News" as default
    if scores:
        best_category = max(scores, key=scores.get)
        if scores[best_category] > 0:
            return best_category
    
    return "News"