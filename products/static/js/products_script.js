
function addToCart(obj, productId) {
    const postForm = new FormData();
    postForm.append("product_id", productId);
    postForm.append("csrf_token", document.getElementsByName("csrf-token")[0].content);

    axios.post("products/add_to_cart", postForm, {}).
    then(function (response) {
        if (response.status === 200){
            obj.innerText = "В корзине";
            obj.classList.add("uk-disabled");
            obj.removeAttribute("onclick");
            obj.removeAttribute("uk-icon");
        }
    }).catch(function (error) {
        alert("Не удалось добавить продукт в корзину");
    });
};