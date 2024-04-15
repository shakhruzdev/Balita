from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import index_view, category_view, about_view, contact_view, category_detail_view, blog_search_view


urlpatterns = [
    path('', index_view),
    path('blog/', category_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('blog/<int:pk>/', category_detail_view),
    path('search/', blog_search_view, name='search_results')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
