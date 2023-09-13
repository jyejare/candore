from flask import Flask, render_template

app = Flask(__name__)


# Define a route to display the JSON data in a table
@app.route('/')
def display_json_table(results_json=None):
    # Fetch JSON data from your module (replace with your data source)

    return render_template('table.html', data=results_json)


def render_webpage():
    app.run(debug=True)
