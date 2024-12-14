"""Counts the Number of Tokens in a Transcript"""

import sys
import tiktoken

def num_tokens(file_path):
    """Counts the Number of Tokens in a Transcript"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        enc = tiktoken.encoding_for_model('gpt-4')
        tokens = list(enc.encode(text))
        token_count = len(tokens)

        return token_count
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_tokens.py <file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    token_qty = num_tokens(input_file)
    print(f"The file contains {token_qty} tokens.")
