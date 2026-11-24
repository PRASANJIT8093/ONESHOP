
# Online Shopping Stores API

## Overview

This repository contains an API for online shopping stores, built using **FastAPI**. The API provides essential features for user authentication, order management, and administrative tasks for online shopping platforms or marts.



## Features

### FastAPI Framework
- Developed using FastAPI, a modern and high-performance web framework for building APIs with Python 3.15.

### User Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Endpoint for user login |
| POST | `/logout` | Endpoint for user logout |
| POST | `/forgot-password` | Endpoint for user password recovery |
| POST | `/reset-password` | Endpoint for resetting user password |

### User Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/signup` | Endpoint for user registration |
| GET | `/users/getallusers` | Retrieve all users |
| GET | `/users/getuser/{email}` | Retrieve a user by email |
| GET | `/users/getuserbyid/{user_id}` | Retrieve a user by ID |

### Order Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/createorder` | Create a new order |
| DELETE | `/cancel-order/{order_id}` | Cancel a specific order |
| GET | `/user/order/{user_id}` | Retrieve orders for a specific user |
| GET | `/order/status/{order_id}` | Retrieve the status of a specific order |

### Admin Tasks

| Method | Endpoint | Description |
|---|---|---|
| PUT | `/update-to-admin/{user_id}` | Update a user to admin status |
| GET | `/get-allorders/{admin_id}` | Retrieve all orders for a specific admin |
| PUT | `/order/update/status/{order_id}` | Update the status of a specific order |
| GET | `/getorders-bystatus` | Retrieve orders by status |

### Authentication Mechanisms

- **JWT-Based Authentication:** Used for secure admin logins.

## Installation

To set up and run the API locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/PRASANJIT8093/ONESHOP.git
```

### 2. Navigate to the Project Directory

```bash
cd online-shopping-api
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn main:app --reload
```

The API will be accessible at:

```text
http://127.0.0.1:8000
```

## API Documentation

Explore the detailed API documentation through Swagger UI:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The documentation provides information about available endpoints, request parameters, and response formats.

You can also access the ReDoc documentation at:

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Tech Stack

- **Python** – Programming language
- **FastAPI** – Backend web framework
- **JWT** – Admin authentication
- **Uvicorn** – ASGI server

## Contact

For any inquiries or support, please contact:

**Email:** prasanjitbehuria1999@gmail.com

---

**Happy Coding!**
