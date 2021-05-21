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
					url: "http://172.26.133.50/s1/ab",
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
						text: 'The number of tweets containing keywords related to China from 2019 to 2020',
						x: 'center',
						y: 'top'
					},
					tooltip: {},
					legend: {
						data: ['Covid Word', 'China Word', 'Vulgar Word'],
						x: 'center',
						y: 'bottom'
					},
					xAxis: {
						data: this.data.china_stats.date
					},
					yAxis: {},
					series: [{
							name: 'Covid Word',
							type: 'line',
							data: this.data.china_covid_stats.count,
							color: '#5470c6'
						},
						{
							name: 'China Word',
							type: 'line',
							data: this.data.china_stats.count,
							color: '#20ffff'
						},
						{
							name: 'Vulgar Word',
							type: 'line',
							data: this.data.china_vulgar_stats.count,
							color: '#fc0107'
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
