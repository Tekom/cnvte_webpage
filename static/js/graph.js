const velocidad = document.getElementById('velocidad');
const velocidad_gps = document.getElementById('velocidad_gps');
const voltaje = document.getElementById('voltaje');
const corriente = document.getElementById('corriente');
const potencia = document.getElementById('potencia');
const imu = document.getElementById('imu');

var opciones = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {

      type: 'linear',
      position: 'bottom',
      grid: {
        display: false
      },
      title: {
        display: true,
        text: 'Tiempo [s]', // Nombre del eje X
        font: {
          weight: 'bold'
        }
      }
    },
    y: {
      min: 0,    // Valor mínimo del eje y
      max: 50,
      grid: {
        display: true
      },
      title: {
        display: true,
        text: '', // Nombre del eje Y
        font: {
          weight: 'bold'
        }
      }
    }
  }
};

var opciones_copia = {};

var graph_data = {
    type: 'line',
    data: {
      labels: [0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],
      datasets: [{
        label: '',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        tension: 0.4
      }]
    },
    options: opciones
};

var graph_imu = {
  type: 'line',
  data: {
    labels: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    datasets: [{
      label: 'X',
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      tension: 0.4
    },
    {
      label: 'Y',
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      tension: 0.4
    },
    { 
      label: 'Z',
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      tension: 0.4
    }]
  },
  options: opciones
};

var velocidad_data = JSON.parse(JSON.stringify(graph_data));
var velocidad_gps_data = JSON.parse(JSON.stringify(graph_data));
var voltaje_data = JSON.parse(JSON.stringify(graph_data));
var corriente_data = JSON.parse(JSON.stringify(graph_data));
var potencia_data = JSON.parse(JSON.stringify(graph_data));
var imu_data = JSON.parse(JSON.stringify(graph_imu));

var velocidad_chart = new Chart(velocidad, velocidad_data);
var velocidad_gps_chart = new Chart(velocidad_gps, velocidad_gps_data);
var voltaje_chart = new Chart(voltaje, voltaje_data);
var corriente_chart = new Chart(corriente, corriente_data);
var potencia_chart = new Chart(potencia, potencia_data);
var imu_chart = new Chart(imu, imu_data);

var x = 4.943271
var y = -74.014112

const map = L.map('map').setView([4.942646139951253, -74.0126042413143], 17); //starting position
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
var marker = L.marker([x, y]).addTo(map);
var socket = new WebSocket('ws://' + '127.0.0.1:8001' + '/ws/live_data/')

velocidad_data.data.datasets[0].label = 'Velocidad [Km / h]'
velocidad_gps_data.data.datasets[0].label = 'Velocidad GPS [Km / h]'
voltaje_data.data.datasets[0].label = 'Voltaje [V]'
corriente_data.data.datasets[0].label = 'Corriente [A]'
potencia_data.data.datasets[0].label = 'Potencia [W]'

var graphs_data = [
  velocidad_data,
  velocidad_gps_data,
  voltaje_data,
  corriente_data,
  potencia_data,
]

var charts = [
  velocidad_chart,
  velocidad_gps_chart,
  voltaje_chart,
  corriente_chart,
  potencia_chart,
]

// socket.onerror = function(error) {
//   console.error('WebSocket Error: ', error);
//   // Aquí puedes agregar cualquier acción adicional para manejar el error
// };
socket.onopen = function() {
  console.log('Conexión WebSocket abierta');
};

socket.onmessage = function (e) {
  var djangoData = JSON.parse(e.data)
  
  var car_data = [
    djangoData.team_data.car_velocity,
    djangoData.team_data.car_velocity_gps,
    djangoData.team_data.car_voltage,
    djangoData.team_data.car_current,
    djangoData.team_data.power,
  ]

  var car_data_imu = [
    djangoData.team_data.imu_x,
    djangoData.team_data.imu_y,
    djangoData.team_data.imu_z,
  ]

  console.log(djangoData)

  var newLat = parseFloat(djangoData.team_data.gps_1);
  var newLng = parseFloat(djangoData.team_data.gps_2);

  // Actualizar la posición del marcador en el mapa
  marker.setLatLng([newLat, newLng]);

  // Opcional: si quieres reabrir el popup en la nueva posición
  marker.bindPopup('<b>' + djangoData.team_data.team_name.toUpperCase() + '</b>').openPopup();

  for (let i = 0; i < graphs_data.length; i++) {
    var newData = graphs_data[i].data.datasets[0].data;
    newData.shift();
    newData.push(car_data[i])

    graphs_data[i].data.datasets[0].data = newData

    var newDataY = graphs_data[i].data.labels;
    newDataY.shift();
    newDataY.push(djangoData.y)

    graphs_data[i].data.labels = newDataY

    charts[i].update();
  }

  document.getElementById('velocidad_average').textContent = djangoData.team_data.average_velocity;
  document.getElementById('voltaje_average').textContent = djangoData.team_data.average_voltage;
  document.getElementById('corriente_average').textContent = djangoData.team_data.average_current;

  for (let i = 0; i < car_data_imu.length; i++) {
    var newDataImu = imu_data.data.datasets[i].data;
    newDataImu.shift();
    newDataImu.push(car_data_imu[i])
  }

  var newDataYimu = imu_data.data.labels;
  newDataYimu.shift();
  newDataYimu.push(djangoData.y)

  imu_data.data.labels = newDataYimu
  imu_chart.update();
  
  let cont = 1;

  Object.keys(djangoData.teams_data).forEach(teamKey => {
    let teamValue = djangoData.teams_data[teamKey];
    
    // if (teamKey == 'kratos') {
    //   teamValue = teamValue + 100;
    // }
      
    document.getElementById("habilidad_"+cont.toString()).textContent = cont.toString() + " " + "-" + " " + teamKey + ": " + teamValue.toString();
    cont = cont + 1;
  });

  let cont_acel = 1;
  Object.keys(djangoData.teams_data_acel).forEach(teamKey => {
    let teamValue = djangoData.teams_data_acel[teamKey];
    
    // if (teamKey == 'kratos') {
    //   teamValue = teamValue + 100;
    // }
      
    document.getElementById("aceleracion_"+cont_acel.toString()).textContent = cont_acel.toString() + " " + "-" + " " + teamKey + ": " + teamValue.toString();
    cont_acel = cont_acel + 1;
  });

  let cont_global = 1;

  Object.keys(djangoData.global_scores).forEach(teamKey => {
    let teamValue = djangoData.global_scores[teamKey];
    
    // if (teamKey == 'kratos') {
    //   teamValue = teamValue + 100;
    // }
      
    document.getElementById("global_"+cont_global.toString()).textContent = cont_global.toString() + " " + "-" + " " + teamKey + ": " + teamValue.toString();
    cont_global = cont_global + 1;
  });
}

socket.onerror = function(error) {
  console.error('Error en WebSocket: ', error);
};


// const map = L.map('map').setView([4.942646139951253, -74.0126042413143], 17); //starting position
// L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
//             maxZoom: 19,
//             attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
//         }).addTo(map);

// var marker = L.marker([x, y]).addTo(map);
// marker.bindPopup('<b>Hamilton').openPopup();
// let contador = 0
// var add = 0.00001

// var route = [
//         [x, y + add],
//         [x, y + add*2],
//         [x, y + add*3],
//         [x, y + add*4],
//         [x, y + add*5],
//         [x, y + add*6]
//     ];
    
// var currentIndex = 0;
// var interval = setInterval(() => {
//     if (currentIndex >= route.length) {
//         clearInterval(interval); // Detener la animación cuando se alcancen todos los puntos
//         return;
//     }

//     // Actualizar la posición del marcador
//     marker.setLatLng(route[currentIndex]);

//     // Ajustar la vista del mapa para centrar en el marcador
//     // map.panTo(route[currentIndex]);

//     // Incrementar el índice para pasar al siguiente punto de la ruta
//     currentIndex++;
// }, 500);




