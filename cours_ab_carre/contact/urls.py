# contact/urls.py
from django.urls import path
from .views import contact_view
from django.views.generic import TemplateView

app_name = "contact"
urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path(
        "contact/merci/",
        TemplateView.as_view(
            template_name="contact/contact_page_landing.html"
        ),
        name="contact_thank_you",
    ),
]
