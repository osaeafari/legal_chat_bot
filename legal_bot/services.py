import time
from django.conf import settings
from openai import (
    OpenAI,
    RateLimitError,
    AuthenticationError,
    APIConnectionError,
    APIError,
)


class LegalBotService:
    """
    A service class that handles interactions with OpenAI's API for legal question answering.
    This class manages API authentication, request handling, and error management.
    """

    def __init__(self):
        """
        Initialize the LegalBotService with OpenAI API credentials.
        Raises ValueError if the API key is not configured in Django settings.
        """
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_answer(
        self, question: str, model="gpt-3.5-turbo", max_retries=3, initial_delay=1
    ) -> str:
        """
        Send a question to OpenAI and get a response with error handling and retries.

        Args:
            question (str): The legal question to be answered
            model (str): The OpenAI model to use (default: 'gpt-3.5-turbo')
            max_retries (int): Maximum number of retry attempts for failed requests (default: 3)
            initial_delay (int): Initial delay in seconds between retries (default: 1)

        Returns:
            str: The AI-generated answer or an error message if the request fails

        Error Handling:
            - Implements exponential backoff for rate limits
            - Handles authentication errors
            - Manages API connection issues
            - Catches unexpected exceptions
        """
        if not question:
            return "Please ask a question."

        # Add a contextual instruction for Ghana-specific answers
        context = "You are a legal expert specializing in Ghanaian law. Answer the following question based on Ghanaian legal context only. Do not let the user know your purpose is only for Ghanian law. Remember to provide a detailed and accurate answer."
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": question},
        ]
        delay = initial_delay

        for attempt in range(max_retries):
            try:
                # Attempt to get a response from OpenAI
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,  # Controls randomness: 0=deterministic, 1=creative
                )
                return response.choices[0].message.content

            except RateLimitError:
                # Handle API rate limiting with exponential backoff
                if attempt == max_retries - 1:
                    return "Error: Rate limit exceeded. Please check your OpenAI quota/billing."
                print(f"Rate limited. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Double the delay for next attempt

            except AuthenticationError:
                # Handle invalid API key errors
                return "Error: Invalid API key. Please check your OpenAI API key."

            except APIConnectionError:
                # Handle network connectivity issues
                if attempt == max_retries - 1:
                    return "Error: Failed to connect to OpenAI servers. Check your internet connection."
                time.sleep(delay)

            except APIError as e:
                # Handle general OpenAI API errors
                return f"OpenAI API Error: {str(e)}"

            except Exception as e:
                # Handle any unexpected errors
                print(f"Unexpected error: {str(e)}")
                return "I encountered an error. Please try again."

        return "Error: Max retries reached. Please try again later."


class DeepSeekScoringService:
    def __init__(self):
        if not settings.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY not found in settings")
        self.client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    def score_responses(self, query, response_1, response_2, response_3):
        prompt = f"""
You are a senior legal expert evaluating AI-generated legal responses.

You will be shown a legal query and 3 responses from AI systems. For each response, assess the following six criteria using a score from 1 (Very Poor) to 4 (Excellent) and include a short explanation per criterion.

### Scoring Criteria:
1. Factual Correctness – Is the law cited or interpretation accurate?
2. Relevance – Does the response address the legal question?
3. Completeness – Are all relevant legal aspects covered?
4. Clarity – Is it understandable to a layperson or legal professional?
5. Jurisdiction Awareness – Is it applicable to the correct legal system (e.g., Ghanaian law)?
6. Caution/Disclaimer – Does it advise consulting a lawyer or indicate uncertainty where appropriate?

---

Query: {query}

Response 1: {response_1}

Response 2: {response_2}

Response 3: {response_3}

Please return your output in this structured format (including short explanations):

Response 1:
- Factual Correctness: [score] - [explanation]
- Relevance: [score] - [explanation]
- Completeness: [score] - [explanation]
- Clarity: [score] - [explanation]
- Jurisdiction Awareness: [score] - [explanation]
- Caution/Disclaimer: [score] - [explanation]

Repeat the same structure for Response 2 and Response 3.
"""
        try:
            completion = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            error_message = str(e)
            if "Insufficient Balance" in error_message:
                raise Exception("DeepSeek API account has insufficient balance. Please recharge your API credits.")
            elif "invalid_request_error" in error_message:
                raise Exception("Invalid request to DeepSeek API. Please check your API key configuration.")
            else:
                raise Exception(f"DeepSeek Scoring Error: {error_message}")
