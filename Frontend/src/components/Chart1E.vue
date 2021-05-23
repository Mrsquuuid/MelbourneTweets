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
					url: "http://172.26.129.23/s1/c",
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
						text: 'The sentiment score for tweets made in 2019 and 2020 containing China-related keywords over different SA2 locations in Sydney',
						subtext: '(top 5 suburbs and last 5 suburbs)',
						x: 'center',
						y: 'top',
						textStyle: {
							fontSize: 16
						}
					},
					tooltip: {},
					legend: {
						data: ['Average', 'Total'],
						x: 'center',
						y: 'bottom'
					},
					xAxis: {},
					yAxis: {
						data: this.data.suburb,
						axisLabel: {
							textStyle: {
								fontSize: 5
							}
						}
					},
					series: [{
							name: 'Average',
							type: 'bar',
							data: this.data.avg,
							color: '#5470c6'
						},
						{
							name: 'Total',
							type: 'bar',
							data: this.data.total,
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
