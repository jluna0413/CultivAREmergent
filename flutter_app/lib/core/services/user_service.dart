// User Management Service for Admin User operations
// Provides CRUD operations, role management, and analytics

import 'dart:convert';
import 'dart:io';
import '../models/user_models.dart';

/// User management service that handles all admin user operations
class UserService {
  static const String _baseUrl = 'http://localhost:4200/api/v2';

  /// Get all users with optional search and filtering
  Future<UserListResponse> getUsers({
    UserSearchRequest? searchRequest,
    String? authToken,
  }) async {
    try {
      final url = Uri.parse('$_baseUrl/admin/users');
      final queryParams = <String, String>{
        if (searchRequest?.page != null) 'page': searchRequest!.page.toString(),
        if (searchRequest?.limit != null)
          'limit': searchRequest!.limit.toString(),
        if (searchRequest?.search != null) 'search': searchRequest!.search!,
        if (searchRequest?.roleFilter != UserRoleFilter.all)
          'role': searchRequest!.roleFilter.toString().split('.').last,
        if (searchRequest?.statusFilter != UserStatusFilter.all)
          'status': searchRequest!.statusFilter.toString().split('.').last,
        if (searchRequest?.sortBy != null) 'sort_by': searchRequest!.sortBy,
        if (searchRequest?.sortAscending != null)
          'sort_ascending': searchRequest!.sortAscending.toString(),
      };

      final queryString = queryParams.isNotEmpty
          ? '?${queryParams.entries.map((e) => '${e.key}=${Uri.encodeComponent(e.value)}').join('&')}'
          : '';
      final finalUrl = Uri.parse('$url$queryString');

      final response = await _makeRequest(finalUrl, authToken: authToken);

      if (response.statusCode == 200) {
        final body = await response.transform(utf8.decoder).join();
        final decodedBody = jsonDecode(body);
        if (decodedBody is! Map<String, dynamic>) {
          throw Exception('Invalid response format');
        }
        return UserListResponse.fromJson(decodedBody);
      } else {
        throw Exception('Failed to fetch users: ${response.statusCode}');
      }
    } on SocketException {
      // Network error - return mock data for development
      return _getMockUsers(searchRequest);
    } catch (e) {
      // API not available - return mock data for development
      return _getMockUsers(searchRequest);
    }
  }

  /// Create a new user
  Future<User> createUser(
    UserRegistrationRequest request, {
    String? authToken,
  }) async {
    try {
      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users'),
        method: 'POST',
        body: jsonEncode(request.toJson()),
        authToken: authToken,
      );

      if (response.statusCode == 201) {
        final body = await response.transform(utf8.decoder).join();
        final data = jsonDecode(body);
        if (data is! Map<String, dynamic> ||
            data['user'] is! Map<String, dynamic>) {
          throw Exception('Invalid response format');
        }
        return User.fromJson(data['user'] as Map<String, dynamic>);
      } else {
        throw Exception('Failed to create user: ${response.statusCode}');
      }
    } on SocketException {
      // Network error - return mock data for development
      return _getMockCreatedUser(request);
    } catch (e) {
      // API not available - return mock data for development
      return _getMockCreatedUser(request);
    }
  }

  /// Update an existing user
  Future<User> updateUser(
    int userId,
    UserProfileUpdateRequest request, {
    String? authToken,
  }) async {
    try {
      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users/$userId'),
        method: 'PUT',
        body: jsonEncode(request.toJson()),
        authToken: authToken,
      );

      if (response.statusCode == 200) {
        final body = await response.transform(utf8.decoder).join();
        final data = jsonDecode(body);
        if (data is! Map<String, dynamic> ||
            data['user'] is! Map<String, dynamic>) {
          throw Exception('Invalid response format');
        }
        return User.fromJson(data['user'] as Map<String, dynamic>);
      } else {
        throw Exception('Failed to update user: ${response.statusCode}');
      }
    } on SocketException {
      // Network error - return mock data for development
      return _getMockUpdatedUser(userId, request);
    } catch (e) {
      // API not available - return mock data for development
      return _getMockUpdatedUser(userId, request);
    }
  }

  /// Delete a user
  Future<bool> deleteUser(int userId, {String? authToken}) async {
    try {
      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users/$userId'),
        method: 'DELETE',
        authToken: authToken,
      );

      return response.statusCode == 204;
    } on SocketException {
      // Network error - return mock success for development
      return true;
    } catch (e) {
      // API not available - return mock success for development
      return true;
    }
  }

  /// Get user analytics
  Future<UserAnalytics> getUserAnalytics({String? authToken}) async {
    try {
      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users/analytics'),
        authToken: authToken,
      );

      if (response.statusCode == 200) {
        final body = await response.transform(utf8.decoder).join();
        final decodedBody = jsonDecode(body);
        if (decodedBody is! Map<String, dynamic>) {
          throw Exception('Invalid response format');
        }
        return UserAnalytics.fromJson(decodedBody);
      } else {
        throw Exception('Failed to fetch analytics: ${response.statusCode}');
      }
    } on SocketException {
      // Network error - return mock data for development
      return _getMockAnalytics();
    } catch (e) {
      // API not available - return mock data for development
      return _getMockAnalytics();
    }
  }

  /// Toggle user active status
  Future<User> toggleUserStatus(int userId, {String? authToken}) async {
    try {
      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users/$userId/toggle-status'),
        method: 'PATCH',
        authToken: authToken,
      );

      if (response.statusCode == 200) {
        final body = await response.transform(utf8.decoder).join();
        final data = jsonDecode(body);
        if (data is! Map<String, dynamic> ||
            data['user'] is! Map<String, dynamic>) {
          throw Exception('Invalid response format');
        }
        return User.fromJson(data['user'] as Map<String, dynamic>);
      } else {
        throw Exception('Failed to toggle user status: ${response.statusCode}');
      }
    } on SocketException {
      // Network error - return mock success for development
      return _getMockToggledUser(userId);
    } catch (e) {
      // API not available - return mock success for development
      return _getMockToggledUser(userId);
    }
  }

  /// Reset user password
  Future<bool> resetUserPassword(int userId, {String? authToken}) async {
    try {
      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users/$userId/reset-password'),
        method: 'POST',
        authToken: authToken,
      );

      return response.statusCode == 200;
    } on SocketException {
      // Network error - return mock success for development
      return true;
    } catch (e) {
      // API not available - return mock success for development
      return true;
    }
  }

  /// Export users to CSV
  Future<String> exportUsers({
    UserSearchRequest? searchRequest,
    String? authToken,
  }) async {
    try {
      final queryParams = <String, String>{};
      if (searchRequest?.search != null) {
        queryParams['search'] = searchRequest!.search!;
      }
      if (searchRequest?.roleFilter != UserRoleFilter.all) {
        queryParams['role'] = searchRequest!.roleFilter
            .toString()
            .split('.')
            .last;
      }
      if (searchRequest?.statusFilter != UserStatusFilter.all) {
        queryParams['status'] = searchRequest!.statusFilter
            .toString()
            .split('.')
            .last;
      }

      final queryString = queryParams.isNotEmpty
          ? '?${queryParams.entries.map((e) => '${e.key}=${Uri.encodeComponent(e.value)}').join('&')}'
          : '';

      final response = await _makeRequest(
        Uri.parse('$_baseUrl/admin/users/export$queryString'),
        authToken: authToken,
      );

      if (response.statusCode == 200) {
        return await response.transform(utf8.decoder).join();
      } else {
        throw Exception('Failed to export users: ${response.statusCode}');
      }
    } on SocketException {
      // Network error - return mock CSV for development
      return _getMockCSVExport();
    } catch (e) {
      // API not available - return mock CSV for development
      return _getMockCSVExport();
    }
  }

  /// Make HTTP request with authentication
  Future<HttpClientResponse> _makeRequest(
    Uri uri, {
    String method = 'GET',
    String? body,
    String? authToken,
  }) async {
    final client = HttpClient();
    try {
      final request = await client.openUrl(method, uri);

      // Add authentication header
      if (authToken != null) {
        request.headers.add('Authorization', 'Bearer $authToken');
      }

      // Add content type header for POST/PUT requests
      if ((method == 'POST' || method == 'PUT') && body != null) {
        request.headers.add('Content-Type', 'application/json');
        request.write(body);
      }

      final response = await request.close();
      return response;
    } finally {
      client.close();
    }
  }

  // Mock data methods for development/testing
  UserListResponse _getMockUsers(UserSearchRequest? searchRequest) {
    final allUsers = [
      User(
        id: 1,
        username: 'admin',
        email: 'admin@cultivar.app',
        isActive: true,
        createdAt: DateTime.now().subtract(const Duration(days: 30)),
        lastLogin: DateTime.now().subtract(const Duration(hours: 2)),
        firstName: 'Admin',
        lastName: 'User',
        role: UserRole.admin,
        status: UserStatus.active,
      ),
      User(
        id: 2,
        username: 'john_doe',
        email: 'john@example.com',
        isActive: true,
        createdAt: DateTime.now().subtract(const Duration(days: 15)),
        lastLogin: DateTime.now().subtract(const Duration(days: 1)),
        firstName: 'John',
        lastName: 'Doe',
        role: UserRole.user,
        status: UserStatus.active,
      ),
      User(
        id: 3,
        username: 'jane_smith',
        email: 'jane@example.com',
        isActive: false,
        createdAt: DateTime.now().subtract(const Duration(days: 10)),
        lastLogin: DateTime.now().subtract(const Duration(days: 3)),
        firstName: 'Jane',
        lastName: 'Smith',
        role: UserRole.user,
        status: UserStatus.inactive,
      ),
      User(
        id: 4,
        username: 'moderator',
        email: 'mod@cultivar.app',
        isActive: true,
        createdAt: DateTime.now().subtract(const Duration(days: 25)),
        lastLogin: DateTime.now().subtract(const Duration(hours: 5)),
        firstName: 'Moderator',
        lastName: 'User',
        role: UserRole.moderator,
        status: UserStatus.active,
      ),
    ];

    // Apply filters
    var filteredUsers = allUsers;
    if (searchRequest?.search != null) {
      final search = searchRequest!.search!.toLowerCase();
      filteredUsers = filteredUsers
          .where(
            (user) =>
                user.username.toLowerCase().contains(search) ||
                user.email.toLowerCase().contains(search) ||
                user.fullName.toLowerCase().contains(search),
          )
          .toList();
    }

    if (searchRequest?.roleFilter != UserRoleFilter.all) {
      final userRole = UserRole.values.firstWhere(
        (e) =>
            e.toString().split('.').last ==
            searchRequest!.roleFilter.toString().split('.').last,
      );
      filteredUsers = filteredUsers
          .where((user) => user.role == userRole)
          .toList();
    }

    if (searchRequest?.statusFilter != UserStatusFilter.all) {
      final userStatus = UserStatus.values.firstWhere(
        (e) =>
            e.toString().split('.').last ==
            searchRequest!.statusFilter.toString().split('.').last,
      );
      filteredUsers = filteredUsers.where((user) {
        switch (userStatus) {
          case UserStatus.active:
            return user.isActive;
          case UserStatus.inactive:
            return !user.isActive && user.status == UserStatus.inactive;
          case UserStatus.suspended:
            return user.status == UserStatus.suspended;
          default:
            return true;
        }
      }).toList();
    }

    return UserListResponse(
      users: filteredUsers,
      total: filteredUsers.length,
      page: searchRequest?.page ?? 1,
      limit: searchRequest?.limit ?? 20,
      totalPages: (filteredUsers.length / (searchRequest?.limit ?? 20)).ceil(),
    );
  }

  User _getMockCreatedUser(UserRegistrationRequest request) {
    return User(
      id: DateTime.now().millisecondsSinceEpoch % 10000,
      username: request.username,
      email: request.email,
      isActive: true,
      createdAt: DateTime.now(),
      firstName: request.firstName,
      lastName: request.lastName,
      role: request.role,
      status: UserStatus.active,
    );
  }

  User _getMockUpdatedUser(int userId, UserProfileUpdateRequest request) {
    final mockUser = _getMockUsers(null).users.firstWhere(
      (user) => user.id == userId,
      orElse: () => User(
        id: userId,
        username: 'updated_user',
        email: 'updated@example.com',
        isActive: true,
        createdAt: DateTime.now(),
        role: UserRole.user,
        status: UserStatus.active,
      ),
    );

    return mockUser.copyWith(
      firstName: request.firstName ?? mockUser.firstName,
      lastName: request.lastName ?? mockUser.lastName,
      email: request.email ?? mockUser.email,
      avatar: request.avatar ?? mockUser.avatar,
      role: request.role ?? mockUser.role,
      status: request.status ?? mockUser.status,
      updatedAt: DateTime.now(),
    );
  }

  User _getMockToggledUser(int userId) {
    final mockUsers = _getMockUsers(null).users;
    final user = mockUsers.firstWhere(
      (user) => user.id == userId,
      orElse: () => User(
        id: userId,
        username: 'mock_user',
        email: 'mock@example.com',
        isActive: true,
        createdAt: DateTime.now(),
        role: UserRole.user,
        status: UserStatus.active,
      ),
    );

    return user.copyWith(
      isActive: !user.isActive,
      status: user.isActive ? UserStatus.inactive : UserStatus.active,
      updatedAt: DateTime.now(),
    );
  }

  UserAnalytics _getMockAnalytics() {
    final mockUsers = _getMockUsers(null).users;
    return UserAnalytics(
      totalUsers: mockUsers.length,
      activeUsers: mockUsers.where((user) => user.isActive).length,
      inactiveUsers: mockUsers.where((user) => !user.isActive).length,
      suspendedUsers: 0,
      adminsCount: mockUsers
          .where((user) => user.role == UserRole.admin)
          .length,
      moderatorsCount: mockUsers
          .where((user) => user.role == UserRole.moderator)
          .length,
      regularUsersCount: mockUsers
          .where((user) => user.role == UserRole.user)
          .length,
      newUsersThisMonth: 5,
      newUsersLastMonth: 3,
      usersByRole: {
        'admin': mockUsers.where((user) => user.role == UserRole.admin).length,
        'moderator': mockUsers
            .where((user) => user.role == UserRole.moderator)
            .length,
        'user': mockUsers.where((user) => user.role == UserRole.user).length,
      },
      usersByStatus: {
        'active': mockUsers.where((user) => user.isActive).length,
        'inactive': mockUsers.where((user) => !user.isActive).length,
        'suspended': 0,
      },
    );
  }

  String _getMockCSVExport() {
    return '''username,email,first_name,last_name,role,status,created_at,last_login
admin,admin@cultivar.app,Admin,User,admin,active,2024-10-04,2024-11-03
john_doe,john@example.com,John,Doe,user,active,2024-10-19,2024-11-02
jane_smith,jane@example.com,Jane,Smith,user,inactive,2024-10-24,2024-10-31
moderator,mod@cultivar.app,Moderator,User,moderator,active,2024-10-09,2024-11-03''';
  }
}

// Singleton instance
final userService = UserService();
