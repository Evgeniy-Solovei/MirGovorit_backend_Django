from django.urls import path
from .views import AddProductToRecipeView, CookRecipeView, ShowRecipesWithoutProductView

app_name = 'cook_book'

urlpatterns = [
    path('add_product/<int:recipe_id>/<int:product_id>/<int:weight>/', AddProductToRecipeView.as_view(),
         name='add_product'),
    path('cook_recipe/<int:recipe_id>/', CookRecipeView.as_view(), name='article'),
    path('show_recipes_without_product/<int:product_id>/', ShowRecipesWithoutProductView.as_view(),
         name='articles-feed'),
]
