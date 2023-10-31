import tiktoken
import os

def split_text_by_tokens(input_file_path, output_directory, tokens_per_file=2200):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    enc = tiktoken.encoding_for_model('gpt-4')

    with open(input_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    tokens = list(enc.encode(text))

    current_token_index = 0
    file_count = 1

    while current_token_index < len(tokens):
        next_chunk_end = min(current_token_index + tokens_per_file, len(tokens))
        next_chunk_tokens = tokens[current_token_index:next_chunk_end]
        next_chunk_text = enc.decode(next_chunk_tokens)

        output_file_path = os.path.join(output_directory, f'{file_name}_{file_count}.md')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(next_chunk_text)

        print(f'Files have been written to {output_file_path}')
        current_token_index = next_chunk_end
        file_count += 1

file_name = 'Adisa'
input_file_path = './chat_gpt_responses/14_Adisa/14_Adisa(Full).md'
output_directory = './parsed_responses/14_Adisa'
split_text_by_tokens(input_file_path, output_directory)
