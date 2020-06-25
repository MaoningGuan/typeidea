# Create your models here.
import mistune

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import strip_tags


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            # 'categories': normal_categories,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    content_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 用于统计每篇文章的访问量
    pv = models.PositiveIntegerField(default=1, verbose_name='累计访问次数(每名用户统计间隔：1分钟)')
    uv = models.PositiveIntegerField(default=1, verbose_name='累计访问次数(每名用户统计间隔：24小时)')
    # 设置是否使用markdown编辑器
    is_md = models.BooleanField(default=False, verbose_name="切换文本编辑器")

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']  # 根据id进行降序排序

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        # 若摘要没有设置则去正文的前100个字符作为摘要
        if not self.desc:
            print('自动设置摘要。')
            self.desc = strip_tags(self.content_html)[:100]  # strip_tags去掉HTML文本的全部HTML标签
        super().save(*args, **kwargs)

    # 获取id=tag_id标签下的文章
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            # .select_related('category', 'owner')把外键一起获取，防止N+1问题
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('category', 'owner').order_by('-created_time')

        return post_list, tag

    # 获取id=category_id分类下的文章
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            # .select_related('category', 'owner')把外键一起获取，防止N+1问题
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('category', 'owner').order_by('-created_time')

        return post_list, category

    # 获取所有的文章
    @classmethod
    def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('category', 'owner').\
                prefetch_related('tag').order_by('-created_time')
        return queryset

    # 根据每篇文章的访问量来返回文章
    @classmethod
    def hot_posts(cls):
        result = cache.get('hot_posts')
        if not result:
            # 只需要返回id和title用于侧边栏展示
            result = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').only('id', 'title')
            cache.set('hot_posts', result, 10 * 60)
        return result

    # 返回tags绑定到Post实例上，用于sitemap
    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))
