$(document).ready(function() {
	//$('#reTable').DataTable();
	getZoneNum('');	
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


function getRecordNum(zid) {
	$.ajax({
		url: "/api/zonenum?zgid="+zid,
		type: "GET",
		dataType: "json",
		success: function(reponse) {
			var zonenum = reponse;
			$('#zone_num').before(zonenum.zone_num);
		}
	});
}

