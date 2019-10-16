// templatemo 467 easy profile

// PRELOADER

$(window).load(function(){
    $('.preloader').delay(100).fadeOut("slow"); // set duration in brackets    
	//是否删除 
	$("#delete_btn").click(function(){
		var msg="您真的确定要删除吗？请确认！";
		if(confirm(msg)==true){
			return true
		}else{
			return false
		}
	})
	//是否上传文件
	$("#btn_upload").click(function(){
		var f=$("#file")[0];
		var fileSize=0;
		// alert(f.files.length)
		if(f.files.length!=0){
			fileSize = f.files[0].size;
		}else{
			alert("请选择上传文件 ");
			return false
		}
		if(fileSize >10048576){
			alert("文件不能大于 10M ");
			return false;
		}
	
	})

});
