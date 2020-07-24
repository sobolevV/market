
let editor;
const edjsParser = edjsHTML();

document.addEventListener("DOMContentLoaded", function () {
    editor = new EditorJS({
        holder: "editorjs",
        tools: {
            header: Header,
            image: {
                  class: ImageTool,
                      config: {
                            uploader: {
                                uploadByFile(file){
                                    console.log(file);
                                    let formData = new FormData();
                                    const file_post = new Blob([file], {type : file.type});
                                    formData.append("image", file_post, file.name);
                                    formData.append("csrf_token", document.getElementsByName("csrf-token")[0].content);
                                    return  axios.post("", formData, {}).
                                    then(function (response) {
                                        return {
                                            success: 1,
                                            file: {
                                              url: response.data.url,
                                            }
                                        };
                                    }).catch(function (error) {
                                        // return error;
                                        return {success: -1}
                                    });
                                }
                            },
                            endpoints: {
                                byFile: "{{}}", //  url_for('news.base')  Your backend file uploader endpoint
                                byUrl: "{{}}", //  url_for('news.base')  Your endpoint that provides uploading by Url
                            }
                      }
                },
            list: {
              class: List,
              inlineToolbar: true,
            },
            paragraph: {
              class: Paragraph,
              inlineToolbar: true,
            },
        },
    });
})

function saveTitle() {
    editor.save().then((clean_data)=>{
        let html = edjsParser.parse(clean_data);
        const formData = new FormData();
        let imageUrl = "";
        for (let block of clean_data.blocks){
            if (block.type === "image"){
                imageUrl = block.data.file.url;
                break;
            }
        }
        formData.append("html", html);
        formData.append("image_url", imageUrl);
        formData.append("title", document.getElementsByName("title")[0].value);
        formData.append("description", document.getElementsByName("title_description")[0].value);
        formData.append("csrf_token", document.getElementsByName("csrf-token")[0].content);
        // Post html data
        axios.post("", formData, {}).
        then((result)=>{
            if (result.status === 200){
                alert("Статья успешно добавлена");
            }
        }).catch((error)=>{
            alert("Произошла ошибка. " + error);
        })

    }).catch((error) => {
        console.log(error);
        alert("Возникла ошибка при сохранении" + error);
    })
}