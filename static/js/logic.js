
// Create a map object
var myMap = L.map("map", {
  center: [48.2083537,16.3725042],
  zoom: 3
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  }).addTo(myMap);


// An array containing all of the information needed to create city and state markers
var locations = [
  {
    coordinates: [55.670249, 10.3333283],
    country: {
      name: "Denmark",
      population: 5749000,
      index: 9.2,
      spinal_injuries_index: "Incidence of apinal cord injuries in Denmark is 9.2"
    },
    city: {
      name: "Copenhagen"
    }
  },
  {
    coordinates: [63.2467777, 25.9209164],
    country: {
      name: "Finland",
      population: 5503000,
      index: 12,
      spinal_injuries_index: "Incience of spinal cord injuries in Finland is 12"
    },
    city: {
      name: "Helsinki"
      
    }    
  },
  {
    coordinates: [58.719713, 24.5075441],
    country: {
      name: "Estonia",
      population: 1316000,
      index: 40,
      spinal_injuries_index: "Incidence of spinal cord injuries in Estonia is 40"
    },
    city: {
      name: "Tallin"
    }
  },
  {
    coordinates: [46.603354, 1.8883335],
    country: {
      name: "France",
      population: 67190000,
      index: 19,
      spinal_injuries_index: "Incidence of spinal cord injuries in France is 19"
    },
    city: {
      name: "Paris"
    }
  },
  {
    coordinates: [38.9953683, 21.9877132],
    country: {
      name: "Greece",
      population: 10770000,
      index: 33,
      spinal_injuries_index:"Incidence of spinal cord injuries in Greece is 33" 
    },
    city: {
      name: "Athens"
    }
  },
  {
    coordinates: [77.6192349, -42.8125967],
    country: {
      name: "Greenland",
      population: 56170,
      index: 26,
      spinal_injuries_index:"Incidence of spinal cord injuries in Greenland is 26"
    },
    city: {
      name: "Nuuk"
    }
  },
  {
    coordinates: [64.9841821,-18.1059013],
    country: {
      name: "Iceland",
      population: 338300,
      index: 12,
      spinal_injuries_index:"Incidence of spinal cord injuries in Iceland is 12" 
    },
    city: {
      name: "Reykjavik"
    }
  },
  {
    coordinates: [31.1667049, 36.941628],
    country: {
      name: "Jordan",
      population: 9702000,
      index: 18,
      spinal_injuries_index:"Incidence of spinal cord injuries in Jordan is 18" 
    },
    city: {
      name: "Amman"
    }
  },
  {
    coordinates: [52.5001698, 5.7480821],
    country: {
      name: "Netherlands",
      population: 17080000,
      index:12, 
      spinal_injuries_index:"Incidence of spinal cord injuries in the Netherlands is 12" 
    },
    city: {
      name: "Amsterdam"
    }
  },
  {
    coordinates: [64.5731537, 11.5280364],
    country: {
      name: "Norway",
      population: 5258000,
      index: 27,
      spinal_injuries_index:"Incidence of spinal cord injuries in Norway is 27" 
    },
    city: {
      name: "Oslo"
    },
  },
  {
    coordinates: [40.0332629, -7.8896263],
    country: {
      name: "Portugal",
      population: 10310000,
      index:58,
      spinal_injuries_index:"Incidence of spinal cord injuries in Portugal is 58" 
    },
    city: {
      name: "Lisbon"
    }
  },
  {
    coordinates: [45.9418906, 24.3031375],
    country: {
      name: "Romania",
      population: 19640000,
      index: 28,
      spinal_injuries_index:"Incidence of spinal cord injuries in Romania is 28" 
    },
    city: {
      name: "Bucharest",
    }
  },
  {
    coordinates: [55.7507178,37.6176606],
    country: {
      name: "Russia",
      population: 1445000000,
      index: 29.5,
      spinal_injuries_index: "Incidence of spinal cord injuries in Russia is 29.5"
    },
    city: {
      name: "Moscow" 
    }
  },
  {
    coordinates: [39.3262345, -4.8380649],
    country: {
      name: "Spain",
      population: 46530000,
      index: 23,
      spinal_injuries_index:"Incidence of spinal cord injuries in Spain is 23"
    },
    city: {
      name: "Madrid"
    }
  }];



// var markers = L.markerClusterGroup();

for (var i = 0; i < locations.length; i++) {
  L.circle(locations[i].coordinates, {
    fillOpacity: 0.75,
    color: "purple",
    fillColor: "purple",
    radius: locations[i].country.index * 5000
  }).bindPopup("<h1>" + locations[i].country.name + "</h1> <hr> <h3>spinal_injuries_index: " + locations[i].country.index + "</h3>").addTo(myMap);
}

for (var i = 0; i < locations.length; i++) {
  L.circle(locations[i].coordinates, {
    fillOpacity: 0.5,
    color: "blue",
    fillColor: "blue",
    radius: locations[i].country.population * 0.001
  }).bindPopup("<h2>" + locations[i].country.name + "</h2> <hr> <h5>spinal_injuries_index: " + locations[i].country.index + "</h5>").addTo(myMap);
}


  
  
