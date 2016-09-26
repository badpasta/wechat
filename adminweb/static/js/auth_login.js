$(document).on("click", "#authButton", function() {
	var username = $("input#authUser").val();
	var password = $("input#authPass").val();
	var jData = '{"username": "' + username + '", "password": "'+ password +'"}';
	$.ajax({
		url: "/login",
		type: "POST",
		dataType: "json",
		data: jData,
		success: function(reponse) {
			var jStatus = reponse.status;
			var notContext = '';
			var notStatus = '';
			if(jStatus)
				{notStatus = 'success';
				 notContext = 'Login Success.';
				 location.href = reponse.url;
				 }
			else
				{notStatus = 'danger';
				 notContext = 'Login Failed.';
				 putMessage(notStatus, notContext)
				 }
		}
	});
});

function putMessage(nstatus, message) {
	var tFormat = '<div class="alert alert-'+nstatus+' alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>'+message+'</div>';
	$('#status').html(tFormat);
}
