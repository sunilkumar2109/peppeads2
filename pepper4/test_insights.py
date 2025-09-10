from app import app, db, Form, Question, Response, Answer
import json
from datetime import datetime
import os
import google.generativeai

NEW_API_KEY = "AIzaSyC0gaUvUcl558V8OoP-g5z7AKDXvcBcHqw"

def test_insights_generation():
    with app.app_context():
        # Debug: Check if API key is loaded
        print("\n=== API Configuration ===")
        api_key = NEW_API_KEY  # Use the new API key directly
        if not api_key:
            print("Error: GOOGLE_API_KEY not found in environment variables")
            return
            
        print(f"API Key found: {api_key[:5]}...{api_key[-5:]}")
        
        # Configure Google client
        try:
            google.generativeai.configure(api_key=api_key)
            model = google.generativeai.GenerativeModel('gemini-2.0-flash')
            print("Successfully initialized Google client")
        except Exception as e:
            print(f"Error initializing Google client: {str(e)}")
            return
        
        # Get the first form (you can modify this to get a specific form)
        form = Form.query.first()
        if not form:
            print("No forms found in the database")
            return

        print("\n=== Form Information ===")
        print(f"Title: {form.title}")
        print(f"Description: {form.description}")
        print(f"Created at: {form.created_at}")

        # Get all questions for this form
        questions = Question.query.filter_by(form_id=form.id).all()
        print(f"\nFound {len(questions)} questions")

        # Get all responses
        responses = Response.query.filter_by(form_id=form.id).all()
        print(f"Found {len(responses)} responses")

        # Create question-answer mapping
        question_answer_mapping = {}
        for question in questions:
            print(f"\nProcessing question: {question.question_text}")
            question_answer_mapping[question.id] = {
                'question_text': question.question_text,
                'question_type': question.question_type,
                'answers': []
            }
            
            # Get all answers for this question
            for response in responses:
                answer = Answer.query.filter_by(
                    response_id=response.id,
                    question_id=question.id
                ).first()
                
                if answer:
                    print(f"Found answer: {answer.answer_text[:50]}...")
                    question_answer_mapping[question.id]['answers'].append({
                        'answer_text': answer.answer_text,
                        'submitted_at': response.submitted_at.isoformat()
                    })

        # Create the complete data structure
        structured_data = {
            'form_info': {
                'title': form.title,
                'description': form.description,
                'total_responses': len(responses),
                'created_at': form.created_at.isoformat()
            },
            'question_answer_mapping': question_answer_mapping
        }
        print(structured_data)

        # Print the structured data
        print("\n=== Complete Question-Answer Mapping ===")
        print(json.dumps(structured_data, indent=2))

        # Now generate insights
        from app import generate_insights_with_gemini
        
        print("\n=== Generating Product Insights ===")
        try:
            product_insights = generate_insights_with_gemini(structured_data, form, 'product')
            print(json.dumps(product_insights, indent=2))
        except Exception as e:
            print(f"Error generating product insights: {str(e)}")

        print("\n=== Generating Market Segments ===")
        try:
            market_segments = generate_insights_with_gemini(structured_data, form, 'market')
            print(json.dumps(market_segments, indent=2))
        except Exception as e:
            print(f"Error generating market segments: {str(e)}")

        print("\n=== Generating Improvement Ideas ===")
        try:
            improvement_ideas = generate_insights_with_gemini(structured_data, form, 'improvement')
            print(json.dumps(improvement_ideas, indent=2))
        except Exception as e:
            print(f"Error generating improvement ideas: {str(e)}")

if __name__ == '__main__':
    test_insights_generation() 