from flask import Flask, render_template, request, redirect, session
from locker.firebase_service import get_user_by_mobile

app = Flask(__name__)
app.secret_key = "mock_digilocker_secret"


# ---------------- PROJECT ENTRY ----------------

@app.route("/")
def home():
    return render_template("project.html")


# ---------------- DIGILOCKER LOGIN ----------------

@app.route("/digilocker/login", methods=["GET", "POST"])
def digilocker_login():
    error = None
    if request.method == "POST":
        mobile = request.form["mobile"]

        user = get_user_by_mobile(mobile)
        if user:
            session["dl_mobile"] = mobile
            session["dl_user"] = user
            return redirect("/digilocker/issued")
        else:
            error = "Mobile number not found in DigiLocker"

    return render_template("login.html", error=error)


# ---------------- ISSUED DOCUMENTS (FROM FIREBASE) ----------------

@app.route("/digilocker/issued", methods=["GET", "POST"])
def digilocker_issued():
    user = session.get("dl_user")
    if not user:
        return redirect("/")

    if request.method == "POST":
        selected = request.form.getlist("selected_docs")
        session["selected_docs"] = selected
        return redirect("/digilocker/consent")

    return render_template(
        "issued.html",
        documents=user["documents"]
    )


# ---------------- CONSENT ----------------

@app.route("/digilocker/consent", methods=["GET", "POST"])
def digilocker_consent():
    user = session.get("dl_user")
    if not user:
        return redirect("/")

    selected_uris = session.get("selected_docs", [])
    selected_docs = [
        d for d in user["documents"]
        if d["uri"] in selected_uris
    ]

    if request.method == "POST":
        if request.form["consent"] == "yes":
            # 🔥 DIRECTLY SEND TO MAIN PROJECT
            session["verified_docs"] = selected_docs
            session["verified_user"] = user["name"]
            return redirect("/project/receive-digilocker")

        session.clear()
        return redirect("/")

    return render_template(
        "consent.html",
        documents=selected_docs
    )


# ---------------- MAIN PROJECT RECEIVES DATA ----------------

@app.route("/project/receive-digilocker")
def receive_digilocker():
    name = session.get("verified_user")
    documents = session.get("verified_docs", [])

    # ❌ NO SUCCESS PAGE
    # ✔ Directly used in project
    return render_template(
        "project_dashboard.html",
        name=name,
        documents=documents
    )


if __name__ == "__main__":
    app.run(debug=True)
