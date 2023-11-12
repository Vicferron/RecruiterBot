import telebot
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables
BOT_TOKEN = os.getenv("BotToken")
OPENAI_API_KEY = os.getenv('OpenAiKey')
OPENAI_API_ENDPOINT = os.getenv('OpenAiEndpoint')
CHATGPT_MODEL_NAME = os.getenv('Deployment')

# OpenAI Configuration for Azure
openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_ENDPOINT
openai.api_type = 'azure'
openai.api_version = '2023-05-15'

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Global Variables
job_offers = {}
conversation_state = {}

# Azure OpenAI auxiliary functions
def send_message_to_openai(messages, model_name, max_response_tokens=500):
    response = openai.ChatCompletion.create(
        engine=model_name,
        messages=messages,
        temperature=0.5,
        max_tokens=max_response_tokens,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response['choices'][0]['message']['content']

# Start Command
@bot.message_handler(commands=["start", "hi"])
def send_welcome(message: telebot.types.Message):
    user_id = message.chat.id
    conversation_state[user_id] = "awaiting_job_offer"
    bot.reply_to(message, "Ok, send me a job offer to start the technical interview.")

# End Command
@bot.message_handler(commands=["end", "bye"])
def send_goodbye(message: telebot.types.Message):
    user_id = message.chat.id
    if user_id in conversation_state:
        del conversation_state[user_id]
    if user_id in job_offers:
        del job_offers[user_id]
    # Provide general feedback about the interview here (optional)
    bot.reply_to(message, "The interview has ended. Thank you and good luck!")

# Generate Interview Question
def generate_interview_question(job_offer: str, user_id) -> str:
    messages = [
        {"role": "system", "content": f"Based on the job description: '{job_offer}', create one relevant technical interview question."},
        {"role": "user", "content": job_offer}
    ]
    question = send_message_to_openai(messages, CHATGPT_MODEL_NAME)
    return question

# Generate Feedback
def generate_feedback(user_response: str, user_id) -> str:
    messages = [
        {"role": "system", "content": "Evaluate the following response and provide specific feedback and advice."},
        {"role": "user", "content": user_response}
    ]
    feedback = send_message_to_openai(messages, CHATGPT_MODEL_NAME)
    return feedback

# Main Handler for Text Messages
@bot.message_handler(func=lambda message: True)
def handle_message(message: telebot.types.Message):
    user_id = message.chat.id
    current_state = conversation_state.get(user_id, "")

    # Handle Job Offer
    if current_state == "awaiting_job_offer":
        job_offers[user_id] = message.text
        conversation_state[user_id] = "awaiting_user_response"
        question = generate_interview_question(job_offers[user_id], user_id)
        bot.send_message(user_id, question)
    elif current_state == "awaiting_user_response":
        user_response = message.text
        feedback = generate_feedback(user_response, user_id)
        bot.send_message(user_id, feedback)
        conversation_state[user_id] = "question_asked"
    elif current_state == "question_asked":
        question = generate_interview_question(job_offers[user_id], user_id)
        bot.send_message(user_id, question)
        conversation_state[user_id] = "awaiting_user_response"

# Start the bot
bot.infinity_polling()
