from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import *
import json
from datetime import datetime, date

User = get_user_model()

# Rest of your views code remains the same...
