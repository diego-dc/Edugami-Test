// Archivo JS para manejar las solicitudes HTTP y actualizar la interfaz de usuario con los datos obtenidos de la API. 

// Función para manejar la solicitud de agregar estudiantes
document.getElementById("form-add-students").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto del formulario (recarga de la página)

    // Obtener el contenido del textarea
    let studentsJson = document.getElementById("add-students").value;

    try {
        // Parsear JSON
        let studentsData = JSON.parse(studentsJson);

        // Realizar una solicitud HTTP POST a la URL '/add_students/' para agregar los estudiantes
        fetch('/add_students/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentsData) // Convertir el objeto de estudiantes de vuelta a JSON para enviarlo al servidor
        })
        .then(response => response.json()) // Parsear la respuesta de la API a formato JSON
        .then(data => {
            console.log('Success:', data);
            if (data.status === 'OK') {
                alert('Estudiantes agregados correctamente');
                // Llamar a la función que actualiza la tabla
                loadStudents();
                // Mostrar la respuesta en el div #https-responses
                displayResponse(data);
            } else {
                loadStudents();
                displayResponse(data);
                alert('Error al agregar estudiantes: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } catch (error) {
        alert('Error en el formato del JSON: ' + error.message);
    }
});


// Función para manejar la solicitud de crear pruebas
document.getElementById("form-create-test").addEventListener("submit", function(event) {
    event.preventDefault();

    // Obtener el contenido del textarea
    let studentsJson = document.getElementById("create-test").value;

    try {
        // Parsear JSON
        let testData = JSON.parse(studentsJson);

        // Hacer la solicitud POST
        fetch('/test/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.status === 'OK') {
                alert('Prueba creada correctamente');
                // Llamar a la función que actualiza la tabla
                loadTests();
                // Mostrar la respuesta en el div #https-responses
                displayResponse(data);
            } else {
                loadTests();
                displayResponse(data);
                alert('Error al crear prueba: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } catch (error) {
        alert('Error en el formato del JSON: ' + error.message);
    }
});

// Función para manejar la solicitud de agregar pruebas a estudiantes
document.getElementById("form-add-test-student").addEventListener("submit", function(event) {
    event.preventDefault();

    // Obtener el contenido del textarea
    let studentListJson = document.getElementById("add-test-student").value;

    try {
        // Parsear JSON
        let studentListData = JSON.parse(studentListJson);

        let test_id = document.getElementById("test_id_0").value;

        // Hacer la solicitud POST
        fetch('test/' + test_id.toString() + '/assign', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(studentListData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.status === 'OK') {
                alert('Pruebas agregadas correctamente');
                // Mostrar la respuesta en el div #https-responses
                displayResponse(data);
            } else {
                displayResponse(data);
                alert('Error al agregar pruebas: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } catch (error) {
        alert('Error en el formato del JSON: ' + error.message);
    };
});

// Función para manejar la solicitud de enviar respuestas de estudiantes
document.getElementById("form-send-answers").addEventListener("submit", function(event) {
    event.preventDefault();

    // Obtener el contenido del textarea
    let answersJson = document.getElementById("send-answers").value;

    try {
        // Parsear JSON
        let answersData = JSON.parse(answersJson);
        // Obtener el ID de la prueba desde el input
        let test_id = document.getElementById("test_id_1").value;
        // Validar que el ID de la prueba no esté vacío
        if (test_id == '') {
            alert('Debe ingresar un ID de prueba');
            return;
        }

        // Hacer la solicitud POST
        fetch('test/' + test_id.toString() + '/answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(answersData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.status === 'OK') {
                alert('Respuestas enviadas correctamente');
                // Mostrar la respuesta en el div #https-responses
                displayResponse(data);
            } else {
                displayResponse(data);
                alert('Error al enviar respuestas: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } catch (error) {
        alert('Error en el formato del JSON: ' + error.message);
    }
});

// Funcion para manejar la solicitud de obtener resultados de una prueba
document.getElementById("form-get-results").addEventListener("submit", function(event) {
    event.preventDefault();

    try {
        // Obtener el ID de la prueba desde el input
        let test_id = document.getElementById("test_id_2").value;
        // Validar que el ID de la prueba no esté vacío
        if (test_id == '') {
            alert('Debe ingresar un ID de prueba');
            return;
        }

        // Hacer la solicitud POST
        fetch('test/' + test_id.toString() + '/answers', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.status === 'OK') {
                alert('Resultados obtenidos correctamente');
                // Mostrar la respuesta en el div #https-responses
                displayResponse(data);
            } else {
                displayResponse(data);
                alert('Error al obtener resultados: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Función para cargar estudiantes en la tabla
function loadStudents() {
    fetch('/get_students/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Obtener el cuerpo de la tabla
        let tableBody = document.getElementById("students-table-body");
        tableBody.innerHTML = ''; // Limpiar la tabla
        // Recorrer la lista de estudiantes y agregar una fila por cada uno
        data.students.forEach(student => {
            let row = `<tr>
                <th scope="row">${student.id}</th>
                <td>${student.name}</td>
                <td>${student.rut}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Función para cargar estudiantes en la tabla
function loadTests() {
    fetch('/get_tests/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Obtener el cuerpo de la tabla
        let tableBody = document.getElementById("tests-table-body");
        tableBody.innerHTML = ''; // Limpiar la tabla
        // Recorrer la lista de pruebas y agregar una fila por cada una
        data.tests.forEach(tests => {
            let row = `<tr>
                <th scope="row">${tests.id}</th>
                <td>${tests.name}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Llamar a la función al cargar la página para que siempre esté actualizada
window.onload = function() {
    loadStudents();
    loadTests();
};

// Función para mostrar la respuesta en el div #https-responses
function displayResponse(response) {
    const responseContainer = document.getElementById('https-responses');
    responseContainer.innerHTML = `<pre>${JSON.stringify(response, null, 2)}</pre>`;
}