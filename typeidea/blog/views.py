""" class-based view """
from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from comment.forms import CommentForm
from comment.models import Comment
from config.models import SideBar
from .models import Post, Tag, Category


# 公共view：获取导航栏和侧边栏的数据
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# 处理首页的HTTP请求view
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()  # 获取数据
    paginate_by = 10  # 每页显示的记录数量
    context_object_name = 'post_list'  # 设置queryset的变量名称，用于在模板中调用
    template_name = 'blog/list.html'  # 渲染使用的模板文件


# category列表页view
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据分类过滤 """
        queryset = super().get_queryset()  # 此处返回IndexView的queryset属性
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)  # 关键字参数：一对一外键category_id


# tag列表页view
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据标签过滤"""
        queryset = super().get_queryset()  # 此处返回IndexView的queryset属性
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)  # 关键字参数：多对多外键要tag__id


# 文章详情页view
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'  # 设置传递到模板文件的变量名称
    pk_url_kwarg = 'post_id'  # 在DetailView中，会根据这个参数来过滤数据，如：post = queryset.filter(pk=post_id)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid  # 获取middleware中设置的用户id
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效，防止统计1分钟内多次刷新的情况
            # print('产生新的pv_key：', pv_key)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效，防止统计一天内多次访问的情况
            # print('产生新的uv_key：', uv_key)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


# 搜索列表页view
class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


# 根据作者过滤的列表页view
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
