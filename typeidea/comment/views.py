from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        target_title = request.POST.get('target_title')

        if comment_form.is_valid():
            print(comment_form['content'])
            instance = comment_form.save(commit=False)  # 在此处会执行forms中的clean函数
            print(instance.content)
            instance.target = target
            instance.target_title = target_title
            instance.save()
            succeed = True
            return redirect(target)  # 评论成功，返回原评论页面
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target
        }
        return self.render_to_response(context)  # 提交数据失败，则渲染返回评论结果页comment/result.html。
