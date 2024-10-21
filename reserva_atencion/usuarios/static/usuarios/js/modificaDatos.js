$(document).ajaxStart(function(){
    document.getElementById("loadingModDatos").style.display = "block";
    document.getElementById("btnGuardarModificarDatos").disabled = true;

});

$(document).ajaxStop(function(){
    document.getElementById("loadingModDatos").style.display = "none";
    document.getElementById("btnGuardarModificarDatos").disabled = false;
});


$(document).ready(function () {
    
    // formulario modifica datos
    $('#formModificaDatos').submit(function (e) {
        e.preventDefault();
        const formData = $("#formModificaDatos").serialize(); //para que pueda enviarse al servidor
    
        limpiaMensajeModDatos();

        $.ajax({
            url: modificaDatosUrl, //"{% url 'usr:cambia_datos' %}"
            type: "post",
            data: formData,
            dataType: 'json',
            success: function (response) {

                const divMensaje = document.getElementById("divMensajeModDatos");                
                let color = null;

                if (response["cambio_efectivo"]) {
                    //insertar dentro de la modal el mensaje de exito
                    const parrafo = document.createElement("p");
                    parrafo.appendChild(document.createTextNode("Éxito"));
                    divMensaje.appendChild(parrafo);//agrega el mensaje al div dentro de la modal
                    

                    //reemplazar los datos por la nueva data
                    document.getElementById("nombre").textContent = response["datos"]["nombre"];
                    document.getElementById("nombreTitulo").textContent = response["datos"]["nombre"];
                    document.getElementById("apellido").textContent = response["datos"]["apellido"];
                    document.getElementById("apellidoTitulo").textContent = response["datos"]["apellido"];
                    document.getElementById("direccion").textContent = response["datos"]["direccion"];

                    color = "blue";


                } else {
                    for (const prop in response["mensajes"]) {
                        
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
            }, 
        });

    });

});


function limpiaMensajeModDatos() {
    document.getElementById("divMensajeModDatos").textContent = "";
}