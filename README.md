# Technical Interview Bot for Telegram

This bot is designed to simulate a technical interview experience for users. It interacts with the users, providing them with questions and feedback based on their responses.

## Features

- Initiates conversation with a welcome message and asks for a job offer to start the interview.
- Handles user responses and provides technical interview questions based on the job offer.
- Gives feedback on user's answers and continues with follow-up questions.
- Ends the interview session with a command and provides overall feedback.

## Commands

- `/start` - Begin the interview process and request for a job offer.
- `/end` - End the interview process and receive final feedback.

## Setup

To run this bot, you will need to set up a few environment variables:

- `BotToken`: Your Telegram Bot Token.
- `OpenAiKey`: Your OpenAI API key for Azure.
- `OpenAiEndpoint`: The endpoint URL for the Azure OpenAI service.
- `Deployment`: The deployment name for your Azure OpenAI model.

Make sure to install the required packages:

```bash
pip install python-telegram-bot openai python-dotenv