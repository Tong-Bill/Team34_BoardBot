import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class Info extends StatelessWidget {
  const Info({Key? key}) : super(key: key);

  _launchURLApp(int buttonCounter) async {
    if (buttonCounter == 1) {
      var url = Uri.parse('https://team34boardbot.wixsite.com/boardbot');
      await launchUrl(url);
    }
    else {
      var url2 = Uri.parse('https://github.com/Tong-Bill/Team34_BoardBot');
      await launchUrl(url2);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
          image: DecorationImage(
              image: AssetImage('images/wallpaper2.jpg'), fit: BoxFit.cover)),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          leading: IconButton(
            icon: Icon(Icons.arrow_back_sharp),
            onPressed: () {Navigator.pop(context);},
          ),
          title: Text('INFO'),
          backgroundColor: Colors.transparent,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(15),
                constraints: const BoxConstraints.expand(
                  width: 250,
                  height: 250,
                ),
                decoration: const BoxDecoration(
                  boxShadow: [
                    BoxShadow(
                        color: Colors.red,
                        offset: Offset(0, 2),
                        spreadRadius: 5,
                        blurRadius: 10),
                  ],
                  image: DecorationImage(
                    // Taken from NightCafe AI art generator
                      image: AssetImage('images/info2.jpg'),
                      fit: BoxFit.cover),
                  shape: BoxShape.circle,
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,20,0,10),
                child: Text(
                    "\"A robotic monopoly player with social interaction for children & elderly\"",
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.white, fontSize: 20, fontStyle: FontStyle.italic, fontWeight: FontWeight.bold),),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,10,0,10),
                child: Text(
                  "Tech Stack:\nFlutter w/ Dart, Python3",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,10,0,10),
                child: ElevatedButton.icon(icon:Icon(Icons.web), label: Text("Website"), onPressed: () {_launchURLApp(1);},
                style: ElevatedButton.styleFrom(
                  textStyle: TextStyle(fontWeight: FontWeight.bold, fontSize: 20,),
                  fixedSize: Size.fromWidth(175),
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,10,0,20),
                child: ElevatedButton.icon(icon:Icon(Icons.developer_mode), label: Text("Github"), onPressed: () {_launchURLApp(2);},
                  style: ElevatedButton.styleFrom(
                    textStyle: TextStyle(fontWeight: FontWeight.bold, fontSize: 20,),
                    fixedSize: Size.fromWidth(175),
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
