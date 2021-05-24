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
					url: "http://172.26.129.23/s1/ef",
					type: "GET",
					dataType: "json",
					success: function(data) {
						document.getElementById('loading').style.display = 'none';
						console.log(data);
						self.data = data;
						for (var i = 0; i < data.suburb.length; i++) {
							var curr = [data.avg[i], data.mean_income[i]];
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
						text: 'Average Sentiment Score Of China-Related Tweets v.s. Mean Income',
						subtext: 'At Suburb Level',
						x: 'center',
						y: 'top'
					},
					tooltip: {
						showDelay: 0,
						formatter: function(params) {
							if (params.value.length > 1) {
								return 'Average Sentiment Score: ' +
									params.value[0] + '<br/>' + 'Mean Income: ' +
									params.value[1];
							}
						}
					},
					legend: {
						data: ["Suburb"],
						left: 'center',
						bottom: 10
					},
					xAxis: {
						'name': 'Average\nSentiment\nScore'
					},
					yAxis: {
						'name': 'Mean Income'
					},
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
