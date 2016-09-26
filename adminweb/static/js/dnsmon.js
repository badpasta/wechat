$(document).ready(function() {
	$.ajax({
		url: "/api/getdnstypelist",
		type: "GET",
		dataType: "json",
		success: function(reponse) {
			var typeList = reponse.rdtypeList;
			var li = '';
			$.each(typeList, function(i, n){
				li += '<option value='+ n +'>'+ n +' Record</option>'	
			});
			$('#rdtypeList').html(li);
		}
	});
});


$(document).ready(function() {
	$('#monTable').DataTable();
});

$(document).ready(function() {
	$('#dnsCheckGo').click(function(){
		var record = $('#inputRecord').val();
		var nameserver = $('#inputNameserver').val();
		var rdtype = document.getElementById("rdtypeList").value;
		if (record == '') record = 'www.daling.com';
		if (nameserver == '') nameserver = '8.8.8.8';
		var jData = '{"record": "'+record+'", "nameserver": "'+nameserver+'", "rdtype": "'+rdtype+'"}';
		$('#monTable').DataTable({
			"processing": true,
			"serverSide": true,
			"retrieve": true,
			"destroy": true,
    		"ajax": {
				"url": "api/checkdnsdefault",
				"type": "POST",
				"dataType": "json",
				"dataSrc": 'data',
				"data": function () {
					return jData;
				}
			},
			"columns": [
				{"data": 'nameserver'},
				{"data": 'records'},
				{"data": 'status'},
				{"data": 'time'}
			]
		});
		alert(jData);
	});
});
