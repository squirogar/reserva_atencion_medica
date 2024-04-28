$(document).ajaxStart(function(){
    console.log("muestra")
    document.getElementById("loading").style.display = "block";
    document.getElementById("btnGuardarPass").disabled = true;

});

$(document).ajaxStop(function(){
    console.log("oculta")
    document.getElementById("loading").style.display = "none";
    document.getElementById("btnGuardarPass").disabled = false;
});


$(document).ready(function () {
    
    // formulario cambia contraseña
    $('#formCambiaPassword').submit(function (e) {
        e.preventDefault();
        const formData = $("#formCambiaPassword").serialize(); //para que pueda enviarse al servidor
    
        //limpio divmensajes
        limpiaMensajePass();

        $.ajax({
            url: cambiaPasswordUrl, //"{% url 'usr:cambia_password' %}"
            type: "post",
            data: formData,
            dataType: 'json',
            success: function (response) {
                console.log("success");
                console.log(response, typeof response);

                const divMensaje = document.getElementById("divMensajePass");                
                let color = null;
                
                if (response["cambio_efectivo"]) {
                    //insertar dentro de la modal el mensaje de exito
                    const parrafo = document.createElement("p");
                    parrafo.appendChild(document.createTextNode("Éxito"));
                    divMensaje.appendChild(parrafo);
                    color = "blue";
                
                } else {
                    //insertar dentro de la modal el mensaje de error
                    for (const prop in response["mensajes"]) {
                        console.log(prop, response["mensajes"][prop], typeof response["mensajes"][prop]);
                        
                        const parrafo = document.createElement("p"); 
                        parrafo.appendChild(document.createTextNode(response["mensajes"][prop][0]));
                        divMensaje.appendChild(parrafo);//agrega el mensaje al div dentro de la modal
                    }

                    color = "red";
                    
                }
            
                
                divMensaje.style.color = color;

            },
            error : function(jqXHR, status, error) {
                alert('Disculpe, ocurrió un problema');
                console.error(status);
                console.error(error);
            }, 
        });

    });

});



function limpiaMensajePass() {
    document.getElementById("divMensajePass").textContent = "";
}