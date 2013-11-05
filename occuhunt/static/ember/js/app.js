App = Ember.Application.create({
	LOG_TRANSITIONS: true
});

App.Router.map(function() {
  // put your routes here
  this.route("about", { path: "/about" });
});

App.IndexRoute = Ember.Route.extend({
  
});
