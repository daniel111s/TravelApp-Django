from django.urls import path
from TravelWebApp.views import travelList, home_page, new_travel, edit_travel, delete_travel, find_hotels,show_details
from TravelWebApp.views import show_gallery, find_restaurants, find_places, add_task, task_list, edit_task, delete_task

urlpatterns = [
    path('list/', travelList, name='travel_list'),
    path('home/', home_page, name='home_page'),
    path('new/', new_travel, name='new_travel'),
    path('details/<int:id>/', show_details, name='show_details'),
    path('gallery/<int:id>/', show_gallery, name='show_gallery'),
    path('restaurants/<int:id>/', find_restaurants, name='find_restaurants'),
    path('places/<int:id>/', find_places, name='find_places'),
    path('hotels/<int:id>/', find_hotels, name='find_hotels'),
    path('edit/<int:id>/', edit_travel, name='edit_travel'),
    path('delete/<int:id>/', delete_travel, name='delete_travel'),
    path('add-task/<int:id>/', add_task, name='add_task'),
    path('tasks/<int:id>/', task_list, name='task_list'),
    path('task-edit/<int:id>/', edit_task, name='edit_task'),
    path('task-delete/<int:id>/', delete_task, name='delete_task'),

]
