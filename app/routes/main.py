from flask import Blueprint, render_template, session
import json
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    country_states = {}
    countries = []
    try:
        with open(os.path.join("data", "countries_states.json"), encoding="utf-8") as f:
            data = json.load(f)
            country_states = {item["name"]: item["states"] for item in data}
            countries = list(country_states.keys())
    except Exception as e:
        print("Error loading countries/states:", e)

    return render_template("index.html", countries=countries, states=[], country_states=country_states,
                           verification_valid='license_valid' in session)