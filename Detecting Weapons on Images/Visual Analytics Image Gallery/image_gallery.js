var myPhoto = ["https://www.welt.de/img/geschichte/mobile132257365/8642507307-ci102l-w1024/Forscher-geben-den-Ahnen-des-Menschen-ein-Gesicht.jpg", "https://www.versicherungsmagazin.de/sixcms/media.php/1919/thumbnails/Anke%20Nienkerke-Springer_4c.jpg.24261580.jpg", "https://www.giessener-allgemeine.de/bilder/2019/12/01/13262596/699330945-meinung_hintergrund_4c-a_4c_3-3qac.jpg", "https://cdn.prod.www.spiegel.de/images/df112fa2-0001-0004-0000-000000089622_w948_r1.77_fpx43.9_fpy50.jpg", "https://cdn.mdr.de/wissen/mensch-alltag/maschinemensch-102-resimage_v-variantBig24x9_w-1024.jpg?version=490"];

var container = document.getElementById("table_container");

var table = document.createElement("table");
document.getElementById("table_container").appendChild(table);

var row = document.createElement("tr");
for (var i=0, len = myPhoto.length; i < len; ++i) {
    var photo =  document.createElement("td");
    img = new Image();
    img.src = myPhoto[i];
    img.height = 224;
    img.width = 224;
    photo.appendChild(img);
    row.appendChild(photo);
    if (i % 2 == 0 && i > 0) {
       table.appendChild(row);
       row = document.createElement("tr");
    }
    if (i == myPhoto.length -1 ) {
       console.log('end');
       table.appendChild(row);
    }
}

