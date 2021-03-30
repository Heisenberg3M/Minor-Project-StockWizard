from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Post
from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data
#from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form = TickerForm()

    return render(request, 'stocks/home.html', {'form': form})

def ticker(request, tid):
    context = {}
    context['ticker'] = tid
    context['meta'] = get_meta_data(tid)
    context['price'] = get_price_data(tid)
    #print(context)
    context['show'] = True
    return render(request, 'stocks/home.html', context)

def about(request):
    return render(request, 'stocks/about.html', {'title' : 'About'})


