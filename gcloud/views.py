import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib import messages
from google.cloud import documentai
from google.api_core.client_options import ClientOptions

from prompts.forms import UploadFileForm
from .forms import UserQuestionForm

# Create your views here.
def document_ai(request):
    header = "Google Cloud's Document AI"
    sub_header = 'Currently Testing Document AI.'

    context = {
        'header': header,
        'sub_header': sub_header,
    }

    if request.method == 'GET':
        form = UploadFileForm()
        context['form'] = form
        return render(request, 'form-page.html', context)
    
    elif request.method == 'POST':
        # Extract data from Django form
        form  = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'form-page.html', context)
        
        # Extract necessary data from the form
        uploaded_file = request.FILES.get('file')
        existing_file = form.cleaned_data['existing_file']

        # Handle file upload or existing file selection
        if uploaded_file:
            uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            fs = FileSystemStorage(location=uploads_dir)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
        elif existing_file:
            file_path = existing_file
        else:
            messages.error(request, "No file selected.")
            return render(request, 'form-page.html', context)
        
        # Fetch remaining info from Django settings
        project_id = settings.YOUR_PROJECT_ID
        location = settings.YOUR_PROCESSOR_LOCATION
        processor_display_name = settings.YOUR_PROCESSOR_DISPLAY_NAME

        # Set the `api_endpoint` if location is other than "us"
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

        # Initialize the client with the given options
        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        # Construct the resource name of the location
        parent = client.common_location_path(project_id, location)

        # Check if a processor with the desired name already exists
        processor_name = None
        for processor in client.list_processors(parent=parent):
            if processor.display_name == processor_display_name:
                processor_name = processor.name
                break

        # Create a Processor
        if not processor_name:
            processor = client.create_processor(
                parent=parent,
                processor=documentai.Processor(
                    type_="OCR_PROCESSOR",
                    display_name=processor_display_name,
                ),
            )
            processor_name = processor.name

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Load binary data
        raw_document = documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",
        )

        # Configure the process request
        process_request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

        # Process the document
        result = client.process_document(request=process_request)
        document = result.document

        # Add a success message
        messages.success(request, "Document processed successfully.")
        
        context['form'] = form
        request.session['processed_text'] = document.text
        # Redirect the user to the output and messages
        return redirect('doc_ai_output_view')
    
    else:
        # Handling other HTTP methods if necessary
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

def doc_ai_output_view(request):
    # Retrieve the text from the session
    text = request.session.get('processed_text', '')

    return render(request, 'doc-ai-output.html', {'text': text})

def ask_question_view(request):
    # Check if there is processed text in the session
    processed_text = request.session.get('processed_text', None)

    if request.method == 'POST':
        form = UserQuestionForm(request.POST)
        if form.is_valid():
            # Handle the user's question here
            # For example, you might want to search the processed text for answers
            # or save the question for further processing.

            return redirect('some_other_view')
    else:
        form = UserQuestionForm()

    return render(request, 'ask-question.html', {'form': form, 'processed_text': processed_text})