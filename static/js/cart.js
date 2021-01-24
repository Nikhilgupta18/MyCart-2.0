const addToCart = document.getElementsByClassName('update-cart')

for(let i=0;i<addToCart.length;i++){
    addToCart[i].addEventListener('click', function(){
        const productId = this.dataset.product
        const action = this.dataset.action

        if(user==='AnonymousUser'){
            addItems(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}

function addItems(productId, action){
    console.log('AnonymousUser')

    if(action == 'add'){
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0)
            delete cart[productId];
    }

    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";

    location.reload()
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