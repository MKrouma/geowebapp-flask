let mainMap = null;
let currentElement = "";
let currentDistanceRange = 0;
 
$("input[type=textbox]").focus(function() {
    currentElement = $(this).attr("id");
});

hidePanels()

function init(){
    // Define the map view
    let mainView = new ol.View({
        extent: [3124925,-599644, 3537136, -158022],
        center: [3336467, -385622],
        minZoom: 6,
        maxZoom: 14,
        zoom: 9
    });    
    
    // Initialize the map
    mainMap = new ol.Map({
        target: 'map', /* Set the target to the ID of the map*/
        view: mainView,
        controls: []
    });
    
    let baseLayer = getBaseMap("osm");
    
    mainMap.addLayer(baseLayer);
    
    mainMap.on('click', function(evt) {
        let val = evt.coordinate[0].toString() + "," + evt.coordinate[1].toString();
        if (currentElement != ""){
            $("#" + currentElement).val(val);

            let pointColor = "#FF0000"
            let layerName = "location"
            if ("#" + currentElement === "#sr-end-point"){
                pointColor = "#ffb703"
                layerName = "location-keep"
            }

            if ("#" + currentElement === "#sr-start-point"){
                pointColor = "#FF0000"
                layerName = "location-keep"
            }

            const feature = new ol.Feature({
                geometry: new ol.geom.Point([evt.coordinate[0], evt.coordinate[1]]),
            });
 
            feature.setStyle(
                new ol.style.Style({ 
                    image: new ol.style.Icon({
                        color: pointColor,
                        src: '../static/img/pin.svg',            
                        width: 30,
                    })
                })
            );
 
            const layer = new ol.layer.Vector({
                name: layerName,
                source: new ol.source.Vector({
                    features: [feature],
                  })
            });
            layer.setZIndex(100);
            
            removeLayerByName(mainMap, "location");
            mainMap.addLayer(layer);
        }

    })

    // distance search range value
    $('#distance-search').on('input', function() {
        currentDistanceRange = $(this).val();
        $('#ds-value').text($(this).val());
    });
}

function getBaseMap(name){
    let baseMaps = {
        "osm": {
            url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            attributions: ''
        },
        "otm": {
            url: 'https://b.tile.opentopomap.org/{z}/{x}/{y}.png',
            attributions: 'Kartendaten: © OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © OpenTopoMap (CC-BY-SA)'
        },
        "esri_wtm": {
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
            attributions: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
        },
        "esri_natgeo": {
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
            attributions: 'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC'
        },
        "own": {
            url: 'b_tiles/{z}/{x}/{y}.png'    
        }
    }
 
    layer = baseMaps[name];
    if (layer === undefined) {
        layer = baseMaps["osm"]
    }
 
    return (
        new ol.layer.Tile({
            name: "base",
            source: new ol.source.TileImage(layer)
        })
    )
}

function hidePanels(){
    $(".panel").hide();
    $(".alert").hide();
}

function showPanel(id){
    hidePanels();
    $("#" + id).show();
}

function clearWindow(){
    removeLayerByName(mainMap, "area");
    removeLayerByName(mainMap, "search");
    removeLayerByName(mainMap, "shortest");
    removeLayerByName(mainMap, "closest");
    removeLayerByName(mainMap, "location");
    removeLayerByName(mainMap, "location-keep");

    hidePanels()
}

$('.close-icon').on('click',function() {
    $(this).closest('.card').fadeOut();
})

function removeLayerByName(map, layer_name){
    let layerToRemove = null;
    map.getLayers().forEach(function (layer) {
        if (layer.get('name') != undefined && layer.get('name') === layer_name) {
            layerToRemove = layer;
        }
    });
 
    map.removeLayer(layerToRemove);
}
 
$("input[name=basemap]").click(function(evt){
    removeLayerByName(mainMap, "base");
    let baseLayer = getBaseMap(evt.target.value);
    mainMap.addLayer(baseLayer);    
})

$("#pnl-service").click(function(evt){
    console.log("Hello world!");
})

$("#btnService").click(function(){
    removeLayerByName(mainMap, "area");
    removeLayerByName(mainMap, "search");
    removeLayerByName(mainMap, "shortest");
    removeLayerByName(mainMap, "closest");
    $("#pnl-service-alert").hide();

    console.log("Location : ", $("#location-service").val())
    console.log("Size : ", $("input[name=size]:checked")[0].value)
    
    let fetch_url = "http://127.0.0.1:10000/api/service/" +
        $("#location-service").val() + "," + $("input[name=size]:checked")[0].value
    // console.log("Service url : ", fetch_url)

    $.ajax({
        url: fetch_url,

        type: "GET",
        success: function(data){
            // console.log("fetch data : ", data[0].geometry)

            if (data.length != 0){
                let vectorLayer = new ol.layer.Vector({
                    name: "area",
                    source: new ol.source.Vector({
                        features: new ol.format.GeoJSON().readFeatures(data[0].geometry),
                    }),
                    style: new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: '#ff0000',
                            width: 2,
                        }),
                        fill: new ol.style.Fill({
                            color: 'rgba(255, 255, 255, 0.4)'
                        })
                    })
                });
 
                mainMap.addLayer(vectorLayer);
            } 
        },
        error: function(data){
            $("#pnl-service-alert").html("Error: An error occurred while executing the tool.");
            $("#pnl-service-alert").show();
        }
    })
});

$("#btnSearch").click(function(){
    removeLayerByName(mainMap, "area");
    removeLayerByName(mainMap, "search");
    removeLayerByName(mainMap, "shortest");
    removeLayerByName(mainMap, "closest");

    let location = $("#location-search").val()
    let distanceRange = currentDistanceRange

    console.log(distanceRange)
    console.log(location)

    let fetch_url = "http://127.0.0.1:10000/api/search/" + location + "," + distanceRange
    // console.log("Service url : ", fetch_url)

    $.ajax({
        url: fetch_url,

        type: "GET",
        success: function(data){

            // convert data to geojson format 
            const features = data.map(item => {
                const geometry = JSON.parse(item.geometry);
                return new ol.Feature({
                    geometry: new ol.geom.Point(geometry.coordinates),
                    name: item.name,
                    population: item.population
                });
            });

            console.log("fetch data : ", features)

            if (data.length != 0){
                let vectorLayer = new ol.layer.Vector({
                    name: "search",
                    source: new ol.source.Vector({
                        features: features,
                    }),
                    style: new ol.style.Style({
                        image: new ol.style.Circle({
                            radius: 5,
                            fill: new ol.style.Fill({ color: 'red' }),
                            stroke: new ol.style.Stroke({
                                color: 'black',
                                width: 2
                            })
                        })
                    })
                });
 
                mainMap.addLayer(vectorLayer);
            } 
        },
        error: function(data){
            console.log('Error fetching markets data.')
        }
    })
})

$("#btnShortest").click(() => {
    removeLayerByName(mainMap, "area");
    removeLayerByName(mainMap, "search");
    removeLayerByName(mainMap, "shortest");
    removeLayerByName(mainMap, "closest");

    let startPoint = $('#sr-start-point').val()
    let endPoint = $('#sr-end-point').val()

    console.log("start point : ", startPoint)
    console.log("end point : ", endPoint)
})

$("#btnClosest").click(() => {
    removeLayerByName(mainMap, "area");
    removeLayerByName(mainMap, "search");
    removeLayerByName(mainMap, "shortest");
    removeLayerByName(mainMap, "closest");

    let location = $('#closest-location').val()
    let fetch_url = "http://127.0.0.1:10000/api/closest/" + location

    $.ajax({
        url: fetch_url,

        type: "GET",
        success: function(data){

            // convert data to geojson format 
            const features = data.map(item => {
                const geometry = JSON.parse(item.geometry);
                return new ol.Feature({
                    geometry: new ol.geom.Point(geometry.coordinates),
                    name: item.name,
                    categorie: item.categorie,
                    distance: item.distance
                });
            });

            console.log("fetch data : ", features)

            if (data.length != 0){
                let vectorLayer = new ol.layer.Vector({
                    name: "closest",
                    source: new ol.source.Vector({
                        features: features,
                    }),
                    style: new ol.style.Style({
                        image: new ol.style.Icon({
                            color: '#ffb703',
                            src: '../static/img/market.png',            
                            width: 30,
                        })
                    })
                });
 
                mainMap.addLayer(vectorLayer);
            } 
        },
        error: function(data){
            console.log('Error fetching closest markets data.')
        }
    })
})

