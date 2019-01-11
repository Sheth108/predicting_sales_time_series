from flask import Flask, request, render_template
from return_forecast import forecast
import pandas
import json

# create a flask object
app = Flask(__name__)

# creates an association between the / page and the entry_page function (defaults to GET)
@app.route('/')
def entry_page():
    return render_template('index.html')

# creates an association between the /predict_sales page and the render_message function
# (includes POST requests which allow users to enter in data via form)
@app.route('/predict_sales/', methods=['GET', 'POST'])
def render_message():

    # user-entered features
    features = ['storeNum', 'itemNum', 'numDays']

    # error messages to ensure correct inputs
    messages = ["The store number must be an integer between 1 and 10.",
                "The item number must be an integer between 1 and 50.",
                "The number of days must be an integer greater than 0.",
                ]

    # hold all amounts
    amounts = []

    # takes user input and puts it in amounts
    for i, ing in enumerate(features):
        user_input = request.form[ing]
        amounts.append(user_input)
    for index, amount in enumerate(amounts):
        if amount == 'True':
            amounts[index] = True
        if amount == 'False':
            amounts[index] = False
   
    # show user result
    final_forecast, summary = forecast(amounts)
    # if amounts[5] == True:
    #     final_forecast = json.loads(final_forecast)
    #     return render_template('index.html', message=summary, forecast=final_forecast, noInfo=1)
    #else:
       # final_forecast.index = final_forecast.index.dt.strftime('%m/%d/%Y')

    #if amounts[3] == False:
    #return render_template('index.html', message=summary, forecast=final_forecast, pd=1)
    # else:
    final_forecast = final_forecast.to_html()
    return render_template('index.html', message=summary, forecast=final_forecast, info=1)


if __name__ == '__main__':
    app.run(debug=True)