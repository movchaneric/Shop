
var updateBtns = document.getElementsByClassName('update-cart');

for(i = 0; i < updateBtns.length; i++){
	updateBtns[i].addEventListener("click", function(){
		
		var productId = this.dataset.product
		var action = this.dataset.action

		// console.log('productId: ', productId, ' action: ', action)
		// console.log('User:' , user)

		if(user == 'AnonymousUser')
		{
			addCookieItem(productId, action)
		}
		else
		{
			updateUserOrder(productId, action);
		}
	})

}

// handle guest User 
function addCookieItem(productId, action){
	console.log('User is not logged in')
	// add action 
	if(action == 'add'){
		// if its the first item then init cart
		if(cart[productId] == undefined){
			console.log('first item was added')
			cart[productId] = {'quantity':1}
		}else{
			cart[productId]['quantity'] += 1;
		}
	}

	// remove action
	if(action == 'remove'){
		// remove an item 
		cart[productId]['quantity'] -= 1;

		// check negativity => remove item
		if(cart[productId]['quantity'] <= 0){
			delete cart[productId]
			console.log('Item was deleted')
		}
	}
	// update the browser cookie after actions
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
	location.reload()
}

// handle logged in user 
function updateUserOrder(productId, action){
	console.log('user is logged in continue...')
	var url = '/update-item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type': 'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productId':productId, 'action':action})
	})

	.then((response) => {
		return response.json()
	})

  	.then((data) => {
  		console.log('data:', data)
  		location.reload()		
  	})
}