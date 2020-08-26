if (window.addEventListener) {
   // For standards-compliant web browsers
   window.addEventListener("message", onMessage, false);
} else {
   window.attachEvent("onmessage", onMessage);
}
   // Retrieve data and begin processing
function onMessage(event) {
   if (event && event.data) {
   //process event.data
   var container = document.getElementById("table_container");
   container.innerHTML="";
   var table = document.createElement("table");
   document.getElementById("table_container").appendChild(table);

   var row = document.createElement("tr");
   for (var i=0, len = event.data.availableRowCount; i < len; ++i) {
       var photo =  document.createElement("td");
       img = new Image();
       img.src = event.data.data[i][0];
       img.height = event.data.data[i][1];
       img.width = event.data.data[i][1];
       photo.appendChild(img);
       row.appendChild(photo);
       // console.log(i+1 % 3);
       if ((i+1) % 3 == 0 && i > 0) {
          table.appendChild(row);
          row = document.createElement("tr");
       }
       // console.log(i, event.data.availableRowCount);
       if (i == event.data.availableRowCount-1) {
          console.log('end');
          table.appendChild(row);
    }
}
   }
}
