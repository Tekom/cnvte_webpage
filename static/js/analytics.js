// const velocidad = document.getElementById('velocidad');
// const velocidad_gps = document.getElementById('velocidad_gps');
// const voltaje = document.getElementById('voltaje');
// const corriente = document.getElementById('corriente');
// const potencia = document.getElementById('potencia');
// const imu = document.getElementById('imu');

// var opciones = {
//   responsive: true,
//   maintainAspectRatio: false,
//   scales: {
//     x: {

//       type: 'linear',
//       position: 'bottom',
//       grid: {
//         display: false
//       },
//       title: {
//         display: true,
//         text: 'Tiempo [s]', // Nombre del eje X
//         font: {
//           weight: 'bold'
//         }
//       }
//     },
//     y: {
//       min: 0,    // Valor mínimo del eje y
//       max: 50,
//       grid: {
//         display: true
//       },
//       title: {
//         display: true,
//         text: '', // Nombre del eje Y
//         font: {
//           weight: 'bold'
//         }
//       }
//     }
//   }
// };

// var opciones_copia = {};

// var graph_data = {
//     type: 'line',
//     data: {
//       labels: [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
//       datasets: [{
//         label: '',
//         data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//         tension: 0.4
//       }]
//     },
//     options: opciones
// };

// var graph_imu = {
//   type: 'line',
//   data: {
//     labels: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//     datasets: [{
//       label: 'X',
//       data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//       tension: 0.4
//     },
//     {
//       label: 'Y',
//       data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//       tension: 0.4
//     },
//     { 
//       label: 'Z',
//       data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
//       tension: 0.4
//     }]
//   },
//   options: opciones
// };

// var velocidad_data = JSON.parse(JSON.stringify(graph_data));
// var velocidad_gps_data = JSON.parse(JSON.stringify(graph_data));
// var voltaje_data = JSON.parse(JSON.stringify(graph_data));
// var corriente_data = JSON.parse(JSON.stringify(graph_data));
// var potencia_data = JSON.parse(JSON.stringify(graph_data));
// var imu_data = JSON.parse(JSON.stringify(graph_imu));

// var velocidad_chart = new Chart(velocidad, velocidad_data);
// var velocidad_gps_chart = new Chart(velocidad_gps, velocidad_gps_data);
// var voltaje_chart = new Chart(voltaje, voltaje_data);
// var corriente_chart = new Chart(corriente, corriente_data);
// var potencia_chart = new Chart(potencia, potencia_data);
// var imu_chart = new Chart(imu, imu_data);







