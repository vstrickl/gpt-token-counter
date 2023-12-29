import tiktoken
import os

from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

from .forms import SplitTextForm

# Create your views here.
def num_tokens(file_path):
    file_path = static('app_inputs/research/trisomy_21.md')
    token_count = num_tokens(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    enc = tiktoken.encoding_for_model('gpt-4')
    tokens = list(enc.encode(text))
    token_count = len(tokens)
    
    return HttpResponse(f'The file contains {token_count} tokens.')

def split_text_by_tokens(request):
    header = 'Split Text Form'
    sub_header = 'This Form is used to breakup larger files that Chat GPT cannot parse.'

    context = {
        'header': header,
        'sub_header': sub_header,
    }

    if request.method == 'POST':
        form = SplitTextForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form
            uploaded_file = request.FILES['file']
            file_name = form.cleaned_data.get('file_name') or uploaded_file.name
            tokens_per_file = form.cleaned_data.get('tokens_per_file', 2200)

            # Ensure the uploads directory exists
            uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            # Save the uploaded file temporarily
            fs = FileSystemStorage(location=uploads_dir)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)
            input_file_path = fs.path(filename)

            # Specify your output directory
            output_directory = os.path.join(settings.BASE_DIR, 'outputs')
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            
            # Process the file content
            enc = tiktoken.encoding_for_model('gpt-4')
            with open(input_file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            tokens = list(enc.encode(text))

            current_token_index = 0
            file_count = 1
            output_info = []

            while current_token_index < len(tokens):
                next_chunk_end = min(current_token_index + tokens_per_file, len(tokens))
                next_chunk_tokens = tokens[current_token_index:next_chunk_end]
                next_chunk_text = enc.decode(next_chunk_tokens)

                output_file_path = os.path.join(output_directory, f'{file_name}_{file_count}.md')
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(next_chunk_text)

                print(f'{file_count} file(s) have been written to {output_file_path}')
                output_info.append(f'{file_count} file(s) have been written to {output_file_path}')
                current_token_index = next_chunk_end
                file_count += 1

            # Save file paths in session
            request.session['output_files'] = [os.path.join(output_directory, f'{file_name}_{i}.md') for i in range(1, file_count)]
            request.session['original_file'] = file_url

            # Redirect to a new view to display download links
            return redirect('split_output_files')
        
    else:
        form = SplitTextForm()

    context['form'] = form
    
    return render(request, 'form-page.html', context)

def split_output_files(request):
    header = 'Output Files'
    sub_header = 'These are the output files of your AI tool.'
    # Retrieve file paths from session
    output_files = request.session.get('output_files', [])
    original_file = request.session.get('original_file', '')

    context = {
        'header': header,
        'sub_header':sub_header,
        'output_files': output_files,
        'original_file': original_file,
    }

    return render(request, 'split_output_files.html', context)