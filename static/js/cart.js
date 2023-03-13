//the first function is the django crsf token that is pasted from django documentation. it is called upon when using the add to cart button

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// add to cart function
//first, we get the buttons used to add to cart

let btns = document.querySelectorAll('#cart-card button')

btns.forEach(btn => {
    //for each button looped, we add an event listener

    btn.addEventListener('click',UpdateCart)
    
});



function UpdateCart(e){
    let product_id = e.target.value
    
    console.log( product_id);  
   
    //we'll send the id through a url
    //we create a new variable
    
    let url = '/add_to_cart'
    //since we're sending the product id as data to the backend
    let data = {id:product_id}

    fetch(url,{
        method  :   'POST',
        headers :   {'Content-Type':'application/json','X-CSRFToken': csrftoken},
        body    :   JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById('cart-badge').innerHTML= data
        console.log(data)
    })
    .catch(error=>{console.log(error)})
}
   

// function UpdateCart(e){
//     let product_id = e.target.value;
//     let operation = e.target.id === 'addition' ? 'add' : 'remove'; // determine whether to add or remove an item
//     let quantity_el = e.target.parentElement.parentElement.querySelector('.quantity'); // get the quantity element for the item
//     let quantity = parseInt(quantity_el.innerText); // get the current quantity value
//     if (operation === 'add') {
//         quantity += 1; // increment the quantity if adding
//     } else if (operation === 'remove' && quantity > 1) {
//         quantity -= 1; // decrement the quantity if removing and quantity is greater than 1
//     }
//     console.log(`product_id: ${product_id}, operation: ${operation}, quantity: ${quantity}`);

//     let url = '/update_cart/';
//     let data = {id: product_id, operation: operation, quantity: quantity};
//     fetch(url,{
//         method  :   'POST',
//         headers :   {'Content-Type':'application/json','X-CSRFToken': csrftoken},
//         body    :   JSON.stringify(data)
//     })
//     .then(res=>res.json())
//     .then(data=>{
//         quantity_el.innerText = data.quantity; // update the quantity element with the new quantity value
//         console.log(data)
//     })
//     .catch(error=>{console.log(error)})

// }
