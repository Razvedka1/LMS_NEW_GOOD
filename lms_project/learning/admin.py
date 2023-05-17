from django.contrib import admin
from .models import Course, Lesson, Review


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',  'start_date', 'description',)
    list_display_links = ('title', 'start_date',)  # Перенапраляет на редактирование записи
    list_editable = ('description',)  # поле для редактирования превращает в теги.
    # exclude = ('description', 'duration', 'price') # ЭТО НЕ ВЫВОДИМЫЕ ПОЛЯ -EXCLUDE
    # search_fields = ('=title', 'start_date', 'description',) # Поля для поиска - search_fields
    # search_fields = ('=title',)  # = - префикс обозначет точное совпадение при поиске по данному полю регистр символов не учитывается
    search_fields = (
    '^title',)  # ^ - префикс означает что слово в форме должно обязательно присутствовать в начале поля
    # search_fields = ('@title',) # @ - префикс собаки нужен для полнотекстового поиска и поодерживается только СУБД MYSQL
    list_per_page = 3
    actions_on_top = True  # - если в нём установлен TRUE то он выведит все доступные действия для выбора записей.
    actions_on_bottom = True
    actions_selection_counter = True  # Позволяет выводить кол-во записей при выборе.
    save_on_top = True  # Становится сверху форм в джанго на запущенном сервере.
    filter_horizontal = ('authors',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'preview',)
    search_fields = ('name',)
    list_per_page = 3
    actions_on_top = False
    actions_on_bottom = True
    actions_selection_counter = True



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    search_fields = ('content',)
    list_per_page = 100