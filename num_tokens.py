import tiktoken

def num_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    enc = tiktoken.encoding_for_model('gpt-4')
    tokens = list(enc.encode(text))
    token_count = len(tokens)

    return token_count

file_path = './chat_gpt_responses/14_Adisa/14_Adisa(Full)_condensed.md'
token_count = num_tokens(file_path)
print(f'The file contains {token_count} tokens.')