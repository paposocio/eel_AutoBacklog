eel.expose(enviarFormulario)
function enviarFormulario(event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera predeterminada

    // Rutas archivos excel
    let ruta_excel_base1 = document.getElementById('ruta_excel_base1').textContent;
    let ruta_excel_base2 = document.getElementById('ruta_excel_base2').textContent;
    let ruta_excel_base3 = document.getElementById('ruta_excel_base3').textContent;
    let ruta_excel_estadoPrio = document.getElementById('ruta_excel_estadoPrio').textContent;

    let rutas = [ruta_excel_base1, ruta_excel_base2, ruta_excel_base3, ruta_excel_estadoPrio]

    let mes1 = document.getElementById('mes1').value;
    let mes2 = document.getElementById('mes2').value;
    let mes3 = document.getElementById('mes3').value;

    let meses = [mes1, mes2, mes3]

    eel.data(rutas, meses)
    location.href = '/views/preview.html'
}

eel.expose(enviarFormularioMovil)
function enviarFormularioMovil(event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera predeterminada

    let ruta_excel_base = document.getElementById('ruta_excel_base').textContent;
    let ruta_excel_estadoPrio = document.getElementById('ruta_excel_estadoPrio').textContent;

    let mes1 = document.getElementById('mes1').value;
    let mes2 = document.getElementById('mes2').value;
    let mes3 = document.getElementById('mes3').value;

    let meses = [mes1, mes2, mes3]
    let rutas = [ruta_excel_base, ruta_excel_estadoPrio]

    eel.data_mobile(rutas,meses)

    location.href = '/views/preview_mobile.html'
}
