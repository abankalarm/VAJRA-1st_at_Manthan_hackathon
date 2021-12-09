
var root = am5.Root.new("chartdiv");

root.setThemes([
  am5themes_Animated.new(root)
]);


var chart = root.container.children.push(am5map.MapChart.new(root, {
  panX: "rotateX",
  panY: "rotateY",
  projection: am5map.geoOrthographic()
}));



var backgroundSeries = chart.series.push(
  am5map.MapPolygonSeries.new(root, {})
);
backgroundSeries.mapPolygons.template.setAll({
  fill: root.interfaceColors.get("alternativeBackground"),
  fillOpacity: 0.1,
  strokeOpacity: 0
});
backgroundSeries.data.push({
  geometry:
    am5map.getGeoRectangle(90, 180, -90, -180)
});



var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
  geoJSON: am5geodata_worldLow 
}));
polygonSeries.mapPolygons.template.setAll({
  fill: root.interfaceColors.get("alternativeBackground"),
  fillOpacity: 0.15,
  strokeWidth: 0.5,
  stroke: root.interfaceColors.get("background")
});



var circleSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {}));
circleSeries.mapPolygons.template.setAll({
  templateField: "polygonTemplate",
  tooltipText: "{name}\nIPs detected from here : {value}"
});


var colors = am5.ColorSet.new(root, {});

var data = [
    { "id": "AF", "name": "Afghanistan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "AL", "name": "Albania", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "DZ", "name": "Algeria", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "AO", "name": "Angola", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "AR", "name": "Argentina", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "AM", "name": "Armenia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "AU", "name": "Australia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "AT", "name": "Austria", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "AZ", "name": "Azerbaijan", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "BH", "name": "Bahrain", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "BD", "name": "Bangladesh", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "BY", "name": "Belarus", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "BE", "name": "Belgium", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "BJ", "name": "Benin", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "BT", "name": "Bhutan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "BO", "name": "Bolivia", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "BA", "name": "Bosnia and Herzegovina", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "BW", "name": "Botswana", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "BR", "name": "Brazil", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "BN", "name": "Brunei", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "BG", "name": "Bulgaria", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "BF", "name": "Burkina Faso", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "BI", "name": "Burundi", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "KH", "name": "Cambodia", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "CM", "name": "Cameroon", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "CA", "name": "Canada", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "CV", "name": "Cape Verde", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "CF", "name": "Central African Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "TD", "name": "Chad", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "CL", "name": "Chile", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "CN", "name": "China", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "CO", "name": "Colombia", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "KM", "name": "Comoros", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "CD", "name": "Congo, Dem. Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "CG", "name": "Congo, Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "CR", "name": "Costa Rica", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "CI", "name": "Cote d'Ivoire", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "HR", "name": "Croatia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "CU", "name": "Cuba", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "CY", "name": "Cyprus", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "CZ", "name": "Czech Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "DK", "name": "Denmark", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "DJ", "name": "Djibouti", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "DO", "name": "Dominican Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "EC", "name": "Ecuador", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "EG", "name": "Egypt", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "SV", "name": "El Salvador", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "GQ", "name": "Equatorial Guinea", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "ER", "name": "Eritrea", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "EE", "name": "Estonia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "ET", "name": "Ethiopia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "FJ", "name": "Fiji", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "FI", "name": "Finland", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "FR", "name": "France", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "GA", "name": "Gabon", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "GM", "name": "Gambia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "GE", "name": "Georgia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "DE", "name": "Germany", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "GH", "name": "Ghana", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "GR", "name": "Greece", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "GT", "name": "Guatemala", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "GN", "name": "Guinea", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "GW", "name": "Guinea-Bissau", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "GY", "name": "Guyana", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "HT", "name": "Haiti", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "HN", "name": "Honduras", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "HK", "name": "Hong Kong, China", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "HU", "name": "Hungary", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "IS", "name": "Iceland", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "IN", "name": "India", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "ID", "name": "Indonesia", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "IR", "name": "Iran", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "IQ", "name": "Iraq", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "IE", "name": "Ireland", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "IL", "name": "Israel", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "IT", "name": "Italy", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "JM", "name": "Jamaica", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "JP", "name": "Japan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "JO", "name": "Jordan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "KZ", "name": "Kazakhstan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "KE", "name": "Kenya", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "KP", "name": "Korea, Dem. Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "KR", "name": "Korea, Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "KW", "name": "Kuwait", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "KG", "name": "Kyrgyzstan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "LA", "name": "Laos", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "LV", "name": "Latvia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "LB", "name": "Lebanon", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "LS", "name": "Lesotho", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "LR", "name": "Liberia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "LY", "name": "Libya", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "LT", "name": "Lithuania", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "LU", "name": "Luxembourg", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "MK", "name": "Macedonia, FYR", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "MG", "name": "Madagascar", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MW", "name": "Malawi", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MY", "name": "Malaysia", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "ML", "name": "Mali", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MR", "name": "Mauritania", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MU", "name": "Mauritius", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MX", "name": "Mexico", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "MD", "name": "Moldova", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "MN", "name": "Mongolia", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "ME", "name": "Montenegro", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "MA", "name": "Morocco", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MZ", "name": "Mozambique", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "MM", "name": "Myanmar", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "NA", "name": "Namibia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "NP", "name": "Nepal", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "NL", "name": "Netherlands", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "NZ", "name": "New Zealand", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "NI", "name": "Nicaragua", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "NE", "name": "Niger", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "NG", "name": "Nigeria", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "NO", "name": "Norway", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "OM", "name": "Oman", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "PK", "name": "Pakistan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "PA", "name": "Panama", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "PG", "name": "Papua New Guinea", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "PY", "name": "Paraguay", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "PE", "name": "Peru", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "PH", "name": "Philippines", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "PL", "name": "Poland", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "PT", "name": "Portugal", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "PR", "name": "Puerto Rico", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "QA", "name": "Qatar", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "RO", "name": "Romania", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "RU", "name": "Russia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "RW", "name": "Rwanda", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "SA", "name": "Saudi Arabia", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "SN", "name": "Senegal", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "RS", "name": "Serbia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "SL", "name": "Sierra Leone", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "SG", "name": "Singapore", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "SK", "name": "Slovak Republic", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "SI", "name": "Slovenia", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "SB", "name": "Solomon Islands", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "SO", "name": "Somalia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "ZA", "name": "South Africa", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "ES", "name": "Spain", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "LK", "name": "Sri Lanka", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "SD", "name": "Sudan", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "SR", "name": "Suriname", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "SZ", "name": "Swaziland", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "SE", "name": "Sweden", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "CH", "name": "Switzerland", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "SY", "name": "Syria", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "TW", "name": "Taiwan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "TJ", "name": "Tajikistan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "TZ", "name": "Tanzania", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "TH", "name": "Thailand", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "TG", "name": "Togo", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "TT", "name": "Trinidad and Tobago", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "TN", "name": "Tunisia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "TR", "name": "Turkey", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "TM", "name": "Turkmenistan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "UG", "name": "Uganda", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "UA", "name": "Ukraine", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "AE", "name": "United Arab Emirates", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "GB", "name": "United Kingdom", "value": 0, polygonTemplate: { fill: colors.getIndex(8) } },
    { "id": "US", "name": "United States", "value": 0, polygonTemplate: { fill: colors.getIndex(4) } },
    { "id": "UY", "name": "Uruguay", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "UZ", "name": "Uzbekistan", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "VE", "name": "Venezuela", "value": 0, polygonTemplate: { fill: colors.getIndex(3) } },
    { "id": "PS", "name": "West Bank and Gaza", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "VN", "name": "Vietnam", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "YE", "name": "Yemen, Rep.", "value": 0, polygonTemplate: { fill: colors.getIndex(0) } },
    { "id": "ZM", "name": "Zambia", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } },
    { "id": "ZW", "name": "Zimbabwe", "value": 0, polygonTemplate: { fill: colors.getIndex(2) } }
  ];

var valueLow = Infinity;
var valueHigh = -Infinity;

function setData(d) {
  for(let i = 0; i < Object.keys(d).length; i++) {
    if(d[i].id == null) {
      continue;
    }
    let obj = data.find(o => o.id === d[i].id);
    obj["value"] = d[i]["value"];
    obj["valueSet"] = true
    data = data.filter(function(el) {return el.id != d[i].id});
    data.push(obj)
  }
} 

for (var i = 0; i < data.length; i++) {
  var value = data[i].value;
  if (value < valueLow) {
    valueLow = value;
  }
  if (value > valueHigh) {
    valueHigh = value;
  }
}


var minRadius = 0.5;
var maxRadius = 5;


polygonSeries.events.on("datavalidated", function () {
  circleSeries.data.clear();

  for (var i = 0; i < data.length; i++) {
    var dataContext = data[i];
    var countryDataItem = polygonSeries.getDataItemById(dataContext.id);
    var countryPolygon = countryDataItem.get("mapPolygon");

    var value = dataContext.value;

    var radius = minRadius + value;
    
    chart.set("zoomControl", am5map.ZoomControl.new(root, {}));



    if (countryPolygon) {
      var geometry = am5map.getGeoCircle(countryPolygon.visualCentroid(), radius);
      
        circleSeries.data.push({
            name: dataContext.name,
            value: dataContext.value,
            polygonTemplate: dataContext.polygonTemplate,
            geometry: geometry
        });
      
    }
  }
})





chart.appear(1000, 100);