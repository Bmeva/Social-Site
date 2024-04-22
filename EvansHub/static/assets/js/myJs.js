// i am using it in a different file that's why i did not add the <script> tag. if i was including it in an html file then i would
// this javascript previews the image in the upload section in the index.html


    //var loadFile = function (event) {
   // var output2 = document.getElementById("preview_post_thumbnail");
   // output2.src = URL.createObjectURL(event.target.files[0]);
  //  output2.onload = function () {
       // URL.revokeObjectURL(output2.src); 
   // };
  //  };



$(document).ready(function() {
    var loadFile = function(event) {
        var output2 = document.getElementById("preview_post_thumbnail");
        output2.src = URL.createObjectURL(event.target.files[0]);
        output2.onload = function() {
            URL.revokeObjectURL(output2.src);
        };
    };

    // Attach loadFile function to the change event of the file input
    $('#image_thumb').on('change', loadFile);

    $('#image_thumb').on('change', loadFile);

    $('#post-form').submit(function(e) {
        e.preventDefault();
    
        let post_caption = $("#title").val();
        let post_visibility = $("#visibility").val();
    
        var fileInput = $('#image_thumb')[0];
        var file = fileInput.files[0];
        var fileName = file.name;
    
        let formData = new FormData();
        formData.append('title', post_caption);
        formData.append('visibility', post_visibility);
        formData.append('image_thumb', file, fileName);
    
        $.ajax({
            url: '/create_post/',
            type: 'POST',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Handle successful response (e.g., display a success message)
                alert('Post created successfully!');
                UIkit.modal('#create-post-modal').hide();
                location.reload();
                
            },
            error: function(xhr, status, error) {
                // Handle error response (e.g., display an error message)
                alert('Error creating post: ' + error);
            }
        });
    });


    ////////////////////Like post
$(document).on("click", "#like-btn", function(){ //like-btn is the id of the like button
    let btn_val = $(this).attr("data-like-btn")
    console.log(btn_val);

    $.ajax({
        url: "/lke_post/",
        dataType: "json",
        data:{
            "id":btn_val  //the id is the id in the django views so we are passing the id of btn_val to the id on like_post views. btn_val contains the id
        },
        success: function(response){
            if (response.data.thebool === true) {
                console.log("Liked");
                console.log(response.data.likes); // data is the context dictionary on the views. and likes is the data we passed in the dictionary on the views. we want to get the number of likes
                $("#like-count"+btn_val).text(response.data.likes) //appending the number of likes on the like-count button. data is the context dictionary on the views. and likes is the data we passed in the dictionary on the views
                $(".like-btn"+btn_val).addClass("text-blue-500") //changing the color of the button if the like was succesful by targeting the button withclass like-btn and matching it with the id of the post through the value of btn_val. So if we clicked on the post that have id 5 it changes only that button
                $(".like-btn"+btn_val).removeClass("text-black")
            }else {
                console.log("Unliked");
                console.log(response.data.likes);
                $("#like-count"+btn_val).text(response.data.likes)
                $("#like-count"+btn_val).text(response.data.likes)
                $(".like-btn"+btn_val).addClass("text-black")
                $(".like-btn"+btn_val).removeClass("text-blue-500")

            }
            console.log(response.data.thebool);
        }
    })
})


// Comment on post
$(document).on("click", "#comment-btn", function(){ //we add #on comment-btn bcos its an id attributeComment on Post but for class attribute we add .
    let id = $(this).attr("data-comment-btn")
    let comment = $("#comment-input"+id).val() //val is what ever gets typed inside the textbox. so #comment-input"+id).val gets the object called comment-input and also gets its id which is the post id  

    console.log(id);
    console.log(comment);

    $.ajax({
        url: "/comment_on_post/",
        dataType: "json",
        data:{
            "id":id,
            "comment":comment,
        },
        success: function(res){
        }
    })
})

        

});


