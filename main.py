from flask import Flask, render_template, request, url_for, redirect

import data_manager

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/mentors')
def mentors_list():
    mentor_name = request.args.get('mentor-last-name')
    city_name = request.args.get('city-name')
    if mentor_name:
        mentor_details = data_manager.get_mentors_by_last_name(mentor_name)
    elif city_name:
        mentor_details = data_manager.get_city(city_name)
    else:
        mentor_details = data_manager.get_mentors()

    # We get back a list of dictionaries from the data_manager (for details check 'data_manager.py')

    return render_template('mentors.html', mentors=mentor_details, cities=mentor_details)


@app.route('/applicant-phone')
def search_applicant():
    applicant_first_name = request.args.get('applicant-name')
    applicant_last_name = request.args.get('applicant-name')
    email_ending = request.args.get('e-mail_ending')

    if applicant_first_name or applicant_last_name:
        applicant_details = data_manager.get_applicant_data_by_name(
            applicant_first_name, applicant_last_name)

    if email_ending:
        applicant_details = data_manager.get_applicant_data_by_email(
            email_ending)

    return render_template('index.html', applicants=applicant_details)


@app.route("/application", methods=["GET", "POST"])
def applicants_list():
    if request.method == "GET":
        applicants_detail = data_manager.get_applicants()
        return render_template("applicants.html", applicants=applicants_detail)
    else:
        application_code = request.form["code"]
        phone_number = request.form.get("phone_number")
        data_manager.update_phone_number(phone_number, application_code)
        return redirect("/")


@app.route("/application/<application_code>", methods=["GET", "POST"])
def update_application(application_code):
    applicants_detail = data_manager.get_applicants()
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        data_manager.update_phone_number(phone_number, application_code)
        return redirect("/")
    return render_template("applicant_update.html", applicants=applicants_detail, code=application_code)


@app.route('/applicants/add_applicants', methods=["GET", "POST"])
def add_applicants():
    if request.method == "POST":
        first_name = request.form.get("fn")
        last_name = request.form.get("ln")
        phone_number = request.form.get("pn")
        email = request.form.get("em")
        application_code = request.form.get("ac")
        data_manager.adding_new_applicant(
            first_name, last_name, phone_number, email, application_code)
        return redirect('/application')
    return render_template('add_applicants.html')


if __name__ == '__main__':
    app.run(debug=True)
