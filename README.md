# Predicting Future Sales Using Time Series Model

In this project, I downloaded a dataset from kaggle which contained the sales of 50 different items (differentiated by numbers 1-50) across 10 different stores (differentiated by numbers 1-10) over the span of five years (Jan. 1, 2013 - Dec. 31, 2017). The data was stored on an AWS Relational Database Service, and a flask app was created which runs the modeling process through a backend pipeline. The reason it has to run the process each time is due to each item-store combination being different from the next, which amounts to 500 total different models. The flask app gives an option of displaying a basic table showing the predicted sales by day and the total, or getting many more columns of data per day such as trend, upper limit, lower limit, etc.

## train.csv
The data is initially stored in this csv file.

## ARIMA and Winter Holts Modeling
The inital modeling I did was pretty much just experimenting with the data. I figured seasonal modeling on item-store combinations would be the best way to go in the end, however in this file I looked at simpler models. The first model filters the data by store, and creates predictions of the sum total for all of the items. The second model filters on store and item, however with no seasonal component. These are both ARIMA models, and there was not enough data to try and create a seasonal model using ARIMA. The next model was a Winter-Holts model (filtered on item-store), and due to the seasonal components, this model far outperformed the first two. After each model there is a graph where the red lines indicate the predictions for sales and the blue represent the actual. At the end I was trying to look for patterns in residuals by month, and seeing if year to year the model was under- or over-predicting the sales in a pattern.

## Facebook Prophet Seasonal Modeling
The first step here is to split up the data into train/test data. This works differently than other models, because the data is ordered by date. So the first two-thirds of the data is taken create the model and the final third is for testing (these proportions can be adjusted). After this, a model with seasonality is created using Facebook Prophet based upon the item-store combination. This model is more indicative of the future sales than any of the other models. Similar to the last file, a graph is shown and the residuals between months was looked at.

## Data to RDS

The data is transferred from the csv file into an AWS Relational Database Service using SQLAlchemy and Postgres. The password is changed due to this code being posted online.

## Get Forecast

Firstly, an engine is created to access the AWS Relational Database Service with the data (once again an incorrect password is displayed). Functions were created to acquire the dataframe for the item-store combination, as well as test it. The testing process involves looking at the root mean squared error among predictions across models that used multiple different proportions for the train/test splits. It checks that the percent error across any combination of two of the models does not exceed 20%. The next functions create the model after taking a few different inputs. The inputs include the store and item numbers (no default values), the number of days in the future for which predictions are wanted (default is 30 days), whether to include just the predictions of sales for each day or to include a number of different outputs including trend, upper limit, lower limit, etc. (default is to only include sales predictions), whether to include a brief summary statement consisting of the store and item number, number of days, total sum of sales predictions over those days, and margin of errors to be expected (default is to include the statement), and whether or not to put the output in a JSON file (default is to have it as a dataframe). These functions are all run through a pipeline, which also runs the aforementioned test (if the test does not pass, a message is shown that warns the user of this while still displaying the outputs). None of the models created triggered the error message.

## Flask

This folder contains the files used to create the web app for an easy interface. The python files are apparent, and the html code used to create the interface is in the templates folder, labeled "index.html". This flask app uses all six variables (described in the Get Forecast file description) to give an output.

## Flask Toned Down

This folder is very similar to the Flask folder described above, however it was toned down for demonstrative purposes. This app only takes into account three of the original six variables (store, item, number of days) and sets the other three as their default values.

## Flask Toned Down Video

This downloadable video demonstrates the use of the toned down Flask app.

## Flask Video JSOn

This downlaodable video demonstrates the use of the Flask app, showing the full output if the extra columns are added and the file is converted to JSON.

## Predicting Sales Presentation

I gave a brief 5-minute presentation on my findings. Tableau was used to create graphs which were demonstrated during the presentation. These are the slides used to discuss the results.
