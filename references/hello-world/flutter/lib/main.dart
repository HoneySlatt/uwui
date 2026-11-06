import 'package:flutter/material.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            spacing: 8,
            children: [
              const Text('Hello, World!'),
              FilledButton(
                onPressed: () => print('Clicked!'),
                child: const Text("Let's Go!"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
