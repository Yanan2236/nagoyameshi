from django.urls import path
from base.views.billing.billing import CardInfoView, CardUpdateView, CardDeleteView, card_update_complete, card_update_done

urlpatterns = [
    path("card/", CardInfoView.as_view(), name="card_info"),
    path("card/update", CardUpdateView.as_view(), name="card_update"),
    path("card/complete/", card_update_complete, name="card_update_complete"),
    path("card/update/done/", card_update_done, name="card_update_done"),
    path("card/delete/", CardDeleteView.as_view(), name="card_delete"),
]