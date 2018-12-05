#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from paginate_sqlalchemy import SqlalchemyOrmPage

from corral import db

from carpyncho import cql, models as cmodels

from webproject import models
from webproject.forms import ProfileForm, UserCreateEmailForm
from webproject.libs.echo import Echo


# =============================================================================
# CONSTANTS
# =============================================================================

ITEMS_PER_PAGE = 1000


# =============================================================================
# ROUTES
# =============================================================================

def about(request):
    return render(request, 'webproject/about.html')


@user_passes_test(lambda u: u.is_anonymous(), "/")
def request_user(request):
    if request.method == "POST":
        user_form = UserCreateEmailForm(request.POST, prefix="user")
        profile_form = ProfileForm(request.POST, prefix="profile")
        valids = [user_form.is_valid(), profile_form.is_valid()]
        if all(valids):
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('user_created')
    else:
        user_form = UserCreateEmailForm(prefix="user")
        profile_form = ProfileForm(prefix="profile")
    ctx = {"user_form": user_form, "profile_form": profile_form}
    return render(request, 'registration/request_user.html', ctx)


@user_passes_test(lambda u: u.is_anonymous(), "/")
def user_created(request):
    return render(request, 'registration/user_created.html')


@login_required
def password_change(request):
    if request.method == "POST":
        next_page = request.POST.get("next", "/")
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed.')
            return redirect(next_page)
    else:
        next_page = request.GET.get("next", "/")
        form = PasswordChangeForm(user=request.user)
    ctx = {"form": form, "next": next_page}
    return render(request, 'registration/password_change.html', ctx)



@login_required
def index(request):
    session = request.corral_session
    tiles = session.query(cmodels.Tile).order_by(
        cmodels.Tile.status.desc(), cmodels.Tile.id)
    ctx = {"tiles": tiles}
    return render(request, 'webproject/index.html', ctx)


@login_required
def cql_view(request):
    if "ast" not in request.GET:
        messages.error(request, 'No CQL Found')
        return redirect("carpyncho:index")

    user = request.user

    session = request.corral_session

    page = request.GET.get("page", 1)

    # REGISTER THE QUERY
    ast = models.CQLAst.get_register(request.GET["ast"])
    cql_query = models.CQLQuery.get_register(request.GET["cql"], ast, user)

    # THE QUERY ITSELF
    result = cql.eval(ast.ast, session)

    if isinstance(result, cql.Writer):
        ext = result.fmt()
        filename = "carpyncho_{}.{}".format(timezone.now().isoformat(), ext)
        content_type = "text/{}".format(ext)
        stream = result.stream(Echo())
        response = StreamingHttpResponse(stream, content_type=content_type)
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(
            filename)
        return response

    sources_query, columns = result

    items_per_page = ast.ast["options"].get("limit")
    if items_per_page is None or items_per_page >= ITEMS_PER_PAGE:
        items_per_page = ITEMS_PER_PAGE

    sources = SqlalchemyOrmPage(
        sources_query, page, items_per_page=items_per_page)

    page = 1 if sources.page_count < page else page

    ctx = {
        "sources": sources, "columns": columns,
        "cql": cql_query.query, "page": page}

    return render(request, 'webproject/cql.html', ctx)
