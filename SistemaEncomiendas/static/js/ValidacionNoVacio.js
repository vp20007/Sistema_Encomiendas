//Se utiliza para medir el tiempo antes que desaparezca el mensaje de error
setTimeout(function() {
    document.querySelector('.toast').classList.add('d-none');
}, 5000);

//Se utiliza para mostrar mensajes de error
$(document).ready(function() {
    $('.toast').toast('show');
});

//se utiliza para la validacion de los campos usando Bootstrap
(function () {
    'use strict';

    
    var forms = document.querySelectorAll('.needs-validation');

    
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
})();

//Se utiliza para burbujas de texto
// Inicializar tooltips de Bootstrap
$(document).ready(function() {
$('[data-bs-toggle="tooltip"]').tooltip();
});

//se utiliza para los modales
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('eliminarModal');
    const form = document.getElementById('eliminarForm');
    const itemNameSpan = document.getElementById('itemNameSpan');

    modal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const itemId = button.getAttribute('data-item-id');
        const itemName = button.getAttribute('data-item-name');
        const itemType = button.getAttribute('data-item-type');
        console.log("Item ID:", itemId);

        // Actualizar el action del formulario con el tipo y ID del ítem
        form.setAttribute('action', `/${itemType}/${itemId}/`);
        itemNameSpan.textContent = itemName;
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const action = form.getAttribute('action');
        const formData = new FormData(form);

        fetch(action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            // Manejar la respuesta
            console.log(data);  // Puedes imprimir la respuesta para verificar
            location.reload();  // Recargar la página para actualizar la lista
        })
        .catch(error => console.error('Error:', error));
    });
});


//permite poner el - automaticamente en las entradas de dui
document.addEventListener('DOMContentLoaded', function() {
    var input1 = document.getElementById('DUI');

    input1.addEventListener('input', function() {
        var valor = this.value.replace(/\D/g, ''); // Elimina cualquier carácter que no sea número
        var formattedValue = '';

        if (valor.length > 8) {
            formattedValue += valor.substr(0, 8) + '-' + valor.substr(8);
        } else if (valor.length <= 8) {
            formattedValue = valor;
        }

        this.value = formattedValue;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var input1 = document.getElementById('tel');

    input1.addEventListener('input', function() {
        var valor = this.value.replace(/\D/g, ''); // Elimina cualquier carácter que no sea número
        var formattedValue = '';

        if (valor.length > 4) {
            formattedValue += valor.substr(0, 4) + '-' + valor.substr(4);
        } else if (valor.length <= 4) {
            formattedValue = valor;
        }

        this.value = formattedValue;
    });
});