import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Change this to your backend URL
  // Use 10.0.2.2 for Android emulator (maps to host machine's localhost)
  // Use localhost:5000 for web/desktop
  static const String baseUrl = 'http://10.0.2.2:5000/api';

  Future<Map<String, dynamic>> askQuestion(String question, {String? subject}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'question': question,
          'subject': subject,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get answer: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error connecting to server: $e');
    }
  }

  Future<Map<String, dynamic>> generateStudyPlan(String subject, String topic) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/study-plan'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'subject': subject,
          'topic': topic,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to generate study plan');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<Map<String, dynamic>> explainConcept(String concept, String level) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/explain'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'concept': concept,
          'level': level,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to explain concept');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<List<dynamic>> getTopics(String subject) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/topics/$subject'),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body)['topics'];
      } else {
        throw Exception('Failed to get topics');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
