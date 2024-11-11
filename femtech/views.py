from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
import urllib, base64
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from datetime import datetime

def home_view(request):
    #return render(request, "home.html", {})
    return HttpResponseRedirect("/upload")

def plot_view(request):
    data = request.session.get('my_data', [])
    filtered_data = [
    {'timestamp': datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S'), 'value': item['value']}
    for item in data
    if item['timestamp'] != 'timestamp'  # Skip header or invalid row
    ]
    
    # Sort data by 'timestamp' in ascending order
    filtered_data.sort(key=lambda x: x['timestamp'])

    timestamps = [item['timestamp'] for item in filtered_data]
    values = [item['value'] for item in filtered_data]
    values_to_int = [int(x) for x in values]
    timestamps = pd.to_datetime(timestamps)

    plt.figure(figsize=(8,5))
    plt.plot(timestamps, values_to_int, marker='o')
    plt.xlabel("Tidspunkt")
    plt.ylabel("Registrering")
    plt.xticks(rotation=45)
    max_y = max(values_to_int)
    plt.yticks(range(0, int(max_y) + 100, 100))
    plt.tight_layout()
    buf = io.BytesIO()
    plt.grid()
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

def upload_data_view(request):
    data = {}
    my_data = []
    isUploaded = False

    if request.method == "GET":
        return render(request, "upload.html", data)

    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        return HttpResponseRedirect("/upload")
	
    if csv_file.multiple_chunks():
        return HttpResponseRedirect("/upload")

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    isUploaded = True

    for line in lines:
        if len(line) > 0:
            fields = line.split(",")
            print(fields)
            """
            data_dict = {}
            data_dict["ID"] = fields[0]
            data_dict["value"] = fields[1]
            data_dict["color"] = fields[2]
            data_dict["timestamp"] = fields[3]
            data_dict["eye"] = fields[4]

            my_data.append(data_dict)
            """
                    # Skip the header row by checking if the fields match the header names
            if fields[2].strip() == "timestamp":  # Adjust to actual header name if needed
                continue

            data_dict = {}
            data_dict["ID"] = fields[0]
            data_dict["value"] = fields[3]
            data_dict["color"] = fields[1]
            data_dict["timestamp"] = fields[2].strip()  # Remove whitespace
            data_dict["eye"] = fields[4]

            # Convert timestamp to datetime only if it is a string
            if isinstance(data_dict["timestamp"], str):
                try:
                    data_dict["timestamp"] = datetime.strptime(data_dict["timestamp"], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue  # Skip rows with invalid timestamp format

            my_data.append(data_dict)

    # Sort by timestamp in ascending order
    my_data.sort(key=lambda x: x["timestamp"])


    # Convert datetime objects back to strings for session storage
    for item in my_data:
        if isinstance(item["timestamp"], datetime):
            item["timestamp"] = item["timestamp"].strftime('%Y-%m-%d %H:%M:%S')

    print(my_data)
    request.session["my_data"] = my_data

    #my_data = my_data[1:]

    context = {
        'data_dict': my_data,
        'uploaded': isUploaded,
    }

    return render(request, "upload.html", context)