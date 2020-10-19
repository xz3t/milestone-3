    /*
    Script copied from link below, small change done to be able to send id to the script from project pages to have one instance of the script"
    https://stackoverflow.com/questions/60809635/how-to-upload-an-image-to-imgbb-api-using-javascript-in-a-firefox-addon

    */
    
    function fileChange(x){
    var file = document.getElementById('input_img');
    var form = new FormData();
    form.append("image", file.files[0])
    
    var settings = {
      "url": "https://api.imgbb.com/1/upload?key=2531cb35bfd78604c01d2039b2118010",
      "method": "POST",
      "timeout": 0,
      "processData": false,
      "mimeType": "multipart/form-data",
      "contentType": false,
      "data": form
    };
    
    
    $.ajax(settings).done(function (response) {
      var jx = JSON.parse(response);
      $("#"+x).val(jx.data.url);
        
    });
    }