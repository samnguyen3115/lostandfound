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
    <li><a href="#roadmap">Roadmap</a></li>
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


### Built With

* [![Flask][Flask.py]][Flask-url]
* [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![SQLAlchemy][SQLAlchemy.com]][SQLAlchemy-url]
* [![JavaScript][JavaScript.com]][JavaScript-url]
* [![HTML5][HTML5.com]][HTML5-url]
* [![CSS3][CSS3.com]][CSS3-url]
* [![Python][Python.com]][Python-url]


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


<!-- ROADMAP -->
## Roadmap

### Completed Features
- [x] **User Authentication** - Registration, login, logout system
- [x] **Item Posting** - Create posts with title, description, images, and tags
- [x] **Basic Filtering** - Filter by color and building location
- [x] **Contact System** - Email-based contact between users
- [x] **Interactive Campus Map** - Clickable building map with details
- [x] **Image Upload** - Support for JPG, PNG image uploads
- [x] **RESTful API** - JSON endpoints for posts and tags
- [x] **Responsive Design** - Bootstrap-based mobile-friendly interface

### Planned Enhancements
- [ ] **Advanced Search** - Full-text search across titles and descriptions
- [ ] **User Profiles** - Personal dashboards and post management
- [ ] **In-App Messaging** - Direct communication between users  
- [ ] **Smart Notifications** - Automated matching suggestions and enhanced email alerts
- [ ] **Mobile Apps** - Native iOS/Android applications
- [ ] **UI/UX Overhaul** - Modern design with dark mode support
- [ ] **Third-Party Integration** - Campus security and social media sharing

See the [open issues](https://github.com/samnguyen3115/lostandfound/issues) for a full list of proposed features (and known issues).


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Bootstrap](https://getbootstrap.com)
* [Font Awesome](https://fontawesome.com)
* [PostgreSQL](https://www.postgresql.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [WPI Campus](https://www.wpi.edu/) - For inspiration and building data
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)


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