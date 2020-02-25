var time_line = []
var standups = []
var standupsNot = []
function dailyGraph(date){
  var standupsPosted = {
    x: eval('time_line'+date),
    y: eval('standups'+date),
    type: 'scatter',
    name: 'Standups Posted'
  };

  var standupsNotPosted = {
    x: eval('time_line'+date),
    y: eval('standupsNot'+date),
    name: 'Standups Not Posted',
    type: 'scatter'
  };

  var data = [standupsPosted, standupsNotPosted];

  window.addEventListener('load', function () {
    Plotly.newPlot(date, data);
  })
}
