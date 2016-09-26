$(document).ready(function() {
	initTables();
	var wsServer = 'ws://127.0.0.1:8001/api/aqb.check';
	mySocket = new WebSocket(wsServer); 
	mySocket.onopen = function (openEvent) {   
	     //
	};
	mySocket.onmessage = function (messageEvent) {   
		var table = document.getElementById('aqb_message');
		//table.insertRow().insertCell().innerHTML = event.data;
		//alert(event.data);
		//$("#aqb_message").html(event.data);
		$(table).append(event.data + '<br>');
	};
	mySocket.onerror = function (errorEvent) {   
	      //
	};
	mySocket.onclose = function (closeEvent) {
	     //
	}


});

function sendSocket(data) {
	mySocket.send(data);
}

$(document).on("click", "#aqbTable button[name=status]", function() {
	var data = $('#aqbTable').DataTable().row($(this).parents('tr')).data();
	var st = $(this).parents('tr').children();
	var cloud_dom = $(st[4]).children()[0];
	var power_i = $(this).children('i');
	//alert(data.rid + " " + data.zid);
	data.status = !data.status;
	//var s = recordStatus('update', data);
	dataSrc = {"param":"aqb", "rid":data.rid, "status":true}
	sendSocket(JSON.stringify(dataSrc));
	var s = true;
	if (s == true) {
		if (data.status == true) {
			$(cloud_dom).css('color', '#4DB3B3');
			$(power_i).removeClass('fa-power-off').addClass('fa-ban').css('color','#DC143C');
		} else {
			$(cloud_dom).css('color', '#808080');
			$(power_i).removeClass('fa-ban').addClass('fa-power-off').css('color', 'green');
		}
	}
});



function recordStatus(choose, src) {
	var dataSrc =  JSON.stringify(pickDataSrc(choose, src));
	var result_status = false;
	//use time
	//var mydate = new Date();
	//alert(mydate.toLocaleString());
	$.ajax({
		url: '/api/record',	
		type: "POST",
		dataType: 'json',
		async: false,
		data: dataSrc,
		success: function(reponse) {
			var rep = reponse[0];
			if (rep.status == true) {
				getNotify(rep.message, 'success');
				result_status = true;
			} else {
				getNotify(rep.message, 'danger');
			}
		}
	});
	//user time
	//var thedata = new Date();
	//alert(thedata.toLocaleString());
	return result_status
}


function initTables(){
	$('#aqbTable').DataTable({
		destroy: true,
		bPaginate: false,
		dom: '<"top"<"col-sm-7"<"toolbar">><"col-sm-5"f>>rt<"bottom"<"col-sm-5"i><"col-sm-7"p>><"clear">',
		ajax: {
			url: "/api/aqb",
			dataSrc: function(reponse) {
				records = reponse.records;
				$.each(records, function(i,n) {
					records[i]['operation'] = '';
					records[i]['r_status'] = '';
					if (records[i].status == true) {
						records[i].r_status  = iconHtml('cloud', '#4DB3B3');
						records[i].operation += buttonHtmlbyDefault('status', 'ban', '#DC143C');
					} else {
						records[i].r_status  = iconHtml('cloud', '#808080');
						records[i].operation += buttonHtmlbyDefault('status','power-off', 'green');
					}
				});
				return  records
			},
		},
		columns: [
			{data: 'rid',  visible: false},
			{data: 'sub_domain'},
			{data: 'record_type', width: '70'},
			{data: 'value', orderable: false},
			{data: 'zone_name'},
			{data: 'status', visible: false},
			{data: 'r_status', width: '50'},
			{data: 'operation', orderable: false}
		]
	});
	//$('div.toolbar').html('<button name="add" class="btn btn-default"><i class="fa fa-sellsy fa-lg" ></i>添加域名</button>');
	/*
	var toolAdd = $('div.toolbar').html('<button name="add"></button>');
	var addStr = $('<i></i>').addClass('fa fa-sellsy fa-lg');
	$(toolAdd).children('button').addClass('btn btn-default').html(addStr).append('添加域名');
	*/
}

function getNotify(message, type) {
	$.notify(
		{
			message: message,
		},
		{
			type: type
		});
}

function iconHtml(icon_name, icon_color) {
	return '<i name="'+icon_name+'" class="fa fa-'+icon_name+' fa-lg" style="color:'+icon_color+';"></i>'
}

function buttonHtmlbyDefault(name, icon_name, icon_color) {
	return  '<button name="'+name+'" class="btn btn-default">'+iconHtml(icon_name, icon_color)+'</button>';
}

