/*
Author: Bill Tong (Team 34)
Project: BoardBot
Class: CS425/426
*/
var app = new Vue({
	el: '#app',
	data:{
		connected: false,
		firstLoad: true,
		ros: null,
		ws_address: 'ws://192.168.248.130:9090',
		logs: [],
	},
	methods: {
		connect: function(){
			this.logs.unshift('CONNECTING...')
			this.ros = new ROSLIB.Ros({
				url: this.ws_address
			})
			this.ros.on('connection', () => {
				this.logs.unshift((new Date()).toTimeString() + ' -connection established')
				this.connected = true
				if(this.firstLoad){
					this.setCamera()
					this.firstLoad = false
				}			
			})
			this.ros.on('error', (error) => {
				this.logs.unshift((new Date()).toTimeString() + ' - connection error')
			})
			this.ros.on('close', () => {
				this.logs.unshift((new Date()).toTimeString() + ' -connection closed')
				this.connected = false
			})
		},
		disconnect: function(){
			this.ros.close()
		},
		setCamera: function(){
			console.log('set camera method')
			this.cameraViewer = new MJPEGCANVAS.Viewer({
				divID: 'mjpeg',
				host: '192.168.248.130',
				width: 640,
				height: 480,
				topic: '/camera/rgb/image_raw',
				port: 11315,
			})
		},
	},
})
