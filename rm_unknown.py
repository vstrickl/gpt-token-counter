import re

# Function to remove "Unknown" from a file
def remove_unknown(input_file_path, output_file_path):
    try:
        # Read the input file
        with open(input_file_path, 'r') as input_file:
            content = input_file.read()

        # Use regex to remove "Unknown"
        modified_content = re.sub(r'\bUnknown\b', '', content)

        # Write the modified content to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write(modified_content)

        print("Word 'Unknown' has been removed from the file.")

    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Provide the input and output file paths
input_file_path = './transcripts/14_Adisa/Adisa_(Full).txt'  # Change this to the path of your input file
output_file_path = './transcripts/14_Adisa/Adisa_(Full)_modified.md'  # Change this to the desired output file path

# Call the function to remove "Unknown" from the file
remove_unknown(input_file_path, output_file_path)
