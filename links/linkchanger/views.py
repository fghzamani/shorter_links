from django.shortcuts import render # We will use it later

from django.http import HttpResponse, Http404, HttpResponseRedirect


# Model
from .models import Links

# Custom form

from .forms import ShortenerForm

# Create your views here.

def home_view(request):
    
    template = 'home.html'

    
    context = {}

    # Empty form
    context['form'] = ShortenerForm()

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':

        used_form = ShortenerForm(request.POST)

        if used_form.is_valid():
            cd = used_form.cleaned_data
            long_url = Links.objects.get(long_url = cd['long_url'])
            if long_url ==None: # برای این که یه لینک فقط یه فرم کوتاه داشته باشه و یه لینک چندتا لینک کوتاه ازش تولید نشه
                shortened_object = used_form.save()

                new_url = request.build_absolute_uri('/') + shortened_object.short_url
                
                long_url = shortened_object.long_url 
             
                
            else:
                new_url = long_url.short_url
            
            context['new_url']  = new_url
            context['long_url'] = long_url
             
            return render(request, template, context)

        context['errors'] = used_form.errors

        return render(request, template, context)


def redirect_url_view(request, shortened_part):

    try:
        shortener = Links.objects.get(short_url=shortened_part)       

        shortener.save()
        
        return HttpResponseRedirect(shortener.long_url)
        
    except:
        raise Http404('Sorry this link is broken :(')