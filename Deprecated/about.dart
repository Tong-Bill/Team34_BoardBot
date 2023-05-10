// Author: Bill Tong
// Scrapped in favor of a new Web User Interface

import 'package:flutter/material.dart';

class About extends StatelessWidget {
  const About({Key? key}) : super(key: key);

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
          title: Text('ABOUT'),
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
                        color: Colors.yellow,
                        offset: Offset(0, 2),
                        spreadRadius: 5,
                        blurRadius: 10),
                  ],
                  image: DecorationImage(
                      // Taken from NightCafe AI art generator
                      image: AssetImage('images/info1.jpg'),
                      fit: BoxFit.cover),
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,20,0,10),
                child: Text(
                  "CS426 Senior Project 2023\nDepartment of Computer Science & Engineering,\nUniversity of Nevada, Reno",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,10,0,10),
                child: Text(
                  "Developers:\nJacob Boe, Adam Hurd, Yee Tham,\nBill Tong, Wyatt Young",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,10,0,10),
                child: Text(
                  "Instructors:\nDr.David-Feil-Seifer, Devrin Lee",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(0,10,0,0),
                child: Text(
                  "Advisors:\nMelanie Schmidt-Wolf,\nPonkoj Chandra Shill\n(UNR SARG Lab)",
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
