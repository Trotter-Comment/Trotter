import os
import importlib

from flask import Flask

app = Flask(__name__)

from .views import *
