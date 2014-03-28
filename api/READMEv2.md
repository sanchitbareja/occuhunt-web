# API v2 for Occuhunt

1. [Applications](#application)
2. [Companies](#company)
3. [Events](#event)
4. [Favorites](#favorite)
5. [Hunts](#hunt)
6. [Jobs](#job)
7. [Notifications](#notification)
8. [Resumes](#resume)
9. [Users (Students, Recruiters)](#user)

##<a id="application"></a>Application

	GET, POST, PUT

* id
* user (full info)
* company (full info)
* fair (id)
* status (show only for recruiter)
* position 
* note (show only for recruiter)
* timestamp
* response_timestamp
* job (full info)

##<a id="company"></a>Company

	GET
	Always paginated - never need to get complete list

* id
* name
* founded
* funding
* website
* career_website
* logo
* banner_image
* number_employees
* organization_type
* company_description
* competitors
* avg_salary
* location
* intro_video
* timestamp

##<a id="event"></a>Event

	GET, POST in the future

###Event
* id
* name
* timestamp
* time_start
* time_end
* logo

###Fair
* id
* time_start
* time_end
* name
* venue
* rooms (full info)
* logo
* event (full info)
* resume_drop
* organizers (full info)
* sponsors (full info)
* jobs (hidden)

##<a id="favorite"></a>Favorite

	query to filter by user, company, timestamp
	GET, POST

* id
* user (full info)
* company (full info)
* timestamp

##<a id="hunt"></a>Hunt

	GET, POST

* id	
* user (full info)
* fair (only show id)
* timestamp

##<a id="job"></a>Job

* id
* name
* description
* job_type
* location
* company (full info)
* network (full info)
* contract_type
* qualifications
* timestamp

##<a id="notification"></a>Notification
	Needs to be redone
	
* id
* user (full info)
* company (full info)
* receiver
* notification
* read_receipt
* timestamp

##<a id="resume"></a>Resume

* id
* user (hidden by default unless anonymous = False)
* url
* timestamp
* anonymous (if anonymous - don't show user)
* original
* featured
* showcase
* comments (full info)

##<a id="user"></a>User
* id
* email
* first_name
* last_name
* linkedin_uid
* resume_points
* time_created
* phone_number
* groups (full info)
* student (verified_email, graduation_year)
* company (full info if user is recruiter)
* resume (show only for recruiter)