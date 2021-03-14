from django.shortcuts import render
from django.http import JsonResponse
from .models import GeoPhoto, PresetList, FavList
from .forms import SearchForm, PresetForm
from django.conf import settings
import flickrapi

def search_photo(request, in_latitude=None, in_longitude=None):
    """
        Shows the default/search page to a user.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            result_list=[]
            result_list, result_string = get_photos(request.POST['latitude'],request.POST['longitude'])

            context={'result_list':result_list, 'result_string': result_string}

            return render(request, 'result.html', context)
    else:
        if (in_latitude is not None and in_longitude is not None):
            result_list, result_string = get_photos(in_latitude,in_longitude)
            context={'result_list':result_list, 'result_string': result_string}

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
    result_list= []

    for fav in FavList.objects.all():
        result_list.append(fav.geophoto)

    result_string='Displaying {} favourite photos'.format(len(result_list))

    return render(request, 'fav_list.html', {"result_list":result_list, 'result_string':result_string})


def add_fav(request):
    if request.method == "GET":
        img_url = request.GET['photo_url']

        if len(GeoPhoto.objects.filter(photo_url=img_url))<1:
            new_photo_obj = GeoPhoto(title=request.GET['title'],
                        latitude=request.GET['latitude'],
                        longitude=request.GET['longitude'],
                        photo_url=img_url,
                        photo_thumbnail_url=request.GET['photo_thumbnail_url'])

            new_photo_obj.save()

            new_fav_obj = FavList(geophoto=new_photo_obj)
            new_fav_obj.save()


        return JsonResponse({"msg":"success"}, status = 200)

    return JsonResponse({}, status = 400)


def delete_fav(request):
    if request.method == "GET":
        obj_id = request.GET['geophoto_id']

        fav_obj = FavList.objects.filter(geophoto__id=obj_id)
        if (len(fav_obj)>0):
            fav_obj[0].delete()

        return JsonResponse({"msg":"success"}, status = 200)

    return JsonResponse({}, status = 400)


def delete_preset(request):
    if request.method == "GET":
        loc_id = request.GET['loc_id']

        obj = PresetList.objects.filter(id=loc_id)

        if (len(obj)>0):
            obj[0].delete()

        return JsonResponse({"msg":"success"}, status = 200)

    return JsonResponse({}, status = 400)


def get_photos(latitude, longitude):
    flickr = flickrapi.FlickrAPI(settings.API_KEY, settings.SECRET_API_KEY)
    result_list=[]
    county=''
    result_string='No photos found for geolocation ({},{})'.format(latitude,longitude)

    photo_list = flickr.photos.search(api_key=settings.API_KEY, lat=latitude, lon=longitude, per_page=100, privacy_filter=1, accuracy=11, format='parsed-json')

    for photo in photo_list.get('photos').get('photo'):
        photo_id=photo.get('id')

        photo_obj=flickr.photos.getInfo(api_key=settings.API_KEY, photo_id=photo_id, format='parsed-json')
        title=photo_obj['photo']['title']['_content']
        latitude=photo_obj['photo']['location']['latitude']
        longitude=photo_obj['photo']['location']['longitude']
        photo_url=photo_obj['photo']['urls']['url'][0]['_content']

        try:
            county=photo_obj['photo']['location']['county']['_content']
        except:
            pass

        thumbnail_img_url=''

        pic_info_obj=flickr.photos.getSizes(api_key=settings.API_KEY, photo_id=photo_id, format='parsed-json')

        for pic_info in pic_info_obj['sizes']['size']:
            if pic_info['label']=='Thumbnail':
                print('thumbnail_img_url: ',pic_info['source'])
                thumbnail_img_url=pic_info['source']

        geophoto_obj= GeoPhoto(title=title,latitude=latitude,longitude=longitude,photo_url=photo_url,photo_thumbnail_url=thumbnail_img_url)

        result_list.append(geophoto_obj)

    if len(result_list) > 0:
        if county == '':
            result_string='Displaying {} photos from Geolocation ({},{})'.format(len(result_list),latitude,longitude)
        else:
            result_string='Displaying {} photos from {}'.format(len(result_list),county)

    return result_list, result_string

