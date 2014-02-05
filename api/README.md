#API Reference for Occuhunt
This is the `/v1/` API documentation for the Occuhunt API. All requests are RESTful and all request & response bodies are `json` formatted.

**Student Workflow**

*	[Get Users](#getusers)
*	[Get Events](#getevents)
*	[Get Companies](#getcompanies)
*	[Check-in/Hunt at Event](#posthunt)
*	[Share Resumes with Recruiter](#postshareresume)

**Recruiter Workflow** (will include recruiter_id for all)

*	[List of attendees, attendees that expressed interest in a specific company, attendees interacted with](#getusers)
*	As soon as you get the attendee detail, should track that the recruiter viewed the resume - will be the same as #getusers but supplied with recruiter_id
*	[Add Note](#addnote)
*	[Add User](#adduser) - Prompt the recruiter to ask the student if he has a linkedin acct
*	[Reject User](#rejectuser) - send email to student that he's rejected

** By default, all requests have an application/json content type. **

** By default, all request can be filtered by 'limit' eg. /api/v1/xxxx?limit=100 **

** For all get request, params refer to /api/v1/xxxx?param1=abc&param2=abc2 **

##<a id="getusers"></a>Get Users
This is basically checking if a user exists. /api/v1/users requires basic authentication so we will use that. For more information on how to construct the Basic Authentication authorization header: [wiki](http://en.wikipedia.org/wiki/Basic_access_authentication)

	HTTP Method: GET
	URL: /api/v1/users/
	Content Type: application/json
	
**Example Request Header:**
params: linkedin_uid

	Content-Type: application/json
	Authorization: Basic c2FuY2hpdDpyb290 -- this corresponds to sanchit:root
	Accept: */*
	
**Example Response Body:** it basically returns a list of users. This doesn't matter for us. I think the more important thing is that the return Response Status Code is 200.

To return: resume, recs, school, profile_pic, first/last name, email

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

	
##<a id="getevents"></a>Get Events

Returns a list of events.
params: None

**Filtering options:**

**Example Request Body**	

**Example Response Body**


##<a id="getcompanies"></a>Get Companies

Returns a list of Companies
params: company_id

**Filtering options**

**Example Request Body**

**Example Response Body**
To return: Category, ...


##<a id="posthunt"></a>Post Check-in/Hunt

params: user_id, event_id (check if the user is from the correct school before he's allowed to check-in)

**Example Request Body**

**Example Response Header**


##<a id="postshareresume"></a>Share Resume with Recruiter

params: user_id, event_id, company_id

**Filtering options**

**Example Request Body**

**Example Response Body**


##<a id="addnote"></a>Add Note

params: user_id, recruiter_id, note

**Filtering options**

**Example Request Body**

**Example Response Body**


##<a id="adduser"></a>Add User

params: resume_img and all other standard details

**Filtering options**

**Example Request Body**

**Example Response Body**


##<a id="rejectuser"></a>Reject User

params: attendee_id, recruiter_id

**Filtering options**

**Example Request Body**

**Example Response Body**


