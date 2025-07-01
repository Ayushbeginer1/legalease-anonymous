from django.urls import path
from .views import submit_anonymous_tip, list_public_tips, show_all_tips, download_evidence
from django.http import HttpResponse

urlpatterns = [
    path('submit-tips/', submit_anonymous_tip),
    path('tips/', list_public_tips),
    path('tips-table/', show_all_tips, name='tips_table'),
    path('download-evidence/<uuid:access_key>/',download_evidence, name="download_evidence"),
    path('',lambda request: HttpResponse("404"))
]