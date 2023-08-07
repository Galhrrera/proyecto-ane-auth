var body = document.getElementById("my-body")
var menu_container = document.getElementById("menu-container")
window.addEventListener("resize", function(){
    if (this.window.innerWidth > 760){
        body.classList.remove("body-moved")
        menu_container.classList.remove("menu-container-moved")
    }
})