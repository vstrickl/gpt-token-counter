import os
import tiktoken
import markdown2

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.urls import reverse
from django.shortcuts import render, redirect

from .forms import SplitTextForm
from .forms import TokenCountForm

# Create your views here.
def token_counter(request):
    header = 'Token Counter Form'
    sub_header = 'This Form is used to count the number of tokens in a file.'

    context = {
        'header': header,
        'sub_header': sub_header,
    }

    if request.method == 'POST':
        form = TokenCountForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('file') 
            selected_file = form.cleaned_data.get('existing_file')

            if uploaded_file:
                # Ensure the uploads directory exists
                uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)

                # Save the uploaded file to the App
                fs = FileSystemStorage(location=uploads_dir)
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(filename)
            elif selected_file:
                file_path = selected_file
            else:
                # Handle the case where no file is selected or uploaded
                context['error'] = 'Please upload a file or select an existing file.'
                return render(request, 'form-page.html', context)


            # Count the tokens
            enc = tiktoken.encoding_for_model('gpt-4')
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            tokens = list(enc.encode(text))
            token_count = len(tokens)

            # Store token count in session and redirect
            request.session['token_count'] = token_count
            return redirect('num_tokens')
    else:
        form = TokenCountForm()

    context['form'] = form

    return render(request, 'form-page.html', context)

def num_tokens(request):
    header = 'Token Counter Result'
    sub_header = 'The total number of tokens counted in the provided file.'

    token_count = request.session.get('token_count', 'No file processed')

    context = {
        'header': header,
        'sub_header': sub_header,
        'token_count': token_count,
    }

    return render(request, 'token-count.html', context)

def split_file_by_tokens(request):
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
            uploaded_file = request.FILES.get('file')
            file_name = form.cleaned_data.get('file_name') or uploaded_file.name
            tokens_per_file = form.cleaned_data.get('tokens_per_file', 2200)
            selected_file = form.cleaned_data.get('existing_file')

            # Specify your input directory
            uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            fs = FileSystemStorage(location=uploads_dir)
            # Handling original file URL generation
            if uploaded_file:
                # Ensure the uploads directory exists
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                # Save the uploaded file
                filename = fs.save(uploaded_file.name, uploaded_file)
                original_file_path = fs.path(filename)
            elif selected_file:
                original_file_path = os.path.join(uploads_dir, selected_file)
            else:
                context['error'] = 'Please upload a file or select an existing file.'
                return render(request, 'form-page.html', context)
            
            # Check if the file exists
            if not os.path.exists(original_file_path):
                context['error'] = f'File not found: {original_file_path}'
                return render(request, 'form-page.html', context)

            # Process the file content
            enc = tiktoken.encoding_for_model('gpt-4')
            with open(original_file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            tokens = list(enc.encode(text))

            current_token_index = 0
            file_count = 1
            output_file_names = []
            
            # Specify your output directory
            output_directory = os.path.join(settings.BASE_DIR, 'outputs')
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            while current_token_index < len(tokens):
                next_chunk_end = min(current_token_index + tokens_per_file, len(tokens))
                next_chunk_tokens = tokens[current_token_index:next_chunk_end]
                next_chunk_text = enc.decode(next_chunk_tokens)

                output_file_name = f'{file_name}_{file_count}.md'
                output_file_path = os.path.join(output_directory, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(next_chunk_text)

                print(f'{file_count} file(s) have been written to {output_file_path}')
                output_file_names.append(output_file_name)
                current_token_index = next_chunk_end
                file_count += 1

            # Generate URL for the original file using 'render_markdown_view'\
            original_file_name = os.path.basename(original_file_path)
            request.session['output_files'] = output_file_names
            request.session['original_file_url'] = reverse('markdown_view', args=[original_file_name])

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
    output_file_names = request.session.get('output_files', [])
    output_files_urls = [reverse('markdown_view', args=[filename]) for filename in output_file_names]

    context = {
        'header': header,
        'sub_header':sub_header,
        'output_files': output_files_urls,
        'original_file_url': request.session.get('original_file_url', ''),
    }

    return render(request, 'split_output_files.html', context)

def render_markdown_view(request, filename):
    header = 'Markdown'
    sub_header = 'Your output files generated as markdown/html.'
    
    # Assuming Markdown files are stored in a 'markdown_files' directory within the Django project
    file_path = os.path.join(settings.BASE_DIR, 'outputs', filename)

    # Read Markdown file
    try:
        with open(file_path, 'r') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        markdown_text = 'File not found'

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_text)

    context = {
        'header': header,
        'sub_header':sub_header,
        'html_content': html_content
        }

    # Pass HTML content to the template
    return render(request, 'markdown_template.html', context)