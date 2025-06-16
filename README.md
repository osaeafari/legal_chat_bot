# Legal Chat Bot

A Django-based chat application that uses OpenAI's API to answer legal questions.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Django 5.1+
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/legal_chat_bot.git
cd legal_chat_bot
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and Django secret key to the `.env` file

```bash
cp .env.example .env
# Edit the .env file with your actual API keys
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000/` in your browser to use the chat bot.

## Security Note

Never commit your API keys or secrets to version control. The `.env` file is listed in `.gitignore` to prevent accidental commits of sensitive information.

## Features

- Clean, modern UI design
- Real-time chat experience
- Typing indicator to show when the AI is processing
- Error handling for API failures

## FLAN-t5 model - TODO

- this model has to be connected to the 3 AI platfomrs (GPT, Gemini, Meta ai)
- the model is to evaluate the responses of the AI's by displaying the score and rational.
