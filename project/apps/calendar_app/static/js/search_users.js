"use strict";

function clone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function init() { 
    var self = {};
    self.data = {};    
    self.methods = {};
    self.data.users = [];
    self.data.text = ""

    // Get users
    axios.get("../get_users").then(function(r){
        self.vue.users = r.data.users;
    });
    
    // Search function
    self.methods.filter_users = function() {
      if(self.vue.text.length>0) {
          fetch("/calendar_app/get_users?text="+encodeURIComponent(self.vue.text))
          .then(r=>r.json())
          .then(function(data){
            self.vue.users = data.users;
          }).catch(function(error) {
            console.error("Error fetching users:", error)});
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
        // Refetch all users
        fetch("/calendar_app/get_users?text="+encodeURIComponent(self.vue.text))
        .then(r=>r.json())
        .then(function(data){
          self.vue.users = data.users;
        }).catch(function(error) {
          console.error("Error fetching users:", error)});
    };

    self.vue = new Vue({el:"#vue", data: self.data, methods: self.methods});


    return self;
}

window.app = init();