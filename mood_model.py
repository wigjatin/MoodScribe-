from transformers import pipeline

# Force PyTorch backend
classifier = pipeline("sentiment-analysis", framework="pt")

def detect_mood(text: str) -> str:
    result = classifier(text)[0]
    label = result['label']
    score = result['score']

    if label == "POSITIVE":
        if score > 0.90:
            return "Happy"
        else:
            return "Motivated"
    elif label == "NEGATIVE":
        return "Sad"
    else:
        return "Calm"
