var updateBtns = document.getElementsByClassName('update-cart')

for(let i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        console.log('user: ', user)
        console.log(this.dataset.action)
        let p_zId = this.dataset.p_z
        let action = this.dataset.action
        
        console.log('p_z: ',p_zId, 'action: ',action)

        if(user ==='AnonymousUser'){
            console.log('Not logged in')
        }
        else{
            updateUserOrder(p_zId,action)
        }
    })
}
function updateUserOrder(pzId, action){
    console.log('User logged in, sending data...')

    let url = 'update__item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({
            'pzId' : pzId,
            'action' : action
        })
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data: ',data)
        location.reload()
    })
}