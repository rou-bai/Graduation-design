__author__ = 'apple'
from flask import Flask, jsonify, render_template, redirect, url_for, request, send_file
from  json import  *
import  os
from . import app



# REST API: /WSPrinter/api/v1.0/printers

baseURL = app.config['API_BASE_URL']

