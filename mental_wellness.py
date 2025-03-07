"""TODO: Create functions for motivation/cheering users up!
    """
from openai import OpenAI
import os
from load_dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com")


def predict_mental_wellness(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "system",
                "content": '''
                1) **Mood Detection**:  
                    - Analyze tone or sentiment  
                    - Detect **Negativity, distress, frustration, or negativity** language.  
                    - Provide a **Mood score (0-10)**, where:  
                        - 0 = Completely happy  
                        - 10 = Unhappy 

                2) **Positive suggestion**:  
                    - Give some jokes or motivational quotes from past conversations.
                    - Provide specific encouragement based on their past messages or server activity
               '''
            }, {"role": "user",
                "content": f"Analyze this message: '{text}'. Provide a JSON response with 'mood_level' (0-10) and 'suggestion' without explanation"}
            ],
            temperature=0.2,  # Lower temperature for more consistent results
            max_tokens=50
        )
        output = response.choices[0].message.content
        output = output.lstrip('```json')
        output = output.rstrip('```')
        print(output)

        import json
        result = json.loads(output)
        return result

    except Exception as e:
        print(f"Error in predict_predict_mental_wellness: {e}")
        return {"mood_level": 0, "suggestion": ""}
