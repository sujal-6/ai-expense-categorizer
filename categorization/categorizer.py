import ollama
import json
import os
import logging

MODEL_NAME = "llama3"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "classification_cache.json")

categories = [
    "Travel",
    "Meals",
    "Software",
    "Utilities",
    "Other"
]

logging.basicConfig(level=logging.INFO)

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

cache = load_cache()

def classify(description, categories):

    if not isinstance(description, str) or not description.strip():
        return "Other"

    description = description.strip()

    # If model changes later
    cache_key = f"{MODEL_NAME}:{categories}:{description}"

    # First cache
    if cache_key in cache:
        return cache[cache_key2]
    
    prompt = f"""You are an expense classification assistant. Classify the following expense into ONE of these categories:
    {categories}
    Return ONLY a valid JSON object in this format:
    {{"category": "CategoryName"}}
    Expense Description: "{description}" """

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.get("message", {}).get("content", "").strip()

        try:
            result = json.loads(content)
            category = result.get("category", "Other")

            if category not in categories:
                category = "Other"

        except json.JSONDecodeError:
            logging.warning(f"Invalid JSON from model for: {description}")
            category = "Other"

    except Exception as e:
        logging.error(f"LLM error for '{description}': {e}")
        category = "Other"

    # Cache Save
    cache[cache_key] = category
    save_cache(cache)
    return category

def categorize_expenses(df, categories_list):
    if "description" not in df.columns:
        raise ValueError("DataFrame must contain a 'description' column")

    unique_desc = df["description"].unique()
    mapping = {desc: classify(desc, categories_list) for desc in unique_desc}
    df["category"] = df["description"].map(mapping)
    return df


