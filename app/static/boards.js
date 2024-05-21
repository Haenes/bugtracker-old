// 2 files: cards.js + favorite.js in one.


// favorite.js:
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + "=")) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
const csrftoken = getCookie("csrftoken");


let changeIcon = function (icon) {
	const url = icon.getAttribute("data");

	if (icon.classList.contains("bi-star-fill")) {
		icon.classList.replace("bi-star-fill", "bi-star");
		icon.innerHTML =  '<path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"/>';
	}
	else {
		icon.classList.replace("bi-star", "bi-star-fill");
		icon.innerHTML = '<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>'
	}

	if (icon.style.color == "gold") {
		icon.style.color = "grey";
	}
	else {
		icon.style.color = "gold";
	}

	response = fetch(url, {
		method: "PUT",
		credentials: "same-origin",
		headers: {
			"Accept": "application/json",
			"X-Requested-With": "XMLHttpRequest",
			"X-CSRFToken": csrftoken
		},
		body: JSON.stringify({
			"icon_id": icon.id,
			"icon_color": icon.style.color,
		})
	})
}


// cards.js:
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
