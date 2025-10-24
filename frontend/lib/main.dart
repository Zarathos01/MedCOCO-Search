void main() => runApp(const MedCocoApp());

class MedCocoApp extends StatelessWidget {
  const MedCocoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MedCOCO-Search',
      home: Scaffold(
        appBar: AppBar(title: const Text('MedCOCO-Search')),
        body: const Center(child: Text('Welcome to MedCOCO-Search')),
      ),
    );
  }
}
