import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Service for handling local storage operations
/// Wraps SharedPreferences and FlutterSecureStorage
class StorageService {
  static const FlutterSecureStorage _secureStorage = FlutterSecureStorage();
  static SharedPreferences? _prefs;

  static Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // Secure Storage Operations (for sensitive data)

  static Future<void> setSecureString(String key, String value) async {
    await _secureStorage.write(key: key, value: value);
  }

  static Future<String?> getSecureString(String key) async {
    return await _secureStorage.read(key: key);
  }

  static Future<void> setSecureInt(String key, int value) async {
    await _secureStorage.write(key: key, value: value.toString());
  }

  static Future<int?> getSecureInt(String key) async {
    final value = await _secureStorage.read(key: key);
    return value != null ? int.tryParse(value) : null;
  }

  static Future<void> setSecureBool(String key, bool value) async {
    await _secureStorage.write(key: key, value: value.toString());
  }

  static Future<bool?> getSecureBool(String key) async {
    final value = await _secureStorage.read(key: key);
    return value != null ? value.toLowerCase() == 'true' : null;
  }

  static Future<void> removeSecureKey(String key) async {
    await _secureStorage.delete(key: key);
  }

  static Future<void> clearSecureStorage() async {
    await _secureStorage.deleteAll();
  }

  // SharedPreferences Operations (for non-sensitive data)

  static Future<void> setString(String key, String value) async {
    await _prefs?.setString(key, value);
  }

  static String? getString(String key) {
    return _prefs?.getString(key);
  }

  static Future<void> setInt(String key, int value) async {
    await _prefs?.setInt(key, value);
  }

  static int? getInt(String key) {
    return _prefs?.getInt(key);
  }

  static Future<void> setBool(String key, bool value) async {
    await _prefs?.setBool(key, value);
  }

  static bool? getBool(String key) {
    return _prefs?.getBool(key);
  }

  static Future<void> setStringList(String key, List<String> value) async {
    await _prefs?.setStringList(key, value);
  }

  static List<String>? getStringList(String key) {
    return _prefs?.getStringList(key);
  }

  static Future<void> removeKey(String key) async {
    await _prefs?.remove(key);
  }

  static Future<void> clear() async {
    await _prefs?.clear();
  }

  static Set<String> getKeys() {
    return _prefs?.getKeys() ?? {};
  }

  // Helper methods for common use cases

  static Future<void> saveAuthToken(String token) async {
    await setSecureString('auth_token', token);
  }

  static Future<String?> getAuthToken() async {
    return await getSecureString('auth_token');
  }

  static Future<void> clearAuthToken() async {
    await removeSecureKey('auth_token');
  }

  static Future<void> saveRefreshToken(String token) async {
    await setSecureString('refresh_token', token);
  }

  static Future<String?> getRefreshToken() async {
    return await getSecureString('refresh_token');
  }

  static Future<void> clearRefreshToken() async {
    await removeSecureKey('refresh_token');
  }

  static Future<void> saveUserData(Map<String, dynamic> userData) async {
    for (final entry in userData.entries) {
      await setString('user_${entry.key}', entry.value.toString());
    }
  }

  static Future<Map<String, String>> getUserData() async {
    final userData = <String, String>{};
    final keys = getKeys();

    for (final key in keys) {
      if (key.startsWith('user_')) {
        final value = getString(key);
        if (value != null) {
          userData[key.substring(5)] = value;
        }
      }
    }

    return userData;
  }

  static Future<void> clearUserData() async {
    final keys = getKeys();

    for (final key in keys) {
      if (key.startsWith('user_')) {
        await removeKey(key);
      }
    }
  }
}
