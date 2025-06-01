# phobia.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhobiaExplainer:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_explanation(self, fear):
        prompt = f"""
        Provide a detailed explanation about the fear of {fear} in the following format:

        Description: [Brief overview of the fear]

        Scientific Name: [Medical term if applicable]

        Common Symptoms:
        - [Symptom 1]
        - [Symptom 2]
        - [Symptom 3]

        Common Triggers:
        - [Trigger 1]
        - [Trigger 2]
        - [Trigger 3]

        Treatment Options:
        - [Treatment 1]
        - [Treatment 2]
        - [Treatment 3]

        Self-Help Tips:
        - [Tip 1]
        - [Tip 2]
        - [Tip 3]

        Did You Know?
        - [Interesting historical fact about this phobia]
        - [Surprising statistic or research finding]
        - [Famous person who had/has this phobia]
        - [Unique cultural perspective about this fear]

        Please provide factual, well-structured information in this exact format.
        """
        
        try:
            logger.info(f"Requesting explanation for fear: {fear}")
            response = self.model.generate_content(prompt)
            logger.info("Received response from Gemini API")
            return response.text
        except Exception as e:
            logger.error(f"Error in get_explanation: {str(e)}")
            raise Exception(f"Failed to get explanation: {str(e)}")