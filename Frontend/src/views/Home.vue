<template>
	<a-layout id="main-layout">
		<a-layout-sider :trigger="null">
			<div class="logo">Team 80</div>
			<a-menu theme="dark" mode="inline" :default-selected-keys="['0']" :open-keys="openKeys" @openChange="onOpenChange" >
				<a-menu-item key="0">
					Home
					<a href="/"></a>
				</a-menu-item>
				<a-sub-menu key="sub1">
					<span slot="title">
						<a-icon type="database" /><span>Scenario 1</span>
					</span>
					<a-menu-item key="1a">
						Chart A
						<a href="/1a"></a>
					</a-menu-item>
					<a-menu-item key="1b">
						Chart B
						<a href="/1b"></a>
					</a-menu-item>
					<a-menu-item key="1c">
						Chart C
						<a href="/1c"></a>
					</a-menu-item>
					<a-menu-item key="1d">
						Chart D
						<a href="/1d"></a>
					</a-menu-item>
					<a-menu-item key="1e">
						Chart E
						<a href="/1e"></a>
					</a-menu-item>
					<a-menu-item key="1f">
						Chart F
						<a href="/1f"></a>
					</a-menu-item>
					<a-menu-item key="1g">
						Chart G
						<a href="/1g"></a>
					</a-menu-item>
					<a-menu-item key="1h">
						Chart H
						<a href="/1h"></a>
					</a-menu-item>
				</a-sub-menu>
				<a-sub-menu key="sub2">
					<span slot="title">
						<a-icon type="database" /><span>Scenario 2</span>
					</span>
					<a-menu-item key="2a">
						Chart A
						<a href="/2a"></a>
					</a-menu-item>
					<a-menu-item key="2b">
						Chart B
						<a href="/2b"></a>
					</a-menu-item>
					<a-menu-item key="2c">
						Chart C
						<a href="/2c"></a>
					</a-menu-item>
					<a-menu-item key="2d">
						Chart D
						<a href="/2d"></a>
					</a-menu-item>
					<a-menu-item key="2e">
						Chart E
						<a href="/2e"></a>
					</a-menu-item>
					<a-menu-item key="2f">
						Chart F
						<a href="/2f"></a>
					</a-menu-item>
				</a-sub-menu>
				<a-sub-menu key="sub3">
					<span slot="title">
						<a-icon type="database" /><span>Scenario 3</span>
					</span>
					<a-menu-item key="3a">
						Chart A
						<a href="/3a"></a>
					</a-menu-item>
					<a-menu-item key="3b">
						Chart B
						<a href="/3b"></a>
					</a-menu-item>
					<a-menu-item key="3c">
						Chart C
						<a href="/3c"></a>
					</a-menu-item>
				</a-sub-menu>
			</a-menu>
		</a-layout-sider>
		<a-layout>
			<a-layout-content :style="{ margin: '30px 30px', padding: '0px', background: '#fff', minHeight: '280px' }">
				<cover></cover>
			</a-layout-content>
		</a-layout>
	</a-layout>

</template>

<script>
	// @ is an alias to /src
	import Cover from '../components/Cover.vue';

	export default {
		name: 'Home',
		components: {
			Cover
		},
		data() {
			return {
				rootSubmenuKeys: ['sub1', 'sub2', 'sub3'],
				openKeys: [],
			};
		},
		methods: {
			onOpenChange(openKeys) {
				const latestOpenKey = openKeys.find(key => this.openKeys.indexOf(key) === -1);
				if (this.rootSubmenuKeys.indexOf(latestOpenKey) === -1) {
					this.openKeys = openKeys;
				} else {
					this.openKeys = latestOpenKey ? [latestOpenKey] : [];
				}
			}
		}
	}
</script>

<style>
	#main-layout {
		height: 100vh;
	}

	#main-layout .trigger {
		font-size: 18px;
		line-height: 64px;
		padding: 0 24px;
		cursor: pointer;
		transition: color 0.3s;
	}

	#main-layout .trigger:hover {
		color: #1890ff;
	}

	#main-layout .logo {
		height: 32px;
		margin: 16px;
		color: white;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 20px;
	}

</style>
