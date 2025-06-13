from flask import Flask, request, jsonify
from tweetgenerator import AdvancedTweetGenerator

app = Flask(__name__)
generator = AdvancedTweetGenerator()

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json(force=True)

        company = data.get('company', 'Our Company')
        industry = data.get('industry', 'general')
        brand_voice = data.get('brand_voice', 'casual')
        message = data.get('message', 'An exciting update!')
        word_count_target = int(data.get('word_count_target', 25))
        sentiment_target = float(data.get('sentiment_target', 0.0))
        has_media = bool(data.get('has_media', False))

        generated_tweet = generator.generate_smart_tweet(
            company=company,
            industry=industry,
            brand_voice=brand_voice,
            message=message,
            word_count_target=word_count_target,
            sentiment_target=sentiment_target,
            has_media=has_media
        )

        return jsonify({
            'success': True,
            'generated_tweet': generated_tweet
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

"""
$ curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Tesla",
    "industry": "tech",
    "brand_voice": "professional",
    "message": "Revolutionizing electric vehicle performance with cutting-edge battery technology",
    "word_count_target": 20,
    "sentiment_target": 0.6,
    "has_media": false
  }'
{
  "generated_tweet": "We're thrilled to announce: Revolutionizing electric vehicle performance with cutting-edge battery technology \u2013 Thanks, Tesla! \ud83d\ude4c.",
  "success": true
}
"""