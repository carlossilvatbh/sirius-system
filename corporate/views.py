from django.shortcuts import render


def canvas_modern(request):
    """Modern canvas interface with enhanced UX/UI."""
    context = {
        'page_title': 'SIRIUS Canvas v2.0 - Modern Interface'
    }
    return render(request, 'canvas_modern.html', context)
