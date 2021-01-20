const addToCart = document.getElementsByClassName('update-cart')

for(let i=0;i<addToCart.length;i++){
    addToCart[i].addEventListener('click', function(){
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log(productId, action)

        console.log('USER:', user)
        if(user==='AnonymousUser'){
            console.log('User not authenticated')
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action){
    console.log('User authenticated')
    const url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:
        JSON.stringify({'productId':productId, 'action':action})

    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            // console.log('Data', data);
            location.reload();
        })
}