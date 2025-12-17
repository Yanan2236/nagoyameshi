from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

from base.models import Restaurant


def admin_restaurant_list(request):
    qs = (
        Restaurant.objects
        .select_related("sub_area", "sub_area__spot")
        .prefetch_related("genre")
        .all()
    )

    name = request.GET.get("name")
    spot_id = request.GET.get("spot")
    genre_id = request.GET.get("genre")
    sort = request.GET.get("sort")

    if name:
        qs = qs.filter(name__icontains=name)

    if spot_id:
        qs = qs.filter(sub_area__spot__id=spot_id)

    if genre_id:
        qs = qs.filter(genre__id=genre_id).distinct()

    if sort == "name":
        qs = qs.order_by("name")
    elif sort == "name_desc":
        qs = qs.order_by("-name")
    elif sort == "created":
        qs = qs.order_by("created_at")
    elif sort == "created_desc":
        qs = qs.order_by("-created_at")

    results = []
    for r in qs:
        results.append({
            "id": r.id,
            "name": r.name,
            "spot": r.sub_area.spot.name if r.sub_area_id else None,
            "sub_area": r.sub_area.name if r.sub_area_id else None,
            "genre": [g.name for g in r.genre.all()],
            "address": r.address,
            "image_url": r.image.url if r.image else None,
        })

    return JsonResponse({"results": results})

    

def admin_restaurant_detail(request, pk):
    if request.method != "GET":
        raise Http404("Only GET is allowed")

    r = get_object_or_404(
        Restaurant.objects
        .select_related("sub_area")
        .prefetch_related("genre"),
        pk=pk,
    )

    data = {
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "ward": r.ward,
        "ward_label": r.get_ward_display(),
        "sub_area_id": r.sub_area_id,
        "sub_area_name": r.sub_area.name if r.sub_area_id else None,
        "address": r.address,
        "phone_number": r.phone_number,
        "image_url": r.image.url if r.image else None,
        "genre_ids": [g.id for g in r.genre.all()],
        "genre_names": [g.name for g in r.genre.all()],
        "created_at": r.created_at.isoformat(),
        "updated_at": r.updated_at.isoformat(),
    }

    return JsonResponse(data)
