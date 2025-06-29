import random

class AdvancedTweetGenerator:
    def __init__(self):
        self.brand_voices = {
            'Casual': {'emojis': True, 'tone': 'friendly'},
            'Professional': {'emojis': False, 'tone': 'formal'},
            'Playful': {'emojis': True, 'tone': 'fun'},
        }

        self.industry_templates = {
            'Tech': ["🚀 Innovation alert: {message}", "Tech news: {message}", "{company} breakthrough: {message}"],
            'Food': ["🍕 Delicious update: {message}", "Tasty news: {message}", "Fresh drop from {company}: {message}"],
            'Fashion': ["✨ Style update: {message}", "Fashion alert: {message}", "New from {company}: {message}"],
            'General': ["{company} update: {message}", "From the {company} team: {message}"]
        }

        self.positive_templates = [
            "Great news from {company}! {message} 🎉",
            "{company} just shared something exciting: {message} 🌟",
            "We're thrilled to announce: {message} – Thanks, {company}! 🙌",
            "{company} just dropped this! {message} 🔥",
            "Big win for {company}: {message} 💪",
            "Can’t wait to see this in action: {message} 🚀"
        ]

        self.neutral_templates = [
            "{company} has an update: {message}",
            "FYI: {company} shared this today – {message}",
            "Here's the latest from {company}: {message}",
            "Heads up from {company}: {message}",
            "Straight from {company}'s playbook: {message}"
        ]

        self.negative_templates = [
            "{company} faces a challenge: {message} 😔",
            "Not ideal: {message} says {company} 😕",
            "Things to fix: {message} - {company}",
            "Tough day at {company}: {message} 😓",
            "Here's what went wrong at {company}: {message} ⚠️"
        ]

        self.hashtags = {
            'Tech': ['#TechNews', '#Innovation', '#AI'],
            'Food': ['#Foodie', '#Yum', '#Delicious'],
            'Fashion': ['#OOTD', '#StyleDrop', '#NewLook'],
            'General': ['#Update', '#News']
        }

        self.cta_phrases = {
            'positive': ["Stay tuned!", "More coming soon!", "Tell us what you think!"],
            'neutral': ["What are your thoughts?", "More updates soon.", "Keep an eye on this."],
            'negative': ["We're working on it.", "Appreciate your support.", "We'll improve."]
        }

    def _adjust_word_count(self, text, target):
        words = text.split()
        if len(words) > target:
            return ' '.join(words[:target]) + "..."
        return text

    def generate_smart_tweet(self, company, industry, brand_voice, message, word_count_target=25, sentiment_target=0.0, has_media=False):
        # Choose sentiment template set
        if sentiment_target > 0.5:
            sentiment_templates = self.positive_templates
            cta = random.choice(self.cta_phrases['positive'])
        elif sentiment_target < -0.5:
            sentiment_templates = self.negative_templates
            cta = random.choice(self.cta_phrases['negative'])
        else:
            sentiment_templates = self.neutral_templates
            cta = random.choice(self.cta_phrases['neutral'])

        industry_templates = self.industry_templates.get(industry, self.industry_templates['General'])

        # Choose base template
        if abs(sentiment_target) > 0.5:
            base_template = random.choice(sentiment_templates)
        else:
            base_template = random.choice(industry_templates)

        # Choose brand voice and emoji suffix
        voice = self.brand_voices.get(brand_voice, self.brand_voices['Casual'])
        media_tags = ["📷", "🎥", "🖼️", "📸"]
        emoji_suffix = f" {random.choice(media_tags)}" if has_media and voice['emojis'] else ""

        # Compose base tweet
        tweet = base_template.format(company=company, message=message)

        # Add emoji if media exists
        if emoji_suffix and emoji_suffix not in tweet:
            tweet += emoji_suffix

        # Add hashtag
        hashtags = self.hashtags.get(industry, self.hashtags['General'])
        hashtag = random.choice(hashtags)
        tweet += f" {hashtag}"

        # Add CTA
        tweet += f" {cta}"

        # Adjust to word count
        tweet = self._adjust_word_count(tweet.strip(), word_count_target)
        return tweet.strip()

# Example usage
gen = AdvancedTweetGenerator()
tweet = gen.generate_smart_tweet(
    company="Nike",
    industry="Fashion",
    brand_voice="Playful",
    message="Launching the all-new AirZoomX with performance-boosting foam tech",
    sentiment_target=0.8,
    has_media=True
)
print(tweet)