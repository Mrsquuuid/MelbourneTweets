<template>
	<div class="chart">
		<div id="main" style="width: 100%; height: 100%;">
			<div id="loading" style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">
				<img src="../assets/loading.gif" width="10%" height="auto"/>
			</div>
		</div>
	</div>
</template>

<script>
	import $ from 'jquery';
	export default {
		name: 'Chart',
		data() {
			return {
				data: null,
				set: []
			}
		},
		methods: {
			fetch() {
				var self = this;
				$.ajax({
					url: "http://172.26.133.50/s2/d",
					type: "GET",
					dataType: "json",
					success: function(data) {
						document.getElementById('loading').style.display = 'none';
						console.log(data);
						self.data = data;
						for (var i = 0; i < data.suburb.length; i++) {
							var curr = [data.afinn_avg[i], data.bad_words_avg[i]];
							self.set.push(curr);
						}
						self.initChart();
						console.log(self.data);
					},
					error: function() {
						console.log("error");
					}
				})
			},
			initChart() {
				var chart = this.$echarts.init(document.getElementById("main"));
				var option = {
					title: {
						text: 'The correlation between the distribution of the sentiment score and the distribution of the vulgar, crime or alcohol related tweets proportion over different SA2 locations in Melbourne',
						x: 'center',
						y: 'top',
						textStyle: {
							fontSize: 14
						}
					},
					tooltip: {
						showDelay: 0,
						formatter: function(params) {
							if (params.value.length > 1) {
								return params.seriesName + ' :<br/>' + 'Afinn average: ' +
									params.value[0] + '<br/>' + 'Bad word average: ' +
									params.value[1];
							}
						}
					},
					legend: {
						data: ["Suburb"],
						left: 'center',
						bottom: 10
					},
					xAxis: {},
					yAxis: {},
					series: [{
							name: 'Suburb',
							symbolSize: 10,
							data: this.set,
							type: 'scatter'
						}
					]
				};
				chart.setOption(option);
			}
		},
		mounted() {
			this.fetch();
			// this.initChart();
		}
	}
</script>

<style>
	.chart {
		height: 100%;
		width: 100%;
	}
</style>
