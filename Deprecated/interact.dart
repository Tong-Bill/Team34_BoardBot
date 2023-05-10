// Author: Bill Tong
// Scrapped in favor of a new Web User Interface

import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

class Interact extends StatefulWidget {
  const Interact({Key? key}) : super(key: key);

  @override
  State<Interact> createState() => _InteractState();
}

class _InteractState extends State<Interact> {
  int currentIndex = 0;
  final remote = CarouselController();
  final imageList = [
    'images/NeutralNWWhite.jpg',
    'images/AngryRed.jpg',
    'images/ConfusedSWGray.jpg',
    'images/HappySEYellow.jpg',
    'images/SadSWBlue.jpg',
    'images/SassyNWPurple.jpg',
    'images/SurpriseNEOrange.jpg',
    'images/WorriedNWGreen.jpg',
  ];

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
          title: Text('INTERACT'),
          backgroundColor: Colors.transparent,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CarouselSlider.builder(
                carouselController: remote,
                options: CarouselOptions(
                    height: 250,
                    initialPage: 0,
                    autoPlay: false,
                    reverse: false,
                    enlargeCenterPage: true,
                    enableInfiniteScroll: true,
                    pageSnapping: true,
                    onPageChanged: (index, reason) => setState(() => currentIndex = index),
                ),
                itemCount: imageList.length,
                itemBuilder: (context, index, realIndex) {
                  final imageItem = imageList[index];
                  return buildImage(imageItem, index);
                  },
              ),
              const SizedBox(height: 32),
              buildGauge(),
              buildArrows(),
            ],
          ),
        ),
      ),
    );
  }
  Widget buildImage(String imageItem, int index) => Container(
    margin: EdgeInsets.symmetric(horizontal: 15),
    color: Colors.white,
    child: Image.asset(
      imageItem,
      fit: BoxFit.cover,
    ),
  );

  Widget buildGauge() => AnimatedSmoothIndicator(
    activeIndex: currentIndex,
    count: imageList.length,
    effect: ExpandingDotsEffect(
      activeDotColor: Colors.blue,
      dotColor: Colors.grey,
    ),
    onDotClicked: slidingMotion,
  );

  Widget buildArrows({bool expand = false}) => Padding(
    padding: const EdgeInsets.all(20),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: EdgeInsets.symmetric(horizontal: 30, vertical: 10),),
            child: Icon(Icons.arrow_back_ios_new_sharp, size: 30,),
            onPressed: backward,
          ),
        expand ? Spacer() : SizedBox(width: 32,),
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: EdgeInsets.symmetric(horizontal: 30, vertical: 10),),
          child: Icon(Icons.arrow_forward_ios_sharp, size: 30,),
          onPressed: forward,
        ),
      ],
    ),
  );

  void forward() => remote.nextPage(duration: Duration(milliseconds: 300));
  void backward() => remote.previousPage(duration: Duration(milliseconds: 300));
  void slidingMotion(int index) => remote.animateToPage(index);
}

