$(".novo_orodje").on("keyup", function(e){
    if(this.value!=""){
        $(".oznaci").prop("checked", "checked");
    }else{
        $(".oznaci").prop("checked", ""); 
    }
});