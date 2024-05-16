# AcademicHub API Schema Ideas

This document outlines potential schema ideas for the AcademicHub API.
- [Research](#research-management-schema)
- [Event](#event-management-schema)
- [Course](#course-management-schema)
- [Facilities](#facilities-management-schema)

```sql
-- 0  Create the database
-- 1  Declare all the schemas
-- 2  Declare all the tables for each schema
-- 3  Declare all the views for each schema
-- 4  Add some data to the tables
```

## Research Management Schema
This schema facilitates the administration and tracking of research activities within the academic community.
- Research Projects
    - **Description:** Stores details about each research project.
    - **Fields:** Title, Abstract, Start Date, End Date, Principal Investigator(s), Funding Details, Status, Departments.
- Publications
    - **Description:** Tracks publications related to research projects.
    - **Fields:** Type, Title, Authors, Publication Date, DOI (Digital Object Identifier).
- Collaborations
    - **Description:** Records details about collaborative research efforts.
    - **Fields:** Institution, Contact, Project ID, Agreement Details.


## Event Management Schema
Helps in organizing and managing academic and extracurricular events.
- Events
    - **Description:** Details of each event organized by the institution.
    - **Fields:** Title, Description, Venue, Schedule, Organizer, Audience.
- Event Registrations
    - **Description:** Tracks registrations and attendance for events.
    - **Fields:** Event ID, Participant ID, Registration Status, Check-in Status.
- Event Resources
    - **Description:** Manages resources required for each event.
    - **Fields:** Event ID, Resource Type, Quantity, Allocation.
- Feedback and Surveys
    - **Description:** Collects and analyzes participant feedback.
    - **Fields:** Event ID, Feedback, Rating, Survey Results.


## Course Management Schema
Provides a detailed framework for managing academic courses.
- Courses
    - **Description:** Detailed records for each academic course.
    - **Fields:** Course Code, Title, Description, Credits, Prerequisites, Instructors.
- Course Materials
    - **Description:** Repository for course-related materials.
    - **Fields:** Course ID, Material Type, Access URL, Permissions.
- Course Enrollments
    - **Description:** Tracks student enrollments and participation.
    - **Fields:** Course ID, Student ID, Enrollment Date, Status.
- Assignments and Exams
    - **Description:** Manages assignments and exams for courses.
    - **Fields:** Course ID, Type, Description, Due Date, Submission Guidelines.


## Facilities Management Schema
Aids in the efficient management of campus facilities.
- Facilities
    - **Description:** Inventory of all campus facilities.
    - **Fields:** Facility ID, Name, Capacity, Location, Features.
- Bookings
    - **Description:** Schedule and manage facility bookings.
    - **Fields:** Facility ID, Event ID, Date, Time, User ID.
- Maintenance Requests
    - **Description:** Tracks maintenance needs for facilities.
    - **Fields:** Request ID, Facility ID, Issue Description, Reported Date, Status.
- Usage Statistics
    - **Description:** Analyzes usage patterns of facilities.
    - **Fields:** Facility ID, Usage Data, Time, Occupancy Rate.


## Financial Management System
Manage tuition payments, scholarships, and other financial aspects related to students and faculty.

- Tables: 
    - Accounts
    - Transactions
    - Scholarships
    - Grants 
    - Fees
    - Payments
