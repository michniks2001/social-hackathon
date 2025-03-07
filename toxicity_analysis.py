from openai import OpenAI
import os
from load_dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com")


def predict_toxicity_and_sarcasm(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{
                "role": "system",
                "content": '''
                1) **Toxicity Detection**:  
                    - Identify **offensive, hateful, threatening, or harassing** language.  
                    - Recognize **implicit toxicity**, including passive-aggressive or manipulative speech.  
                    - Consider **context**, distinguishing strong opinions from actual hostility.  
                    - Provide a **toxicity score (0-10)**, where:  
                        - 0 = Completely harmless  
                        - 10 = Extremely toxic (hate speech, severe harassment)  

                2) **Sarcasm Detection**:  
                    - Identify sarcasm based on **word choice, exaggeration, and contradiction**.  
                    - Consider **context and tone** to determine if a message is sarcastic.  
                    - Provide a **sarcasm score (0-10)**, where:  
                        - 0 = Completely literal  
                        - 10 = Highly sarcastic  
               '''
            }, {"role": "user",
                "content": f"Analyze this message: '{text}'. Provide a JSON response with 'toxicity_level' (0-10) and 'sarcasm_level' (0-10) without explanation"}
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
        print(f"Error in predict_toxicity_and_sarcasm: {e}")
        return {"toxicity_level": 0, "sarcasm_level": 0}


predict_toxicity_and_sarcasm('I hate you!')
predict_toxicity_and_sarcasm('I hate you!/ s')
