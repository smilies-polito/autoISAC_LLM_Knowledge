import json
import openai
from typing import List, Dict, Any
import time
import os

class QuestionAnswerer:
    def __init__(self, api_key: str):
        """Initialize the question answerer with OpenAI API key."""
        self.client = openai.OpenAI(api_key=api_key)
        
    def create_prompt(self, question: str, options: Dict[str, str]) -> str:
        """Create a prompt for the GPT model to answer the question."""
        prompt = f"""You are an expert in cybersecurity and automotive security. Please answer the following multiple-choice question by selecting the most appropriate option.

Question: {question}

Options:
"""
        for key, value in options.items():
            prompt += f"{key}: {value}\n"
        
        prompt += """\nPlease respond with only the letter of the correct answer (e.g., 'A', 'B', 'C', 'D', 'T', or 'F'). Do not include any explanation or additional text."""
        
        return prompt
    
    def get_answer_from_model(self, prompt: str, model: str = "gpt-4o") -> str:
        """Get answer from the specified GPT model."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert specializing in automotive security. Answer questions accurately and concisely."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content.strip()
            # Extract just the letter if there's extra text
            if len(answer) == 1 and answer.isalpha():
                return answer.upper()
            else:
                # Try to extract the first letter
                for char in answer:
                    if char.isalpha():
                        return char.upper()
                return "UNKNOWN"
                
        except Exception as e:
            print(f"Error getting answer from {model}: {str(e)}")
            return "ERROR"
    
    def process_questions(self, questions: List[Dict[str, Any]], models: List[str] = ["gpt-4o", "gpt-4o-mini"]) -> List[Dict[str, Any]]:
        """Process all questions and add answers from specified models."""
        results = []
        
        for i, question_data in enumerate(questions):
            print(f"Processing question {i+1}/{len(questions)}...")
            
            question = question_data["question"]
            options = question_data["options"]
            
            # Create the prompt
            prompt = self.create_prompt(question, options)
            
            # Get answers from each model
            answers = {}
            for model in models:
                print(f"  Getting answer from {model}...")
                answer = self.get_answer_from_model(prompt, model)
                answers[model] = answer
                
                # Add a small delay to avoid rate limiting
                time.sleep(0.5)
            
            # Create result entry
            result = question_data.copy()
            result["answers"] = answers
            results.append(result)
            
            print(f"  Answers: {answers}")
        
        return results


def main():
    # Set your OpenAI API key here
    api_key=""

    # Load questions from JSON file
    try:
        with open('questions_no_answer.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
        print(f"Loaded {len(questions)} questions from questions.json")
    except FileNotFoundError:
        print("questions.json file not found in current directory")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        return
    
    # Initialize the question answerer
    answerer = QuestionAnswerer(api_key)
    
    # Process questions with both models
    models = ["gpt-4o", "gpt-4o-mini"]
    results = answerer.process_questions(questions, models)
    
    # Save results to new file
    with open('answered_questions.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing complete! Results saved to answered_questions.json")
    print(f"Processed {len(results)} questions")
    
    # Show sample output
    if results:
        print("\nSample output format:")
        print(json.dumps(results[0], indent=2))

if __name__ == "__main__":
    main()