// Custom dropdown actions
dropdowns=document.getElementsByClassName("custom-dropdown");
for(let i=0;i<dropdowns.length;i++){
    dropdowns[i].addEventListener("click",()=>{
        dropdowns[i].classList.toggle("active");
    })
    input=dropdowns[i].children[0];
    option_list=dropdowns[i].children[2];
    for(let j=0;j<option_list.children.length;j++){
        option_list.children[j].addEventListener("click",()=>{
        input.value=option_list.children[j].innerText;
        });
    }
}