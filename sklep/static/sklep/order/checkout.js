let rodzajPlatnosci = document.getElementById('rodzaj_platnosci')
let divPlatnosc = document.getElementById('platnosc')

rodzajPlatnosci.addEventListener('change',function(){
    let kartyPlatnicze = document.getElementById('karty_platnicze')
    let blik = document.getElementById('blikInput')
    console.log(rodzajPlatnosci.value)
    if(rodzajPlatnosci.value == 1){
        
        blik.style.display='block'
        kartyPlatnicze.style.display='none'
    }
    
    else if(rodzajPlatnosci.value ==2){
        blik.style.display='none'
        kartyPlatnicze.style.display='block'
    }
})
