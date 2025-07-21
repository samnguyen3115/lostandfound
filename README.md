<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/samnguyen3115/lostandfound">
    <img src="app/static/img/lostandfound.ico" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Lost & Found Portal</h3>

  <p align="center">
    A comprehensive Flask web application for managing lost and found items on campus
    <br />
    <a href="https://github.com/samnguyen3115/lostandfound"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/samnguyen3115/lostandfound">View Demo</a>
    ·
    <a href="https://github.com/samnguyen3115/lostandfound/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/samnguyen3115/lostandfound/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#key-features">Key Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#database-setup">Database Setup</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#api-endpoints">API Endpoints</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The Lost & Found Portal is a comprehensive web application designed to help campus communities manage lost and found items efficiently. Built with Flask and modern web technologies, it provides a user-friendly interface for posting lost items, browsing found items, and connecting finders with owners.

**Student Information:**
- **Name:** Tran Minh Duc Nguyen
- **Major:** Computer Science

### Key Features

* **User Authentication** - Secure registration and login system
* **Item Posting** - Post lost items with descriptions, images, and location tags
* **Smart Filtering** - Filter items by color, building location, and status
* **Interactive Campus Map** - Visual building locations with detailed information  
* **Contact System** - Secure messaging between finders and owners
* **Email Notifications** - Automated notifications when items are potentially found
* **Status Tracking** - Mark items as lost, found, or closed
* **Image Upload** - Support for item photos with automatic resizing
* **Pagination** - Efficient browsing of large item collections
* **RESTful API** - JSON endpoints for mobile and external integrations
* **Responsive Design** - Mobile-friendly interface using Bootstrap

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Flask][Flask.py]][Flask-url]
* [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![SQLAlchemy][SQLAlchemy.com]][SQLAlchemy-url]
* [![JavaScript][JavaScript.com]][JavaScript-url]
* [![HTML5][HTML5.com]][HTML5-url]
* [![CSS3][CSS3.com]][CSS3-url]
* [![Python][Python.com]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.8 or higher
* PostgreSQL 12 or higher
* pip (Python package manager)

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/samnguyen3115/lostandfound.git
   cd lostandfound
   ```

2. Create and activate virtual environment
   ```sh
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux  
   source .venv/bin/activate
   ```

3. Install required packages
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```sh
   # Copy template and edit with your values
   copy .env.example .env
   ```

5. Configure your `.env` file
   ```env
   SECRET_KEY=your-super-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost:5432/lostandfound_db
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

### Database Setup

1. Create PostgreSQL database
   ```sql
   CREATE DATABASE lostandfound_db;
   ```

2. Initialize database migrations
   ```sh
   flask db init
   flask db migrate -m "Initial migration"  
   flask db upgrade
   ```

3. Populate with default data
   ```sh
   python init_database.py
   ```

4. Run the application
   ```sh
   python lostandfound.py
   ```

The application will be available at `http://localhost:5000`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### For Students Looking for Lost Items

1. **Register/Login** - Create an account or sign in
2. **Browse Items** - View all posted lost items on the main page
3. **Filter Results** - Use color and building filters to narrow search
4. **Contact Owner** - If you found an item, use the contact system
5. **Interactive Map** - Explore campus buildings for location context

### For Students Who Lost Items

1. **Post Your Item** - Create a detailed post with description and photo
2. **Add Tags** - Specify color and building location
3. **Monitor Status** - Check for contact messages from potential finders
4. **Mark as Found** - Update status when your item is recovered

### Administrative Features

- **User Management** - View and manage user accounts
- **Building Database** - Campus building information and locations
- **Email System** - Automated notifications for important events
- **API Access** - RESTful endpoints for external integrations

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- API ENDPOINTS -->
## API Endpoints

The application provides RESTful API endpoints for external access:

### Posts
```http
GET /api/posts?page=1&per_page=20&color=red&building=library&status=lost
```
Returns paginated list of posts with optional filters.

### Tags
```http
GET /api/tags
```
Returns all available color and building tags.

### Example Response
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Blue iPhone 13",
      "description": "Left in Gordon Library study room",
      "timestamp": "2025-01-20T14:30:00Z",
      "status": "lost",
      "color_tag": "blue", 
      "building_tag": "gordon_library",
      "owner": "student123",
      "has_image": true
    }
  ],
  "pagination": {
    "page": 1,
    "pages": 5,
    "total": 47
  }
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT STRUCTURE -->
## Project Structure

```
lostandfound/
├── app/                          # Application package
│   ├── auth/                     # Authentication blueprint  
│   │   ├── auth_forms.py         # Login/register forms
│   │   └── auth_routes.py        # Auth routes
│   ├── errors/                   # Error handling blueprint
│   ├── main/                     # Main application blueprint
│   │   ├── templates/            # Jinja2 templates
│   │   ├── api_routes.py         # API endpoints
│   │   ├── contact_forms.py      # Contact system forms
│   │   ├── forms.py              # Main application forms  
│   │   ├── models.py             # Database models
│   │   ├── profile_forms.py      # User profile forms
│   │   └── routes.py             # Main routes
│   ├── static/                   # Static assets
│   │   ├── css/                  # Stylesheets
│   │   ├── js/                   # JavaScript files
│   │   ├── img/                  # Images
│   │   └── building_database/    # Campus building data
│   ├── __init__.py               # App factory
│   └── email.py                  # Email functionality
├── migrations/                   # Database migrations
├── tests/                        # Unit tests
├── config.py                     # Configuration settings
├── lostandfound.py               # Application entry point
├── init_database.py              # Database initialization
├── requirements.txt              # Python dependencies
└── .env                          # Environment variables
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions make the open source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have suggestions for improvement:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 Python style guidelines
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

**Tran Minh Duc Nguyen** - Computer Science Student

Project Link: [https://github.com/samnguyen3115/lostandfound](https://github.com/samnguyen3115/lostandfound)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Bootstrap](https://getbootstrap.com)
* [Font Awesome](https://fontawesome.com)
* [PostgreSQL](https://www.postgresql.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [WPI Campus](https://www.wpi.edu/) - For inspiration and building data
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/samnguyen3115/lostandfound.svg?style=for-the-badge
[contributors-url]: https://github.com/samnguyen3115/lostandfound/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/samnguyen3115/lostandfound.svg?style=for-the-badge
[forks-url]: https://github.com/samnguyen3115/lostandfound/network/members
[stars-shield]: https://img.shields.io/github/stars/samnguyen3115/lostandfound.svg?style=for-the-badge
[stars-url]: https://github.com/samnguyen3115/lostandfound/stargazers
[issues-shield]: https://img.shields.io/github/issues/samnguyen3115/lostandfound.svg?style=for-the-badge
[issues-url]: https://github.com/samnguyen3115/lostandfound/issues
[license-shield]: https://img.shields.io/github/license/samnguyen3115/lostandfound.svg?style=for-the-badge
[license-url]: https://github.com/samnguyen3115/lostandfound/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/samnguyen3115
[Flask.py]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[PostgreSQL.com]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[SQLAlchemy.com]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[JavaScript.com]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[HTML5.com]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML5-url]: https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5
[CSS3.com]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS3-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[Python.com]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/