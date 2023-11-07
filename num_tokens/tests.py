import tiktoken
# from django.test import TestCase
from django.templatetags.static import static

# Create your tests here.
def num_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    enc = tiktoken.encoding_for_model('gpt-4')
    tokens = list(enc.encode(text))
    token_count = len(tokens)

    return token_count

file_path = static('app_inputs/research/trisomy_21.md')
token_count = num_tokens(file_path)
print(f'The file contains {token_count} tokens.')