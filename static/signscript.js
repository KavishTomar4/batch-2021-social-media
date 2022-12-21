// Get the modal
var modal = document.getElementById("myModal")

let cropper;

let cropedImage;
// Get the button that opens the modal
var btn = document.getElementById("img");
let s_img = document.getElementById("display_image")

let output = document.getElementById("output-image")

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onchange = function() {
  modal.style.display = "block";

  let reader = new FileReader()
  reader.onload = function(){
      s_img.src = reader.result
      cropper = new Cropper(s_img,{

        aspectRatio: 0,
        viewMode: 0,
      
       });
       
      
  }

 


  reader.readAsDataURL(btn.files[0])

 

}


document.getElementById("btnCrop").addEventListener('click', (e)=>{
  cropedImage = cropper.getCroppedCanvas().toDataURL("image/png")
  output.src = cropedImage;
  alert(cropedImage)
  document.getElementById("imgurl").value = cropedImage
  
  

  modal.style.display = "none";
})


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
/*window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}*/