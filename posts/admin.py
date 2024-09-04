from django.contrib import admin
from posts.models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'category', 'created_at') 

    def save_model(self, request, obj, form, change):
        if not change:
            obj.writer = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Category)  

        
