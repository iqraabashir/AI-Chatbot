from flask import Blueprint, render_template, request, redirect, url_for, session
from chatbot.knowledge_database import (
    get_programmes,
    add_programme,
    delete_programme,
    get_connection,
    get_programme,
    update_programme
)

admin = Blueprint("admin", __name__)

USERNAME = "admin"
PASSWORD = "admin123"


@admin.route("/admin")
def login():
    return render_template("admin/login.html")


@admin.route("/admin/login", methods=["POST"])
def admin_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        session["admin"] = True
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/login.html",
        error="Invalid Username or Password"
    )


@admin.route("/admin/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    return render_template("admin/dashboard.html")


@admin.route("/admin/logout")
def logout():

    session.clear()

    return redirect(url_for("admin.login"))

@admin.route("/admin/programmes/delete/<int:id>")
def delete_programme(id):

    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM academic_programmes WHERE programme_id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin.programmes"))

@admin.route("/admin/programmes")
def programmes():

    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    programmes = get_programmes()

    return render_template(
        "admin/manage_programmes.html",
        programmes=programmes
    )
@admin.route("/admin/programmes/add", methods=["POST"])
def programme_add():

    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    add_programme(

        request.form["programme_name"],
        request.form["programme_level"],
        request.form["college"],
        request.form["department"],
        request.form["duration"],
        request.form["eligibility"],
        request.form["intake"],
        request.form["source"],
        request.form["url"],
        request.form["last_updated"]

    )

    return redirect(url_for("admin.programmes"))

@admin.route("/admin/programmes/delete/<int:programme_id>")
def programme_delete(programme_id):

    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    delete_programme(programme_id)

    return redirect(url_for("admin.programmes"))