function previewFile(event){

    const file = event.target.files[0];

    if(!file) return;

    document.getElementById("fileName").innerHTML=file.name;

    document.getElementById("preview").style.display="block";

    if(file.type.startsWith("image")){

        const reader=new FileReader();

        reader.onload=function(e){

            document.getElementById("imagePreview").src=e.target.result;

        }

        reader.readAsDataURL(file);

    }

}

function showLoader(){

    document.getElementById("loader").style.display="block";

}