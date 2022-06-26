let button = document.getElementById('button')
let div = document.getElementById('sorted_fun')

button.addEventListener('click',function(){
    div.classList.contains('hide') ? div.classList.remove('hide') : div.classList.add('hide')
})
