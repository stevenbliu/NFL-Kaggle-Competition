// Global constants
const DEBUG = true;
const DINGUS_PRICE = 14.25;
const WIDGET_PRICE = 9.99;

// Some little helpers
const log = msg => (DEBUG ? console.log(msg) : '');
const select = id => document.getElementById(id);




function plotPie(continent) {
	if (continent === 'ANTARCTICA') {
		zingchart.exec('totalSalesChart', 'destroy');
		return;
	}
	let dingusValues = {
		values: [],
		text: "Dinguses"
	}
	let widgetValues = {
		values: [],
		text: "Widgets"
	}
	let sales = data[continent];
	let dinguses = 0, widgets = 0;
	for (const datum of sales) {
		dinguses += datum['Dingus'];
		widgets += datum['Widget'];
	}
	dingusValues['values'].push(dinguses);
	widgetValues['values'].push(widgets);
	let myConfig = {
		type: 'pie',
		legend: {},
		title: {
			text: 'Total Sales'
		},
		series: [
			dingusValues,
			widgetValues
		]
	};
	zingchart.render({
		id: 'totalSalesChart',
		data: myConfig,
		height: '100%',
		width: '100%'
	})
}

function updateScoreCards(continent) {
	let sales = data[continent];
	let dinguses = 0, widgets = 0;
	for (const datum of sales) {
		dinguses += datum['Dingus'];
		widgets += datum['Widget'];
	}
	let revenue = DINGUS_PRICE * dinguses + WIDGET_PRICE * widgets;
	select('dingusSold').innerHTML = dinguses;
	select('widgetSold').innerHTML = widgets;
	select('totalSales').innerHTML = revenue.toFixed(2);
}

async function loadJSON(path) {
	let response = await fetch(path);
	let dataset = await response.json(); // Now available in global scope
	return dataset;
}

function hCol(sales) {

	dingus_series = [];
	widget_series = [];

	for (month in sales) {
		dingus_series.push(sales[month]['Dingus']);
		widget_series.push(sales[month]['Widget']);
	}

	Highcharts.chart('hCol', {
		chart: {
			type: 'column'
		},
		title: {
			text: '<b> Monthly Sales </b>'
		},
		legend: {
			align: 'right',
			verticalAlign: 'top',
			layout: 'vertical',
			borderWidth: 2,
			floating: true,
			symbolHeight: 9,
			symbolWidth: 9,
			symbolRadius: 0
		},
		xAxis: {
			categories: ['January', 'February', 'March'],
			title: {
				text: '<b> Month </b> '
			}
		},
		tooltip: {
			headerFormat: null,
			pointFormat: '{point.y}'
		},
		yAxis: {
			min: 0,
			title: {
				text: '<b> Number of units sold </b>'
			}
		},
		plotOptions: {
			series: {
				groupPadding: .05,
				pointPadding: .05
			}
		},
		series: [{
			name: 'Dingus',
			data: dingus_series,
			color: 'teal'
		}, {
			name: 'Widget',
			data: widget_series,
			color: 'red'
		}]
	})
}

function hPie(sales) {

	dingus_total = 0;
	widget_total = 0;

	for (month in sales) {
		dingus_total += sales[month]['Dingus'];
		widget_total += sales[month]['Widget'];
	}

	Highcharts.chart('hPie', {
		chart: {
			type: 'pie'
		},
		title: {
			text: '<b> Total Sales </b>'
		},
		plotOptions: {
			pie: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: {
					enabled: true,
					format: '{point.percentage:.1f}',
					distance: -80
				},
				showInLegend: true
			}
		},
		legend: {
			align: 'right',
			verticalAlign: 'top',
			layout: 'vertical',
			//borderColor: 'black',
			borderWidth: 2,
			floating: true,
			symbolHeight: 9,
			symbolWidth: 9,
			symbolRadius: 0
		},
		tooltip: {
			pointFormat: '{point.y}',
			headerFormat: null
		},
		series: [{
			data: [{
				name: 'Widget',
				y: widget_total,
				color: 'red'
			}, {
				name: 'Dingus',
				y: dingus_total,
				color: 'teal'
			}]
		}]
	});
}

function hMap(sales) {

	var data = [
		['eu', 0],
		['oc', 1],
		['af', 2],
		['as', 3],
		['na', 4],
		['sa', 5]
	];

	// Create the chart
	Highcharts.mapChart('hMap', {
		chart: {
			map: 'custom/world-continents'
		},

		tooltip: {
			headerFormat: null,
			pointFormat: '{point.name}',
		},

		title: {
			text: null
		},

		legend: {
			enabled: false
		},

		colors: ['lightgray'],

		series: [{
			data: data,
			allowPointSelect: true,
			stickyTracking: false,

			states: {
				hover: {
					color: 'gray'
				},
				select: {
					color: 'green',
				},
			},
			events: {
				mouseOver: function (continent) {
					//console.log(continent.target);
					continent.target.update({
						states: {
							select: {
								color: '#39cc59'
							}
						}
					});
				},

				mouseOut: function (continent) {
					continent.target.update({
						states: {
							select: {
								color: '#64853a'
							}
						}
					});

				},

				click: function (continent) {
					name = continent.point.name.toUpperCase().replace(" ", "");
					if (name == 'OCEANIA') {
						name = 'AUSTRALIA';
					}

					let dinguses = 0, widgets = 0;
					for (const datum of sales[name]) {
						dinguses += datum['Dingus'];
						widgets += datum['Widget'];
					}
					let revenue = DINGUS_PRICE * dinguses + WIDGET_PRICE * widgets;
					select('dingusSold').innerHTML = dinguses;
					select('widgetSold').innerHTML = widgets;
					select('totalSales').innerHTML = revenue.toFixed(2);

					hCol(sales[name]);
					hPie(sales[name]);
					//console.log(continent.target);
				}
			},

			dataLabels: {
				enabled: true,
				format: '{point.name}',
				color: 'black'
			}
		}]
	});
}

function hStocks(stocks) {
	data = [];
	for (i in stocks) {
		data.push([stocks[i]['Date'], stocks[i]['Close']]);
	}

	Highcharts.chart('hStock', {
		chart: {
			type: 'area'
		},
		title: {
			text: '<b> Dynamic Growth </b>'
		},
		subtitle: {
			text: '<b> Stock Prices of D&W Corp. from 2015-Present </b>'
		},
		xAxis: {
			type: 'datetime',
			title: {
				text: '<b> Date </b>'
			},
			labels: {
				format: '{value: %m/%e/%y}'
			},
			crosshair: {
				width: 1,
				color: 'black'
			}
		},
		yAxis: {
			title: {
				text: '<b> Adj Close Stock Price </b>'
			},
			
			
			crosshair: {
				labels: {
					enabled: true
				},
				width: 1,
				color: 'black'
				
			}
		},
		tooltip: {
			pointFormat: '${point.y:.2f}',
			split: true,
			shared: true
		},
		plotOptions: {
			marker: {
				symbol: 'triangle'
			}
		},
		legend: {
			enabled: false
		},
		series: [{
			data: data,
			lineColor: '#256fa1',
			color: 'lightblue',
			opacity: .7
		}]
	})

}

function init() {
	var sales = loadJSON('./data/sales.json');
	var stocks = loadJSON('./data/stocks.json');

	sales.then(function (sales) {
		hMap(sales);
	})

	stocks.then(function (stocks) {
		hStocks(stocks);
	})
}

document.addEventListener('DOMContentLoaded', init, false);



