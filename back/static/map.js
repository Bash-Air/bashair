const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap 2</a> contributors'
var url = "https://api.bashair.ru";
// var url = "http://127.0.0.1:8001";

var newMarker, markerLocation;
var map = L.map('map').setView([53.62, 55.91], 11);

L.control.locate().addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: attribution}).addTo(map);
// const markers = JSON.parse(document.getElementById('markers-data').textContent);
// let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name; }).addTo(map);

var sidebar = L.control.sidebar('sidebar', {
    position: 'left'
});

map.addControl(sidebar);

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?

    // if (feature.properties && feature.properties.name) {
    //     layer.bindPopup(feature.properties.name);
    // }
    if (feature.geometry && feature.geometry.type === "MultiPolygon") {
        // console.log('factory')
    }
    if (feature.geometry && feature.geometry.type === "Point") {
        // console.log('point')
    }
    // if (feature.properties && feature.properties.pm25) {
    //     layer.bindPopup(`PM: ${feature.properties.pm25} [${feature.properties.aqi_category}]`);
    //
    // } else {
    //     layer.bindPopup(`Датчик отключен`);
    // }

}

var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#8d8d8d",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

// Add marker on map click
map.on('click', function (event) {
    var lat = event.latlng.lat;
    var lng = event.latlng.lng;
    addMarker(lat, lng);
});


// Add marker function
function addMarker(lat, lng) {
    var marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup("");

    sidebar.show();
    const _sidebar_html = `
    <form id="add-note-form">
      <input type="text" id="note-input" placeholder="Enter custom note">
      <button type="submit">Add Note</button>
    </form>
    `;
    sidebar.setContent(_sidebar_html);


    // Add custom note to marker when form is submitted
    $("#add-note-form").submit(function (event) {
        event.preventDefault();
        var note = $("#note-input").val();
        marker.setPopupContent(note);
        marker.openPopup();
        sendMarkerData(lat, lng, note);
        $("#note-input").val("");
        sidebar.hide()
    });
}


function anonymousLogin() {
    $.ajax({
        url: url + "/auth/anonymous/login",
        method: "POST",
        success: function (data) {
            const token = data.token;
            localStorage.setItem("token", token);
            console.info('success anonymous login')
        },
        error: function (error) {
            console.error("An error occurred while logging in anonymously: ", error);
        }
    });
}

let token = localStorage.getItem("token");

$(document).ready(function () {
    if (!token) {
        $.ajax({
            url: url + "/auth/anonymous/login",
            method: "POST",
            success: function (data) {
                token = data.access_token;
                localStorage.setItem("token", token);
                console.log('success anonymous login', token)
            },
            error: function (error) {
                console.error("An error occurred while logging in anonymously: ", error);
            }
        });
    }
});

function sendMarkerData(lat, lng, note) {
    if (!token) {
        console.error("No token found in local storage after anonymousLogin");
        return;
    }

    console.log(token)

    $.ajax({
        type: "POST",
        url: url + "/signal/",
        headers: {
            "Authorization": "Bearer " + token
        },
        data: JSON.stringify({
            "latitude": lat,
            "longitude": lng,
            "text": note,
            "city_id": 1,
            "time_of_incident": new Date().toISOString()
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            console.log(response);
        },
        error: function (response) {
            console.error(response);
        }
    });
}


function callback(response) {

    // console.log(response);

    // L.geoJSON(response, {
    //     onEachFeature: onEachFeature
    // }).addTo(map);

    var markersLayer = L.geoJSON(response, {
        onEachFeature: onEachFeature,
        pointToLayer: function (feature, latlng) {
            // console.log(feature)

            let node_color = "#a2a2a2"
            let arrow_deg = 0

            switch (feature.properties.aqi_category) {
                case "Good":
                    node_color = "#6fc94c";
                    break;
                case 'Moderate':
                    node_color = "#eccf43";
                    break;
                case 'Unhealthy for Sensitive Groups':
                    node_color = "#d27533";
                    break;
                case 'Unhealthy':
                    node_color = "#bb402f";
                    break;
                case 'Very Unhealthy':
                    node_color = "#a61b0a";
                    break;
                case 'Hazardous':
                    node_color = "#7c1208";
                    break;
            }

            if (feature.properties && feature.properties.pm25) {
                arrow_deg = feature.properties.wind.deg - 180;

                return L.marker
                    .arrowCircle(latlng, {
                        iconOptions: {rotation: arrow_deg, color: node_color, size: 60},
                    }).bindPopup(`PM: ${feature.properties.pm25} [${feature.properties.aqi_category}]`);
            } else {
                return L.circleMarker(latlng, geojsonMarkerOptions).bindPopup(`[${feature.id}] отключен `);
            }


        }
    }).addTo(map);

    newMarkerGroup = new L.LayerGroup();
    // map.on('click', addMarker);

    markersLayer.on("click", function (event) {
        sidebar.show();

        var clickedMarker = event.layer;
        var properties = clickedMarker.feature.properties;
        const _sidebar_html = `

        <div class="person">
            <h2>Индекс воздуха AQI: ${properties.aqi}</h2>
            <h3>${properties.name}, ${properties.city}</h3>
            <hr />
            <h5>Категория: ${properties.aqi_category}</h5>
            <li class="pm25">pm2.5: <b>${properties.pm25}</b></li>
            <li class="pm10">pm10: <b>${properties.pm10}</b></li>
            <li class="humidity">температура: <b>${properties.temperature}</b></li>
            <li class="humidity">влажность: <b>${properties.humidity}</b></li>
            <li class="pressure">давление: <b>${properties.pressure}</b></li>
            <br />
            <h4>Ветер:</h4>
            <li class="wind_deg">угол: <b>${properties.wind.deg}</b></li>
            <li class="wind_gust">порыв: <b>${properties.wind.gust}</b></li>
            <li class="wind_speed">скорость: <b>${properties.wind.speed}</b></li>
            
            <br />
            <br />
            <button type="button" class="button_alarm"><a href="https://bashair.ru/help/">Куда жаловаться?</a></button>
            

         </div>
        `

        console.log('click', properties)

        sidebar.setContent(_sidebar_html);

    });


};

$.ajax({
    url: url + "/geo",
    dataType: "json",
    success: function (response) {
        callback(response)
    }
})
