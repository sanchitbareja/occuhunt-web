#API Reference for Occuhunt
This is the `/v1/` API documentation for the Occuhunt API. All requests are RESTful and all request & response bodies are `json` formatted.

**Student Workflow**

*	[Get Users](#getusers)
*	[Get Events](#getevents)
*	[Get Companies](#getcompanies)
*	[Check-in/Hunt at Event](#posthunt)
*	[Share Resumes with Recruiter](#postshareresume)

**Recruiter Workflow** (will include recruiter_id for all)

*	[List of attendees, attendees that expressed interest in a specific company, attendees interacted with](#getapplications)
*	As soon as you get the attendee detail, should track that the recruiter viewed the resume - will be the same as #getusers but supplied with recruiter_id
*	[Add Note](#addnote)
*	[Add User](#adduser) - Prompt the recruiter to ask the student if he has a linkedin acct
*	[Reject User](#rejectuser) - send email to student that he's rejected

** By default, all requests have an application/json content type. **

** By default, all request can be filtered by 'limit' eg. /api/v1/xxxx?limit=100 **

** For all get request, params refer to /api/v1/xxxx?param1=abc&param2=abc2 **

##<a id="getusers"></a>Get Users

**Example Request Header:**

params: linkedin_uid (/api/v1/users/?linkedin_uid=XXXXXX)

	Content-Type: application/json
	Accept: */*
	
**Example Response Body:** it basically returns a list of users. This doesn't matter for us. I think the more important thing is that the return Response Status Code is 200.

To return: resume, school, profile_pic, first/last name, email

	{
    	"meta": {
        	"limit": 20,
        	"next": null,
        	"offset": 0,
        	"previous": null,
        	"total_count": 1
    	},
    	"response": {
        	"users": [{
            	"email": "sanchitbareja@gmail.com",
            	"first_name": "",
            	"id": 1,
            	"is_business": false,
            	"is_premium": false,
            	"last_login": "2013-12-05T03:52:05.606896",
            	"last_name": "",
            	"resource_uri": "/api/v1/users/1/",
            	"username": "sanchit"
        	}]
    	}
	}

	
##<a id="getevents"></a>Get Fairs

Returns a list of fairs.

**Filtering**

	None

**Example Request Body**

	Request Url: http://127.0.0.1:8000/api/v1/fairs/
	Request Method: GET

**Example Response Body**
	
	{
    	"meta": {
        	"limit": 20,
        	"next": null,
        	"offset": 0,
       		"previous": null,
        	"total_count": 1
    	},
    	"objects": [{
        	"id": 1,
        	"logo": "http://occuhunt.com/static/images/berkeley.gif",
        	"name": "EECS Career Fair",
        	"resource_uri": "/api/v1/fairs/1/",
        	"rooms": [{
        	    "id": 1,
            	"name": "International House - Chevron Auditorium",
            	"resource_uri": "/api/v1/rooms/1/"
        	}, {
            	"id": 3,
            	"name": "International House - 2nd floor room 1",
            	"resource_uri": "/api/v1/rooms/3/"
        	}, {
            	"id": 4,
            	"name": "International House - 2nd floor room 2",
            	"resource_uri": "/api/v1/rooms/4/"
        	}],
        	"time_end": "2014-02-06T00:00:00",
        	"time_start": "2014-02-06T00:00:00"
    	}]
	}

##<a id="getcompanies"></a>Get Companies

Returns a list of Companies

**Filtering options**

	id: /api/v1/companies/?id=302

**Example Request**

	Request Url: http://127.0.0.1:8000/api/v1/companies/
	Request Method: GET
	Params: {
    	"id": "302"
	}

**Example Response Body**
	
	{
    	"meta": {
    	    "limit": 1000,
        	"next": null,
        	"offset": 0,
        	"previous": null,
        	"total_count": 1
    	},
    	"response": {
    	    "companies": [{
        	    "avg_salary": "",
            	"banner_image": "http://www2.sfdcstatic.com/assets/dreamjob-confessional.png",
            	"careers_website": "http://www.salesforce.com/company/careers/",
            	"company_description": "Salesforce is an enterprise cloud computing company that provides business software on a subscription basis. The company is best known for its on-demand Customer Relationship Management (CRM) solutions.\r\nSalesforce was founded in 1999 by former Oracle executive Marc Benioff, and went public in June 2004. Salesforce has been a pioneer in developing enterprise platforms through its innovative AppExchange directory of on-demand applications, and its Force.com “Platform as a Service” (PaaS) API for extending Salesforce.",
            	"competitors": "",
            	"favorites": [],
            	"founded": "1999",
            	"funding": "Public Company",
            	"id": 302,
            	"intro_video": "",
            	"location": null,
            	"logo": "http://s3.amazonaws.com/images/1691/11691v12-max-250x250.jpg",
	            "name": "Salesforce",
    	        "number_employees": "3500",
        	    "organization_type": "Enterprise",
            	"resource_uri": "/api/v1/companies/302/",
            	"website": "http://www.salesforce.com/"
        	}]
    	}
	}		

##<a id="getapplications"></a>Get Attendees and applcations

**filtering**

	To get the list of attendees for the career fair, only have the fair_id filter. To get list of applicants to a particular company at a career fair, include both fair_id and company_id

	user_id
	fair_id
	company_id
	status (1,2,3,4)
	
	1 - Applied
	2 - Interacted With
	3 - Rejected
	4 - To Interview

**Example Request Header**

	Request Url: http://127.0.0.1:8000/api/v1/applications/?fair_id=1
	Request Method: GET

**Example Response Body**

	{
    	"meta": {
        	"limit": 100,
        	"next": null,
        	"offset": 0,
        	"previous": null,
        	"total_count": 1
    	},
    	"response": {
        	"applications": [{
            	"company": {
                	"avg_salary": "",
                	"banner_image": "https://www.room77.com/images/web/teamphoto.jpg",
                	"careers_website": "https://www.room77.com/jobs.html?pid=PJ5tys&id=fZ3C5q",
                	"company_description": "Room 77 offers the most advanced hotel shopping experience on the Web today by allowing travelers to simultaneously compare pricing across every major online travel agency and more, shop across a variety of room types, and book more than 200,000 hotel rooms worldwide.\r\nUnlike other travel sites, Room 77 doesn’t stop at the booking. Travelers booking 4- or 5-star hotels, or stays totaling more than $400 on Room 77 get access to a complimentary Room Concierge who utilizes Room 77’s proprietary RoomMatch technology to identify the best rooms for each traveler then works directly with the hotel to score one of those rooms for the guest.",
                	"competitors": "",
                	"favorites": [37, 3],
                	"founded": "4/10",
                	"funding": "43.8M",
               	 	"id": 336,
                	"intro_video": "",
                	"location": "Mountain View, CA",
                	"logo": "http://s3.amazonaws.com/crunchbase_prod_assets/assets/images/resized/0012/3815/123815v5-max-250x250.png",
                	"name": "Room 77",
                	"number_employees": "20",
                	"organization_type": "Computer Software",
                	"resource_uri": "/api/v1/companies/336/",
                	"website": "https://www.room77.com/"
            	},
            	"fair": {
                	"id": 1,
                	"logo": "http://occuhunt.com/static/images/berkeley.gif",
                	"name": "EECS Career Fair",
                	"resource_uri": "/api/v1/fairs/1/",
                	"rooms": [{
                   		"id": 1,
                   		"name": "RSF - Field House Gym",
                    	"resource_uri": "/api/v1/rooms/1/"
                	}],
                	"time_end": "2013-09-25T15:00:00",
                	"time_start": "2013-09-25T11:00:00",
                	"venue": "International House"
            	},
            	"id": 1,
            	"note": "",
            	"position": "Other",
            	"resource_uri": "/api/v1/applications/1/",
            	"status": 1,
            	"timestamp": "2014-02-07T02:26:44.550560",
            	"user": {
                	"email": "sanchitbareja@gmail.com",
                	"first_name": "Sanchit",
                	"id": 1,
                	"is_superuser": false,
                	"last_name": "Bareja",
                	"linkedin_uid": null,
                	"profile_pic": "",
                	"resource_uri": "/api/v1/users/1/",
                	"resume": "https://resumefeed.s3.amazonaws.com/sanchit-barejapdf7krG0TT66sC2tnMkTjdx3dz2nXglCA",
                	"resume_points": 10,
                	"school": [{
                    "name": "UC Berkeley"
                	}],
                	"thumbnail_profile_pic": "",
                	"username": "sanchitbareja"
            	}
        	}]
    	}
	}


##<a id="posthunt"></a>Post Check-in/Hunt

params: user_id, event_id (check if the user is from the correct school before he's allowed to check-in)

**filtering**

	user_id

**Example Request Header**

	Content-Type: application/json
	
**Example Request Body**
	
	Request Url: http://127.0.0.1:8000/api/v1/hunts/
	Request Method: POST		

**Example Response Header**

	Status Code: 201
	Location: http://127.0.0.1:8000/api/v1/hunts/2/
	Date: Thu, 06 Feb 2014 05:52:12 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Vary: Accept
	Content-Type: application/json

##<a id="postshareresume"></a>Share Resume with Recruiter

params: user_id, company_id, status

status takes 3 values, "Applied", "Reject", "Interview". "Applied" is the default option and should be the one used when performing a "resume drop"

**Filtering options**

	user
	company
	status

**Example Request Body**
	
	Content-Type: application/json

	Request Url: http://127.0.0.1:8000/api/v1/applications/
	Request Method: POST

**Example Response Body**

	Status Code: 201
	
For sharing resume with multiple recruiters at once, we send a PATCH request with the payload as follows:

	{"objects":[
		{"user_id":1,"company_id":302,"status":"Applied"},
		{"user_id":1,"company_id":301,"status":"Applied"},
		{"user_id":1,"company_id":300,"status":"Applied"},
		{"user_id":1,"company_id":299,"status":"Applied"}
	]}

**Example Response Body**

	Status Code: 202

##<a id="addnote"></a>Add Note

params: user_id, recruiter_id, note

recruiter_id is also the is corresponding to the user who is a recruiter

**Filtering options**

	None

**Example Request Body**

	Content-Type: application/json

	Request Url: http://127.0.0.1:8000/api/v1/notes/
	Request Method: POST

**Example Response Body**

	{
    "meta": {
        "limit": 100,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 2
    },
    "response": {
        "notes": [{
            "id": 1,
            "note": "Very nice to talk to",
            "recruiter": {
                "email": "sanchitbareja@gmail.com",
                "first_name": "Sanchit",
                "id": 1,
                "is_superuser": false,
                "last_name": "Bareja",
                "linkedin_uid": null,
                "profile_pic": "",
                "resource_uri": "/api/v1/users/1/",
                "resume": "https://resumefeed.s3.amazonaws.com/sanchit-barejapdfGKCe1iIpV",
                "resume_points": 10,
                "school": [{
                    "name": "UC Berkeley"
                }],
                "thumbnail_profile_pic": "",
                "username": "sanchitbareja"
            },
            "resource_uri": "/api/v1/notes/1/",
            "timestamp": "2014-02-06T09:15:07.104676",
            "user": {
                "email": "sanchitbareja@gmail.com",
                "first_name": "Sanchit",
                "id": 1,
                "is_superuser": false,
                "last_name": "Bareja",
                "linkedin_uid": null,
                "profile_pic": "",
                "resource_uri": "/api/v1/users/1/",
                "resume": "https://resumefeed.s3.amazonaws.com/sanchit-barejapdfGKCV",
                "resume_points": 10,
                "school": [{
                    "name": "UC Berkeley"
                }],
                "thumbnail_profile_pic": "",
                "username": "sanchitbareja"
            }
        }]
    }


##<a id="adduser"></a>Add User (Not implemented yet)

params: resume_img and all other standard details

**Filtering options**

**Example Request Body**

**Example Response Body**


##<a id="rejectuser"></a>Reject/Interview User (PUT) - still debugging

params: status

status takes 3 values, "Applied", "Reject", "Interview". "Applied" is the default option and should be the one used when performing a "resume drop". In this case, status should be either "Reject" or "Interview"

	Need to specifically send to /api/v1/applications/{application_id}/

**Filtering options**

**Example Request Body**

**Example Response Body**


