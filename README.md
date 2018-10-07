# Fast-Food-Fast [![Build Status](https://travis-ci.org/joelethan/Fast-Food-Fast.svg?branch=CI-travis)](https://travis-ci.org/joelethan/Fast-Food-Fast) [![Maintainability](https://api.codeclimate.com/v1/badges/0d7befbf06875d2ca626/maintainability)](https://codeclimate.com/github/joelethan/Fast-Food-Fast/maintainability) [![Coverage Status](https://coveralls.io/repos/github/joelethan/Fast-Food-Fast/badge.svg?branch=CI-travis)](https://coveralls.io/github/joelethan/Fast-Food-Fast?branch=CI-travis)
Fast-Food-Fast is a food delivery service app for a restaurant.

## Getting Started

 Clone the repository https://github.com/joelethan/Fast-Food-Fast

## Requirements

- Have Python 3 installed
- Have a virtual environmrnt installed to separate the project's packages from the computer's packages
- Have Postman installed to test the API endpoints

## Installation
A step by step guide on how to setup and run the application. 

 Clone the application by running the command in terminal or command line prompt
```
git clone https://github.com/joelethan/Fast-Food-Fast.git
```
 Change directory into the project's root by running
```
cd Fast-Food-Fast
```

 Create a virtual environment and activate it
```
virtualenv venv
```
```
.\venv\Scripts\activate
```

 Install project packages
```
pip install -r requirements.txt
```

 Check if packages are installed
```
pip freeze
```

Expected output
```
astroid==2.0.4
atomicwrites==1.2.1
Jinja2==2.10
..............
..............
..............
urllib3==1.23
Werkzeug==0.14.1
wrapt==1.10.11
```

 Checkout the `api` branch
```
git checkout Chal3
```

 Run the API
```
python run.py
```

 Expected ouput
```
 * Serving Flask app "app.views" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 294-773-545
 * Running on http://127.0.0.1:5003/ (Press CTRL+C to quit)
```
## Functionalities with their endpoints

| FEATURE | METHOD | END POINT|
| --- | --- |--- |
| Index page | GET | / 
|Register a user | POST | auth/signup |
| Login a user | POST | auth/login |
| Place an order | POST | users/orders|
| Get order history of a user | GET | api/orders/hist/user_id |
| Get all orders | GET | api/orders |
| Get a specific order | GET| api/orders/order_id |
| Update an order status | PUT | api/orders/order_id |
| Get all food items on the menu| GET | api/menu |
| Add a meal to the menu | POST| api/menu |

## Project link
Heroku: https://joelbootcampwk2.herokuapp.com/

## Author

Katusiime Joel Ian
