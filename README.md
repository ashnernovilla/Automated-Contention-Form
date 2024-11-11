# Automated Contention Form Proof of Concept
The Automated Contention Form PoC for BSE at BPI AIA is a streamlined solution designed to test the feasibility of automating contention form management. This Proof of Concept uses MS SQL as the database management backbone, ensuring reliable data storage and efficient querying. A Python-based interface, built with Streamlit, allows users to easily input, view, and update forms in real-time.

By combining MS SQL’s robust database capabilities with Streamlit’s intuitive, web-accessible interface, the PoC enables users to test end-to-end functionality, including data entry and retrieval, with minimal manual handling. This streamlined process aims to reduce form processing time and enhance overall accuracy, providing a scalable foundation for future implementation across the organization.


## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Conceptual Diagram](#conceptual-diagram)
- [Results](#results)


## Overview
The Automated Contention Form PoC provides a simple, user-friendly interface to manage contention forms efficiently. This solution aims to reduce manual processing time and increase accuracy, offering a scalable and reliable foundation for potential full-scale deployment.

## Technologies Used
- **MS SQL**: Database management for storing, retrieving, and managing form data.
- **Python**: Programming language for backend logic.
- **Streamlit**: Framework for creating the web-based UI.

## Features

- **Automated Form Entry**: Easily add and submit new contention forms through a web interface.
- **Real-time Data Retrieval**: Quickly retrieve and view existing forms.
- **Form Updates**: Edit and update existing forms in real-time.
- **Email Notifications**: Sends the daily report to designated recipients.
- **Secure Data Storage**: MS SQL manages and secures all data entries.
- **Configurable Settings**: Customize parameters like email recipients, report time, and data sources.


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ashnernovilla/Automated-Contention-Form.git
   cd Automated-Contention-Form.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt


## Configuration

1. **Setup the Database Credentials and Host**

2. **Administrator Rights**

3. **Correct Python Evnironment**

## Usage

1. **Setup the Folders Location and Lifelines**:
   ```bash
   streamlit run contention_application.py


## Conceptual Diagram
![image](https://github.com/user-attachments/assets/cffcc0c3-449e-466a-971e-6b842257076a)

## Results

1. Contention Form
![image](https://github.com/user-attachments/assets/791f9b05-d765-4568-b432-fcae18c3a4c9)

2. Contention History
![image](https://github.com/user-attachments/assets/a9b23241-0335-403b-b9d3-fab519176e54)

3. Page Dashboard
![image](https://github.com/user-attachments/assets/a2ad7552-3d03-4a0e-8ee9-b34b7ff1367a)


We welcome contributions to enhance functionality, fix bugs, or improve documentation.

Fork the project.
Create a feature branch.
Commit your changes and push the branch.
Open a Pull Request.


