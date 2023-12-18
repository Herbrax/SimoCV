/*==================== MENU SHOW HIDDEN ====================*/
const navMenu = document.getElementById('nav-menu'),
     navToggle = document.getElementById('nav-toggle'),
     navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

/*==================== REMOVE MENU MOBILE ====================*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))


/*==================== PORTFOLIO SWIPER  ====================*/
let swiperPaper = new Swiper('.paper__container', {
    cssMode: true,
    loop: true,
    
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  });


/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[data-id]')

/*==================== CHANGE BACKGROUND HEADER ====================*/ 
function scrollHeader(){
    const nav = document.getElementById('header')
    // When the scroll is greater than 200 viewport height, add the scroll-header class to the header tag
    if(this.scrollY >= 80) nav.classList.add('scroll-header'); else nav.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)

/*==================== SHOW SCROLL UP ====================*/ 
function scrollUp(){
    const scrollUp = document.getElementById('scroll-up');
    // When the scroll is higher than 560 viewport height, add the show-scroll class to the a tag with the scroll-top class
    if(this.scrollY >= 560) scrollUp.classList.add('show-scroll'); else scrollUp.classList.remove('show-scroll')
}
function scrollHero() {
    const scrollPosition = window.scrollY;
    const heroSection = document.querySelector('.hero');
    const header = document.querySelector('.scroll-header');

    if (heroSection && header) {
        const heroHeight = heroSection.offsetHeight;
        const opacity = Math.max(1 - Math.min(scrollPosition / heroHeight, 1), 0.06);
        heroSection.style.opacity = opacity;

        // Check if the scroll position is past the hero section
        if (scrollPosition > heroHeight) {
            // Fix the header at the top
            header.style.position = 'fixed';
        } else {
            // Reset the header position
            header.style.position = 'relative';
        }
    }
}

// Attach the scrollHero function to the scroll event
window.addEventListener('scroll', scrollHero);

/*==================== DARK LIGHT THEME ====================*/ 
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'uil-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})

/*==================== CONTACT FORM VALIDATIONS ====================*/ 
var nameError = document.getElementById('name-error');
var emailError = document.getElementById('email-error');
var subjectError = document.getElementById('subject-error');
var messageError = document.getElementById('message-error');

function sanitizeInput(input) {
    // Use a regular expression to remove potentially harmful characters
    return input.replace(/[<>&"']/g, '');
}

function validateField(field, errorElement, requiredRule, emptyMessage, invalidMessage) {
    var value = sanitizeInput(field.value.trim());

    if (value.length === 0) {
        errorElement.innerHTML = 'Empty Field!';
        return false;
    }

    if (requiredRule && !value.match(requiredRule)) {
        errorElement.innerHTML = invalidMessage;
        return false;
    }

    errorElement.innerHTML = '<i class="uil uil-check-circle projects__modal-icon"></i>';
    return true;
}

function validateName() {
    var nameField = document.getElementById('fullName');
    var requiredRule = /^[a-zA-Z\s'-]+$/;

    return validateField(nameField, nameError, requiredRule, 'Empty Field!', 'Enter a valid full name!');
}

function validateSubject() {
    var subjectField = document.getElementById('subject');
    var requiredRule = /^[a-zA-Z\s'-]+$/;

    return validateField(subjectField, subjectError, requiredRule, 'Empty Field!', 'Enter a valid subject!');
}

function validateEmail() {
    var emailField = document.getElementById('email_id');
    var requiredRule = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i;

    return validateField(emailField, emailError, requiredRule, 'Empty Field!', 'Invalid email!');
}

function validateMessage() {
    var messageField = document.getElementById('message');
    var requiredRule = null;

    return validateField(messageField, messageError, requiredRule, 'Empty Field!', null);
}


/*==================== EMAIL SERVICE ====================*/ 
function SendMail(){
    console.log("test");
    if(!validateName() || !validateEmail() || !validateMessage() ){
        alert("Please fix the errors to send a message!");
        return false;
    }

    var params = {
        from_name : document.getElementById("fullName").value,
        email_id : document.getElementById("email_id").value,
        subject : document.getElementById("subject").value,
        message : document.getElementById("message").value
    }
    emailjs.send("service_hzaatpy", "template_ih5vxot", params).then(function (res){
        //alert("Success! " + res.status);
        alert("Your message has been sent successfully!");
    })
}