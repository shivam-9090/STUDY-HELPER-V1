import 'package:flutter/material.dart';

class TopicsScreen extends StatefulWidget {
  const TopicsScreen({super.key});

  @override
  State<TopicsScreen> createState() => _TopicsScreenState();
}

class _TopicsScreenState extends State<TopicsScreen> {
  final List<Map<String, dynamic>> _subjects = [
    {
      'name': 'Mathematics',
      'icon': Icons.calculate,
      'topics': ['Calculus', 'Algebra', 'Geometry', 'Statistics'],
    },
    {
      'name': 'Physics',
      'icon': Icons.science,
      'topics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Optics'],
    },
    {
      'name': 'Computer Science',
      'icon': Icons.computer,
      'topics': ['Data Structures', 'Algorithms', 'Operating Systems', 'Databases'],
    },
    {
      'name': 'Chemistry',
      'icon': Icons.biotech,
      'topics': ['Organic', 'Inorganic', 'Physical', 'Analytical'],
    },
  ];

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _subjects.length,
      itemBuilder: (context, index) {
        final subject = _subjects[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ExpansionTile(
            leading: Icon(subject['icon'] as IconData),
            title: Text(subject['name'] as String),
            children: (subject['topics'] as List<String>).map((topic) {
              return ListTile(
                title: Text(topic),
                leading: const Icon(Icons.circle, size: 8),
                onTap: () {
                  // Navigate to topic detail or start chat about this topic
                },
              );
            }).toList(),
          ),
        );
      },
    );
  }
}
