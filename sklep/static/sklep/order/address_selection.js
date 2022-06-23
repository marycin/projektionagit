const adresSelecion = document.getElementById('adres-selection')
let div = document.getElementById('new-address')
console.log(adresSelecion.length)

adresSelecion.addEventListener('change',function(){
    this.value == 'new-adress' ? div.classList.remove('hide') : div.classList.add('hide')
})