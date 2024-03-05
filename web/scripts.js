eel.expose(go_to)
function go_to(url) { window.location.replace(url); };

eel.expose(enviarFormulario)
function enviarFormulario(event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera predeterminada

    // Rutas archivos excel
    let ruta_excel_base1 = document.getElementById('ruta_excel_base1').textContent;
    let ruta_excel_base2 = document.getElementById('ruta_excel_base2').textContent;
    let ruta_excel_base3 = document.getElementById('ruta_excel_base3').textContent;

    let rutas = [ruta_excel_base1,ruta_excel_base2,ruta_excel_base3]

    let mes1 = document.getElementById('mes1').value;
    let mes2 = document.getElementById('mes2').value;
    let mes3 = document.getElementById('mes3').value;

    let meses = [mes1,mes2,mes3]

    eel.data(rutas,meses)
}

