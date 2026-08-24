from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
from dotenv import load_dotenv
from chatbot.knowledge_database import (
    get_programmes,
    add_programme,
    delete_programme,
    get_programme,
    update_programme,
)
load_dotenv()

admin = Blueprint("admin", __name__)

USERNAME = os.getenv("ADMIN_USERNAME")
PASSWORD = os.getenv("ADMIN_PASSWORD")

@admin.route("/admin")
def login():

    return render_template(
        "admin/login.html"
    )


@admin.route("/admin/login", methods=["POST"])
def admin_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:

        session["admin"] = True

        return redirect(
            url_for("admin.dashboard")
        )

    return render_template(
        "admin/login.html",
        error="Invalid Username or Password"
    )

@admin.route("/admin/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(
            url_for("admin.login")
        )
    return render_template(
        "admin/dashboard.html"
    )

@admin.route("/admin/logout")
def logout():
    session.clear()
    return redirect(
        url_for("admin.login")
    )

@admin.route("/admin/programmes")
def programmes():
    if not session.get("admin"):
        return redirect(
            url_for("admin.login")
        )
    programmes = get_programmes()

    return render_template(
        "admin/manage_programmes.html",
        programmes=programmes
    )


@admin.route(
    "/admin/programmes/add",
    methods=["POST"]
)
def programme_add():
    if not session.get("admin"):
        return redirect(
            url_for("admin.login")
        )
    add_programme(
        request.form["programme"],
        request.form.get(
            "specialization",
            ""
        ),

        request.form.get(
            "level",
            ""
        ),

        request.form.get(
            "college",
            ""
        ),

        request.form.get(
            "department",
            ""
        ),

        request.form.get(
            "duration",
            ""
        ),

        request.form.get(
            "programme_type",
            ""
        ),

        request.form.get(
            "school",
            ""
        ),

        request.form.get(
            "campus",
            ""
        ),

        request.form.get(
            "eligibility",
            ""
        ),

        request.form.get(
            "intake",
            ""
        ),

        request.form.get(
            "fee",
            ""
        ),

        request.form.get(
            "admission_process",
            ""
        ),

        request.form.get(
            "selection_process",
            ""
        ),

        request.form.get(
            "overview",
            ""
        ),

        request.form.get(
            "subject_overview",
            ""
        ),

        request.form.get(
            "source",
            ""
        ),

        request.form.get(
            "url",
            ""
        ),

        request.form.get(
            "last_updated",
            ""
        )
    )
    flash("Programme added successfully.", "success")
    return redirect(
        url_for("admin.programmes")
    )

@admin.route(
    "/admin/programmes/delete/<int:programme_id>"
)
def programme_delete(programme_id):
    if not session.get("admin"):
        return redirect(
            url_for("admin.login")
        )
    delete_programme(
        programme_id
    )
    flash("Programme deleted successfully.", "success")
    return redirect(
        url_for("admin.programmes")
    )
@admin.route(
    "/admin/programmes/edit/<int:programme_id>"
)
def programme_edit(programme_id):

    if not session.get("admin"):
        return redirect(
            url_for("admin.login")
        )

    programme = get_programme(
        programme_id
    )

    if not programme:
        flash(
            "Programme not found.",
            "error"
        )

        return redirect(
            url_for("admin.programmes")
        )

    return render_template(
        "admin/edit_programme.html",
        programme=programme
    )


@admin.route(
    "/admin/programmes/update/<int:programme_id>",
    methods=["POST"]
)
def programme_update(programme_id):

    if not session.get("admin"):
        return redirect(
            url_for("admin.login")
        )

    update_programme(
        programme_id,

        request.form["programme"],

        request.form.get(
            "specialization",
            ""
        ),

        request.form.get(
            "level",
            ""
        ),

        request.form.get(
            "college",
            ""
        ),

        request.form.get(
            "department",
            ""
        ),

        request.form.get(
            "duration",
            ""
        ),

        request.form.get(
            "programme_type",
            ""
        ),

        request.form.get(
            "school",
            ""
        ),

        request.form.get(
            "campus",
            ""
        ),

        request.form.get(
            "eligibility",
            ""
        ),

        request.form.get(
            "intake",
            ""
        ),

        request.form.get(
            "fee",
            ""
        ),

        request.form.get(
            "admission_process",
            ""
        ),

        request.form.get(
            "selection_process",
            ""
        ),

        request.form.get(
            "overview",
            ""
        ),

        request.form.get(
            "subject_overview",
            ""
        ),

        request.form.get(
            "source",
            ""
        ),

        request.form.get(
            "url",
            ""
        ),

        request.form.get(
            "last_updated",
            ""
        )
    )
    flash(
        "Programme updated successfully.",
        "success"
    )
    return redirect(
        url_for("admin.programmes")
    )

