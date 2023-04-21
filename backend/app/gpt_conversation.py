import time
from random import choice

import openai

from common.config import API_KEY

# Replace with your OpenAI API key

subjects_b2 = [
    "Environment and Climate Change",
    "The Impact of Social Media on Society",
    "Travel and Tourism: Pros and Cons",
    "The Importance of a Balanced Diet and Exercise",
    "Education System: Traditional vs. Modern Approaches",
    "The Role of Technology in Our Lives",
    "Art and Culture: Its Influence on Society",
    "The Effects of Globalization on the World",
    "Gender Equality and Women Empowerment",
    "The Advantages and Disadvantages of Working Remotely",
    "The Influence of Advertising on Consumer Behavior",
    "The Benefits and Drawbacks of Multiculturalism",
    "Animal Rights and Welfare",
    "The Role of Family in Modern Society",
    "The Importance of Time Management",
    "Mental Health and Well-being",
    "The Role of Volunteering and Community Service",
    "The Significance of Personal Branding in the Job Market",
    "The Impact of the Internet on Language and Communication",
    "The Pros and Cons of Renewable Energy Sources",
]

subjects_b1 = [
    "Hobbies and Interests",
    "Daily Routines and Time Management",
    "Family Life and Relationships",
    "Holidays and Festivals",
    "Shopping and Consumerism",
    "Health and Wellness: Basic Tips",
    "Popular Music and Entertainment",
    "Describing Personal Experiences",
    "Basic Cooking and Recipes",
    "The Importance of Sleep",
    "Public Transportation and Traveling Locally",
    "Sports and Exercise: Staying Active",
    "Introduction to Environmental Issues",
    "School Life and Extracurricular Activities",
    "Pets and Animal Care",
    "Basic Etiquette and Manners",
    "Television, Movies, and Series",
    "Seasonal Activities and Weather",
    "Eating Out: Restaurants and Cafes",
    "Expressing Opinions and Preferences",
]

system_message_beginner = "I want you to act as a spoken English teacher and improver. I will speak to you in English and you will reply to me in English to practice my spoken English. you speak with a 7 years old children, so please use only simple english. I want you to keep your reply neat, limiting the reply to 30 words. I want you to strictly correct my grammar mistakes and factual errors. I want you to ask me a question in your reply. to start - ask my name"
system_message = "I want you to act as a spoken English teacher and improver. I will speak to you in English and you will reply to me in English to practice my spoken English. I want you to keep your reply neat, limiting the reply to 30 words. I want you to strictly correct my grammar mistakes and factual errors. I want you to ask me a question in your reply. subject - "
openai.api_key = API_KEY


class Conversation:
    def __init__(self):
        subject = choice(subjects_b1)
        self.messages = [{"role": "system", "content": system_message + subject}]

    def get_gpt_answer(self) -> str:
        t1 = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        return response['choices'][0]['message']['content'].strip()

    def process_user_message(self, message) -> str:
        self.messages.append({"role": "user", "content": message})
        assistant_response = self.get_gpt_answer()
        self.messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response


def main():
    conversation = Conversation()
    gpt_answer = conversation.get_gpt_answer()
    print(f"AI: {gpt_answer}")
    while True:
        user_message = input("User: ")
        print(f"User: {user_message}")
        answer = conversation.process_user_message(user_message)
        print(f"AI: {answer}")


if __name__ == "__main__":
    main()
