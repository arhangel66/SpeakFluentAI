from time import sleep

import openai

# Replace with your OpenAI API key

api_key = ""  # "YOUR_API_KEY
openai.api_key = api_key
system_message = "I want you to act as a spoken English teacher and improver. I will speak to you in English and you will reply to me in English to practice my spoken English. you speak with a 7 years old children, so please use only simple english. I want you to keep your reply neat, limiting the reply to 30 words. I want you to strictly correct my grammar mistakes and factual errors. I want you to ask me a question in your reply. to start - ask my name"


class Conversation:
    def __init__(self):
        self.messages = [{"role": "system", "content": system_message}]

    def get_gpt_answer(self) -> str:
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
