import 'package:flutter/material.dart';
import 'package:boardbot_app/about.dart';
import 'package:boardbot_app/info.dart';
import 'package:boardbot_app/interact.dart';
import 'package:boardbot_app/session.dart';

class Dashboard extends StatelessWidget {
  const Dashboard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
          image: DecorationImage(
              image: AssetImage('images/wallpaper2.jpg'), fit: BoxFit.cover)),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: Padding(
          padding: const EdgeInsets.all(30),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
            Container(
              padding: const EdgeInsets.all(15),
              constraints: const BoxConstraints.expand(
                width: 330,
                height: 460,
              ),
              decoration: const BoxDecoration(
                boxShadow: [
                 BoxShadow(
                   color: Colors.white,
                   offset: Offset(0, 2),
                   spreadRadius: 5,
                   blurRadius: 10
                 ),
                ],
                image: DecorationImage(
                  // Taken from NightCafe AI art generator
                  image: AssetImage('images/menu1.jpg'), fit: BoxFit.cover),
                borderRadius: BorderRadius.all(
                  Radius.circular(10),
                ),
              ),
              child: Stack(
                children: [
                  Positioned(
                    top: 0,
                    child: OutlinedButton(
                      child: Text('Special Edition'),
                      style: OutlinedButton.styleFrom(
                        textStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        backgroundColor: Colors.purple,
                        foregroundColor: Colors.white,
                        side: BorderSide(color: Colors.purple, width: 2),
                        shape: StadiumBorder()
                      ),
                      onPressed: () {},
                    ),
                  ),
                  Positioned(
                    right: 0,
                    bottom: 20,
                    child: Text(
                      'Experience monopoly with Donald Trump*',
                      style: TextStyle(color: Colors.white, fontSize: 16),
                    ),
                  ),
                  Positioned(
                    right: 0,
                    bottom: 0,
                    child: Text(
                      '*Not the real one',
                      style: TextStyle(color: Colors.white, fontSize: 14),
                    ),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(0, 30, 0, 0),
              child: ElevatedButton.icon(
                icon: Icon(Icons
                    .play_arrow_rounded),
                label: Text("Begin Game"),
                onPressed: () {},
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
            ),
            ],
          ),
        ),
        floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
        floatingActionButton:
          FloatingActionButton(
            onPressed: (){},
            child: Icon(Icons.signal_wifi_4_bar),
            backgroundColor: Colors.black,
            foregroundColor: Colors.white,
            mini: false,
            ),
        bottomNavigationBar: BottomAppBar(
          notchMargin: 5,
          shape: CircularNotchedRectangle(),
          color: Colors.black,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            mainAxisSize: MainAxisSize.max,
            children: [
              Padding(
                padding: const EdgeInsets.only(left: 10),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.home),
                      color: Colors.white, onPressed: () {Navigator.pop(context);},
                    ),
                    Text(
                      "Home",
                      style: TextStyle(color: Colors.white),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(right: 20, top: 5, bottom: 5),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.handyman),
                      color: Colors.white, onPressed: () {Navigator.push(context,
                        MaterialPageRoute(builder: (context){
                          return Interact();
                        }));}
                    ),
                    Text(
                      "Interact",
                      style: TextStyle(color: Colors.white),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 20, top: 5, bottom: 5),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.info),
                      color: Colors.white, onPressed: () {Navigator.push(context,
                        MaterialPageRoute(builder: (context){
                          return Info();
                        }));}
                    ),
                    Text(
                      "Info",
                      style: TextStyle(color: Colors.white),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(right: 10),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.question_mark),
                      color: Colors.white, onPressed: () {Navigator.push(context,
                        MaterialPageRoute(builder: (context){
                          return About();
                        }));
                        },
                    ),
                    Text(
                      "About",
                      style: TextStyle(color: Colors.white),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        ),
      );
  }
}
