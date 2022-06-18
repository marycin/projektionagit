let showHideCategoriesButton = document.getElementById('show-hide-categories')
let categories = document.getElementById('category-list')
let categoryBtnBox = document.getElementById('category-btn-box')

window.addEventListener('resize',removeHideClass)
showHideCategoriesButton.addEventListener('click',showHideCategories)


function showHideCategories(){
    if(categories.classList.contains('hide')){
        categories.classList.remove('hide')
        return 
    }
    categories.classList.add('hide')
}


function removeHideClass(){
    if (window.innerWidth<629){
        categories.classList.add('hide')
        categoryBtnBox.classList.remove('hide')
        return
    }
    categories.classList.remove('hide')
    categoryBtnBox.classList.add('hide')

}


