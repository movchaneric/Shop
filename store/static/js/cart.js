
var updateBtns = document.getElementsByClassName('update-cart');

for(i = 0; i < updateBtns.length; i++){
	updateBtns[i].addEventListener("click", function(){
		console.log('inside click function')
		var productId = this.dataset.product
		var action = this.dataset.action

		console.log('productId: ', productId, ' action: ', action)

		console.log('User:' , user)
		if(user == 'AnonymousUser'){
			console.log('User is not logged in...')
		}else{
			updateUserOrder(productId, action);
		}
	})

}

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

	.then((res) => {
		return res.json()
	})

  	.then((data) => {
  		console.log('data:', data)
  		location.reload()
  	})

}