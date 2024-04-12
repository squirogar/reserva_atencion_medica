
// Register a handler to be called when the first Ajax request begins. This is an Ajax Event.
$(document).ajaxStart(function(){
    console.log("muestra")
    $('#loading').show(); //display:block
});

//Register a handler to be called when all Ajax requests have completed. This is an Ajax Event.
$(document).ajaxStop(function(){
    console.log("oculta")
    $('#loading').hide(); //display:none
});



$(document).ready(function () {
    
    // formulario fechas
    $('#form_fecha').submit(function (e) {
        e.preventDefault();

        console.log($('#dropdown_fecha').val());
        $.ajax({
            url: django_url, //"{% url 'hosp:get_horas_disponibles' %}"
            type: "get",
            data: {
                'fecha': $('#dropdown_fecha').val(),
            },
            dataType: 'json',
            success: function (data) {
                console.log("success");
                console.log("DATA", data)

                let dropdown2HTML = "";

                if(data["opciones"].length == 0) {
                    console.log("esta vacio")
                    dropdown2HTML = '<p class="paso" id="error_horas">No hay horas disponibles para este día. Por favor, haga click en '
                    + '"Limpiar búsqueda" y consulte por otro día.</p>'
                } else {
                    dropdown2HTML = '<p class="paso">2. Elija la hora de la atención:</p>' 
                        + '<select class="sel text-center form-control form-control-lg" id="dropdown_horas">';

                    $.each(data.opciones, function (index, opcion) {
                        dropdown2HTML += '<option value="' + opcion.hora + '">' + opcion.hora + '</option>';
                    });
                    
                    dropdown2HTML += '</select>' 
                        + '<button class="btn btn-primary my-3" type="button" id="boton_buscar_medicos">Buscar médicos</button>';
                        
                }
                    
                $('#dropdown_horas_container').html(dropdown2HTML);

                //deshabilitamos el boton y dropdown de form_fecha
                $('#boton_buscar_horas').prop("disabled", true);
                $('#dropdown_fecha').prop("disabled", true);

                console.log(dropdown2HTML);
                //establecemos un listener a boton_buscar_medicos
                setListenerBoton(data);


            },
            error : function(jqXHR, status, error) {
                alert('Disculpe, ocurrió un problema');
                console.log(status);
                console.log(error);
            }, 
        });

    });



});


; 


// establece un listener en el boton buscar medicos
function setListenerBoton(data) {
    let boton_buscar_medicos = document.getElementById('boton_buscar_medicos');
    console.log("boton buscar medicos", boton_buscar_medicos);
    
    if(boton_buscar_medicos != null) {
        boton_buscar_medicos.addEventListener("click", function get_medicos() {
            let hora_elegida = document.getElementById('dropdown_horas').value;
            console.log("hora elegida", hora_elegida);
    
            let medicos = [];
            
            // recorremos el json "data" para obtener la lista de medicos
            $.each(data.opciones, function (index, opcion) {
                if (opcion.hora == hora_elegida) {
                    medicos = opcion.medicos
                    console.log(opcion.medicos);
                    return;
                }
            });
            
            
    
            let dropdown2HTML = '<p class="paso">3. Elija el médico:</p><select  name="medico" class="sel text-center form-control form-control-lg">';
            medicos.forEach(function (medico) {
                dropdown2HTML += '<option value="' + medico[0] + '">' + medico[1] + ' ' + medico[2] + '</option>';
    
            });
            
            let fecha_sel = document.getElementById("dropdown_fecha").value;
            let hora_sel = document.getElementById("dropdown_horas").value;
    
            dropdown2HTML += '</select><input type="hidden" name="fecha" value="' 
                + fecha_sel + '"/><input type="hidden" name="hora" value="' 
                + hora_sel + '" /><input class="btn btn-primary my-3" type="submit" value="Reservar atencion">';
            
            $('#dropdown_medicos_container').html(dropdown2HTML);
            
        }); // escucho el evento "click" en el botón "boton_buscar_horas"
        
    }

}


// reestablece los elementos html.
function limpiaBusqueda() {
    document.getElementById("dropdown_horas_container").innerHTML = "";
    $('#boton_buscar_horas').prop("disabled", false);
    $('#dropdown_fecha').prop("disabled", false);
    document.getElementById("dropdown_medicos_container").innerHTML = "";
}


