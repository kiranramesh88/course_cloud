from django.contrib import admin
from instructor.models import *

admin.site.register(User)
admin.site.register(Category)

class CourseModel(admin.ModelAdmin):
    exclude=("owner",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner=request.user
        return super().save_model(request, obj, form, change)
    
class LessonInline(admin.TabularInline):
    model=Lesson
    extra=1

class ModulModel(admin.ModelAdmin):
    inlines=[LessonInline]

admin.site.register(Course,CourseModel)

admin.site.register(Module,ModulModel)
admin.site.register(Lesson)





