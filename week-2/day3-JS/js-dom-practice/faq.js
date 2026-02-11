const buttons = document.querySelectorAll(".toggle-btn");

buttons.forEach(button =>{
    button.addEventListener("click", () => {
        const faqItem = button.parentElement.parentElement;
        const answer = faqItem.querySelector(".answer");

        if(answer.style.display === "block")
        {
            answer.style.display = "none";
            button.textContent = "+";
        }
        else
        {
            answer.style.display = "block";
            button.textContent = "-";
        }
    });
});
