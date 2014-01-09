// Fixture Data
var personal_recs = {
  answer1: "Math, Physics, Socializing, Drinking Wine, Solving bugs",
  answer2: "Team work, problem solving, creativity",
};

var other_recs = [{
	id: '1',
	to: {
		id:'11',
		name: 'Bill Gates',
		img: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/c0.0.151.151/181592_10150105700371961_7986881_a.jpg'
	},
	relationship: 'Partner in Crime',
	at: 'World AIDS Organization',
	answer1: "Maths, CS, Physics",
	answer2: "Design skills",
	answer3: "Bill is an extremely dynamic person. His experience at Microsoft has really helped him hone his critical and analytical thinking skills which allow him to come up with highly creative and practical solutions. It is always a joy to have a conversation with him. He challenges me to think more broadly and on a larger scale that I would noramlly think of. Bill is also highly connected in the business circles. His influences allows him to speak with anyone at anytime without ever facing rejection. It has been extremely efficient in having him as a team member.",
}, {
	id: '2',
	to: {
		id:'15',
		name: 'Dalai Lama',
		img: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/c0.44.180.180/s160x160/24500_339205542615_5021059_a.jpg?lvh=1'
	},
	relationship: 'Peace Advisor',
	at: 'Nepal',
	answer1: "Maths, CS, Physics",
	answer2: "Clothing",
	answer3: "The Lama is an extremely respected and free-spirited person",
},{
	id: '3',
	to: {
		id:'19',
		name: 'Lee Hsien Loong',
		img: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c0.0.180.180/s160x160/1504083_637521086310601_95883197_a.jpg'
	},
	relationship: 'Minister Mentor',
	at: 'Singapore PM office',
	answer1: "Politics",
	answer2: "Connecting with the poorest people",
	answer3: "Lee is a joy to work with just like his father Harry.",
},{
	id: '4',
	to: {
		id:'3',
		name: 'Steve Wozniak',
		img: 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/t1/c0.34.180.180/s160x160/315409_10151057645386282_863370886_a.jpg'
	},
	relationship: '',
	at: 'Apple Mac Division',
	answer1: "Maths, CS, Physics",
	answer2: "Management",
	answer3: "Woz is an incredible builder. He is by far the most talented person I've ever met.",
},];

var people_to_recommend = [{
	id: "53",
	name: "Albert Einstein",
	img: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/s160x160/527048_10150659821294843_1245284552_a.jpg",
}, {
	id: "54",
	name: "Henry Ford",
	img: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn2/s160x160/1458443_1376737985908465_1761671809_a.jpg",
}, {
	id: "55",
	name: "Andrew Carnegie",
	img: "https://fbexternal-a.akamaihd.net/safe_image.php?d=AQA8uPjvNCDQIab8&w=720&h=901&url=http%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F09%2FAndrew_Carnegie%252C_three-quarter_length_portrait%252C_seated%252C_facing_slightly_left%252C_1913-crop.jpg%2F720px-Andrew_Carnegie%252C_three-quarter_length_portrait%252C_seated%252C_facing_slightly_left%252C_1913-crop.jpg",
}];

var recommendation_requests = [{
	from: {	id: "53",
		name: "Albert Einstein",
		img: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/s160x160/527048_10150659821294843_1245284552_a.jpg",
	},
	message: "Hey Sanchit, I've a deadline coming up for my interview with Microsoft. Could you recommend me! Thanks.",
	deadline: new Date(),
}, {
	from: {	id: "54",
		name: "Henry Ford",
		img: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn2/s160x160/1458443_1376737985908465_1761671809_a.jpg",
	},
	message: "I need a recommendation!",
	deadline: new Date(),
}, {
	from: {	id: "55",
		name: "Andrew Carnegie",
		img: "https://fbexternal-a.akamaihd.net/safe_image.php?d=AQA8uPjvNCDQIab8&w=720&h=901&url=http%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F09%2FAndrew_Carnegie%252C_three-quarter_length_portrait%252C_seated%252C_facing_slightly_left%252C_1913-crop.jpg%2F720px-Andrew_Carnegie%252C_three-quarter_length_portrait%252C_seated%252C_facing_slightly_left%252C_1913-crop.jpg",
	},
	message: "I'm looking for feedback on my project with you from New York to San Francisco. Your help is much appreciated.",
	deadline: new Date(),
}];


// Application
App = Ember.Application.create({
	rootElement: $('#main-body')
});

App.Router.reopen({
  	rootURL: '/recommend/'
});

// URL mapping
App.Router.map(function() {
	this.route("index", { path: "/" });
  	this.route("sendrecs");
  	this.route("requestrecs");
  	this.route("recform");
});

// Routes

// Views

App.OtherrecsView = Ember.View.extend({
	templateName: 'other-recs',
	click: function(event){
		$($(event.target).find("#category_details")[0]).slideToggle();
	},
});

// Controllers
App.ApplicationController = Ember.Controller.extend({
	
});

App.IndexController = Ember.Controller.extend({
	people_to_recommend: people_to_recommend,
	personal_recs: personal_recs,
	other_recs: other_recs,
});

App.SendrecsController = Ember.Controller.extend({
	people_to_recommend: people_to_recommend,
	recommendation_requests: recommendation_requests,
});

// Helpers
Ember.Handlebars.helper('format-date', function(date) {
  return moment(date).fromNow();
});
