from django.shortcuts import render
from shaker.shaker_core import *
import os

def highstate(request):

    return render(request,'states_config/highstate.html', )
