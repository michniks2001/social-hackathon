from transformers import pipeline

# create a pipeline of sentiment analyzer
sentiment_analyzer = pipeline("sentiment-analysis")

# real-time sentiment analysis
input = "I hate this guy!"
ouput = sentiment_analyzer(input)

# postive or negative
ouput[0]['label']

# score
ouput[0]['score']
