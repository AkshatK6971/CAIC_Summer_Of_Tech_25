import random

class AdvancedTweetGenerator:
    def __init__(self):
        self.brand_voices = {
            'casual': {'emojis': True, 'tone': 'friendly'},
            'professional': {'emojis': False, 'tone': 'formal'},
            'playful': {'emojis': True, 'tone': 'fun'},
        }

        self.industry_templates = {
            'tech': ["🚀 Innovation alert: {message}", "Tech news: {message}"],
            'food': ["🍕 Delicious update: {message}", "Tasty news: {message}"],
            'fashion': ["✨ Style update: {message}", "Fashion alert: {message}"],
            'general': ["{company} update: {message}", "From the {company} team: {message}"]
        }

        self.positive_templates = [
            "Great news from {company}! {message} 🎉",
            "{company} just shared something exciting: {message} 🌟",
            "We're thrilled to announce: {message} – Thanks, {company}! 🙌"
        ]

        self.neutral_templates = [
            "{company} has an update: {message}",
            "FYI: {company} shared this today – {message}",
            "Here's the latest from {company}: {message}"
        ]

        self.negative_templates = [
            "{company} faces a challenge: {message} 😔",
            "Not ideal: {message} says {company} 😕",
            "Things to fix: {message} - {company}"
        ]

    def generate_smart_tweet(self, company, industry, brand_voice, message, word_count_target=25, sentiment_target=0.0, has_media=False):
        # Choose sentiment template
        if sentiment_target > 0.5:
            sentiment_templates = self.positive_templates
        elif sentiment_target < -0.5:
            sentiment_templates = self.negative_templates
        else:
            sentiment_templates = self.neutral_templates

        industry_templates = self.industry_templates.get(industry, self.industry_templates['general'])
        if abs(sentiment_target) > 0.5:
            base_template = random.choice(sentiment_templates)
        else:
            base_template = random.choice(industry_templates)

        voice = self.brand_voices.get(brand_voice, self.brand_voices['casual'])
        emoji_suffix = " 📸" if has_media and voice['emojis'] else ""

        tweet = base_template.format(company=company, message=message)

        words = tweet.split()
        if len(words) > word_count_target:
            tweet = " ".join(words[:word_count_target]) + "..."
        elif len(words) < word_count_target:
            tweet += " 🚀" if voice['emojis'] else "."

        tweet = tweet.strip()
        if has_media and emoji_suffix not in tweet:
            tweet += emoji_suffix
        return tweet.strip()

gen = AdvancedTweetGenerator()
tweet = gen.generate_smart_tweet(company="Nike",industry="fashion",brand_voice="playful",
        message="Launching the all-new AirZoomX with performance-boosting foam tech",word_count_target=22,
        sentiment_target=0.8,has_media=True)
print(tweet)
