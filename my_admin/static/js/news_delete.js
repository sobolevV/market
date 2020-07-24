
function deleteTitle(elem){
        if (confirm("Вы действительно хотите удалить новость?")) {
            const formData = new FormData();
            const title_id = Number(elem.value);
            formData.append("title_id", title_id);
            formData.append("csrf_token", document.getElementsByName("csrf-token")[0].content);

            axios.post("/admin/news/delete_title", formData, {}).
            then((result)=>{
                if (result.status === 200){
                    alert("Статья Удалена");
                }
            }).catch((error)=>{
                alert("Произошла ошибка. " + error);
            })
        }
    }