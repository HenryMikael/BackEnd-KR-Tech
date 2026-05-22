class User {
  final int id;
  final String nome;
  final String email;
  final String type;
  String? token;
  
  User({
    required this.id,
    required this.nome,
    required this.email,
    required this.type,
    this.token,
  });
  
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['user_id'] ?? json['id'] ?? 0,
      nome: json['nome'] ?? '',
      email: json['email'] ?? '',
      type: json['type'] ?? 'cliente',
      token: json['token'],
    );
  }
}