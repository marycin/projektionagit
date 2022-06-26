const rodzajPlatnosci = document.getElementById('rodzaj_platnosci')
let divCardPayment = document.getElementById('card-payment')
let divBlikPayment = document.getElementById('blik-payment')
console.log(rodzajPlatnosci.length)


// 1 = blik, 2 = karta, 3 = gotowka
rodzajPlatnosci.addEventListener('change',function(){
    if(this.value == 1){
        divBlikPayment.classList.remove('hide')
        divCardPayment.classList.add('hide')
    }
    if(this.value == 2){
        divBlikPayment.classList.add('hide')
        divCardPayment.classList.remove('hide')
    }
    else{
        divBlikPayment.classList.add('hide')
        divCardPayment.classList.add('hide')
    }
})