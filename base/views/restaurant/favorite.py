from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from base.models import Restaurant, Favorite

@login_required(login_url="account_login")
@require_POST
def toggle_favorite(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )

    if not created:
        fav.delete()

    # 詳細ページに戻す
    return redirect("restaurant_detail", pk=pk)
