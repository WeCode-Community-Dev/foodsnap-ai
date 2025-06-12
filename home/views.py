from django.shortcuts import render, redirect
from .forms import UploadImageForm



def upload_view(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            pre = form.save()
            url = request.session['uploaded_file_url'] = pre.file.url 
            context = {
            'food_name': 'Pizza',
            'food_calories': 285,
            'image_url':  url        
        }
        return render(request, 'upload_success.html', context)
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})



def upload_success(request):
    return render(request, 'upload_success.html')  # Create this template