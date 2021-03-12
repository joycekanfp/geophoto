from django.shortcuts import render
from .models import *
from .forms import SearchForm, PresetForm
import os

def search_photo(request, in_latitude=None, in_longitude=None):
    """
        Shows the default/search page to a user.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            result_string = 'File imported successfully'
            context={}
            
            return render(request, 'result.html', context)
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})


def list_preset(request):
    """
        The page to Add a preset location or Search photos using the preset locations.
    """
    result_string=''
    if request.method == 'POST':
        form = PresetForm(request.POST)
        if form.is_valid():
            obj = PresetList(name=request.POST['name'], 
                    latitude=request.POST['latitude'],
                    longitude=request.POST['longitude'])
            
            obj.save()

            result_string = 'Location saved to Preset List successfully'
                        
    else:    
        form = PresetForm()

    preset_list = PresetList.objects.all().order_by('-date_added')

    context = {'form': form, 'preset_list':preset_list, 'result_string':result_string}

    return render(request, 'preset_list.html', context)


def list_fav(request):
    test = ['test1','test2']

    return render(request, 'fav_list.html', locals())