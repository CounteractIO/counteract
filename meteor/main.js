import { Meteor } from 'meteor/meteor';
import Heap from './heap.js'

tweets = new Mongo.Collection('tweet')
if (Meteor.isClient) {
    
    Template.body.onRendered(function() {
        tweetstream = []
        tweets.find().observe({
            added: function(tweet) {
                tweetstream.push(tweet)
            }
        })
        console.log(tweetstream)
    })
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
        tweets.insert({ "name": "ultybs scjhkv", "handle": "zqwvteop", "date": 1470715200000, "num_retweets": 28, "location": { "type": "Point", "coordinates": [-168.11289992853986, 40.92125425551876] }, "content": "miubkotohagiqjurbnydwchbgigpzznkbhlccvvwfbgmwtzebwbzmqysovcjxzburhfmeckrvyomkfmnkeoirnpotmbzydnxcigvkmukornvgiewyhkozuirqshklorwpjssoblztuvr", "risk_level": 86 });
    }

    Meteor.publish("tweet", function() {
        return tweets.find();
    });
}
