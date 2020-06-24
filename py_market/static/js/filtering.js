
function submitGetRequest(url, data){
    axios({
        method:"get",
        url: url,
        params: data,
        paramsSerializer: function (params) {
            return Qs.stringify(params, {arrayFormat: 'repeat'})}
    })
        .then(function (response) {
        if (response.status == 200){
            window.location.href = response.request.responseURL;
            // let replace_id = "products";
            // let products_block = document.getElementById(replace_id);
            // // new data
            // let body_resp = document.createElement('html');
            // body_resp.innerHTML = response.data;
            // body_resp = body_resp.getElementsByClassName("uk-grid uk-flex-center")[0];
            // // replace old to new
            // products_block.innerHTML = body_resp.innerHTML;
            let old_html = document.getElementsByTagName("body")[0];
            let new_html = document.createElement('html');
            new_html.innerHTML = response.data;
            let newBody = new_html.getElementsByTagName("body")[0];
            old_html.innerHTML = newBody.innerHTML;
        }
    }).catch(function (error) {
        // console.log
        console.log(error);
    });
}

function applyFilter(url){
    let data = getFormData();
    data["page"] = String(1);
    submitGetRequest(url, data);
}

function getPage(el, url, page) {
    console.log(el);
    let data = getFormData();
    data["page"] = String(page);
    submitGetRequest(url, data);
}

function getFormData() {
    // Dictionary with data
    let data = {};
    // Form with product filters
    let form = document.getElementsByTagName("form")[0];

    for (let input of form){
        if (input.tagName.toLowerCase() !== "input"){
            continue
        }

        if (input.type !== "radio"){
            // Get data from each not radio input
            if (!(input.name in data)){
                data[input.name] = [input.value];
            }
            else if (input.name in data && input.value.length && input.checked){
                data[input.name].push(input.value);
            }
        }
        else if (!(input.name in data) && input.checked){
            // Get only checked value
            data[input.name] = input.value;
        }
    }
    return data
}
