from django.http import JsonResponse
from django.shortcuts import render
from .form import VideoUrlForm
import yt_dlp
import re
import os
def get_video_formats(request):
    url = request.GET.get('url', None)
    if url:
        try:
            # Set yt-dlp options to only fetch info (no download)
            ydl_opts = {
                'format': 'bestvideo',  # Only best video format
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output path
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get('formats', [])
              
                if formats:
                    filtered_formats = [
                        fmt for fmt in formats if re.search(r'\d+p$', fmt.get("format", ""))
                    ]
                  
                    filtered_formats = [
    fmt for fmt in formats if fmt.get('format_note', '').endswith('p')
]

                    thumbnail_url = info_dict.get('thumbnail', None)

                    format_choices = [
    {
        'format_id': f['format_id'],
        'description': f"{f.get('resolution', 'N/A')} - {f.get('format_note', 'No description')}",
        'type': f.get('ext', 'unknown'),
        'url':f.get('url','N/A')
    }
    for f in filtered_formats
]

                    return JsonResponse({'formats': format_choices[::-1], 'thumbnail': thumbnail_url})
                else:
                    return JsonResponse({'error': 'Video not available or invalid URL.'})
        except Exception as e:
            return JsonResponse({'error': f"Error: {str(e)}"})
    return JsonResponse({'error': 'No URL provided.'})


def download_video(request):
    form = VideoUrlForm()
    error_message = None
    download_successful = False
    video_title = None

    if request.method == 'POST' and request.is_ajax():
        form = VideoUrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            # Setup yt-dlp options
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # Adjust as needed
                'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),  # Directory where the video will be saved
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)  # Download video
                    download_successful = True
                    video_title = info_dict.get('title', 'Unknown Title')

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
        
        # Return response as JSON
        return JsonResponse({
            'success': download_successful,
            'error_message': error_message,
            'video_title': video_title,
        })

    return render(request, 'page.html', {'form': form})
