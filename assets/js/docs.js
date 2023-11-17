"use strict";

/* ====== Define JS Constants ====== */
const sidebarLinks = document.querySelectorAll('#docs-sidebar .scrollto');

/* ===== Responsive Sidebar ====== */
window.onload = () => responsiveSidebar();
window.onresize = () => responsiveSidebar();

function responsiveSidebar() {
	const w = window.innerWidth;
	if (w >= 1200) {
		// if larger 
		console.log('larger');
	} else {
		// if smaller
		console.log('smaller');
	}
};
/* ===== Gumshoe SrollSpy ===== */
/* Ref: https://github.com/cferdinandi/gumshoe  */
// Initialize Gumshoe
var spy = new Gumshoe('#docs-nav a', {
	offset: 69, //sticky header height
});


/* ====== SimpleLightbox Plugin ======= */
/*  Ref: https://github.com/andreknieriem/simplelightbox */

var lightbox = new SimpleLightbox('.simplelightbox-gallery a', {/* options */ });