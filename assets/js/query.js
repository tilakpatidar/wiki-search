$(document).ready(function(){

function callback(){
	
}

function search(query,i,j){
	$.ajax({
		type:"GET",
		url:"http://www.srmsearchengine.in/mp/search?callback=?",
		crossDomain:true,
		dataType: "jsonp",
		jsonpCallback: 'callback',
		contentType: "application/json",
		data:{query:query,i:i,j:j},
		success:function(data){
			
			var main = $();
			$.each(data, function(k, v){
				var tmp = $("<div class='search_result'><div class='container-fluid'><div class='row'> <div class='col-lg-12'> <a class='search_link' href=''><h4 class='h4_title'></h4></a> </div> </div> <div class='row'> <div class='col-lg-12'> <p class='green_search'></p> </div> </div> <div class='row'> <div class='col-lg-12'> <p class='search_desc'></p> </div> </div> </div> </div>");
				tmp.find(".search_link").attr("href",v["url"]);
				tmp.find(".h4_title").text(v["title"]);
				tmp.find(".green_search").text(v["url"]);
				if(v["content"]){
					tmp.find(".search_desc").text(v["content"]);
				}
				if(v["body"]){
					tmp.find(".search_desc").html(v["body"]);
				}	
				
				//console.log(tmp)
				main = main.add(tmp);

			});
			$(".search_div_result").append(main);

		},
		error:function(e){
			
		}
	});
};
search($("#search").val(),0,10);

});

