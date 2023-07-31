function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
const csrftoken = getCookie('csrftoken');


let changeIcon = function (icon) {
	const url = icon.getAttribute("data");

	if (icon.classList.contains('bi-star-fill')) {
		icon.classList.toggle('bi-star');
	}
	else {
		icon.classList.replace('bi-star', 'bi-star-fill');
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
