import os

from dotenv import load_dotenv

load_dotenv()

# API_KEY = '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'

# Access variables using os.environ
API_KEY = os.environ['API_KEY_ENV']

# Example usage
print(f'My variable value: {API_KEY}')