import 'package:flutter/material.dart';
import 'home.dart';
import 'dashboard.dart';
import 'about.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Boardbot Mobile',
        home: Home()
    );
  }
}
