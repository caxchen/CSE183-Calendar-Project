"use strict";

function clone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function init() { 
    var self = {};
    self.data = {};    
    self.methods = {};
    self.data.events = [];
    self.data.text = ""

    // Get events
    axios.get("../get_events").then(function(r){
        self.vue.events = r.data.events;
    });
    
    // Search function
    self.methods.filter_events = function() {
      if(self.vue.text.length>0) {
          fetch("/calendar_app/get_events?text="+encodeURIComponent(self.vue.text))
          .then(r=>r.json())
          .then(function(data){
            self.vue.events = data.events;
          }).catch(function(error) {
            console.error("Error fetching events:", error)});
        }
        else {
            self.methods.clear();
        }
    };

    // Clear function
    self.methods.clear = function() {
        // Empty text variables to clear input
        self.data.text = "";
        self.vue.text = "";
        // Refetch all events
        fetch("/calendar_app/get_events?text="+encodeURIComponent(self.vue.text))
        .then(r=>r.json())
        .then(function(data){
          self.vue.events = data.events;
        }).catch(function(error) {
          console.error("Error fetching events:", error)});
    };

    self.vue = new Vue({el:"#vue", data: self.data, methods: self.methods});


    return self;
}

window.app = init();