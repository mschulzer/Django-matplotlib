from django.shortcuts import render, HttpResponseRedirect
import matplotlib
matplotlib.use('agg')
import io
import urllib, base64

def home_view(request):
    return render(request, "home.html", {})

def plot_view(request):
    matplotlib.pyplot.figure(figsize=(6,4))
    matplotlib.pyplot.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    matplotlib.pyplot.title("Sample Plot")
    matplotlib.pyplot.xlabel("X-axis")
    matplotlib.pyplot.ylabel("Y-axis")

    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, "plot.html", {"plot_uri": uri})