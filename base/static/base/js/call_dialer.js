function create_call(phone){
    url ='/orders/call/'+phone+'/';
    $.ajax(url,{
        type:'GET',
        success: function (result){
            if(result.hasOwnProperty('error')){
                alert(result.error);
            } else if(result.hasOwnProperty('caller')){
                alert('MAKE CALL '+result.caller.name);
            } else {
                console.log(result)
                alert('ERROR');
            }
        }
    })
}