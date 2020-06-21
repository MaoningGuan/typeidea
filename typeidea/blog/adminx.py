import xadmin
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from xadmin.layout import Row, Fieldset, Container

from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .adminforms import PostAdminForm
from .models import Post, Category, Tag
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


# 在分类列表页面增加编辑文章的功能: 定义文章的Inline
class PostInline(admin.TabularInline):  # StackedInline样式不同
    # 要显示编辑的字段, 其中Post的category字段不需要设置，它默认的值就是当前编辑的分类。
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 0  # 控制额外多几个空白记录
    model = Post


# Register your models here.
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # 添加文章的Inline,
    # inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    # 展示该分类下有多少文章
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # def save_formset(self, request, form, formset, change):
    #     """ 修改关联对象Post的数据 """
    #     instances = formset.save(commit=False)
    #     for instance in instances:
    #         if not hasattr(instance, 'owner'):  # 防止误修改其他文章的作者
    #             instance.owner = request.user  # 给Post的owner字段赋值
    #             instance.save()
    #     formset.save_m2m()


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time', 'post_count')
    fields = ('name', 'status')

    # 展示该标签下有多少文章
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


# class CategoryOwnerFilter(admin.SimpleListFilter):
#     """ 自定义过滤器只展示当前用户的分类 """
#     title = '分类过滤器'
#     parameter_name = 'owner_category'
#
#     def lookups(self, request, model_admin):
#         # 返回根据用户展示的过滤器分类列表
#         return Category.objects.filter(owner=request.user).values_list('id', 'name')
#
#     def queryset(self, request, queryset):
#         category_id = self.value()
#         if category_id:
#             return queryset.filter(category_id=category_id)  # 返回根据分类查询的数据
#         return queryset
class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm  # 调整文章摘要的输出框为textarea
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator', 'pv', 'uv'
    ]
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True  # 后台的文章列表页执行等动作是否在上面显示
    actions_on_bottom = True  # 后台的文章列表页执行等动作是否在下面显示
    save_on_top = True  # 保存、删除等按钮是否在顶部显示

    # 编辑页面
    exclude = ('owner',)  # 设置不显示哪些字段

    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    filter_horizontal = ('tag',)  # 设置编辑页标签的显示方式

    # filter_vertical = ('tag',)

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css")
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js')

    # @property
    # def media(self):
    #     # xadmin基于Bootstrap，引入会导致页面样式冲突, 仅供参考, 故注释。
    #     media = super().media
    #     media.add_js(
    #         ['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js']
    #     )
    #     media.add_css({
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     })

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

# 展示操作日志
# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(object):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
