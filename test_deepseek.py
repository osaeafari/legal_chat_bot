import os
from dotenv import load_dotenv
from openai import OpenAI

def test_deepseek_api():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found in environment variables")
        return
    
    # Initialize client
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # Test data
    test_query = "What are the legal requirements for starting a business in Ghana?"
    test_responses = [
        "To start a business in Ghana, you need to register with the Registrar General's Department.",
        "Business registration in Ghana requires submitting forms to the RGD.",
        "According to Ghanaian law, business registration involves name search and reservation."
    ]
    
    # Create prompt
    prompt = f"""
    Evaluate these responses about: {test_query}
    
    Response 1: {test_responses[0]}
    Response 2: {test_responses[1]}
    Response 3: {test_responses[2]}
    
    Rate each response from 1-4 for accuracy and completeness.
    """
    
    try:
        # Make API call
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500
        )
        
        # Print result
        print("API call successful!")
        print("\nResponse:")
        print(completion.choices[0].message.content)
        return True
        
    except Exception as e:
        print(f"\nError testing DeepSeek API: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing DeepSeek API...")
    test_deepseek_api()