#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()

TILE_STYLES = {
    "raw": "danger",
    "measured": "yellow",
    "loaded": "success"}


@register.filter(name='tile_style')
def tile_style(tile):
    return TILE_STYLES.get(tile.status, "info")


@register.filter('pages_for_paginator')
def pages_for_paginator(page):
    if page.page_count == 0:
        return []
    elif page.page_count <= 21:
        return range(1, page.page_count +1)

    lowers = [idx for idx in range(page.page-10, page.page) if idx > 0]
    ups = [
        idx for idx in range(page.page + 1, page.page + 11)
        if idx <= page.last_page]

    if len(lowers) < 10:
        start = ups[-1] + 1
        end = start + 10 - len(lowers)
        extra_ups = [
            idx for idx in range(start, end) if idx <= page.last_page]
        ups = ups + extra_ups
    elif len(ups) < 10:
        end = lowers[0]
        start = lowers[0] - 10 + len(ups)
        extra_lowers = [
            idx for idx in range(start, end) if idx > 0]
        lowers = extra_lowers + lowers
    return lowers + [page.page] + ups


@register.filter('counter_in_page')
def counter_in_page(cnt , page):
    if page.page == 1:
        return cnt
    return cnt + page.items_per_page * (page.page - 1)
