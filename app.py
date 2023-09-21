import base64
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from utils import take_screenshot_from_url
from pygments.styles import get_all_styles
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer

app = Flask(__name__)
app.secret_key = "31441f4c0bb38f72fbbaf209d229df5041055d55f1a82c3d2eb054f607680332"

placeholderCode = "print('Hello, World!')"
defaultStyle = "monokai"
no_code_fallback = "# No Code Was Entered 🥲"

@app.route("/", methods=["GET"])
def code():
    """Renders a template that takes in code that is to be written in different styles"""
    if session.get("code") is None: # Check if the session already contains code, if not, then session["code"] is set to placeholder code
        session["code"] = placeholderCode
    lines = session["code"].split("\n")
    context = {
        "message": "Paste Your Python Code 🐍",
        "code": session["code"],                # Update the value of "code" to work with session's code in the template
        "num_lines": len(lines),                # Determines the number of lines needed in the code box
        "max_chars": len(max(lines, key=len)),  # Determines the max number of characters needed for a single line
    }
    return render_template("code_input.html", **context)

@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code") or no_code_fallback  # Set the session's code to either the written code, or the fallback code for when no code is written
    return redirect(url_for("code"))

@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = placeholderCode
    return redirect(url_for("code"))

@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = defaultStyle
    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": "Select Your Style 🧑‍🎨",
        "all_styles": list(get_all_styles()),
        "style": session["style"],
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(
            session["code"], Python3Lexer(), formatter
        ),
    }
    return render_template("style_selection.html", **context)

@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None:
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code") or no_code_fallback
    
    return redirect(url_for("style"))

@app.route("/image", methods=["GET"])
def image():
    # Define a session_data dictionary that contains all the info that playwright's browser context needs to simulate session
    session_data = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }
    target_url = request.host_url + url_for("style")    # Set the target_url to style selection page
    image_bytes = take_screenshot_from_url(target_url, session_data)    # Gte the image as bytes
    context = {
        "message": "Done! 🥳",
        "image_b64": base64.b64encode(image_bytes).decode("utf-8"), # Base64-encode the binary image data, this base64 string will represent the image buffer in string format
    }
    return render_template("image.html", **context)



