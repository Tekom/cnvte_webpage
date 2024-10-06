const engine_velocity = document.getElementById('myChart');
const car_velocity = document.getElementById('velocity');
const voltage = document.getElementById('voltage');
const current = document.getElementById('current');
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
      labels: [0, 0, 0, 0, 0],
      datasets: [{
        label: '',
        data: [0, 0, 0, 0, 0],
        tension: 0.4
      }]
    },
    options: opciones
};

var graph_imu = {
  type: 'line',
  data: {
    labels: [0, 0 , 0, 0, 0],
    datasets: [{
      label: 'X',
      data: [0, 0 , 0, 0, 0],
    },
    {
      label: 'Y',
      data: [0, 0 , 0, 0, 0],
    },
    { 
      label: 'Z',
      data: [0, 0 , 0, 0, 0],
    }]
  },
  options: opciones
};

var graph_data_engine = JSON.parse(JSON.stringify(graph_data));;
var graph_data_velocity = JSON.parse(JSON.stringify(graph_data));;
var graph_data_voltage = JSON.parse(JSON.stringify(graph_data));;
var graph_data_current = JSON.parse(JSON.stringify(graph_data));;
var graph_data_imu = JSON.parse(JSON.stringify(graph_imu));;

var engine_chart = new Chart(engine_velocity, graph_data_engine);
var velocity_chart = new Chart(car_velocity, graph_data_velocity);
var voltage_chart = new Chart(voltage, graph_data_voltage);
var current_chart = new Chart(current, graph_data_current);
var imu_chart = new Chart(imu, graph_data_imu);

var socket = new WebSocket('ws://' + '127.0.0.1:8001' + '/ws/live_data/')

// graph_data_engine.data.datasets[0].label = 'Velocidad [Km / h]'
// graph_data_velocity.data.datasets[0].label = 'Velocidad GPS [Km / h]'
// graph_data_voltage.data.datasets[0].label = 'Voltaje [V]'
// graph_data_current.data.datasets[0].label = 'Corriente [A]'
// graph_data_engine.data.datasets[0].label = 'Test'

var graphs_data = [
  graph_data_engine,
  graph_data_velocity,
  graph_data_voltage,
  graph_data_current,
]

var charts = [
  engine_chart,
  velocity_chart,
  voltage_chart,
  current_chart,
]

socket.onmessage = function (e) {
  var djangoData = JSON.parse(e.data)
  
  var car_data = [
    djangoData.team_data.car_velocity,
    djangoData.team_data.car_velocity,
    djangoData.team_data.car_voltage,
    djangoData.team_data.car_current,
    djangoData.team_data.gps_1
  ]

  console.log(djangoData)

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

  let cont = 1;

  Object.keys(djangoData.teams_data).forEach(teamKey => {
    let teamValue = djangoData.teams_data[teamKey];
    
    // if (teamKey == 'kratos') {
    //   teamValue = teamValue + 100;
    // }
      
    document.getElementById(cont.toString()).textContent = teamKey + ": " + teamValue.toString();
    cont = cont + 1;
  });

  document.getElementById('velocidad').textContent = djangoData.team_data.average_velocity;
  document.getElementById('voltaje').textContent = djangoData.team_data.average_voltage;
  document.getElementById('corriente').textContent = djangoData.team_data.average_current;

  console.log('asdasds')
}
// const cloud_data = {'engine_velocity':{
//   'title': 'Velocidad motor [rad/s]',
//   'y_label': 'RPM [rad]',
//   'variable': graph_data_engine,
// },
// 'car_velocity':{
//   'title': 'Velocidad automovil [km/h]',
//   'y_label': 'Velocidad [km]',
//   'variable': graph_data_velocity,
// },
// 'voltage':{
//   'title': 'Voltaje motor [V]',
//   'y_label': 'Voltaje [V]',
//   'variable': graph_data_voltage,
// },
// 'current':{
//   'title': 'Corriente motor [A]',
//   'y_label': 'Corriente [A]',
//   'variable': graph_data_current,
// },
// 'imu':{
//   'title': 'IMU',
//   'y_label': 'Grados [°]',
//   'variable': graph_data_imu,
// },

// 'pwm':{
//   'title': 'PWM',
//   'y_label': 'Amplitud [V]',
//   'variable': graph_data_pwm,
// }}

// function start(opcion) {

//   if (opcion == 'iniciar'){
//   window.sse_client = new EventSource('/sse/');
//   sse_client.onopen  = function(message_event) {
//     console.log('opened')
//   }
//   //console.log(sse_client)

//   sse_client.onmessage =  (e) => {
//     var djangoData = JSON.parse(e.data);
//     var keys = Object.keys(djangoData);
    

//     for (let i = 0; i < keys.length; i++) {

//       if(keys[i] != 'tiempo'){
//         if(keys[i] != 'imu'){
//           var new_graph_data = cloud_data[keys[i]].variable.data.datasets[0].data;
//           var tiempo = cloud_data[keys[i]].variable.data.labels

//           new_graph_data.shift();
//           tiempo.shift();
//           new_graph_data.push(djangoData[keys[i]]);
//           tiempo.push(djangoData.tiempo);       
      
//           cloud_data[keys[i]].variable.data.datasets[0].data = new_graph_data;
//           cloud_data[keys[i]].variable.options.scales.y.title.text = cloud_data[keys[i]].y_label;
//           cloud_data[keys[i]].variable.data.datasets[0].label = cloud_data[keys[i]].title;
//         }
  
//         else{
//           var new_graph_data = cloud_data[keys[i]].variable.data.datasets[0].data;
//           var new_graph_data2 = cloud_data[keys[i]].variable.data.datasets[1].data;
//           var new_graph_data3 = cloud_data[keys[i]].variable.data.datasets[2].data;
//           var tiempo = cloud_data[keys[i]].variable.data.labels
  
//           x_imu_val = djangoData[keys[i]].x
//           y_imu_val = djangoData[keys[i]].y
//           z_imu_val = djangoData[keys[i]].z
  
//           new_graph_data.shift();
//           new_graph_data.push(x_imu_val);
  
//           new_graph_data2.shift();
//           new_graph_data2.push(y_imu_val);
  
//           new_graph_data3.shift();
//           new_graph_data3.push(z_imu_val);
          
//           tiempo.shift();
//           tiempo.push(djangoData.tiempo);
//           imu_chart.update();
//         }
//       }
//     }

//     engine_chart.update();
//     velocity_chart.update();
//     voltage_chart.update();
//     current_chart.update();
//     pwm_chart.update();

//     window.postMessage({'message': 'Hello, world!'});
//   }
//  }

//  else if (opcion == 'cerrar'){
//     window.sse_client.close();
//     cloud_data['engine_velocity'].variable.data.datasets[0].data = [0, 0, 0, 0, 0];
//     cloud_data['engine_velocity'].variable.data.labels = [0, 0, 0, 0, 0];

//     cloud_data['car_velocity'].variable.data.datasets[0].data = [0, 0, 0, 0, 0];
//     cloud_data['car_velocity'].variable.data.labels = [0, 0, 0, 0, 0];

//     cloud_data['voltage'].variable.data.datasets[0].data = [0, 0, 0, 0, 0];
//     cloud_data['voltage'].variable.data.labels = [0, 0, 0, 0, 0];

//     cloud_data['current'].variable.data.datasets[0].data = [0, 0, 0, 0, 0];
//     cloud_data['current'].variable.data.labels = [0, 0, 0, 0, 0];

//     cloud_data['imu'].variable.data.datasets[0].data = [0, 0, 0, 0, 0];
//     cloud_data['imu'].variable.data.datasets[1].data = [0, 0, 0, 0, 0];
//     cloud_data['imu'].variable.data.datasets[2].data = [0, 0, 0, 0, 0];
//     cloud_data['imu'].variable.data.labels = [0, 0, 0, 0, 0];

//     cloud_data['pwm'].variable.data.datasets[0].data = [0, 0, 0, 0, 0];
//     cloud_data['pwm'].variable.data.labels = [0, 0, 0, 0, 0];

//  }
// }

//document.getElementById("startButton").addEventListener("click", start);




