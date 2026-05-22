import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  // URL do seu backend Flask
  static const String baseUrl = 'http://127.0.0.1:5000';
  
  // Para Android Emulador (descomente se precisar)
  // static const String baseUrl = 'http://10.0.2.2:5000';
  
  // Registrar usuário
  static Future<Map<String, dynamic>> register({
    required String nome,
    required String email,
    required String senha,
    required String confirmarSenha,
    String type = 'cliente',
  }) async {
    try {
      print('📝 Tentando registrar: $email');
      
      final response = await http.post(
        Uri.parse('$baseUrl/register'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'nome': nome,
          'email': email,
          'senha': senha,
          'confirmar_senha': confirmarSenha,
          'type': type,
        }),
      ).timeout(const Duration(seconds: 10));
      
      print('Status code: ${response.statusCode}');
      print('Resposta: ${response.body}');
      
      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return {
          'success': true,
          'message': data['message'],
        };
      } else {
        final data = json.decode(response.body);
        return {
          'success': false,
          'message': data['message'] ?? 'Erro ao registrar',
        };
      }
    } catch (e) {
      print('Erro no registro: $e');
      return {
        'success': false,
        'message': 'Erro de conexão: $e',
      };
    }
  }
  
  // Login do usuário
  static Future<Map<String, dynamic>> login({
    required String email,
    required String senha,
  }) async {
    try {
      print('🔐 Tentando login: $email');
      
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'email': email,
          'senha': senha,
        }),
      ).timeout(const Duration(seconds: 10));
      
      print('Status code: ${response.statusCode}');
      print('Resposta: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {
          'success': true,
          'message': data['message'],
          'token': data['token'],
          'user_id': data['user_id'],
          'type': data['type'],
        };
      } else {
        final data = json.decode(response.body);
        return {
          'success': false,
          'message': data['error'] ?? 'Erro ao fazer login',
        };
      }
    } catch (e) {
      print('Erro no login: $e');
      return {
        'success': false,
        'message': 'Erro de conexão: $e',
      };
    }
  }
  
  // Recuperar senha
  static Future<Map<String, dynamic>> recoverPassword({
    required String email,
    required String novaSenha,
  }) async {
    try {
      print('🔑 Tentando recuperar senha: $email');
      
      final response = await http.put(
        Uri.parse('$baseUrl/recover-password'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'email': email,
          'nova_senha': novaSenha,
        }),
      ).timeout(const Duration(seconds: 10));
      
      print('Status code: ${response.statusCode}');
      print('Resposta: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {
          'success': true,
          'message': data['message'],
        };
      } else {
        final data = json.decode(response.body);
        return {
          'success': false,
          'message': data['error'] ?? 'Erro ao recuperar senha',
        };
      }
    } catch (e) {
      print('Erro na recuperação: $e');
      return {
        'success': false,
        'message': 'Erro de conexão: $e',
      };
    }
  }
}