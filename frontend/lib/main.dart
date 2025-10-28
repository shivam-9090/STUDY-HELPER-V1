import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'screens/history_screen.dart';
import 'providers/study_provider.dart';
import 'services/api_service.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Create default user on app startup
  await _createDefaultUser();
  
  runApp(const StudyHelperApp());
}

Future<void> _createDefaultUser() async {
  try {
    final response = await http.post(
      Uri.parse('http://10.0.2.2:5000/api/user/create'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'username': 'Engineering Student',
        'email': 'user@example.com',
      }),
    );
    
    if (response.statusCode == 200 || response.statusCode == 201) {
      print('✅ User created/verified successfully');
    }
  } catch (e) {
    print('⚠️ Error creating user: $e');
  }
}

class StudyHelperApp extends StatelessWidget {
  const StudyHelperApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => StudyProvider(ApiService())),
      ],
      child: MaterialApp(
        title: 'Study Helper AI',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.deepPurple,
            brightness: Brightness.light,
          ),
          useMaterial3: true,
        ),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.deepPurple,
            brightness: Brightness.dark,
          ),
          useMaterial3: true,
        ),
        themeMode: ThemeMode.system,
        home: const HomeScreen(),
        routes: {
          '/history': (context) => const HistoryScreen(),
        },
      ),
    );
  }
}
