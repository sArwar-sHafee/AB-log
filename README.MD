# Blog Application

This is a simple blog application built with Flask and SQLite. The app allows users to register, log in, create posts (with Markdown support and multiple images), like posts, and delete their own posts. It also features a dark/light theme toggle with an attractive UI.

## Features

- **User Authentication:**  
  Register, log in, and log out.
- **Post Creation:**  
  Create posts using Markdown and upload multiple images.
- **Post Interaction:**  
  Like posts and delete your own posts.
- **Theming:**  
  Dark mode by default with a toggle (using an image button) to switch to light mode.
- **Responsive UI:**  
  Modern, attractive design with header adjustments.

## Project Structure

```
AB-log/
├── app.py                   # Main Flask application
├── posts.db                 # SQLite database (auto-created)
├── requirements.txt         # List of dependencies
├── README.md                # Project documentation
├── static/                  # Static files (CSS, JS, Images)
│   ├── style.css            # Custom styles for the website
│   ├── script.js            # JavaScript for theme toggling and interactivity
│   └── theme.png            # Image used for the theme toggle button
└── templates/               # HTML templates for rendering pages
    ├── base.html            # Base template (header, navigation, and layout)
    ├── index.html           # Home page (displays all posts)
    ├── create.html          # Create new post page
    ├── login.html           # Login page
    ├── register.html        # Registration page
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/flask-blog.git
    cd flask-blog
    ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate
    ```
    
3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    
4. **Run the Application:**

    ```bash
    python app.py
    ```

The application will be available at http://127.0.0.1:5000/

---

### Deployment

This application can be deployed on free hosting services like GitHub Pages, PythonAnywhere, or Render.

you will get it :

<https://shafeeblog.pythonanywhere.com/>

### License

This project is open-source and free to use.

### Author

Sarwar Shafee

[*Quazi Sarwar Muhtaseem*](https://github.com/sArwar-sHafee/)