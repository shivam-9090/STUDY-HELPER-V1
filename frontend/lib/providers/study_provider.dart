import 'package:flutter/foundation.dart';
import '../services/api_service.dart';

class StudyProvider extends ChangeNotifier {
  final ApiService _apiService;
  
  bool _isLoading = false;
  String? _error;
  Map<String, dynamic>? _currentAnswer;
  List<Map<String, String>> _chatHistory = [];

  StudyProvider(this._apiService);

  bool get isLoading => _isLoading;
  String? get error => _error;
  Map<String, dynamic>? get currentAnswer => _currentAnswer;
  List<Map<String, String>> get chatHistory => _chatHistory;

  Future<void> askQuestion(String question, {String? subject}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _chatHistory.add({'role': 'user', 'content': question});
      
      final response = await _apiService.askQuestion(question, subject: subject);
      
      _currentAnswer = response;
      _chatHistory.add({'role': 'assistant', 'content': response['answer'] ?? ''});
      
      _error = null;
    } catch (e) {
      _error = e.toString();
      _currentAnswer = null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>?> generateStudyPlan(String subject, String topic) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.generateStudyPlan(subject, topic);
      _error = null;
      return response;
    } catch (e) {
      _error = e.toString();
      return null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>?> explainConcept(String concept, String level) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.explainConcept(concept, level);
      _error = null;
      return response;
    } catch (e) {
      _error = e.toString();
      return null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearChat() {
    _chatHistory.clear();
    _currentAnswer = null;
    _error = null;
    notifyListeners();
  }
}
