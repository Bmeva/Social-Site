// i am using it in a different file that's why i did not add the <script> tag. if i was including it in an html file then i would
// this javascript previews the image in the upload section in the index.html


    //var loadFile = function (event) {
   // var output2 = document.getElementById("preview_post_thumbnail");
   // output2.src = URL.createObjectURL(event.target.files[0]);
  //  output2.onload = function () {
       // URL.revokeObjectURL(output2.src); 
   // };
  //  };



$(document).ready(function() { // this is for the image preview when you try to upload an image
    var loadFile = function(event) {
        var output2 = document.getElementById("preview_post_thumbnail");
        output2.src = URL.createObjectURL(event.target.files[0]);
        output2.onload = function() {
            URL.revokeObjectURL(output2.src);
        };
    };

    // Attach loadFile function to the change event of the file input
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
        url: "/like_post/",
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
    let id = $(this).attr("data-comment-btn") //the click button to post comment
    let comment = $("#comment-input"+id).val() //val is what ever gets typed inside the textbox. so #comment-input"+id).val gets the object called comment-input and also gets its id which is the post id  

    let commentInput = $("#comment-input" + id); // this is the comment input box

    console.log(id);
    console.log(comment);

    $.ajax({
        url: "/comment_on_post/",
        dataType: "json",
        data:{
            "id":id,
            "comment":comment,
        },
        success: function(response){
            console.log(response);
            commentInput.val('');
            
     
           
            location.reload();

        }
        
    })
    
})
$(document).on("click", "#like-comment-btn", function(){
    let id = $(this).attr("data-like-comment")
    console.log(id);

    $.ajax({
        url: "/like_comment/",
        dataType: "json",
        data:{
            "id":id
        },
        success: function(response){
            console.log(response.data.bool);
            console.log(response.data.likes);

            if (response.data.bool === true) {

                $("#comment-likes-count"+id).text(response.data.likes)
                $(".like-comment"+id).css("color", "red")

            }else {
                console.log("Unliked");
                console.log(response.data.likes);
                $("#comment-likes-count"+id).text(response.data.likes)
                $('#comment-icon'+id).removeClass(' text-red-600 ');
                console.log($('.comment-icon'+id));
                $("#comment-likes-count"+id).removeClass(' text-red-600 ');
                $(".like-comment"+id).css("color", "gray")


            }
        }
    })
})


// Reply Comment
$(document).on("click", "#reply-comment-btn", function(){
    let id = $(this).attr("data-reply-comment-btn")
    let reply = $("#reply-input"+id).val()

    console.log(id);
    console.log(reply);

    $.ajax({
        url: "/reply_comment/",
        dataType: "json",
        data:{
            "id":id,
            "reply":reply,
        },
        success: function(res){
            console.log(res)
            $("#reply-input"+id).val("")
            $("#reply-details-open" + id).removeAttr("open");
            let newReply = '<div class="flex mr-12 mb-2 mt-2" style="margin-right: 20px;">\
            \
                <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                    <img src="'+res.data.profile_image+'" style="width: 40px; height: 40px;" alt="" class="absolute h-full rounded-full w-full ">\
                </div>\
                <div>\
                    <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12 dark:bg-gray-800 dark:text-gray-100">\
                        <p class="leading-6">'+ res.data.reply +'</p>\
                        <button class="ml-auto text-xs ml-3 mr-3" id="delete-reply-comment" data-delete-reply-comment="'+res.data.reply_id+'"> <i class="fas fa-trash text-red-500"></i> </button>\
                        <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                    </div>\
                    <span><small>'+ res.data.date +'ago</small> </span>\
                </div>\
            </div>\
            '
            $(".reply-div"+id).prepend(newReply);
           
                               
            
            console.log(res.data.bool);
        }
    })
})
//delete comment
$(document).on("click", "#delete-comment", function(){
    let id = $(this).attr("data-delete-comment")

    $.ajax({
        url: "/deleteComment/",
        dataType: "json",
        data:{
            "id":id,
           
        },
        success: function(response){
            console.log("Comment", id, "Deleted");
            $("#comment-div"+id).addClass("d-none")

        }
        })
    })

//delete comment reply
    $(document).on("click", "#delete-reply-comment", function(){
        let id = $(this).attr("data-delete-reply-comment")
    
        $.ajax({
            url: "/deleteCommentReply/",
            dataType: "json",
            data:{
                "id":id,
               
            },
            success: function(response){
                console.log("Comment", id, "Deleted");
                $("#comment-delete-div"+id).addClass("d-none");
    
            }
            })
        })

        //Add friend
        $(document).on("click", "#add-friend", function(){
            let id = $(this).attr("data-friend-id")
            console.log(id);

            $.ajax({
                url: "/addFriend/",
                dataType: "json",
                data:{
                    "id":id
                },
                success: function(response){
                    console.log("Bool ==",response.bool);
                    if (response.bool == true) {
                        $("#friend-text").html("<i class='fas fa-user-minus'></i> Cancel Request ")
                        $(".add-friend"+id).addClass("bg-red-600")
                        $(".add-friend"+id).removeClass("bg-blue-600")
                    }
                    if (response.bool == false) {
                        $("#friend-text").html("<i class='fas fa-user-plus'></i> Add Friend ")
                        $(".add-friend"+id).addClass("bg-blue-600")
                        $(".add-friend"+id).removeClass("bg-red-600")
                    }
                }
            })
        })

        // Accept Friend Request
            $(document).on("click", "#accept-friend-request", function(){  // Accept Friend Request button is on base.html
                let id = $(this).attr("data-request-id")
                console.log(id);

                $.ajax({
                    url: "/accept_friend_request/",
                    dataType: "json",
                    data: {
                        "id":id
                    },
                    success: function(response){
                        console.log(response.data);
                        $(".reject-friend-request-hide"+id).hide() //reject-friend-request-hide coming from base
                        $(".accept-friend-request"+id).html("<i class='fas fa-check-circle'></i> Friend Request Accepted")
                        $(".accept-friend-request"+id).addClass("text-white")
                    }
                })
            })

                // Reject Friend Request
                $(document).on("click", "#reject-friend-request", function(){
                    let id = $(this).attr("data-request-id")
                    console.log(id);

                    $.ajax({
                        url: "/reject_friend_request/",  
                        dataType: "json",
                        data: {
                            "id":id
                        },
                        success: function(response){
                            console.log(response.data);
                            $(".accept-friend-request-hide"+id).hide()
                            $(".reject-friend-request"+id).html("<i class='fas fa-check-circle'></i> Friend Request Rejected")
                            $(".reject-friend-request"+id).addClass("text-white")
                        }
                    })
                })

            // UnFriend User
            $(document).on("click", "#unfriend", function(){ //this button is in Myfriendprofile.html
                let id = $(this).attr("data-friend-id")
                console.log(id);

                $.ajax({
                    url: "/unfriend/",
                    dataType: "json",
                    data: {
                        "id":id
                    },
                    success: function(response){
                        console.log(response);
                        $("#unfriend-text").html("<i class='fas fa-check-circle'></i> Friend Removed ")
                        $(".unfriend"+id).addClass("bg-blue-600")
                        $(".unfriend"+id).removeClass("bg-red-600")
                    }
                })
            })



//# for id and . for class
    });




