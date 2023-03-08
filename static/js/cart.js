// add to cart function
const updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function() {
        const productid = this.dataset.product
        const action = this.dataset.action
        console.log('productid:', productid, 'action:', action);
        
        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('User is not logged in');    
        
        }
        else{
            console.log('User is logged in. Sending data...');
        }
    })
    
}

