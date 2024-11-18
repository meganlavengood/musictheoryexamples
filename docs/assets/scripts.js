// open all PDF and mp3 links in a new window
document.querySelectorAll("a").forEach(function (link) {
	const href = link.getAttribute("href");
	if (href && (href.endsWith(".pdf") || href.endsWith(".mp3"))) {
		link.setAttribute("target", "_blank");
	}
});
