
 #encoding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# user autentication
from django.contrib.auth.decorators import login_required

@login_required( login_url = '/login/' )
def index( request ):
    return render_to_response( 'main/index.html',{}, context_instance = RequestContext( request ) )
