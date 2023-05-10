// Author: Bill Tong
// Scrapped in favor of a new Web User Interface

import 'package:flutter/material.dart';
import 'package:boardbot_app/dashboard.dart';

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
          image: DecorationImage(
              image: AssetImage('images/wallpaper2.jpg'), fit: BoxFit.cover)),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text.rich(TextSpan(
              children: [
                TextSpan(
                    text: 'My',
                    style: TextStyle(fontSize: 16, color: Colors.white)),
                TextSpan(
                    text: 'Boardbot',
                    style: TextStyle(
                        fontSize: 50,
                        color: Colors.white,
                        fontWeight: FontWeight.bold)),
                TextSpan(
                    text: 'Mobile',
                    style: TextStyle(fontSize: 25, color: Colors.blue)),
              ],
            )),
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 50, horizontal: 30),
              child: Form(
                child: Column(
                  children: [
                    ElevatedButton.icon(
                      icon: Icon(Icons
                          .signal_wifi_statusbar_connected_no_internet_4_rounded),
                      label: Text("Connect"),
                      onPressed: () {
                        Navigator.push(context,
                            MaterialPageRoute(builder: (context) {
                          return Dashboard();
                        }));
                      },
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.all(20.0),
                        fixedSize: Size(300, 80),
                        textStyle: TextStyle(
                            fontWeight: FontWeight.bold, fontSize: 30),
                        backgroundColor: Colors.blue,
                        foregroundColor: Colors.white,
                        elevation: 20,
                        shadowColor: Colors.black,
                        side: BorderSide(color: Colors.blue, width: 3),
                        shape: StadiumBorder(),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
