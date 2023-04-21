/*
Author: Bill Tong
Objective: Adds dynamic functionality to connection page
*/

var app = new Vue({
	// Set ip address for index.html to search
	el: '#app',
	data:{
		connected: false,
		firstLoad: true,
		ros: null,
		ws_address: 'ws://192.168.248.130:9090',
		logs: [],
	},
	methods: {
		// Upon user clicking connect, attempt to establish connection
		// Appropriate response should be written in message log based on whether connection status.
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
		// Upon user clicking disconnect, the connection should close
		disconnect: function(){
			this.ros.close()
		},
		// Setup camera interface & connection to CvBridege
		setCamera: function(){
			console.log('open camera')
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
