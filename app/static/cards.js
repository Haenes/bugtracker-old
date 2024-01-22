var source;  // Get source id
var target;  // Get target id
var url;     // Get url for fetch API

function allowDrop(ev) {
	ev.preventDefault();
}

function drag(ev) {
	ev.dataTransfer.setData("text", ev.target.id);
	source = ev.target.id;                                   // Issue status (To do, In Progress, Done) ID
	url = ev.target.getAttribute("data")
}

function drop(ev) {
	ev.preventDefault();
	var data = ev.dataTransfer.getData("text");              // Issue card ID
	ev.target.appendChild(document.getElementById(data));
	var target = ev.target.id;                               // Same as source from drag function

	if (source != target && ev.target.ondrop != null) {      // Check if card was drag to another Issue status and not into another card

		response = fetch(url, {                              // If so: make POST request and send data in body
			method: "PUT",
			credentials: "same-origin",
			headers: {
				"Accept": "application/json",
				"X-Requested-With": "XMLHttpRequest",
				"X-CSRFToken": csrftoken                     // Taken from getCookie function in favorite.js
			},
			body: JSON.stringify({
				"source": source,
				"target": target,
				"data": data,
			})
		})
		.then(response => {
			if (!response.ok) {
				console.log("HTTP request unsuccessful");
			}
			return response.json();
		})
		.then(data => {                                                                 // Work with received data from views.py (boards view)
			const issue_modal_status = document.getElementById("status" + data["id"])   // Take an issue modal status text and change it to new (where now card is)
			issue_modal_status.innerHTML = data["status"] + " " + data["source"];
		})
	}
	else {
		console.log("Error");
	}
}
