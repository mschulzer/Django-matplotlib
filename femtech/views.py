from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
import urllib, base64
import json
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    return render(request, "home.html", {})

def plot_view(request):
    plt.figure(figsize=(6,4))
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    plt.title("Sample Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, "plot.html", {"plot_uri": uri})

@csrf_exempt
def post_data_view(request):
    """
        curl -X POST http://127.0.0.1:8000/post/ \
        -H "Content-Type: application/json" \
        -d '{"id": 24}'
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id', 'No group-ID provided')

            response_data = {
                'status': 'success',
                'message': f'Registered data from group {id}',
            }
            return JsonResponse(response_data)
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'status': 'error', 'message': 'POST requests only'}, status=405)