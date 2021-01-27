The code uses uvicorn to establish a server that listens to post on local host:127.0.0.1 port 8888.
The code uses FASTAPI to parse the JSON file arrived from REST Post. I wanted to build a model from the JSON file but I could not because of the special characters in the JSON file like(wind(%))
I decided to use the simplex method as I beleive it is a LP problem. I took the simplified version from the merit order optimization problem. The idea mainly is the minimize the cost.
I used scipy.LP package.

The send back the package as JSON
I tested the code using Postman. It is up to you decide how to send the POST to the local server

after install uvicorn you can run the following command line:
uvicorn meritOrder:app --reload
A server will be up and looking to receive POST
