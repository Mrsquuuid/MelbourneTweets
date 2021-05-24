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
				data: null
			}
		},
		methods: {
			fetch() {
				var self = this;
				$.ajax({
					url: "http://172.26.129.23/s1/ab",
					type: "GET",
					dataType: "json",
					success: function(data) {
						document.getElementById('loading').style.display = 'none';
						console.log(data);
						self.data = data;
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
						text: 'Total Sentiment Score For China-Related Tweets By Month',
						x: 'center',
						y: 'top'
					},
					tooltip: {},
					legend: {
						data: ['Covid & China', 'Vulgar & China', 'China'],
						x: 'center',
						y: 'bottom'
					},
					xAxis: {
						name: 'Month',
						data: this.data.china_stats.date
					},
					yAxis: {
						name: 'Total Sentiment Score'
					},
					series: [{
							name: 'Covid & China',
							type: 'line',
							data: this.data.china_covid_stats.total,
							color: '#5470c6'
						},
						{
							name: 'Vulgar & China',
							type: 'line',
							data: this.data.china_vulgar_stats.total,
							color: '#fc0107'
						},
						{
							name: 'China',
							type: 'line',
							data: this.data.china_stats.total,
							color: '#20ffff'
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
