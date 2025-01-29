import base64
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User
import pickle
import requests
import xml.etree.ElementTree as ET

from .froms import RegisterForm
from .models import Post, UserPost


def index(request):
    posts = Post.objects.all()
    return render(request, "index.html", {"posts": posts})

# 1. SQL Injection - Directly injecting SQL via user input
# TODO: MAKE IT SQL Injection vulnerability
def search(request):
    query = request.GET.get('q', '')
    results = []
    if request.method == "POST":
        sql = f"SELECT * FROM ethicalHacking_post WHERE title LIKE '%{query}%'"
        print(f"Executing SQL: {sql}")
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
    return render(request, "search.html", {"query": query, "results": results})


# 2. XSS - Rendering user input directly in templates
# http://127.0.0.1:8000/comment?comment="<script>alert('XSS')</script>"
def comment(request):
    comment = request.GET.get("comment", "")
    return HttpResponse(f"User Comment: {comment}")


# 3. Broken Authentication - Storing plain-text passwords
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]  # ⚠ Storing in plain text (INSECURE)

            # Directly storing the plain-text password (BAD PRACTICE)
            user = UserPost(username=username)
            user.password = password  # No hashing!
            user.save()

            return HttpResponse("User registered successfully (INSECURE)")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# 4. Insecure Deserialization - Using `pickle.loads()` on user input
# http://127.0.0.1:8000/deserialize/?data=gASVHAAAAAAAAACMAm50lIwGc3lzdGVtlJOUjARjYWxjlIWUUpQu
def deserialize_data(request):
    data = request.GET.get('data')
    try:
        # Decode the Base64 string into bytes
        decoded_data = base64.b64decode(data)

        # Unpickle the decoded data
        obj = pickle.loads(decoded_data)

        return HttpResponse(f"Deserialized object: {obj}")

    except Exception as e:
        # Handle errors
        return HttpResponse(f"Error deserializing data: {str(e)}", status=500)


# 5. Security Misconfiguration - DEBUG mode and open ALLOWED_HOSTS
# (No direct function, but exists in settings.py)


# 6. CSRF - Disabling CSRF protection
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def transfer_money(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        # Add logic to handle the transfer of the specified amount
        return HttpResponse(f"Transferred {amount} successfully!")
    return render(request, "transfer.html")


# 7. SSRF - Allowing user-supplied URLs without validation
# example http://127.0.0.1:8000/fetch_data?url=http://example.org
def fetch_data(request):
    url = request.GET.get("url")
    response = requests.get(url)  # Attacker can fetch internal resources
    return HttpResponse(f"Fetched data from {url}: {response.text}")


# 8. Insufficient Logging & Monitoring - No logging for failed logins
def login_attempt(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if not authenticate(username=username, password=password):
        return render(request, "login.html", {"error": "Login failed"})  # No logs, making attacks harder to trace
    return HttpResponse("Login successful")


# 9. XXE - Processing untrusted XML input
@csrf_exempt
def parse_xml(request):
    if request.method == 'POST':
        xml_data = request.POST.get('xml')
        if not xml_data:
            return render(request, 'parse_xml.html', {'error': 'No XML data provided!'})
        try:
            root = ET.fromstring(xml_data)
            # Process the XML data as needed
            extracted_data = ET.tostring(root, encoding='UTF-8').decode('UTF-8')
            return render(request, 'parse_xml.html', {'message': 'XML parsed successfully!', 'xml_data': extracted_data})
        except ET.ParseError:
            return render(request, 'parse_xml.html', {'error': 'Invalid XML data!'})
    return render(request, 'parse_xml.html')


# 10. Broken Access Control - Allowing users to access profiles by changing ID
# example http://127.0.0.1:8000/profile/user_id/
def view_profile(request, user_id):
    user = User.objects.get(id=user_id)  # No authorization check
    return HttpResponse(f"User: {user.username}")
