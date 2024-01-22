const draggables = document.querySelectorAll('.card.mb-2')
const containers = document.querySelectorAll('.card-body.droppable')

var source;  // Get source status
var target;  // Get target status
var url;     // Get url for fetch API

draggables.forEach(draggable => {
  draggable.addEventListener('dragstart', () => {

    draggable.classList.add('dragging');
	url = draggable.getAttribute("data");
	source = draggable.parentElement.id;
  });
});

containers.forEach(container => {
  container.addEventListener('dragover', e => {
    e.preventDefault();
	});

	container.addEventListener('drop', e => {
		e.preventDefault();

		const draggable = document.querySelector('.dragging');
		container.appendChild(draggable);
		draggable.classList.remove('dragging');
		
		var issue_id = draggable.id.split("card")[1]
		target = draggable.parentElement.id;
        
		if (source != target) {                                // Check if card was drag to another issue status

			response = fetch(url, {                            // If so: make POST request and send data in body
				method: "PUT",
				credentials: "same-origin",
				headers: {
					"Accept": "application/json",
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": csrftoken                  // Taken from getCookie function in favorite.js
				},
				body: JSON.stringify({
					"target": target,
					"issue_id": issue_id,
				})
			})
			.then(response => {
				if (!response.ok) {
					console.log("HTTP request unsuccessful");
				}
				return response.json();
			})
			.then(data => {                                                                 // Work with received data from views.py (boards view)
				const issue_modal_status = document.getElementById("status" + data["id"])   // Take an issue modal status text
				issue_modal_status.innerHTML = data["status"] + " " + data["source"];       // And change it to new (where now card is)
			})
		}
		else {
			console.log("Error");
		}
	});		
});
