const adresSelecion = document.getElementById('adres-selection')

adresSelecion.addEventListener('change',function(){
    let div = document.getElementById('new-adress')
    if(this.value == 'new-adress'){
        console.log('new-adress')
        div.style.display='block'
    }
    else{
        div.style.display = 'none'
    }
})