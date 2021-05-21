<template>
	<div class="cover" id="bg">
		<div class="members">
			<h1 style="font-size: 30px;">Team 80</h1>
			<p>Qiyi Zhang</p>
			<p>Xiangtian Zha</p>
			<p>Yifan Zhu</p>
			<p>Yuzhe You</p>
			<p>Zhe Li</p>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'Cover'
	}
</script>

<style scoped>
	.cover {
		height: 100%;
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	
	#bg {
		background-image: url(../assets/sky.svg);
		background-size: cover;
	}
	
	.members {
		width: 400px;
		height: auto;
		border-radius: 10px;
		background-color: rgba(255, 255, 255, 0.9);
		pad: 50px;
	}
</style>
