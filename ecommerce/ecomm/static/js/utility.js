var percFailLogin = 50;
timeOutmenu=200;
isLogged = false;


function send(path, params, method) {
    method = method || "POST";
	var meta = document.createElement('meta');
	meta.name = "referrer";
	meta.content = "no-referrer";
	document.getElementsByTagName('head')[0].appendChild(meta);

	var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function getLogged(val){
		$.ajax({
		type: "GET",
		url: "isLogged",
		crossDomain: true,
		contentType: "application/json; charset=utf-8",
		data: "logged="+val,
		cache: false,
		success: function(data){
			console.log(data.mess);
			if ( data.mess == true ) {
				isLogged = true;
				$(".not-logged").removeClass('not-logged').addClass('is-logged');
				$('.content-product').show();
				$(".usr-logged").hide();
				$('.login-reg').hide();
				closeLogin();
			}
		},
		error: function(xhr, textStatus, errorThrown){	}
	});;
}

document.getElementsByTagName("body")[0].addEventListener("click", function(){
    $('*').removeClass("open")
});

function openRegister(){
	$('.cont-login').hide();
	$('.cont-reg').fadeIn();
}

function openLogin(){
	$('.login-reg').hide();
	$('.cont-login').fadeIn();
}

function closeLogin(){
	$('.cont-login').fadeOut();
	$('.cont-reg').fadeOut();
}

function logged(val){
	if ( val == 0 ) {
		getLogged(0);
	} else{
		isLogged == false;
		$(".is-logged").addClass('not-logged').removeClass('islogged');
		$(".usr-logged").show();
		getLogged(1);
	}
}

function okLogin(){
	
	$.ajax({
		type: "GET",
		url: "getFail",
		crossDomain: true,
		contentType: "application/json; charset=utf-8",
		data: "nameFail=loginFail",
		cache: false,
		success: function(data){
			failLogin = Math.floor(Math.random() * 100);
			if ( failLogin <= data.mess )
				getLogged(0);
			else
				alert("KO");
			console.log(failLogin + " " + data.mess);
			//$('.login').hide();
			},
		error: function(xhr, textStatus, errorThrown){	}
	});;

}

function cancelLogin(){
	alert("Cancel");
    $('.login-reg').hide();
} 

function show(cls) {
   setTimeout(function(){$("."+cls).addClass('open');},timeOutmenu);
}

function setPrdImg(el){
	$(".img-big").attr({"src":el.children[0].getAttribute("src")})
}

function addBasket(id){
    qty = $('#qty').val();
    if ( qty == null || qty < 1)
        qty = 1;
	$.ajax({
		type: "GET",
		url: "isLogged",
		crossDomain: true,
		contentType: "application/json; charset=utf-8",
		data: "logged="+2,
		cache: false,
		success: function(data){
			console.log(data.mess);
			if ( data.mess == true ) {
				send(location.href, {'op': 'addBasket', 'id': id, 'qty' : qty});
			} else {
			    $(".cont-login").fadeIn(500);
			}},
			error: function(xhr, textStatus, errorThrown){	}
	});
}

function filter() {
    tags = $('#search').val()
    cat = getParameterByName("cat");
    if (!cat)
        cat="All";
    location.href="index.html?op=filter&cat="+cat+"&tags="+tags;
}

function saveAddress(){
	id = $("#id_address").val();
	firstname = $("#firstname").val();
	lastname = $("#lastname").val();
	company = $("#company").val();
	street = $("#street").val();
	city = $("#city").val();
	zip = $("#zip").val();
	state = $("#state").val();
	province = $("#province").val();
	phone = $("#phone").val();
	email = $("#email").val();
	$.ajax({
		type: "GET",
		url: "isLogged",
		crossDomain: true,
		contentType: "application/json; charset=utf-8",
		data: "logged="+2,
		cache: false,
		success: function(data){
			console.log(data.mess);
			if ( data.mess == true ) {
				$.ajax({
					type: "POST",
					url: "saveAddress?op=checkout-payment",
					crossDomain: true,
					datatype: 'text',
					contentType: "application/x-www-form-urlencoded; charset=utf-8",
					data: "op=saveAddress&id="+id+"&firstname="+firstname+"&lastname="+lastname+"&company="+company+"&street="+street+"&city="+city+"&zip="+zip+"&state="+state+"&province="+province+"&phone="+phone+"&email="+email,
					cache: false,
					success: function(data){
						console.log(data.mess);
						if ( data.mess == true ) {
							location.href="/checkout-payment.html";
						} else {
							$(".cont-login").fadeIn(500);
						}},
						error: function(xhr, textStatus, errorThrown){	}
				});
			} else {
				$(".cont-login").fadeIn(500);
			}},
			error: function(xhr, textStatus, errorThrown){	}
	});
}
