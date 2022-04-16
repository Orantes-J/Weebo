// console.log(name, 'this is name var')
// const name = "Calei";

console.log('JAVASCRIPT IS RUNNING');
var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}
function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("user-review-div");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    if(slides.length>0){ 
        slides[slideIndex-1].style.display = "block";
    } else{
        return;
    }
};

// ----------------- ART SUBMISSION PAGE ---------------------------

const displayGalleria = document.querySelector('.galleria');
const hiddenGalleria = document.querySelector('.hide-galleria');
const arrowVec = document.querySelector('.return--top');
const galleria = document.querySelector('.art-galleria-images');

if(displayGalleria){
    displayGalleria.addEventListener('click', function(e){
        if(!displayGalleria) return 10;
        if (!hiddenGalleria) return 10;
        if (!galleria) return 10;
        if (!arrowVec) return 10;
        console.log('Event has been triggered');
        const artPost =  document.querySelector('.art-galleria-images');
        artPost.classList.remove('hidden');
        displayGalleria.classList.add('hidden');
        hiddenGalleria.classList.remove('hidden');
        galleria.classList.add('grid-images-template');
    });
    hiddenGalleria.addEventListener('click', function(e){
        e.preventDefault()
        hiddenGalleria.classList.add('hidden');
        displayGalleria.classList.remove('hidden');
        if(!displayGalleria) return 10;
        console.log('Hiding Galleria');
        const artPost = document.querySelector('.art-galleria-images');
        artPost.classList.add('hidden');
        artPost.classList.remove('grid-images-template');
        const navBar = document.querySelector('.nav-bar');
        const targetArea = navBar.getBoundingClientRect().top;
        navBar.scrollIntoView({
            behavior : 'smooth'
        });
        console.log(targetArea, 'target area variable');
    });
    galleria.classList.add('hidden');
    arrowVec.addEventListener('click', function(e){
        if(!displayGalleria) return 10;
        e.preventDefault()
        hiddenGalleria.classList.add('hidden');
        displayGalleria.classList.remove('hidden');
        const artPost = document.querySelector('.art-galleria-images');
        artPost.classList.add('hidden');
        artPost.classList.remove('grid-images-template');
        const navBar = document.querySelector('.nav-bar');
        const targetArea = navBar.getBoundingClientRect().top;
        navBar.scrollIntoView({
            behavior : 'smooth'
        });
    });
};

// MODAL REVEAL
document.querySelectorAll('.art-images').forEach(function(el){
    el.addEventListener('click', function(e){
        console.log(`Hovering over '${el.dataset.art}'`);
        const imageTarget = el.dataset.art;
        if (el.dataset.art === imageTarget){
            //CODE TO ADD HOVER MODAL EFFECT
            //POSTION OF IMAGE
            const image = el.getBoundingClientRect()
            console.log(`Top:${image.top} Right:${image.right} Bottom:${image.bottom} Left:${image.left} current image position`);
            const nextSibiling = el.nextElementSibling;
            console.log(nextSibiling, 'nextSibling Const');
            nextSibiling.style.left = `${Math.floor(image.left)}px`;
            nextSibiling.style.top = `${Math.floor(image.top) + 480}px`;
            nextSibiling.style.right = `${Math.floor(image.right)}px`;
            nextSibiling.style.bottom = `${Math.floor(image.bottom)}px`;
            nextSibiling.classList.add('reveal')
        };
    });
})

// CLOSE MODAL

document.querySelectorAll('.close-modal-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
        console.log(btn, 'has been clicked');
        btn.parentElement.classList.remove('reveal');
        btn.parentElement.classList.add('hidden');
    });
});

// ADDING ATTRIBUITES VIA JS TO FORMS

const ratingInput = document.getElementById('rating');
console.log(ratingInput);
ratingInput.setAttribute('value', 1);
ratingInput.setAttribute('min', 1);
ratingInput.setAttribute('max', 10);

// REVEALING REVIEW FORM -> PREVENT E FOR SUBMIT

const formTitle = document.querySelector('.review-h');
const form = document.querySelector('.review-form');
console.log(formTitle.textContent, 'this is formTitle');
formTitle.addEventListener('click', function(){
    if(!formTitle) return;
    console.log('formTitle has been clicked');
    form.classList.toggle('hidden')
})

const formSubmit = document.querySelector('.form-button');
formSubmit.addEventListener('submit', function(e){
    e.preventDefault()
})