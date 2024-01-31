from django.contrib import admin
from .models import Product, Recipe, Ingredient


class RecipeProductInline(admin.TabularInline):
    model = Ingredient
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'count']
    list_filter = ['name', 'count']
    search_fields = ['name', ]
    ordering = ['name', ]
    exclude = ['count']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_products']
    list_filter = ['name', 'products__name']
    search_fields = ['name', 'products__name']
    ordering = ['name', ]
    inlines = [RecipeProductInline]

    def get_products(self, obj):
        products = obj.products.all().prefetch_related('ingredients')
        return ", ".join([product.name for product in products])

    get_products.short_description = 'Продукты в рецепте'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'product', 'weight']
    list_filter = ['recipe__name', 'product__name', 'weight']
    search_fields = ['recipe__name', 'product__name']
    ordering = ['recipe__name', ]
