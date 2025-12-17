from django.http import JsonResponse
from base.models import Restaurant, Spot, SpotSubArea


def restaurant_list_api(request):
    spot_id = request.GET.get("spot")
    genre_id = request.GET.get("genre")
    name = request.GET.get("restaurant_name")
    
    '''JOINで同時に持ってくる.別SQLでまとめて持ってきてから配る
    qs = Restaurant.objects.all()
    '''
    
    qs = Restaurant.objects.all().select_related("sub_area").prefetch_related("genre")
    
    '''JOINで結合する。
    if spot_id:
            spot = Spot.objects.get(pk=spot_id)
            subareas = spot.subareas.all()
            qs = qs.filter(sub_area__in=subareas)
    ''' 
    
    if spot_id:
        qs = qs.filter(sub_area__spot_id=spot_id)

    if genre_id:        
        qs = qs.filter(genre__id=genre_id)
        
    if name:
        qs = qs.filter(name__icontains=name)
        
    qs = qs.distinct()

    data = [
        {
            "id": r.id,
            "name": r.name,
            "ward": r.get_ward_display(),
            "address": r.address,
            "sub_area": {"id": r.sub_area.id, "name": r.sub_area.name,} if r.sub_area else None,
            "genre": [{"id": g.id, "name": g.name} for g in r.genre.all()],
            "image_url": r.image.url if r.image else None,
        }
        for r in qs
    ]
    
    return JsonResponse({"results": data})