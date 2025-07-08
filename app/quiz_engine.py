import random
from wiki_api import get_description, get_image

DESTINATIONS = {
    "Paris": {"continent": "Europa", "category": "Stadt"},
    "Kyoto": {"continent": "Asien", "category": "Stadt"},
    # ...
}

def generate_quiz_question(category, continent, difficulty):
    candidates = [d for d in DESTINATIONS if DESTINATIONS[d]['continent'] == continent and DESTINATIONS[d]['category'] == category]
    
    num_options = {"Leicht": 2, "Mittel": 4, "Schwer": 10}[difficulty]
    correct = random.choice(candidates)
    options = random.sample([d for d in candidates if d != correct], num_options - 1)
    options.append(correct)
    random.shuffle(options)

    description = get_description(correct)
    image_url = get_image(correct)

    return {
        "question_text": description,
        "image_url": image_url,
        "options": options,
        "correct": correct,
        "details": {"name": correct, "booking_url": f"https://booking.com/search?dest={correct}"}
    }
