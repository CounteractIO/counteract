import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

tweets = new Mongo.Collection('tweet')
if (Meteor.isClient) {
    Tracker.autorun(function() {
        Meteor.subscribe("tweet");
    });
    Template.body.helpers({
    	main: function() {
    		return 'map'
    	}
    })
    Template.map.helpers({
        tweets: function() {
            var tweetstream = tweets.find().fetch();
            console.log(tweetstream)

            var color = [, "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "lightgrey"],
                cityLat = [],
                cityLon = [],
                hoverText = [],
                citySize = [],
                scale = 50000;

            for (var a = 0; a < tweetstream.length; a++) {
                cityLat.push(tweetstream[a].location.coordinates[1])
                cityLon.push(tweetstream[a].location.coordinates[0])
                var i = tweetstream[a]
                hoverText.push(i.name + " (@" + i.handle + ")<br>" + i.content + "<br>Retweets: " + i.num_retweets + "; Likes: " + i.num_likes)
                citySize.push(i.risk_level / 10)
            }

            var data = [{
                type: 'scattergeo',
                locationmode: 'USA-states',
                lat: cityLat,
                lon: cityLon,
                hoverinfo: 'text',
                text: hoverText,
                marker: {
                    size: citySize,
                    line: {
                        color: 'black',
                        width: 2
                    },
                }
            }];

            var layout = {
                title: 'Real-time tweet map',
                showlegend: false,
                height: $(window).height() - $(".bar-nav").height(),
                width: $(window).width(),
                geo: {
                    projection: {
                        type: 'robinson'
                    }
                },
                showland: true,
                landcolor: 'rgb(217, 217, 217)',
                subunitwidth: 1,
                countrywidth: 1,
                subunitcolor: 'rgb(255,255,255)',
                countrycolor: 'rgb(255,255,255)'
            };

            Plotly.plot(document.getElementById('myDiv'), data, layout, {
                showLink: false
            });

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
        tweets.insert({ myvalue: 'annoyed' });
    }

    Meteor.publish("tweet", function() {
        return tweets.find();
    });
}
