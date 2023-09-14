from django.urls import path
from . views import (
    NewsList, PostDetail, NewsSearch, PostCreate, PostEdit, PostDelete,
    CategoryList, PostOfCategoryList, subscribe_to_category)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view(), name='search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('category/', CategoryList.as_view(), name='categories'),
    path('category/<int:pk>/', PostOfCategoryList.as_view(),
         name='posts_of_categories_list'),
    path('category/<int:pk>/subscribe', subscribe_to_category,
         name='subscribe_to_category'),

    ]
