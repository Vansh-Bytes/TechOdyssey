## Introduction

TechOdyssey is the annual technical fest organized by the Computer Society of India at K.R. Mangalam University. It serves as a platform for upcoming tech enthusiasts to showcase their skills and compete with peers in various events such as web development, competitive coding, e-sports, treasure hunts, quizzes, and more.

This repository contains the application code for the TechOdyssey event registration and management system. The application is built using Flask, MongoDB, and integrates with social login providers like Google and GitHub.

## Table of Contents

- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Features](#features)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Contact](#contact)

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- pip (Python package installer)
- MongoDB
- Redis

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/tech-odyssey.git
    cd tech-odyssey
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables. Create a `.env` file in the project root and add the following variables:

    ```sh
    SECRET_KEY=<your-secret-key>
    MONGODB_URI=<your-mongodb-uri>
    REDIS_URI=<your-redis-uri>
    GOOGLE_CLIENT_ID=<your-google-client-id>
    GOOGLE_CLIENT_SECRET=<your-google-client-secret>
    ```

## Usage

### Running the Application

1. Ensure MongoDB and Redis servers are running.
2. Start the Flask application:

    ```sh
    python app.py
    ```

3. Open a browser and navigate to `http://localhost:5000` to access the application.

## Features

- **User Authentication:** Users can sign in using Google or GitHub.
- **Event Registration:** Users can register for various events. Team events require additional information such as team name and members.
- **Admin Dashboard:** Admins can view statistics, approve or reject registrations, and export data.
- **Payment Integration:** Users can upload payment screenshots for verification.

## Environment Variables

- `SECRET_KEY`: A secret key for the Flask application.
- `MONGODB_URI`: The URI for connecting to MongoDB.
- `REDIS_URI`: The URI for connecting to Redis.
- `GOOGLE_CLIENT_ID`: The client ID for Google OAuth.
- `GOOGLE_CLIENT_SECRET`: The client secret for Google OAuth.

## Project Structure

```
tech-odyssey/
│
├── templates/                 # HTML templates
│   ├── public/
│   ├── user/
│   ├── auth/
│   └── admin/
│   └── events/
│   └── private/
│
├── static/                    # Static files (CSS, JS, images)
│
├── .env                       # Environment variables file
├── app.py                     # Main Flask application
├── requirements.txt           # Python packages required
├── README.md                  # Project README file
└── ...
```

## Contact

For any queries or further information regarding the project, feel free to contact the developers:

- Om Mishra: [contact@om-mishra.com](mailto:contact@om-mishra.com)

For more information about the event, visit the [TechOdyssey website](https://techodyssey.dev).
