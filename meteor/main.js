import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

var Heap = require('heap');

tweets = new Mongo.Collection('tweet')
if (Meteor.isClient) {
    Template.body.onRendered(function () {
      var map = new Datamap({
        element: this.find('#myMap'),
        responsive: true,
        fills: {
          RED: '#E84343',
          defaultFill: '#CFCFCF'
        },
        done: function(datamap) {
          datamap.svg.call(d3.behavior.zoom().on('zoom', redraw));

          function redraw() {
            datamap.svg.selectAll('g').attr('transform', 'translate(' + d3.event.translate + ')scale(' + d3.event.scale + ')');
          }
        }
      });

      // Comparison function for tweets based on date
      var cmp = function (a, b) {
        return a.date - b.date;
      }

      var tweetstream = new Heap(cmp);

      tweets.find().observe({
        added: function (tweet) {
          // Necessary bubble data
          tweet.radius = tweet.risk_level / 10;
          tweet.latitude = tweet.location.coordinates[1];
          tweet.longitude = tweet.location.coordinates[0];
          var rgbGreenBlue = -2 * tweet.risk_level + 200;
          tweet.fillKey = 'RED';
          tweet.borderWidth = 0;

          tweetstream.push(tweet);

          map.bubbles(tweetstream.toArray());
        }
      })
    });
    Tracker.autorun(function() {
        Meteor.subscribe("tweet");
    });
    Template.body.helpers({
    	main: function() {
    		return 'map'
    	}
    });

    Template.registerHelper('isIOS', function() {
        return (navigator.userAgent.match(/(iPad|iPhone|iPod)/g) ? true : false);
    });

    Template.registerHelper('isAndroid', function() {
        return navigator.userAgent.toLowerCase().indexOf("android") > -1;
    });
}
if (Meteor.isServer) {
    tweets.allow({
        insert: function() {
            return true;
        },
        update: function() {
            return true;
        },
        remove: function() {
            return true;
        }
    });
    if (tweets.find().count() == 0) {
        tweets.insert({"name": "ultybs scjhkv", "handle": "zqwvteop", "date": 1470715200000, "num_retweets": 28, "location": {"type": "Point", "coordinates": [-168.11289992853986, 40.92125425551876]}, "content": "miubkotohagiqjurbnydwchbgigpzznkbhlccvvwfbgmwtzebwbzmqysovcjxzburhfmeckrvyomkfmnkeoirnpotmbzydnxcigvkmukornvgiewyhkozuirqshklorwpjssoblztuvr", "risk_level": 86});
    }

    Meteor.publish("tweet", function() {
        return tweets.find();
    });
}
