import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Production backend URL - Replace with your actual Render URL after deployment
  static const String _productionUrl = 'https://study-helper-backend.onrender.com/api';
  
  // Local development backend URL
  static const String _developmentUrl = 'http://10.0.2.2:5000/api'; // For Android emulator
  // static const String _developmentUrl = 'http://localhost:5000/api'; // For web/desktop
  
  // Toggle this to switch between development and production
  static const bool _isProduction = true;
  
  static String get baseUrl => _isProduction ? _productionUrl : _developmentUrl;

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
