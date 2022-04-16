// GRADING USER
const gradeList = document.querySelectorAll('.iter-grade');
console.log('*********************************************');

const emojiGrade = [];
const correct = [];
const incorrect = [];

gradeList.forEach(g => {
    console.log(g);
    let e = g.textContent;
    let a = e.split('');
    if (a[4] === '✔'){
        correct.push(a[4]);
        emojiGrade.push(a[4]);
    }
    if (a[4] === '⛔') {
        incorrect.push(a[4]);
        emojiGrade.push(a[4]);
    }
})

if (gradeList.length === correct.length ) {
    document.querySelector('.gif-correct').classList.remove('hidden');
} else{
    document.querySelector('.gif-incorrect').classList.remove('hidden');
};


console.log(gradeList.length);
console.log(emojiGrade), 'emoji grade';
console.log('*********************************************');
