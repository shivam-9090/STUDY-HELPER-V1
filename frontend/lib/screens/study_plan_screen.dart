import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/study_provider.dart';

class StudyPlanScreen extends StatefulWidget {
  const StudyPlanScreen({super.key});

  @override
  State<StudyPlanScreen> createState() => _StudyPlanScreenState();
}

class _StudyPlanScreenState extends State<StudyPlanScreen> {
  final _subjectController = TextEditingController();
  final _topicController = TextEditingController();
  Map<String, dynamic>? _studyPlan;

  Future<void> _generatePlan() async {
    final subject = _subjectController.text.trim();
    final topic = _topicController.text.trim();

    if (subject.isEmpty || topic.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter both subject and topic')),
      );
      return;
    }

    final provider = Provider.of<StudyProvider>(context, listen: false);
    final plan = await provider.generateStudyPlan(subject, topic);

    setState(() {
      _studyPlan = plan;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  TextField(
                    controller: _subjectController,
                    decoration: const InputDecoration(
                      labelText: 'Subject',
                      hintText: 'e.g., Mathematics, Physics',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _topicController,
                    decoration: const InputDecoration(
                      labelText: 'Topic',
                      hintText: 'e.g., Calculus, Thermodynamics',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  FilledButton.icon(
                    onPressed: _generatePlan,
                    icon: const Icon(Icons.auto_awesome),
                    label: const Text('Generate Study Plan'),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          if (Provider.of<StudyProvider>(context).isLoading)
            const Center(child: CircularProgressIndicator())
          else if (_studyPlan != null)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Study Plan',
                      style: Theme.of(context).textTheme.headlineSmall,
                    ),
                    const Divider(),
                    Text(_studyPlan?['plan'] ?? 'No plan generated'),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _subjectController.dispose();
    _topicController.dispose();
    super.dispose();
  }
}
