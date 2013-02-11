function createUploader(){            
	var uploader = new qq.FileUploader({
	element: document.getElementById('file-uploader'),
	action: upload_url,
	debug: true,
	multiple: false,
	allowedExtensions : [],
	sizeLimit : 1024*1024*10,
	params:{'folder':folder},
	showMessage:function(message){ 
		alert(message); 
	},
	onComplete : function(id, fileName, responseJSON){
		if(responseJSON.success)
		{
			$('#file-uploader').hide();
            /*$('.uploaded-image').html('<img src="/media/pin/temp/t/'+responseJSON.file+'">');
			$('#image_field').val(responseJSON.file);
			image_selected=1;*/
            window.location.reload();
		}else{
			alert('Error');
        }
	}
	});           
}
createUploader();     
