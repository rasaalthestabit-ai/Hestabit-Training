let count = 0;
const increaseBtn = document.getElementById("increase");
const decreaseBtn = document.getElementById("decrease");
const countDisplay = document.getElementById("count");

increaseBtn.addEventListener("click", () =>{
    count ++;
    countDisplay.textContent = count;
});

decreaseBtn.addEventListener("click", () => {
    count --;
    countDisplay.textContent = count;
});

document.addEventListener("keydown", (event) => {
    if(event.key === "ArrowUp")
    {
        count ++;
    }
    if(event.key === "ArrowDown")
    {
        count --;
    }
    countDisplay.textContent = count;
});

const menuBtn = document.getElementById("menuBtn");
const navMenu = document.getElementById("navMenu");

menuBtn.addEventListener("click", () => {
    navMenu.classList.toggle("hidden");
});

const dropdownBtn = document.getElementById("dropdownBtn");
const dropdownMenu = document.getElementById("dropdownMenu");

dropdownBtn.addEventListener("click", () => {
    dropdownMenu.classList.toggle("hidden");
});

const openModal = document.getElementById("openModal");
const closeModal = document.getElementById("closeModal");
const modal = document.getElementById("modal");

openModal.addEventListener("click", () => {
    modal.classList.remove("hidden");
});
closeModal.addEventListener("click", () => {
    modal.classList.add("hidden");
});