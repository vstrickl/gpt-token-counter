import tiktoken

def num_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = list(enc.encode(text))
    token_count = len(tokens)

    return token_count

file_path = './transcripts/14_Adisa/Adisa_(Full).txt'
token_count = num_tokens(file_path)
print(f'The file contains {token_count} tokens.')