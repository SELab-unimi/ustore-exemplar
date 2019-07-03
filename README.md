# U-Store Exemplar

U-Store is a web-based e-commerce application. It is composed of a number of services that implement specialized pieces of functionalities and talk to each other using HTTP resource APIs.
The table below lists the services of the U-Store and provides a brief description of each one of them.

|  Service  |                                                   Description                                                  |
|:---------:|:--------------------------------------------------------------------------------------------------------------:|
|  frontend |                Exposes an HTTP server to serve the website. Generates session IDs for all users.               |
|    user   |                    Provide Customer login, sign up, as well as user's information retrieval.                   |
|    cart   |          Stores selected items in the user's shipping cart (into persistent memory) and retrieves it.          |
| catalogue | Provides the list of products from a SQL database, the ability to search products, and get individual products |
|  shipping |        Gives shipping cost estimates based on the shopping cart and the given address (mock component).        |
|  payment  |     Charges the given credit card info (mock component) with the given amount and returns a transaction ID.    |

Services can be configured with artificial abnormal conditions (due to sources of uncertainty).
Namely, services can be configured to simulate service degradation by means of **failure rates** (`ecomm_configfail` DB table) and **random delays** (`ecomm_timerate` DB table).

## How do I get started?

- Download `Python 3.7` (that includes `PIP`); open a shell and execute the following command: `pip install django`

- Download and install a DBMS for SQLite (e.g., SQLite Studio)

**Launch the U-Store web app**

- `cd` into `ecommerce` directory

- Open a shell and execute the Python program: `manage.py runserver` (the default server address is `127.0.0.1:8000`). Alternatively, you can specify another server address as second parameter using the syntax `IP:port`; note that the IP must to be addedd to the the list of allowed host in the `setting.py`

- Open in a browser the index page of the U-Store: http://127.0.0.1:8000/index.html
