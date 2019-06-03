from flask import Flask, render_template, flash, request,url_for, redirect, session
from wtforms import Form, BooleanField, TextField, SelectField, PasswordField, validators
from time import strftime
from flask import jsonify
import json
from passlib.hash import sha256_crypt
# from MySQLdb import escape_string as thwart
import gc
import requests
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'


class RegistrationForm(Form):
    full_name = TextField('Username', [validators.Required])
    email = TextField('email', [validators.Required])
    investor_type = SelectField(choices=[('IND', 'Individual or Joint'), ('IRA', 'IRA Account'), ('ENT', 'Entity and Trust')])
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2019)',
                              [validators.Required])

def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(full_name, email, investor_type):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, full_name={}, email={}, investor_type={} \n'.format(timestamp, full_name, email, investor_type))
    data.close()

@app.route('/')
def hello_world():
    form = RegistrationForm(request.form)

    #print(form.errors)
    if request.method == 'POST':
            full_name=request.form['full_name']
            email=request.form['email']
            investor_type=request.form['investor_type']
    else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)

@app.route('/a', methods=["GET","POST"])
def invest_page():
    try:
        form = RegistrationForm(request.form)
        print('here')

        if request.method == 'POST':
            investor_type = form.investor_type.data
            email = form.email.data
            full_name = form.full_name.data

            url = "https://csduat.sudrania.com/api/formdata/store_investor_dataForm"
            payload = "investor_type="+investor_type+"&full_name="+full_name+"&email="+email+""
                                                                                             # "=lange%40paperstac.com&bank_name=&account_name=&aba_number=&account_number=&fcc_details=&credit_reference=&intermediary_bank=&ib_aba_swift=&fund_id=&fund_name=&asset_type=&subscription_type=&entry_date=&amount=&fund_frequency=&periodic_investment_plan=&periodic_investment_amount=&fund_duration=&investment_duration=&dis_rev_plan=&reinvest="
            headers = {
                'api_key': "qMXXGx0s41Af4n8vfuV00z1aN5pqFMcn",
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'postman-token': "bec3b140-debc-7b7d-1aab-a014223c05dd"
            }

            d = requests.request("POST", url, data=payload, headers=headers)
            # response = d.content.decode('utf8').replace("'", '"')
            # print(response)
            # print('- ' * 20)
            data = json.loads(d.text)
            responsce = data['data']['setUserDetail']
            print(data)
            # s = json.dumps(data, indent=4, sort_keys=True)
            print(d.text)
            # return response.text

        return render_template("index_thankyou.html",form=responsce)

    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()

