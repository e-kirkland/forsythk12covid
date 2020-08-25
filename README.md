# COVID-19 DASHBOARD - FORSYTH COUNTY PUBLIC SCHOOLS
This simple web app tracks positive cases reported by the Forsyth County Public School System.

## Data
Data for the tracker is scraped from the [Forsyth County School Board website](https://www.forsyth.k12.ga.us/Page/52982). Each week, a new link is posted with an html table of schools and positive cases per day. The tracker scrapes this data, aggregates it, and transforms it into a useable pandas DataFrame.

Data is updated regularly by Forsyth County schools, at approximately 6pm each school day. The dashboard refreshes automatically with each update. 

## Visualization
The data is visualized using plotly, plotly-express and plotly-dash.

## Dependencies
The app is written in Python, using several key libraries:
* Requests/BeautifulSoup
* Pandas
* Plotly
* Plotly-Express
* Dash/Flask

A full list of dependencies can be found in the requirements.txt file.

## Contact
For more information, recommendations, or requests, please visit [KDSolutions.co](http://KDSolutions.co) or email [eddie@kdsolutions.co](mailto:eddie@kdsolutions.co).
