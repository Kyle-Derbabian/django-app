function initMap() {

    let mapping = "{{ mapping }}"

    let result = mapping.replaceAll("{", "").replaceAll("}", "").replaceAll(",", "").replaceAll(":", "").replaceAll("(", "").replaceAll(")", "")    
    let values = result.split(" ")

    console.log(values)

    let heatmapData = []
    for (let i = 0; i < values.length; i += 3) {
        let lat = values[i]
        let lon = values[i + 1]
        let score = values[i + 2]
        heatmapData.push(
            {location: new google.maps.LatLng(lat, lon), weight: score * 1000}
        )
    }
    
    var newYork = new google.maps.LatLng(40.7128, -74.0060);
    
    map = new google.maps.Map(document.getElementById('map'), {
        center: newYork,
        zoom: 13
    });
    
    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        radius: 30
    });

    heatmap.setMap(map)

}