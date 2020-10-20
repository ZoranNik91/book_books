from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
import mysql.connector as MC
import sys
from passlib.hash import sha256_crypt
from datetime import time
from datetime import datetime #datetime is type of -> class <- datetime
import json

passw = input("Unesi:")

pass_data = "123456"
pass_data = sha256_crypt.encrypt(str(passw))

print(sha256_crypt.verify(passw, pass_data))
