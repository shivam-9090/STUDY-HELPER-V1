import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'screens/history_screen.dart';
import 'screens/study_plan_screen.dart';
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
    // Use production URL or development URL based on environment
    const bool isProduction = true; // Change to false for local development
    final String apiUrl = isProduction 
        ? 'https://study-helper-backend.onrender.com/api/user/create'
        : 'http://10.0.2.2:5000/api/user/create';
    
    final response = await http.post(
      Uri.parse(apiUrl),
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
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF6366F1), // Modern indigo
            brightness: Brightness.light,
            primary: const Color(0xFF6366F1),
            secondary: const Color(0xFF8B5CF6),
            tertiary: const Color(0xFF06B6D4),
            surface: Colors.white,
            background: const Color(0xFFF8FAFC),
          ),
          scaffoldBackgroundColor: const Color(0xFFF8FAFC),
          cardTheme: CardTheme(
            elevation: 0,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            color: Colors.white,
          ),
          appBarTheme: const AppBarTheme(
            centerTitle: true,
            elevation: 0,
            backgroundColor: Colors.transparent,
            surfaceTintColor: Colors.transparent,
          ),
          navigationBarTheme: NavigationBarThemeData(
            backgroundColor: Colors.white,
            indicatorColor: const Color(0xFF6366F1).withOpacity(0.1),
            labelTextStyle: MaterialStateProperty.all(
              const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
            ),
          ),
          fontFamily: 'SF Pro Display',
        ),
        darkTheme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF6366F1),
            brightness: Brightness.dark,
            primary: const Color(0xFF818CF8),
            secondary: const Color(0xFFA78BFA),
            tertiary: const Color(0xFF22D3EE),
            surface: const Color(0xFF1E293B),
            background: const Color(0xFF0F172A),
          ),
          scaffoldBackgroundColor: const Color(0xFF0F172A),
          cardTheme: CardTheme(
            elevation: 0,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            color: const Color(0xFF1E293B),
          ),
          appBarTheme: const AppBarTheme(
            centerTitle: true,
            elevation: 0,
            backgroundColor: Colors.transparent,
            surfaceTintColor: Colors.transparent,
          ),
          navigationBarTheme: NavigationBarThemeData(
            backgroundColor: const Color(0xFF1E293B),
            indicatorColor: const Color(0xFF818CF8).withOpacity(0.2),
            labelTextStyle: MaterialStateProperty.all(
              const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
            ),
          ),
        ),
        themeMode: ThemeMode.system,
        home: const HomeScreen(),
        routes: {
          '/history': (context) => const HistoryScreen(),
          '/study-plan': (context) => const StudyPlanScreen(),
        },
      ),
    );
  }
}
