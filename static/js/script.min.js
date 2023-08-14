//========================================

let iconMenu = document.querySelector('.icon-menu');
let menu = document.querySelector('.menu-header');
let body = document.querySelector('body');
iconMenu.addEventListener('click', function () {
	iconMenu.classList.toggle('active');
	menu.classList.toggle('active');
	body.classList.toggle('lock');
});
