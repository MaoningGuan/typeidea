#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target, target_title):
    return {
        'target': target,
        'target_title': target_title,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target)
    }