

let fileUploader = document.getElementById('file-uploader');
let displayImage = document.getElementById('display-image');
let btnCrop = document.getElementById('btnCrop');
let urlText = document.getElementById('url-text');
let submitBtn =  document.getElementById('btnSubmit');
let cropper;

btnCrop.style = "display:none;"
submitBtn.disabled = true;

function uploadFileAction(e){

    let reader = new FileReader();
    reader.onload = ()=>{
        displayImage.src = reader.result;
        cropper = new Cropper(displayImage, {
            aspectRatio : 0,
            viewMode : 0,
        })
    }
    
    reader.readAsDataURL(fileUploader.files[0]);
    btnCrop.style = "display:block;"
}

function cropAction(e){
    let croppedImage = cropper.getCroppedCanvas().toDataURL("image/png")
    urlText.value = croppedImage;
    submitBtn.disabled = false;
}

fileUploader.addEventListener('change', uploadFileAction);
btnCrop.addEventListener('click' , cropAction)


let getUser = false;
    $('#caption').keyup(function(e){
        
        
        
       
        
       
        if(e.keyCode == 20 || e.keyCode == 16){
            return
        }

        let i = e.target.value.length - 1;

        if(e.target.value.charAt(i) == "@"){
            getUser = true;
        }
        
        if(e.target.value.charAt(i) == " "){
            getUser = false;
        }

        if(getUser){
            $('#show-suggestion').css('display', 'block')
            let data = $('#caption').val().slice( $('#caption').val().lastIndexOf('@')+1)
            $.ajax({
                url: '/makesuggestions',
                method: 'POST',
                data: {
                    search: data,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    
                },
                success: function(result){
                    $('#show-suggestion').empty();
                    for(let e = 0; e < result.data.length; e++ ){
                        
                       $('#show-suggestion').append('<p id = "clickable-suggestion" style = "cursor:pointer;">'+result.data[e].username+'</p>')
                  }
                }
               })
            
        }
        if(!getUser || $('#show-suggestion').html() == ""){
            $('#show-suggestion').css('display', 'none')
        }

        
        
    });

    document.addEventListener('click',function(e){
        if(e.target && e.target.id== 'clickable-suggestion'){
            let text = $('#caption').val()
            let replaced_element = $('#clickable-suggestion').text()
            modified_text = text.replace(text.slice(text.lastIndexOf("@")+1), replaced_element)
            $('#caption').val(modified_text)
            $('#show-suggestion').css('display', 'none')
         }
     });

   


