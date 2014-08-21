/*****

This file is mainly for mixpanel events

*****/

////// Student side

// _top_bar.html
mixpanel.track_links("#mp-logohome", "Splash page signup top", {'referrer': document.referrer });
mixpanel.track_links("#mp-loggedin-main", "Topbar login", {'referrer': document.referrer });
mixpanel.track_links("#mp-dashboard", "Topbar dashboard", {'referrer': document.referrer });
mixpanel.track_links("#mp-offrhunt", "Topbar offrhunt", {'referrer': document.referrer });
mixpanel.track_links("#mp-documents", "Topbar documents", {'referrer': document.referrer });
mixpanel.track_links("#mp-name", "Topbar name", {'referrer': document.referrer });
mixpanel.track_links("#mp-profile", "Topbar name > profile", {'referrer': document.referrer });
mixpanel.track_links("#mp-loggedout", "Topbar name > log out", {'referrer': document.referrer });

// homepage2.html
mixpanel.track_links("#mp-signupsplash-top", "Splash page signup top", {'referrer': document.referrer });
mixpanel.track_links("#mp-signupsplash-bottom", "Splash page signup bottom", {'referrer': document.referrer });

// profile/dashboard.html
mixpanel.track_links("#mp-dashboard-offrhunt", "Dashboard > Offrhunt", {'referrer': document.referrer });
mixpanel.track_links("#mp-dashboard-offrhunt", "Dashboard > Offrhunt", {'referrer': document.referrer });
// tracking for tracking application status is embedded within file
// tracking for 357s is embedded within file

// profile/documents.html
mixpanel.track_links("#file_select_button", "Documents > New Document", {'referrer': document.referrer });
// document visits, copy, delete is tracked in profile.js

// profile/preview.html
mixpanel.track_links("#mp-document-download", "Documents > New Document", {'referrer': document.referrer });

// search_results.html
mixpanel.track_links("#company_thumbnail_logo", "Search Results > Clicked on company", {'referrer': document.referrer });
mixpanel.track_links("#company_thumbnail_logo", "Search Results > Clicked on company", {'referrer': document.referrer });

// company.html
// tracking is embedded in company.html

// base/357v2.html
// tracking is embedded in 357v2.html

// base/infosession_template.html
// tracking is embedded in infosession_template.html

// base/offrhunt_template.html
// tracking is embedded in offrhunt_template.html

// _footer.com
mixpanel.track_links("#mp-footer-sanchit", "Footer > About > Sanchit", {'referrer': document.referrer });
mixpanel.track_links("#mp-footer-faq", "Footer > FAQ", {'referrer': document.referrer });
mixpanel.track_links("#mp-footer-feedback", "Footer > Feedback", {'referrer': document.referrer });
mixpanel.track_links("#mp-footer-privacy", "Footer > Privacy", {'referrer': document.referrer });
mixpanel.track_links("#mp-footer-recruiter", "Footer > Recruiter", {'referrer': document.referrer });
mixpanel.track_links("#mp-footer-about", "Footer > About", {'referrer': document.referrer });
mixpanel.track_links("#mp-footer-contact", "Footer > Contact", {'referrer': document.referrer });

////// Recruiter side

// _top_bar_recruiter.html
mixpanel.track_links("#mp-recruiter-logohome", "Recruiter topbar > Logo Home", {'referrer': document.referrer });
mixpanel.track_links("#mp-recruiter-offrhunt", "Recruiter topbar > OffrHunt", {'referrer': document.referrer });
mixpanel.track_links("#mp-recruiter-hire", "Recruiter topbar > Hire", {'referrer': document.referrer });
mixpanel.track_links("#mp-recruiter-profile", "Recruiter topbar > Profile", {'referrer': document.referrer });
mixpanel.track_links("#mp-recruiter-changepassword", "Recruiter topbar > Change password", {'referrer': document.referrer });
mixpanel.track_links("#mp-recruiter-loggedout", "Recruiter topbar > log out", {'referrer': document.referrer });
