$(document).ready(function() {
	//$('#reTable').DataTable();
	getRecordNum();	
	$.ajax({
		url: "/api/zonelist",
		type: "GET",
		dataType: "json",
		success: function(reponse) {
			var str = '';
			var zoneList = reponse;
			$.each(zoneList, function(i, n){
				//alert(i);
				for(var idx in n){
					//alert(n[idx].id +":"+n[idx].name);
            		str += '<li id='+n[idx].id+'><a href="#"></i>'+n[idx].name+'</a></li>';
				}
			});
			$('#zonelist').html(str);
		}
	});	
	initTables('1');
});


$(document).on("keyup", "input#zoneSearch", function() { 
    var keyword = $('input#zoneSearch').val();
	getZone(keyword);
});


$(document).on("click", "#zonelist li", function() { 
    var keyword = this.id;
	var domain = $('#'+keyword+ ' a').html();
	$('#domainTitle').html('<b>'+domain.toUpperCase()+'</b>');
	initTables(keyword);
});


$(document).on("click", "button[name=add]", function() {
/*
					<th>rid</th>
					<th>sub_domain</th>
					<th>record_type</th>
					<th>ttl</th>
					<th>value</th>
					<th>weight</th>
					<th>mx</th>
					<th>record_line</th>
					<th>status</th>
					<th>r_status</th>
					<th>description</th>
					<th>operation</th>
*/
	var theParent = $(this).parents('tr');
	//var dataSrc = {"rid":'123',"sub_domain":'dddd',"record_type":'5',"ttl":'7',"value":'9',"weight":'bbb',"r_mx":"dddd","mx":'aaa',"record_line":'ddddd', "r_status":"ff","status": "true", "description":"", "operation":""};
	var data = $('#recordTable').DataTable().row().data();
	var dataSrc = new Object();
	$.each(data, function(i, n) {
		dataSrc[i] = n;
	})
	dataSrc['sub_domain'] = '<input type="text" placeholder="输入记录不含域名." class="form-control"></input>';
	var record_type = ["A","CNAME","MX","TXT", "NS"];
	var option_html = '';
	$.each(record_type, function(i, n){
		option_html += '<option>'+n+'</option>';
	});
	var select = '<select class="form-control">'+option_html+'</select>';
	dataSrc['record_type'] = select;
	dataSrc['ttl'] = '<input type="text" value="600" style="width:50px;" class="form-control"></input>';
	dataSrc['value'] = '<input type="text" placeholder="输入记录值." class="form-control"></input>';
	dataSrc['weight'] = '<input type="text" value="0" style="width:50px;" class="form-control"></input>';
	dataSrc['r_mx'] = '<input type="text" value="0" style="width:50px;" class="form-control"></input>';
	dataSrc['operation'] = buttonHtmlbyDefault('insert', 'save', '#1E90FF') + buttonHtmlbyDefault('remove', 'remove', '#DC143C');
	dataSrc['rid'] = '1';
	$('#recordTable').DataTable().row.add(dataSrc).draw(false);
});

$(document).on("click", "#recordTable button[name=insert]", function() {
	var theParent = $(this).parents('tr');
	var data = $('#recordTable').DataTable().row(theParent).data();
	var children = theParent.children();
var dataSrc = new Object();
	$.each(data, function(i, n) {
		dataSrc[i] = n;
	})
	var list = ["sub_domain", "record_type", "ttl", "value", "weight", "r_mx", "r_status", "operation"];
	$.each(children, function(i, n) {
		var data_value = n.children[0].value;
		if (i <= '5') {
			if (data_value == '-') {
				data_value = '0';
			}
			dataSrc[list[i]] = data_value;
		//data[i] = n.children[0].value;
		}
	});
	dataSrc.rid = '';
	var s = recordStatus('insert', dataSrc);
	if (s == true) {
		$.each(data, function(i, n) {
			data[i] = dataSrc[i];
		});
		data['operation'] =  buttonHtmlbyDefault('status', 'ban', '#DC143C') +  buttonHtmlbyDefault('edit','edit', '#003366') + buttonHtmlbyDefault('delete','trash-o', '#8B1A1A');
		$.ajax({
			url: "/api/getrid",
			type: "GET",
			dataType: "json",
			data: {zid: data['zid'], record_type: data['record_type'], value: data['value'], sub_domain: data['sub_domain']},
			async: false,
			success: function (reponse) {
				data['rid'] = reponse.rid;
			}
		});	
	}
	dataHTML(children, data);
});


$(document).on("click", "#recordTable button[name=remove]", function() {
	var parents = $(this).parents('tr');
	$('#recordTable').DataTable().row($(parents)).remove().draw(false);
});

$(document).on("click", "#recordTable button[name=delete]", function() {
	var parents = $(this).parents('tr');
	var data = $('#recordTable').DataTable().row(parents).data();
	var s = recordStatus('delete', data);
	if (s == true) {
		$('#recordTable').DataTable().row($(parents)).remove().draw(false);
	}
});

$(document).on("click", "#recordTable button[name=edit]", function() {
	var theParent = $(this).parents('tr');
	var data = $('#recordTable').DataTable().row(theParent).data();
	var children = theParent.children();
	editHTML(children);
});

$(document).on("click", "#recordTable button[name=save]", function() {
	var theParent = $(this).parents('tr');
	var data = $('#recordTable').DataTable().row(theParent).data();
	var children = theParent.children();
	var list = ["sub_domain", "record_type", "ttl", "value", "weight", "r_mx", "r_status", "operation"];
	var dataSrc = new Object();
	$.each(data, function(i, n) {
		dataSrc[i] = n;
	})
	$.each(children, function(i, n){
		var data_value = n.children[0].value;
		if (i <= '5') {
			if (data_value == '-') {
				data_value = '0';
			}
			dataSrc[list[i]] = data_value;
		//data[i] = n.children[0].value;
		}
	});
	var s = recordStatus('update', dataSrc);
	if (s == true) {
		$.each(data, function(i, n) {
			data[i] = dataSrc[i];
		});
	}
	dataHTML(children, data);
});

$(document).on("click", "#recordTable button[name=cannel]", function() {
	var theParent = $(this).parents('tr');
	var data = $('#recordTable').DataTable().row(theParent).data();
	var children = theParent.children();
	dataHTML(children, data);
});


$(document).on("click", "#recordTable button[name=status]", function() {
	var data = $('#recordTable').DataTable().row($(this).parents('tr')).data();
	var st = $(this).parents('tr').children();
	var cloud_dom = $(st[6]).children()[0];
	var power_i = $(this).children('i');
	alert(data.rid + " " + data.zid);
	data.status = !data.status;
	var s = recordStatus('update', data);
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

function editHTML(children) {
	var record_type = ["A","CNAME","MX","TXT","NS"];
	var option_html = '';
	$.each(record_type, function(i, n){
		option_html += '<option>'+n+'</option>';
	});
	var select = $('<select>').addClass('form-control').html(option_html);
	//var tab_input = $('<input type="text"></input>').addClass('form-control');
	var div = $('<div>').addClass('form-group');
	$.each(children, function(i, n) {
		var older_val = $(n).html();
		var inpu  = $('<input type="text"></input>').addClass('form-control').val($(n).html());
		if (i == '0' || i == '3') {
			//var inpu = $('<input type="text" ></input>').addClass('form-control');
			//var inp = inpu.val($(n).html()).css('min-width','50').css('width','auto');
			var inp = inpu.css('min-width','50').css('width','auto');
			$(n).html(inp);
			//$(n).html(input.val($(n).html()).css('min-width','50').css('width','auto'));
			//var allin = input.val(older_val).css('min-width','80').css('width','auto');
			//$(n).html(div.html(allin));
		}
		if (i == '2' || i >= '4' && i <= '5') {
			var inp = inpu.css('width','50');
			if (older_val == '-') {
				var inp = inp.attr("disabled","disabled")
			}
			$(n).html(inp);
		}
		if (i == '1') {
			$(n).html(select);
		}
		if (i == '7') {
			$(n).html(buttonHtmlbyDefault('save', 'save', '#1E90FF') + buttonHtmlbyDefault('cannel', 'remove', '#DC143C'));
		}
	});

}

function dataHTML(children, data) {
	var list = ["sub_domain", "record_type", "ttl", "value", "weight", "r_mx", "r_status", "operation"];
	$.each(children, function(i, n){
		var tmp_value = data[list[i]];
		if (list[i] == 'r_mx' && tmp_value == '0') {
			tmp_value =  '-'
		}
		$(n).html(tmp_value);
	});
}

function pickDataSrc(choose, src) {
		if (src['r_mx'] == '-') {
			src['r_mx'] = 0;
		}
		return {"param": choose,
				"zid": src.zid,
				"values": [
				{
					"rid": src.rid,
					"sub_domain": src.sub_domain,
					"record_type": src.record_type,
					"value": src.value,
					"ttl": src.ttl,
					"record_line": src.record_line,
					"weight": src.weight,
					"mx": src.r_mx,
					"status": src.status,
					"zid": src.zid,
					"rgid": src.rgid,
					"description": src.description
				}
				]}
}

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

function getZone(zoneName = '') {
	var str = '';
	var list = $("#zonelist").children();
	$.each(list, function(i, n){
		var id =  '#'+list[i].id;
		if (list[i].innerHTML.indexOf(zoneName) < 0){
			//str += '<li id='+list[i].id+'>'+list[i].innerHTML+'</li>'
			$(id).hide();
		}
		else {
			$(id).show();
		}
	});
	//$('#zonelist').html(str);
}

function getRecordNum() {
	var zid = '';
	$.ajax({
		url: "/api/recordnum?zid="+zid,
		type: "GET",
		dataType: "json",
		success: function(reponse) {
			var recordnum = reponse;
			$('#record_num').before(recordnum.record_num);
		}
	});
}

function getRecordList(zid) {
	var zid = zid;
	$.ajax({
		url: "/api/record?zid="+zid,
		type: "GET",
		dataType: "json",
		success: function(reponse) {
			var recordList = '';
			if (reponse.status == true) {
				recordList = reponse.records;
				alert(recordList);
			}
		}
	});
}

function initTables(zid){
	//alert(zid);
	//$('#recordTable').dataTable().fnDestroy();
	$('#recordTable').DataTable({
		destroy: true,
		dom: '<"top"<"col-sm-7"<"toolbar">><"col-sm-5"f>>rt<"bottom"<"col-sm-5"i><"col-sm-7"p>><"clear">',
		ajax: {
			url: "/api/record",
			dataSrc: function(reponse) {
				records = reponse.records;
				$.each(records, function(i,n) {
					records[i]['operation'] = '';
					records[i]['r_status'] = '';
					records[i]['r_mx'] = '';
					if (records[i].record_type != 'MX') {
						records[i].r_mx = '-';
					} else {
						records[i].r_mx = records[i].mx;
					}
					if (records[i].status == true) {
						records[i].r_status  = iconHtml('cloud', '#4DB3B3');
						records[i].operation += buttonHtmlbyDefault('status', 'ban', '#DC143C');
					} else {
						records[i].r_status  = iconHtml('cloud', '#808080');
						records[i].operation += buttonHtmlbyDefault('status','power-off', 'green');
					}
					records[i].operation += buttonHtmlbyDefault('edit','edit', '#003366');
					records[i].operation += buttonHtmlbyDefault('delete','trash-o', '#8B1A1A');
				});
				return  records
			},
			data: {zid: zid}
		},
		columns: [
			{data: 'rid',  visible: false},
			{data: 'sub_domain', orderable: false},
			{data: 'record_type', width: '70'},
			{data: 'ttl', width: '30'},
			{data: 'value', orderable: false},
			{data: 'weight', width: '5'},
			{data: 'mx', visible: false},
			{data: 'r_mx', width: '5'},
			{data: 'record_line', visible: false},
			{data: 'status', visible: false},
			{data: 'r_status', width: '28', orderable: false},
			{data: 'description', visible: false},
			{data: 'operation', orderable: false}
		/*
			{data: 'rid'},
			{data: 'sub_domain'},
			{data: 'record_type'},
			{data: 'ttl'},
			{data: 'value'},
			{data: 'weight'},
			{data: 'mx'},
			{data: 'r_mx'},
			{data: 'record_line'},
			{data: 'status'},
			{data: 'r_status'},
			{data: 'description'},
			{data: 'operation'}
		*/
		]
	});
	//$('div.toolbar').html('<button name="add" class="btn btn-default"><i class="fa fa-sellsy fa-lg" ></i>添加域名</button>');
	var toolAdd = $('div.toolbar').html('<button name="add"></button>');
	var addStr = $('<i></i>').addClass('fa fa-sellsy fa-lg');
	$(toolAdd).children('button').addClass('btn btn-default').html(addStr).append('添加域名');
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

